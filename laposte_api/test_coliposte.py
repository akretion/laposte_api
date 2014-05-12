#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
import inspect
from .colissimo_and_so import ColiPoste
from .data import (
    colissimo_9L_nhas52b,
    colissimo_9L_hamp13b,
    colissimo_9L_hamp23b,
    colissimo_9V_hamp13,
    colissimo_9V_nhas11,
    colissimo_9V_nhas22,
    colissimo_7Q_camet11,
    colissimo_7Q_camet12,
    colissimo_7Q_anht33,
    colissimo_7Q_anht23,
    colissimo_7Q_camet14,
)


def current_function():
    return inspect.stack()[1][3]


class ColissimoTest(unittest2.TestCase):

    def setUp(self):
        pass

    def run_test(self, par):
        service = ColiPoste(par.sender['account']).get_service(
            'colissimo', par.kwargs['_product_code'])
        label = service.get_label(par.sender, par.delivery, par.address, par.option)
        self.assertEqual(label, par.content)

    def call_test(self, test_name_suffix):
        self.run_test(eval('colissimo_' + test_name_suffix[11:]))

    def test_label_9L_nhas52b(self):
        self.call_test(current_function())

    def test_label_9L_hamp13b(self):
        self.call_test(current_function())

    def test_label_9L_hamp23b(self):
        self.call_test(current_function())

    def test_label_9V_hamp13(self):
        self.call_test(current_function())

    def test_label_9V_nhas11(self):
        self.call_test(current_function())

    def test_label_9V_nhas22(self):
        self.call_test(current_function())

    def test_label_7Q_camet11(self):
        self.call_test(current_function())

    def test_label_7Q_camet12(self):
        self.call_test(current_function())

    def test_label_7Q_anht33(self):
        self.call_test(current_function())

    def test_label_7Q_anht23(self):
        self.call_test(current_function())

    def test_label_7Q_camet14(self):
        self.call_test(current_function())


def main():
    unittest2.main()

if __name__ == '__main__':
    main()
