#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO define possible/mandatory option / label

"""
To know which keys to send to this library read these lists :
- required fields
- fields

in __init__ method for company information
and in manage_required_and_default_field method
"""

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
DEMO = True
#TODO pass the template as an argument
CODING = 'cp1252'
ERROR_BEHAVIOR = 'backslashreplace'
#TODO add a Exception error class
REQUIRED_FIELDS_ALERT = " /!\ !!! needs a valid value HERE !!! /!\ "


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

# Here is all keys used in coliposte templates
ADDRESS_MODEL = {
    "name":      {'required': True, 'max_size': 35},
    "street":    {'required': True, 'max_size': 35},
    "street2":   {'max_size': 35},
    "street3":   {'max_size': 35},
    "zip":       {'required': True, 'max_size': 10},
    "city":      {'required': True, 'max_size': 35},
    "phone":     {'max_size': 20},
    "mobile":    {'max_size': 20},
    "email":     {'max_size': 100},
}
DELIVERY_MODEL = {
    "weight":        {'required': True},
    "date":          {'required': True, 'date': '%d/%m/%Y'},
    "Instructions":  {'max_size': 70},
}
SENDER_MODEL = {
    "name":         {'required': True},
    "street":       {'required': True},
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


class ColiPoste(AbstractLabel):
    _account = None
    _service = None
    _product_code = None
    _test_name = None

    _label_code = {
        'colissimo': ['9V', '9L', '7Q', '8Q'],
        'so_colissimo': ['6C', '6A', '6K', '6H', '6J', '6M', '6MA'],
        'ColiPosteInternational': ['EI', 'AI', 'SO'],
    }

    def __init__(self, account):
        if not self._account:
            self._account = self._check_account(account)

    def get_service(self, service_name, code):
        if service_name == 'colissimo':
            if code in ['EI', 'AI']:
                service = WSInternational(self._account)
                service_name = 'ColiPosteInternational'
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

    def get_cab_suivi(self, sequence):
        #TODO define how to build sequence
        return sequence + ' ' + str(self.get_ctrl_key(sequence[3:]))

    def _set_unit_test_file_name(self, name=None):
        if name:
            self._test_name = name

    def get_label(self, sender, delivery, address, option):
        sender.update({'account': self._account})
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
        delivery.update({'suivi_bar': suivi_bar})
        # direct key values
        kwargs = {
            '_product_code': self._product_code,
            'logo': PRODUCT_LOGO[self._product_code],
        }
        zpl_file = self._service
        if self._product_code in ['6MA']:
            zpl_file = self._product_codeq
        zpl_file = zpl_file + '.mako'

        zpl_file_path = os.path.join(
            os.path.dirname(__file__),
            'report',
            zpl_file)
        with open(zpl_file_path, 'r') as opened_file:
            file_content = opened_file.read()
            try:
                zpl = Template(file_content).render(
                    d=delivery, s=sender, a=address, o=option, **kwargs)
                content = zpl.encode(encoding=CODING, errors=ERROR_BEHAVIOR)
                if self._test_name:
                    self._record_unit_test_datas(
                        content, delivery, sender, address, option, kwargs)
            except:
                traceback = RichTraceback()
                # allow to define where the file mako fail
                for (filename, lineno, fct, line) in traceback.traceback:
                    print "File %s, line %s, in %s" % (filename, lineno, fct)
                    print line, "\n"
                template = str(zpl_file[zpl_file.rfind('/')+1:])
                raise InvalidDataForMako(
                    "%s\nRequired key %s has not been received "
                    "by mako template \n\ntemplate: '%s' \nline: %s"
                    % (str(traceback.error.__class__.__name__),
                       traceback.error, template, lineno))
            return content

    def _record_unit_test_datas(
            self, file_content, delivery, sender, address, option, kwargs):
        try:
            import tempfile
            path = tempfile.gettempdir() + '/' + self._test_name + '.py'
            full_content = '# -*- coding: utf-8 -*-\n\n'
            full_content += 'delivery=' + str(delivery) + '\n\n'
            full_content += 'sender=' + str(sender) + '\n\n'
            full_content += 'address=' + str(address) + '\n\n'
            full_content += 'option=' + str(option) + '\n\n'
            full_content += 'kwargs=' + str(kwargs) + '\n\n'
            full_content += 'content="""' + file_content + '"""'
            with open(path, 'w') as wf:
                wf.write(full_content)
        except:
            raise "Invalid path %s" % path

    def print_label(self, printer_name, content):
        #lp -d <zebra_printer> -h 192.168.1.3:631 my_file -o raw
        #TODO debug
        try:
            from cStringIO import StringIO
        except:
            from StringIO import StringIO
        import os
        file_content = StringIO()
        file_content.write(content)
        os.system('lp -d %s -o raw %s'
                  % (printer_name, file_content.getvalue()))
        file_content.close()

    def _populate_option_with_default_value(self, option):
        for opt in ['ftd', 'ar', 'nm']:
            if opt not in option:
                option[opt] = False
        #TODO
        return option

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


class WSInternational(ColiPoste):

    def get_label(self, sender, delivery, address, option):
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
        if 'name' in delivery:
            exp.ref = delivery['name']
        letter.exp = exp
        self.unmystify_coliposte_webservice(letter)
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
        ws_mess_title = "WebService ColiPoste International\n\n%s"
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
                message = '\n'.join(self.extract_responses_messages(result))
                raise InvalidWebServiceRequest(ws_mess_title % message)
        except (WebFault, Exception) as e:
            raise InvalidWebServiceRequest(ws_mess_title % e.message)
        return res

    def encode_file_data(self, data):
        try:
            data = base64.b64decode(data).decode('iso-8859-15').encode('utf8')
        except (UnicodeEncodeError, Exception) as e:
            raise Exception(e.message)
        return data.replace('^XA', '^XA\n^CI28\n^LH20,0')

    def extract_responses_messages(self, result):
        response = []
        for mess in result.message:
            response.append(
                {'type': mess.type, 'id': mess.id, 'libelle': mess.libelle})
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
        ""
        self.check_model(delivery, DELIVERY_MODEL, 'delivery')
        parc = client.factory.create('ParcelVO')
        parc.typeGamme = self._product_code
        #TODO manage 'return type'
        parc.returnTypeChoice = 3
        #TODO manage insurance range
        parc.insuranceRange = '00'
        parc.insuranceAmount = 0
        parc.insuranceValue = 0
        #TODO manage weight with Access Internat.
        parc.weight = delivery['weight']
        parc.horsGabarit = str(int(option['nm']))
        #TODO manage HorsGabaritAmount
        parc.HorsGabaritAmount = 0
        #TODO manage DeliveryMode/RegateCode pour So Colissimo
        if self._product_code == 'SO':
            parc.DeliveryMode = 'DOM'  # or DOM/DOS/CMT/BDP
            parc.RegateCode = ''
        parc.ReturnReceipt = str(int(option['ar']))
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
            'companyName': False,
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
            if country_code == 'BE' and self._product_code != 'SO':
                raise InvalidCountry(
                    "Belgium destination must use 'SO' "
                    "product.\nCheck your datas"
                    % country_code)
        elif self._product_code[1:] == 'I':
            raise InvalidCountry("EI/AI label type can't be used for France")
        return True


class Colissimo(ColiPoste):

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
                        "Weight limit for Colissimo is '30' or '20' kg."
                        "Please check your stock move lines")
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

    def __init__(self, company):
        required_fields = [
            'name',
            'street',
            'street2',
            'zip',
            'city',
            'account',
            'center_support_city',
        ]
        fields = [
            'phone',
            'account_chargeur',
        ]
        fields.extend(required_fields)
        self.check_required_and_set_default(fields, company, required_fields)
        self.company = company

    def get_cab_suivi(self, delivery):
        control_key = self._build_control_key(delivery['sequence'])
        return "%s %s %s" % (delivery['product_code'],
                             delivery['sequence'],
                             control_key)

    def get_cab_prise_en_charge(self, delivery, company, dropoff_site, label):
        prod_code = delivery['product_code']
        if label.code == '6MA':
            zip_code = '91500'
        elif prod_code in ['6J', '6H', '6M']:
            zip_code = dropoff_site['zip']
        else:
            #TODO FIXME wrong for dropoffsite
            zip_code = delivery['address']['zip']
        barcode = (
            delivery['product_code']
            + '1 '
            + zip_code
            + ' '
            + company['account']
            + " %04d " % (delivery['weight'] * 100)
            #TODO support insurance
            + "00"
            + "%d" % delivery['nm'] # non_machinable
            + "0"
            + delivery['suivi_barcode'][12]
        )
        barcode += self._build_control_key(barcode[10:])
        return barcode

    def _validate_data(self, delivery, dropoff_site):
        #TODO validate also the dropsite zip
        if len(delivery['zip']) != 5:
            raise InvalidZipCode("Invalid zip code %s for France"
                                 % delivery['zip'])
        if delivery['weight'] > 30:
            raise InvalidWeight(
                "Invalid weight intead '%s' is superior to 30Kg"
                % delivery['weight'])
        if type(delivery['sequence']) not in [unicode, str]:
            raise InvalidSequence("The sequence must be an str or an unicode")
        if len(delivery['sequence']) != 10:
            raise InvalidSequence("The sequence len must be 10 instead of %s"
                                  % len(delivery['sequence']))
        if not delivery['sequence'].isdigit():
            raise InvalidSequence("Only digit char are authoried for"
                                  " the sequence")
        try:
            datetime.strptime(delivery['date'], '%d/%m/%Y')
        except ValueError:
            raise InvalidDate('The date must be at the format %d/%m/%Y')

    def get_label(self, label, delivery, dropoff_site):
        self._validate_data(delivery, dropoff_site)
        product_code = delivery['product_code']
        self.manage_required_and_default_field(delivery, dropoff_site)
        # direct key values
        kwargs = {'product_code': product_code, 'livraison_hors_domicile': ''}
        if product_code == '6J':
            if self.company['account_chargeur'] == '':
                kwargs['account_chargeur'] = REQUIRED_FIELDS_ALERT
            else:
                kwargs['account_chargeur'] = self.company['account_chargeur']
        # image 'France métropolitaine remise ...'
        if product_code == '6A':
            # sans signature
            kwargs['signature'] = 'SIGNS'
        else:
            # avec signature
            kwargs['signature'] = 'SIGNA'
        if product_code not in ['6A', '6C', '6K']:
            # produit colis 'mon domicile'
            kwargs['livraison_hors_domicile'] = delivery['address']['name'] \
                + '\n\&'
        kwargs['logo'] = PRODUCT_LOGO[product_code]

        delivery['suivi_barcode'] = self.get_cab_suivi(delivery)
        delivery['prise_en_charge_barcode'] = \
            self.get_cab_prise_en_charge(
                delivery, self.company, dropoff_site, label)

        if label.code == '6MA':
            kwargs['routage_barcode'] = self.routage_barcode(
                delivery, dropoff_site)
            kwargs['routage_barcode_full'] = kwargs['routage_barcode'].replace(
                ' ', '')
        else:
            # relative positionning element
            kwargs['vertical_text_box_width'] = 170
            kwargs['vertical_text_box_height'] = 290
            kwargs['vertical_text_pos_Y_suffix'] = 50
            if product_code in ['6H', '6M']:
                kwargs['vertical_text_pos_X'] = 560
                kwargs['vertical_text_pos_Y'] = 360
            elif product_code == '6J':
                kwargs['vertical_text_pos_X'] = 480
                kwargs['vertical_text_pos_Y'] = 570
            elif product_code in ['6A', '6C', '6K']:
                kwargs['vertical_text_pos_X'] = 590
                kwargs['vertical_text_pos_Y'] = 570
                kwargs['vertical_text_box_width'] = 140
                kwargs['vertical_text_pos_Y_suffix'] = 10

        zpl = Template(label.data).render(
            c=self.company, d=delivery, ds=dropoff_site, **kwargs)
        content = zpl.encode(encoding=CODING, errors=ERROR_BEHAVIOR)
        return {
            "zpl": content,
            "cab_suivi": delivery['suivi_barcode'],
            "cab_prise_en_charge": delivery['prise_en_charge_barcode'],
            "routage_barcode": kwargs.get('routage_barcode'),
        }

    #TODO FIXME should raise an error when fields are required
    #Also find a better way for empty fields
    def manage_required_and_default_field(self, delivery, dropoff_site):
        # delivery['address']
        required_fields = ['street', 'zip', 'city']
        fields = ['street2', 'street3', 'street4', 'door_code',
                  'door_code2', 'intercom', 'mobile', 'phone']
        fields.extend(required_fields)
        self.check_required_and_set_default(
            fields, delivery['address'], required_fields)
        # delivery
        required_fields = ['custom_shipping_ref', 'date', 'weight', 'sequence']
        fields = ['street2', 'street3', 'street4', 'phone', 'non_mecanisable']
        fields.extend(required_fields)
        self.check_required_and_set_default(fields, delivery, required_fields)

        if delivery['product_code'] in ['6M', '6J', '6H']:
            # dropoff_site
            required_fields = ['street', 'zip', 'city']
            fields = ['street2', 'street3', 'phone', 'name']
            fields.extend(required_fields)
            self.check_required_and_set_default(
                fields, dropoff_site, required_fields)
        return True

    def check_required_and_set_default(self, fields, dicto, required_fields):
        for field in fields:
            if field not in dicto or dicto[field] is False:
                if field in required_fields:
                    raise InvalidMissingField("Required field '%s' is missing"
                                              % field)
                else:
                    dicto[field] = ''
        return True

    def routage_barcode(self, delivery, dropoff_site):
        zip = dropoff_site['zip'].zfill(7)
        suivi_barcode = delivery['suivi_barcode'].replace(' ', '')
        barcode = '%' + zip[:4] + ' ' + zip[4:] + '6 '
        barcode += suivi_barcode[1:5] + ' ' + suivi_barcode[5:9]
        barcode += ' ' + suivi_barcode[9:13] + ' 0849 250'
        openbar_var = barcode + self.routage_get_ctrl_key(barcode.replace(
            ' ', ''))
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
            #print i, Y
        CS = MOD + 1 - CS
        if CS == MOD:
            CS = 0
        return CAR[CS]
