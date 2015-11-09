laposte_api
===========

'laposte_api' is a library for Python to generate label for Laposte (France), transportation services

This library allow to produce ZPL files used to print parcel label with Zebra printers

The available services are:
- Colissimo

    * Colissimo France
    * Colissimo International with web service.
- So Colissimo


#Motivation

The first objective of this code is to provide to applications
ZPL files generation?
The first application in which it is used is Odoo / OpenERP.


#Installation

The easiest way to install laposte_api:

    pip install git+https://github.com/akretion/laposte_api.git

#Usage

    #Example for Colissimo transportation service in France

    from laposte_api.colissimo_and_so import (
        ColiPoste,
        InvalidDataForMako)

    from laposte_api.exception_helper import (
        InvalidWeight,
        InvalidSize,
        InvalidMissingField,
        InvalidCode,
        InvalidZipCode,
        InvalidCountry,
        InvalidKeyInTemplate,
        InvalidType)

    # example datas : update with demo datas in ColiPoste specs
    product = 'colissimo'
    label_code = '9V'
    account = '766666'
    parcel_weight = 5


    def get_sequence(label_code):
        """ Sequence must be unique and set only once
            Range numbers are defined by La Poste
            Define your OWN method
        """
        return '9V 00000 00006' #example

    try:
        service = ColiPoste(account).get_service(product, label_code)
    except (InvalidSize, InvalidCode, InvalidType, Exception) as e:
        raise

    tracking_ref = service.get_cab_suivi(get_sequence(label_code))
    
    sender = {
        'city': u'Paris', 'account': account, 'name': u'My Company',
        'zip': u'75001', 'phone': u'01 99 99 99 99', 'country': u'France',
        'support_city': u'MOISSY  PFC', 'street': u'1 rue Clignacourt',
        'email': u'info@mycompany.com'}

    address = {
        'city': u'Lyon', 'name': u'Jim NHASTIC', 'zip': u'69001',
        'countryCode': u'FR', 'street': u'150 rue Vauban'}


    infos = {
        'zip': address['zip'],
        'countryCode': address['countryCode'],
        'weight': parcel_weight,
        'carrier_track': tracking_ref,
    }

    option = {'ftd': False, 'ar': False, 'nm': True, 'insurance': u'03'}
    infos.update(option)

    try:
        prise_en_charge_barcode = service.get_cab_prise_en_charge(infos)
    except (InvalidWeight, Exception) as e:
        raise

    delivery = {
        'weight': parcel_weight, 'date': '22/06/2014',
        'ref_client': u'OUT/00033', 'Instructions': '',
        'cab_suivi': tracking_ref,
        'cab_prise_en_charge': prise_en_charge_barcode,
        }


    try:
        # sender, delivery, address and option are dict contains datas
        # used to generate label in ZPL format (Zebra Programming Language)
        label_file = service.get_label(
            sender, delivery, address, option)
        # you can send these datas to your zebra printer
    except (InvalidDataForMako,
            InvalidKeyInTemplate,
            InvalidKeyInTemplate,
            InvalidMissingField) as e:
        raise

    print "VOICI L'ETIQUETTE ZPL POUR COLISSIMO France:\n"
    print "=========================================\n\n\n", label_file

#Specification
see doc folder


#Copyright and License

laposte_api is copyright (c) 2014 David Béal <david.beal@akretion.com>

licence : GNU Affero General Public License
