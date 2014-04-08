laposte_api
===========

WORK IN PROGRESS

'laposte_api' is a library for Python to generate label for Laposte (France), transportation services

This library allow to produce ZPL files used to print parcel label with Zebra printers

The available services are :
- Colissimo

    * Colissimo France works
    * Colissimo International works only up to 2014 July. Since this date La Poste rules change with mandatory web service use (NOT implemented)
- So Colissimo (on roadmap: partially implemented : DO NOT USE for now)


#Installation

The easiest way to install laposte_api:

    python setup.py install

#Usage
    WORK IN PROGESS

    from laposte_api.colissimo_and_so import ColiPoste, InvalidDataForMako
    from laposte_api.exception_helper import (
        InvalidWeight,
        InvalidSize,
        InvalidMissingField,
        InvalidCode,
        InvalidZipCode,
        InvalidCountry,
        InvalidKeyInTemplate,
        InvalidType)

    WARNING = "'Colissimo and So' warning :\n"
    service = ColiPoste(account).get_service(product, code)
    if self._product == 'Y' and country_code:
        try:
            label_name = service.get_product_code_for_foreign_country(country_code)
        except InvalidCountry, e:
            raise (WARNING + e.message)
        except Exception, e:
            raise Exception("'Colissimo and So' Library Error :\n" + e.message)

    # Your system must built sequence according to laposte specifications
    # depends on self._product_code
    carrier_tracking_ref = service.get_carrier_tracking_ref(sequence)
    try:
        barcode = service.get_cab_prise_en_charge(infos)
    except InvalidWeight, e:
        raise InvalidWeight(WARNING + e.message)
    infos = {
        'zip': zip,
        'country_code': country_code or '',
        'weight': weight,
        'carrier_track': carrier_tracking_ref,
    }
    try:
        barcode = service.get_cab_prise_en_charge(infos)
    except InvalidWeight, e:
        raise (WARNING + e.message)
    label = {
        'file_type': 'zpl2',
        'name': 'File name' + '.zpl',
    }
    try:
        # sender, delivery, address and option are dict contains datas
        # used to generate label in ZPL format (Zebra Programming Language)
        label['file'] = service.get_label(
            sender, delivery, address, option)
    except (InvalidDataForMako, InvalidKeyInTemplate, InvalidMissingField), e:
        raise (WARNING + e.message)
    except Exception, e:
        raise Exception("'Colissimo and So' Library Error :\n" + e.message)


#Specification
see doc folder


#Copyright and License

laposte_api is copyright (c) 2014 David Béal <david.beal@akretion.com>

licence : GNU Affero General Public License
