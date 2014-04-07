#!/usr/bin/env python

"""
This script produces a zpl printing langage output
to test font appearence in zebra printers
Tested with Zebra GX420t
"""

import string

# True to test only one font type in different size
SIZE_VARIATION = False

# used if SIZE_VARIATION == True
FONT_TYPE = '0'

# case text
UPPER = True
# font size
FONT_SIZE = 20
# text to display
SENTENCE = "Mais que fait la police "

# used if SIZE_VARIATION == True
FONT_SIZES = [12, 16, 20, 30, 40, 50, 60]

font = list(range(10))
font_alpha = [letter for letter in string.ascii_uppercase]
font.extend(font_alpha)

prefix = """^XA
^LH30,30

"""
if UPPER == True:
    SENTENCE = SENTENCE.upper()

if SIZE_VARIATION:
    font = FONT_SIZES

startline = 30
strlist = []

# fonts with schizo outputs
fonts_to_exclude = [5,6,7,8,9,'D','J','K','L','M','N','O','V','W','X','Y']

for elm in font:
    if SIZE_VARIATION:
        strlist.append("^FO10,%s^A%s,%s^FD%s:%s '%s' en taille %s ?^FS" % (startline, FONT_TYPE, elm, elm, SENTENCE, FONT_TYPE, elm))
        startline += 60
    else:
        if elm not in fonts_to_exclude:
            strlist.append("^FO10,%s^A%s,%s^FD%s:%s%s ?^FS" % (startline, elm, FONT_SIZE, elm, SENTENCE, elm))
            startline += 40
            if elm == 'U':
                startline += 40

font_samples = prefix + '\n'.join(strlist) + '\n\n^XZ'

myfile = open('font_samples','w')
myfile.write(str(font_samples))
myfile.close()
