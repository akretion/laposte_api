#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
import inspect
import difflib
import os
from laposte_api.colissimo_and_so import ColiPoste
from laposte_api.data import (
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
    colissimo_8Q_ahj2,
    colissimo_8Q_stou2,
)


def current_function():
    return inspect.stack()[1][3]


class ColissimoTest(unittest2.TestCase):

    def setUp(self):
        pass

    def run_test(self, script_name):
        script = eval(script_name)
        service = ColiPoste(script.sender['account']).get_service(
            'colissimo', script.kwargs['_product_code'])
        label = service.get_label(
            script.sender, script.delivery, script.address, script.option)
        diff = difflib.unified_diff(label, script.content)
        files = [
            {'path': "/tmp/script-%s.txt" % script_name, 'type': 'script'},
            {'path': "/tmp/label-%s.txt" % script_name, 'type': 'label'}]
        for elm in files:
            with open(elm['path'], 'w') as f:
                if elm['type'] == 'script':
                    f.write(script.content)
                else:
                    f.write(label)
        if label != script.content:
            print '\n', script_name, '\n', ''.join(diff)
            meld_cmd = 'meld %s %s' % (files[0]['path'], files[1]['path'])
            os.system(meld_cmd)
        self.assertEqual(label, script.content)

    def call_test(self, test_name_fonction):
        script_name = 'colissimo_' + test_name_fonction[11:]
        self.run_test(script_name)

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

    def test_label_8Q_ahj2(self):
        self.call_test(current_function())

    def test_label_8Q_stou2(self):
        self.call_test(current_function())


def main():
    unittest2.main()

if __name__ == '__main__':
    main()
