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
    'CY': 'EXPERT_I',
    'EY': 'EXPERT_I',
    '7Q': 'EXPERT_OM',
    '8R': 'SERVI_F',
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
    "cab_suivi":    {'required': True},
    "weight":                  {'required': True},
    "date":                    {'required': True, 'date': '%d/%m/%Y'},
}
SENDER_MODEL = {
    "name":         {'required': True},
    "street":       {'required': True},
    "zip":          {'required': True},
    "city":         {'required': True},
    "support_city": {'required': True},
}


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
        'colissimo': ['9V', '9L', '7Q', 'Y'],
        'so_colissimo': ['6C', '6A', '6K', '6H', '6J', '6M', '6MA']
    }

    def __init__(self, account):
        if not self._account:
            self._account = self._check_account(account)

    def get_service(self, service_name, code):
        if service_name == 'colissimo':
            service = Colissimo(self._account)
        else:
            service = SoColissimo(self._account)
        service._service, service._product_code = self._check_service(
            service_name, code)
        return service

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
        suffix = ''
        if self._product_code[1:] == 'Y':
            # Expert international colissimo have a suffix string
            # (>6 is for subset B character)
            suffix = ' FR'
        # '>5' is for subset C character
        return sequence + ' ' + str(self.get_ctrl_key(sequence[3:])) + suffix

    def _set_unit_test_file_name(self, name=None):
        if name:
            self._test_name = name

    def get_label(self, sender, delivery, address, option):
        sender.update({'account': self._account})
        if self._product_code in ['EY', 'CY', '7Q']:
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
        #TODO dirty tip to change in better way :
        #contact me if you know to import any existing text file
        #in python lib from an arbitrary execution path
        import laposte_api as api
        zpl_file = api.__file__.replace('__init__.py', 'report/') + zpl_file
        with open(zpl_file, 'r') as opened_file:
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
            path = '/tmp/'
            path += self._test_name + self._product_code + '.py'
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

    def print_label(self, printer_name, content, host='127.0.0.1'):
        #lp -d <zebra_printer> -h 192.168.1.3:631 my_file -o raw
        try:
            from cStringIO import StringIO
        except:
            from StringIO import StringIO
        import os
        file_content = StringIO()
        file_content.write(content)
        os.system('lp -d %s -h %s %s-o raw'
                  % (printer_name, file_content.get_value(), host))
        file_content.close()

    def _populate_option_with_default_value(self, option):
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


class Colissimo(ColiPoste):
    ""

    def get_cab_prise_en_charge(self, infos):
        if len(self._product_code) != 2:
            # exception for Y label
            raise("You must call 'get_product_code_for_foreign_country()' "
                  "method before to call 'get_cab_prise_en_charge()'")
        # ordre de tri
        order = '1'
        if self._product_code[1:] == 'Y':
            order = '2'
        zip_country = self._get_zip_country(
            infos.get('zip'), infos.get('country_code'))
        # weight
        if self._product_code == '8R':
            # '8R' is not fully implemented
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
            # TODO implement real values
        valor = '00'
        # 'non mécanisable' colissimo
        non_machinable = '0'
        if infos.get('non_machinable'):
            non_machinable = '1'
        # FTD/AR management done
            # TODO CRBT management
        crbt = '0'
        ftd = '0'
        ar = '0'
        # outre-mer
        if self._product_code == '7Q' \
                and infos.get('option_ftd', False) is True:
            ftd = '1'
        # outre mer + international
        # TODO calculate cy/ey with y + address
        if self._product_code in ['7Q', 'CY'] \
                and infos.get('option_ar', False) is True:
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
            + non_machinable
            + ''
            + code_crbt_ftd_ar
            + ctrl_link
        )
        #generate ctrl key
        barcode += str(self.get_ctrl_key(barcode[10:]))
        return barcode

    def _populate_option_with_default_value(self, option):
        for opt in ['non_machinable', 'ar', 'ftd']:
            if opt not in option:
                option[opt] = False
        return option

    def _get_zip_country(self, zip_code=None, country_code=None):
        if zip_code:
            zip_country = zip_code
            if self._product_code[1:] != 'Y':
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

    def get_product_code_for_foreign_country(self, country_code):
        """Foreign destination use CY or EY label.
        This method allow to select the right label."""
        if country_code != 'FR':
            if countries.datas.get(country_code):
                product_code = countries.datas[country_code].get('product')
                if not product_code:
                    raise InvalidCountry(
                        "'%s' country can't receive parcel from Colissimo "
                        "\n(country code '%s')"
                        % (countries.datas[country_code]['country'],
                           country_code))
                else:
                    self._product_code = product_code
            else:
                raise InvalidCountry(
                    "Country code '%s' doesn't exists. \nCheck your datas"
                    % country_code)
        elif self._product_code == 'Y':
            raise InvalidCountry("Y label type can't be used for France")
        return self._product_code

    def colissimo_international_calculation(self, key):
        """ CY / EY label colissimo specific calculation
            Y, Z, X variables are described in
            COLISSIMO EXPERT International documentation
        """
        coeff = {2: 7, 3: 9, 4: 5, 5: 3, 6: 2, 7: 4, 8: 6, 9: 8}
        position = 2
        Y = 0
        for arg in key:
            Y += int(arg) * coeff[position]
            position += 1
        Z = Y % 11
        if Z == 0:
            X = 5
        elif Z == 1:
            X = 0
        else:
            X = 11 - Z
        return X

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
        else:
            # CY/EY label colissimo specific calculation : len(key) is 8
            result = self.colissimo_international_calculation(key)
        return result

    def test_colissmo(self):
        suivi_7Q_8V_9V_8L_9L = '20524 75203'
        suivi_CY_or_EY = '2456 1983'
        prise_en_charge_all = '900 001 0860 00003'

        print '  >>> Code de suivi :'
        print 'CY or EY label : control key for \'', suivi_CY_or_EY,
        print ' string is =>', self.get_ctrl_key(suivi_CY_or_EY)
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
            + "%d" % delivery['non_machinable']
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
