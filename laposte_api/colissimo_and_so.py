#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#  licence AGPL version 3 or later
#  see http://www.gnu.org/licenses/agpl-3.0.txt
#  Copyright (C) 2014 Akretion (http://www.akretion.com).
#  @author David BEAL <david.beal@akretion.com>
#
##############################################################################

from mako.template import Template
from mako.exceptions import RichTraceback
from datetime import datetime
import base64
#'https://fedorahosted.org/suds/wiki/Documentation'
from suds.client import Client, WebFault
import re
from .exception_helper import (
    InvalidSequence,
    InvalidWeight,
    InvalidSize,
    InvalidType,
    InvalidMissingField,
    InvalidZipCode,
    InvalidCountry,
    InvalidDate,
    InvalidCode,
    InvalidValue,
    InvalidValueNotInList,
)
import countries
from .label_helper import AbstractLabel
import os


WEBSERVICE_URL = 'https://ws.colissimo.fr/soap.shippingclpV2/services/WSColiPosteLetterService?wsdl'
CODING = 'cp1252'
ERROR_BEHAVIOR = 'backslashreplace'


PRODUCT_LOGO = {
    # so colissimo
    '6A': 'DOMI',
    '6C': 'DOMI',
    '6K': 'RENDEZ',
    '6J': 'CITY',
    '6H': 'BPOSTE',
    '6M': 'COMM',
    # colissimo
    '9L': 'ACCESS_F',
    '9V': 'EXPERT_F',
    '7Q': 'EXPER_OM',
    '8Q': 'ACCES_OM',
    '8R': 'SERVI_F', # NOT implemented
}

FOREIGN_INSURANCE_MAPPING = {
    '01': '15000', '02': '30000', '03': '45000',
    '04': '60000', '05': '75000', '06': '90000', '07': '105000',
    '08': '120000', '09': '135000', '10': '150000'}


# Here is all keys used in coliposte templates
ADDRESS_MODEL = {
    "name":       {'required': True, 'max_size': 35},
    "street":     {'required': True, 'max_size': 35},
    "street2":    {'max_size': 35},
    "street3":    {'max_size': 35},
    "zip":        {'required': True, 'max_size': 10},
    "city":       {'required': True, 'max_size': 35},
    "phone":      {'max_size': 20},
    "mobile":     {'max_size': 20},
    "email":      {'max_size': 100},
    'name2':      {'max_size': 30},  # so colissimo
    'door_code2': {'max_size': 20},  # so colissimo
    'door_code':  {'max_size': 20},  # so colissimo
    'intercom':   {'max_size': 20},  # so colissimo
}

DELIVERY_MODEL = {
    "weight":        {'required': True},
    "date":          {'required': True, 'date': '%d/%m/%Y'},
    "Instructions":  {'max_size': 70},
}

OPTION_MODEL = {}

SENDER_MODEL = {
    "name":         {'required': True},
    "street":       {'required': True},
    "street2":      {'max_size': 20},
    "zip":          {'required': True},
    "city":         {'required': True},
    "support_city": {'required': True},
}


class InvalidWebServiceRequest(Exception):
    ''


class InvalidDataForMako(Exception):
    ''


def is_digit(s):
    return re.search("[^0-9]", s) is None


class ColiPosteConfig(object):
    def __init__(self):
        pass

    def get_image_data(self):
        logo_file_folder = os.path.join(os.path.dirname(__file__), 'logo')
        file_data = ''
        for grf_file in os.listdir(logo_file_folder):
            if grf_file.endswith(".GRF"):
                logo_file_path = os.path.join(logo_file_folder, grf_file)
                with open(logo_file_path) as f:
                    file_data += f.read()
        return file_data


