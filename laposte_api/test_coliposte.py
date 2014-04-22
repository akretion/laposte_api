#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from colissimo_and_so import ColiPoste
from .data import (
    colissimo_nhas11,
    colissimo_nhas22,
    colissimo_hamp13,
    colissimo_hamp23,
    colissimo_hamp14,
    colissimo_camet11,
    colissimo_camet12,
    colissimo_anht33,
    colissimo_anht23,
    colissimo_camet14,
)


class ColissimoTest(unittest2.TestCase):

    def setUp(self):
        pass

    def run_test(d):
        delivery, sender, address = d.delivery, d.sender, d.address
        option, kwargs, content = d.option, d.kwargs, d.content
        code = kwargs['_product_code']
        country_code = sender['country']
        service = ColiPoste(sender['account']).get_service('colissimo', kwargs['_product_code'])
        if code == 'Y' and country_code:
            try:
                label_name = service.get_product_code_for_foreign_country(country_code)
            except Exception, e:
                raise Exception(e.message)
        label = colisimo.get_etiquette(data['params'])
        if label != data['label']:
            assertEqual(label, data['label'])

    def test_label_nhas11(self):
        self.run_test(colissimo_nhas11)


def main():
    unittest2.main()

if __name__ == '__main__':
    main()