class ColiPoste(AbstractLabel):
    _account = None
    _service = None
    _product_code = None
    _test_name = None
    _specific_label = None

    _label_code = {
        'colissimo': ['9V', '9L', '7Q', '8Q'],
        'so_colissimo': ['6C', '6A', '6K', '6H', '6J', '6M'],
        'ColiPosteInternational': ['EI', 'AI'],
    }

    def __init__(self, account):
        if not self._account:
            self._account = self._check_account(account)

    def get_service(self, service_name, code):
        if service_name == 'colissimo':
            if code in ['EI', 'AI']:
                service = WSInternational(self._account)
                service_name = 'ColiPosteInternational'
                if 'cab_suivi' in DELIVERY_MODEL:
                    # drop this key in case of existence in the previous call
                    del DELIVERY_MODEL['cab_suivi']
            else:
                service = Colissimo(self._account)
                self._complete_models()
        elif service_name == 'so_colissimo':
            if code == 'SO':
                service = WSInternational(self._account)
                service_name = 'ColiPosteInternational'
            else:
                service = SoColissimo(self._account)
                self._complete_models()
        service._service, service._product_code = self._check_service(
            service_name, code)
        return service

    def _complete_models(self):
        DELIVERY_MODEL.update({"cab_suivi": {'required': True}})

    def _check_account(self, account):
        if not account or len(account) != 6:
            raise InvalidSize(
                "La Poste account '%s' must have a size of 6 chars " % account)
        if is_digit(account) is False:
            raise InvalidType(
                "Only digit chars are authorised for 'account' '%s'"
                % account)
        return account

    def _check_service(self, service, code):
        if service not in self._label_code.keys():
            raise InvalidCode("The service for the label must be in '%s'"
                              % self._label_code[service])
        if code not in self._label_code[service]:
            raise InvalidCode("The code for the label must be in '%s'"
                              % self._label_code[service])
        return service, code

    def _set_unit_test_file_name(
            self, name, sequence, tracking_ref, prise_en_charge):
        self._test_name = name
        self._test_first_keys = {
            'sequence': sequence,
            'tracking_ref': tracking_ref,
            'prise_en_charge': prise_en_charge,
        }

    def get_label(self, sender, delivery, address, option, return_request=False):
        sender.update({'account': self._account})
        self.complete_and_check_datas(sender, delivery, address, option)
        pec = delivery['cab_prise_en_charge']
        pec_bar = pec[:9].replace(' ', '') + '>5' + pec[9:].replace(' ', '')
        delivery.update({'pec_bar': pec_bar})
        suivi = delivery['cab_suivi']
        # >5  => is subset C invocation code
        suivi_bar = suivi[:4].replace(' ', '') + '>5'
        if suivi[-2:] == 'FR':
            suivi_bar += suivi[4:-2].replace(' ', '') + '>6FR'
        else:
            suivi_bar += suivi[4:].replace(' ', '')
        delivery['suivi_bar'] = suivi_bar
        # direct key values
        kwargs = {
            '_product_code': self._product_code,
            'logo': PRODUCT_LOGO[self._product_code],
        }
        kwargs = self._complete_kwargs(kwargs)
        return self.get_populated_label(delivery, sender, address, option, kwargs)

    def get_populated_label(self, delivery, sender, address, option, kwargs):
        zpl_file = self._service
        if self._specific_label:
            # in this case, you must use a really specific label
            # for 'commerçant' for example
            zpl_file += '_' + self._specific_label
        zpl_file += '.mako'
        zpl_file_path = os.path.join(
            os.path.dirname(__file__),
            'report',
            zpl_file)
        with open(zpl_file_path, 'r') as opened_file:
            file_content = opened_file.read()
            self.validate_mako(file_content, delivery, sender, address, option, kwargs)
            try:
                #print 'd', delivery, '\na', address, '\ns', sender, '\no', kwargs
                zpl = Template(file_content).render(
                    d=delivery, s=sender, a=address, o=option, **kwargs)
                content = zpl.encode(encoding=CODING, errors=ERROR_BEHAVIOR)
                if self._test_name:
                    self._record_unit_test_datas(
                        content, delivery, sender, address, option, kwargs)
            except:
                traceback = RichTraceback()
                self.extract_mako_error(traceback, zpl_file)
            return content

    def extract_mako_error(self, traceback, zpl_file):
        " allow to define where the file mako fail "
        lineno, arg, error = '', '', ''
        raise InvalidDataForMako(
            "Mako Template error: \n%s\n\nin %s file"
            % (traceback.message, zpl_file))

    def validate_mako(self, template, *all_dict):
        list_of_keys_list = [a_dict.keys() for a_dict in all_dict]
        available_keys = []
        for a_list in list_of_keys_list:
            [available_keys.append(y) for y in a_list]
        import re
        keys2match = []
        rx_search = '\$\{[ads](\[\'final_address\'\])?\[\'(.+?)\'\]\}+'
        for match in re.findall(rx_search, template):
            keys2match.append(match)
        keys2match = [x[1] for x in keys2match]
        unmatch = list(set(keys2match) - set(available_keys))
        if len(unmatch) > 0:
            print "\nLabel generation : these keys are defined in mako template",
            "but without valid replacement values", unmatch, '\n'
        return unmatch

    def _record_unit_test_datas(
            self, file_content, delivery, sender, address, option, kwargs):
        try:
            import tempfile
            path = tempfile.gettempdir() + '/' + self._test_name + '.py'
            full_content = '# -*- coding: utf-8 -*-\n\n'
            full_content += 'first_keys = ' + str(self._test_first_keys) + '\n\n'
            full_content += 'delivery = ' + str(delivery) + '\n\n'
            full_content += 'sender = ' + str(sender) + '\n\n'
            full_content += 'address = ' + str(address) + '\n\n'
            full_content += 'option = ' + str(option) + '\n\n'
            full_content += 'kwargs = ' + str(kwargs) + '\n\n'
            full_content += 'content = """' + file_content + '"""'
            with open(path, 'w') as wf:
                wf.write(full_content)
        except:
            raise "Invalid path %s" % path

    def _copy2clipboard(self, content):
        """Allow to copy label content to clipboard"""
        import pygtk
        pygtk.require('2.0')
        import gtk
        clipboard = gtk.clipboard_get()
        clipboard.set_text(content)
        clipboard.store()
        return True

    def _populate_option_with_default_value(self, option):
        for opt in ['ftd', 'ar', 'nm']:
            if opt not in option:
                option[opt] = False
        return option

    def _get_zip_country(self, zip_code=None, country_code=None):
        if zip_code:
            zip_country = zip_code
            if self._product_code[1:] != 'I':
                if len(zip_code) != 5:
                    raise InvalidZipCode(
                        "Address zip '%s' must have a size "
                        "of 5 chars for french destination"
                        % zip_code)
            else:
                # no more used
                if len(zip_code) < 3:
                    raise InvalidZipCode(
                        "International Address zip '%s' "
                        "must have a minimum size of 3 chars"
                        % zip_code)
                # Need country prefix for international colissimo
                # TODO check if code has 2 letters
                if country_code:
                    zip_country = country_code + zip_code[0:3]
                else:
                    raise InvalidCountry(
                        "'Address country' must not be empty' "
                        "for international Colissimo")
        else:
            raise InvalidZipCode("'Address zip' must not be empty'")
        return zip_country

    def _build_control_key(self, key):
        #remove space
        key = key.replace(' ', '')
        # reverse string order
        key = key[::-1]
        pair, odd = [], []
        sum_pair, sum_odd = 0, 0
        my_count = 0
        for arg in key:
            my_count += 1
            if my_count % 2 == 0:
                pair.append(arg)
            else:
                odd.append(arg)
        for number in odd:
            sum_odd += int(number)
        for number in pair:
            sum_pair += int(number)
        my_sum = sum_odd * 3 + sum_pair
        result = (my_sum // 10 + 1) * 10 - my_sum
        if result == 10:
            result = 0
        return str(result)

    def get_cab_suivi(self, sequence):
        if type(sequence) not in [unicode, str]:
            raise InvalidSequence("The sequence must be an str or an unicode")
        #TODO fix check
        #if not sequence.isdigit():
        #    raise InvalidSequence("Only digit char are authoried for"
        #                          " the sequence")
        return sequence + ' ' + str(self.get_ctrl_key(sequence[3:]))

    def get_ctrl_key(self, key):
        warning = "Invalid control key '%s' in get_ctrl_key function"
        if type(key) not in [unicode, str]:
            raise InvalidType(warning + ": must be a string" % key)
            return False
        if type(key) == unicode:
            key = str(key)
        #extract spaces
        key = key.replace(' ', '')
        length = [8, 10, 15]
        #check len
        if len(key) not in length:
            raise InvalidValueNotInList(warning + ": key length must be in %s"
                                        % (key, length))
        # check chars content
        if not key.isdigit():
            raise InvalidValue(warning + ": only digit chars are allowed" % key)
        # reverse string order
        key = key[::-1]
        if len(key) in [10, 15]:
            pair, odd = [], []
            sum_pair, sum_odd = 0, 0
            my_count = 0
            for arg in key:
                my_count += 1
                if my_count % 2 == 0:
                    pair.append(arg)
                else:
                    odd.append(arg)

            for number in odd:
                sum_odd += int(number)
            for number in pair:
                sum_pair += int(number)
            my_sum = sum_odd * 3 + sum_pair
            result = (my_sum // 10 + 1) * 10 - my_sum
            if result == 10:
                result = 0
        return result


class WSInternational(ColiPoste):

    def get_label(self, sender, delivery, address, option, return_request=False):
        infos = {
            'password': {'required': True},
            'phone': {'required': True},
            'country': {'required': True},
        }
        SENDER_MODEL.update(infos)
        option.update(self._populate_option_with_default_value(option))
        client = Client(WEBSERVICE_URL)
        ADDRESS_MODEL.update({'countryCode': {'required': True}})
        letter = client.factory.create('Letter')
        letter.contractNumber = self._account
        letter.password = sender['password']
        letter.profil = 'SPECIFIQUE'
        letter.service = self._set_service(client)
        letter.parcel = self._set_parcel(client, delivery, option)
        dest = client.factory.create('DestEnvVO')
        dest.addressVO = self._set_address_dest(client, address)
        letter.dest = dest
        exp = client.factory.create('ExpEnvVO')
        exp.addressVO = self._set_address_exp(client, sender)
        if 'ref_client' in delivery:
            exp.ref = delivery['ref_client']
        letter.exp = exp
        self.unmystify_coliposte_webservice(letter)
        if return_request:
            return str(letter)
        return self._send_request(client, letter)

    def unmystify_coliposte_webservice(self, letter):
        """ Delete evil attributes from soap xml provided by ColiPoste
            in order to start up the bouzin without fail
            Without these instructions, you'll got this message :
                Server raised fault: 'java.lang.IllegalArgumentException'
            Nice message, good help, bougez avec la poste
        """
        del(letter.service.returnType)
        del(letter.coordinate)
        del(letter.parcel.DeliveryMode)
        del(letter.dest.alert)
        del(letter.dest.codeBarForreference)
        del(letter.exp.alert)
        return True

    def _send_request(self, client, letter):
        """ Wrapper for API requests
        """
        res = {}
        ws_mess_title = "WebService International: \n%s"
        try:
            result = client.service.genererEtiquetteBIC3(letter)
            if hasattr(result, 'file'):
                data = self.encode_file_data(result.file)
                message = False
                if hasattr(result, 'message'):
                    message = self.extract_responses_messages(result)
                parcelNumber = str(result.parcelNumber)
                parcelNumberPartner = str(result.parcelNumberPartenaire)
                return (data, message, parcelNumber, parcelNumberPartner)
            else:
                messages = [self.nicely_dict(elm) for elm
                            in self.extract_responses_messages(result)]
                message_str = '\n'.join(messages)
                raise InvalidWebServiceRequest(message_str)
        except (WebFault, Exception) as e:
            raise InvalidWebServiceRequest(ws_mess_title % e.message)
        return res

    def nicely_dict(self, a_dict):
        return str(a_dict).replace("{'", "'") \
                          .replace(", '", "\n'") \
                          .replace("'}", "'")

    def encode_file_data(self, data):
        try:
            data = base64.b64decode(data).decode('iso-8859-15').encode('utf8')
        except (UnicodeEncodeError, Exception) as e:
            raise Exception(e.message)
        return data.replace('^XA', '^XA\n^CI28\n^LH20,0')

    def extract_responses_messages(self, result):
        """
            Possible messages
            30008: 'Service non autorise pour cet identifiant.
                   Veuillez prendre contact avec votre interlocuteur
                   commercial afin de reinitialiser votre compte client'
            30000: 'Identifiant ou mot de passe incorrect'
        """
        response = []
        for mess in result.message:
            infos = mess
            if not isinstance(mess, dict):
                infos = {
                    'type': str(mess.type).encode('utf8'),
                    'id': str(mess.id).encode('utf8'),
                    'libelle': mess.libelle.encode('iso-8859-15')}
                    #'libelle': mess.libelle.encode('utf8')}
            response.append(infos)
        return response

    def _set_service(self, client):
        service = client.factory.create('ServiceCallContextV2')
        service.dateDeposite = datetime.strftime(
            datetime.now(), '%Y-%m-%dT%H:%M:%S.000Z')
        service.languageConsignor = 'FR'
        service.languageConsignee = 'FR'
        #TODO complete crbt management
        service.crbt = '0'
        service.crbtAmount = 0
        if self._product_code == 'SO':
            service.partnerNetworkCode = 'R12'
            #TODO
            service.CommercialName = None         # mandatory if so colissimo
        return service

    def _set_parcel(self, client, delivery, option):
        parc = client.factory.create('ParcelVO')
        self.check_model(delivery, DELIVERY_MODEL, 'delivery')
        option_model = OPTION_MODEL.copy()
        if 'insurance' in option:
            option_model['insurance'] = {'in': FOREIGN_INSURANCE_MAPPING.keys()}
        self.check_model(option, option_model, 'option')
        parc.typeGamme = self._product_code
        #TODO manage 'return type'
        parc.returnTypeChoice = 3
        #TODO manage insurance range
        parc.insuranceRange = '00'
        parc.insuranceAmount = 0
        insurance_idx = option.get('insurance', '0')
        parc.insuranceValue = FOREIGN_INSURANCE_MAPPING.get(insurance_idx, '0')
        #TODO manage weight with Access Internat.
        parc.weight = delivery['weight']
        parc.horsGabarit = str(int(option['nm']))
        #TODO manage HorsGabaritAmount
        parc.HorsGabaritAmount = 0
        #TODO manage DeliveryMode/RegateCode pour So Colissimo
        if self._product_code == 'SO':
            parc.DeliveryMode = 'DOM'  # or DOM/DOS/CMT/BDP
            parc.RegateCode = ''
        #parc.ReturnReceipt = str(int(option['ar']))
        # 2014-07-16 : change : seems doesn't support ?????
        parc.ReturnReceipt = False
        parc.Instructions = delivery['Instructions'][:71]
        #TODO manage RegateCode si So Colissimo
        #parc.RegateCode =
        #TODO manage other categories
        contents = client.factory.create('ContentsVO')
        cat = client.factory.create('CategorieVO')
        cat.value = 3           # Envoi commercial
        contents.categorie = 3
        #TODO complete articles
        art = client.factory.create('ArticleVO')
        art.description = ''
        #TODO put real valeur
        art.valeur = 3.0
        art.quantite = 3
        art.poids = 5
        art.paysOrigine = 'FR'
        #art.numTarifaire = 5
        contents.article = art
        parc.contents = contents
        return parc

    def _set_address_dest(self, client, address):
        self.check_model(address, ADDRESS_MODEL, 'address')
        addr_dest = client.factory.create('AddressVO')
        self._address_vo(addr_dest, address)
        self._check_country_code(address['countryCode'])
        return addr_dest

    def _set_address_exp(self, client, sender):
        self.check_model(sender, SENDER_MODEL, 'sender')
        addr_exp = client.factory.create('AddressVO')
        if 'countryCode' not in sender or not sender['countryCode']:
            sender.update({'countryCode': 'FR'})
        self._address_vo(addr_exp, sender)
        return addr_exp

    def _address_vo(self, obj, info):
        "Common method for sender and destination address"
        elments = {
            'Name': 'name',
            'city': 'city',
            'postalCode': 'zip',
            'MobileNumber': 'mobile',
            'phone': 'phone',
            'email': 'email',
            'countryCode': 'countryCode',
            'country': False,
            'line0': 'street2',
            'line1': 'street3',
            'line2': 'street',
            'line3': False,
            'DoorCode1': 'door_code',
            'DoorCode2': 'door_code2',
            'Interphone': 'intercom',
            'Civility': False,
            'companyName': 'name',
        }
        for elm, val in elments.items():
            obj[elm] = ''
            if val in info:
                obj[elm] = info[val]
                if info[val] is False:
                    obj[elm] = ''
        obj['Surname'] = ' '
        return True

    def _check_country_code(self, country_code):
        if country_code != 'FR':
            if not countries.datas.get(country_code):
                raise InvalidCountry(
                    "Country code '%s' doesn't exists. \nCheck your datas"
                    % country_code)
        elif self._product_code[1:] == 'I':
            raise InvalidCountry("EI/AI label type can't be used for France")
        return True


class Colissimo(ColiPoste):

    def complete_and_check_datas(self, sender, delivery, address, option):
        if self._product_code in ['7Q', '8Q']:
            infos = {
                'phone': {'required': True},
                'country': {'required': True},
            }
            SENDER_MODEL.update(infos)
        option.update(self._populate_option_with_default_value(option))
        self.check_model(sender, SENDER_MODEL, 'sender')
        self.check_model(delivery, DELIVERY_MODEL, 'delivery')
        self.check_model(address, ADDRESS_MODEL, 'address')
        return True

    def _complete_kwargs(self, kwargs):
        return kwargs

    def get_cab_prise_en_charge(self, infos):
        # ordre de tri
        order = '1'
        zip_country = self._get_zip_country(
            infos.get('zip'), infos.get('countryCode'))
        # weight
        if self._product_code == '8R':
            # '8R' return label is not fully implemented
            weight = '0001 '
        else:
            if infos.get('weight'):
                if infos['weight'] > 30:
                    raise InvalidWeight(
                        "Weight limit for Colissimo is '30' or '20' kg.\n"
                        "Please check your product in parcel")
            else:
                raise InvalidWeight("Weight is required and is not specified")
            weight = str(int(round(infos['weight'] * 100))).zfill(4)
        # Tranche assurance Ad Valorem ou niveau de recommandation
            # TODO implement niveau de recommandation
        valor = '00'
        if 'insurance' in infos:
            valor = infos['insurance']
        # 'non mécanisable' colissimo
        nm = '0'
        if infos.get('nm'):
            nm = '1'
        # FTD/AR management done
            # TODO CRBT management
        crbt = '0'
        ftd = '0'
        ar = '0'
        # outre-mer
        if self._product_code == '7Q':
            if infos.get('ftd', False) is True:
                ftd = '1'
            if infos.get('ar', False) is True:
                ar = '1'
        crbt_ftd_ar = {
            '000': '0',
            '100': '1',
            '010': '2',
            '110': '3',
            '001': '4',
            '101': '5',
            '011': '6',
            '111': '7'}
        code_crbt_ftd_ar = crbt_ftd_ar[crbt + ftd + ar]
        carrier_track = infos.get('carrier_track')
        ctrl_link = carrier_track[-3]
        if carrier_track[-2:] == 'FR':
            ctrl_link = carrier_track[-6]
        barcode = (
            self._product_code
            + order
            + ' '
            + zip_country
            + ' '
            + self._account
            + ' '
            + weight
            + ' '
            + valor
            + nm
            + ''
            + code_crbt_ftd_ar
            + ctrl_link
        )
        #generate ctrl key
        barcode += str(self.get_ctrl_key(barcode[10:]))
        return barcode

    def _populate_option_with_default_value(self, option):
        for opt in ['nm', 'ar', 'ftd']:
            if opt not in option:
                option[opt] = False
        return option

    def test_colissmo(self):
        suivi_7Q_8V_9V_8L_9L = '20524 75203'
        prise_en_charge_all = '900 001 0860 00003'

        print '  >>> Code de suivi :'
        print 'other labels : control key for \'', suivi_7Q_8V_9V_8L_9L,
        print 'string is =>', self.get_ctrl_key(suivi_7Q_8V_9V_8L_9L)

        print '\n  >>> Code de prise en charge :'
        print 'all labels : control key for \'', prise_en_charge_all,
        print 'string is =>', self.get_ctrl_key(prise_en_charge_all)


class SoColissimo(ColiPoste):

    def complete_and_check_datas(self, sender, delivery, address, option):
        infos = {
            # TODO: is required ?
            'phone': {'required': True},
            'chargeur': {'max_size': 8}
        }
        if self._product_code in ['6J']:
            infos['chargeur'] = {'required': True, 'min_size': 9, 'max_size': 9}
        SENDER_MODEL.update(infos)
        ADDRESS_MODEL.update({
            # TODO check with SO Belgium
            "zip": {'required': True},
            })
        # TODO also validate the final partner zip
        self._get_zip_country(address['zip'])
        DELIVERY_MODEL.update({
            #"weight": {'required': True, 'max_number': 30},
            #"sequence": {'required': True, 'max_size': 10, 'min_size': 10},
            })
        option.update(self._populate_option_with_default_value(option))
        self.check_model(sender, SENDER_MODEL, 'sender')
        self.check_model(delivery, DELIVERY_MODEL, 'delivery')
        self.check_model(address, ADDRESS_MODEL, 'address')
        self._set_final_address(address)
        delivery['livraison_hors_domicile'] = ''
        if self._product_code in ['6M', '6J', '6H']:
            delivery['livraison_hors_domicile'] = address['final_address']['name'] + '\n\&'
        # choice between standard and specific label
        self._choose_label(address)
        if self._specific_label == '6MA':
            delivery['routage_barcode'] = self.routage_barcode(
                delivery, address)
            delivery['routage_barcode_full'] = \
                delivery['routage_barcode'].replace(' ', '')
        print '\ndelivery', delivery
        return True

    def _set_final_address(self, address):
        # Customer address, in 6M, 6J, 6H, is stored address['final_address']
        FINAL_ADDRESS = {
            'name': {'max_size': 100},
            'street': {'max_size': 100},
            'street2': {'max_size': 100},
            'street3': {'max_size': 100},
            'street4': {'max_size': 100},
            'zip': {'max_size': 10},
            'city': {'max_size': 100},
            'door_code': {'max_size': 100},
            'door_code2': {'max_size': 100},
            'intercom': {'max_size': 100},
            'mobile': {'max_size': 100},
            'phone': {'max_size': 100},
        }
        final_address = {}
        if 'final_address' in address:
            final_address = address['final_address']
        self.check_model(final_address, FINAL_ADDRESS, 'final_address')
        address['final_address'] = final_address
        return True

    def _choose_label(self, address):
        if (self._product_code == '6M'
                and 'lot_routing' in address and 'distri_sort' in address):
            assert isinstance(address['lot_routing'], (str, unicode))
            assert isinstance(address['distri_sort'], (str, unicode))
            self._specific_label = '6MA'
            return True

    def _complete_kwargs(self, kwargs):
        # logo avec signature
        kwargs['signature'] = 'SIGNA'
        if self._product_code == '6A':
            # sans signature
            kwargs['signature'] = 'SIGNS'
        # relative positionning element
        kwargs['vertical_text_box_width'] = 170
        kwargs['vertical_text_box_height'] = 290
        kwargs['vertical_text_pos_Y_suffix'] = 50
        if self._product_code in ['6H', '6M']:
            kwargs['vertical_text_pos_X'] = 560
            kwargs['vertical_text_pos_Y'] = 360
        elif self._product_code == '6J':
            kwargs['vertical_text_pos_X'] = 480
            kwargs['vertical_text_pos_Y'] = 570
        elif self._product_code in ['6A', '6C', '6K']:
            kwargs['vertical_text_pos_X'] = 590
            kwargs['vertical_text_pos_Y'] = 570
            kwargs['vertical_text_box_width'] = 140
            kwargs['vertical_text_pos_Y_suffix'] = 10
        return kwargs

    def _populate_option_with_default_value(self, option):
        for opt in ['nm']:
            if opt not in option:
                option[opt] = False
        return option

    def get_cab_prise_en_charge(self, infos):
        if self._specific_label == '6MA':
            zip_code = '91500'
        elif self._product_code in ['6J', '6H', '6M']:
            zip_code = infos['zip']
        else:
            #TODO FIXME wrong for dropoffsite
            zip_code = infos['zip']
        barcode = (
            self._product_code
            + '1 '
            + zip_code
            + ' '
            + self._account
            + " %04d " % (infos['weight'] * 100)
            #TODO support insurance
            + "00"
            + "%d" % infos.get('nm', 0) # non_machinable
            + "0"
            + infos['carrier_track'].replace(' ', '')[11]
        )
        barcode += self._build_control_key(barcode[10:])
        return barcode

    def routage_barcode(self, delivery, address):
        if self._product_code not in ['6A', '6C', '6K']:
            zip = address['zip'].zfill(7)
            suivi_barcode = delivery['cab_suivi'].replace(' ', '')
            barcode = '%' + zip[:4] + ' ' + zip[4:] + '6 '
            barcode += suivi_barcode[1:5] + ' ' + suivi_barcode[5:9]
            barcode += ' ' + suivi_barcode[9:13] + ' 0849 250'
            openbar_var = barcode + self.routage_get_ctrl_key(
                barcode.replace(' ', ''))
        return openbar_var

    def routage_get_ctrl_key(self, barcode):
        CAR = [str(x) for x in range(0, 10)]
        string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        CAR.extend([x for x in string])
        CS, MOD = 36, 36
        #First char '%' is not take account
        for i in barcode[1:]:
            Y = CAR.index(i)
            CS += Y
            if CS > MOD:
                CS -= MOD
            CS *= 2
            if CS > MOD:
                CS = CS - MOD - 1
        CS = MOD + 1 - CS
        if CS == MOD:
            CS = 0
        return CAR[CS]

    def check_required_and_set_default(self, fields, dicto, required_fields):
        for field in fields:
            if field not in dicto or dicto[field] is False:
                if field in required_fields:
                    raise InvalidMissingField("Required field '%s' is missing"
                                              % field)
                else:
                    dicto[field] = ''
        return True
