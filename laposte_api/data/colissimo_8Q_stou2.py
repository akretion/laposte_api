# -*- coding: utf-8 -*-

first_keys = {'prise_en_charge': u'8Q1 97212 806951 0630 001029', 'tracking_ref': u'8Q 0000000002 4', 'sequence': u'8Q 0000000002'}

delivery = {'weight': '6.3', 'pec_bar': u'8Q197212>58069510630001029', 'suivi_bar': u'8Q0>50000000024', 'cab_prise_en_charge': u'8Q1 97212 806951 0630 001029', 'date': '13/07/2014', 'cab_suivi': u'8Q 0000000002 4', 'ref_client': u'OUT/00022', 'Instructions': ''}

sender = {'city': u'Tarascon', 'account': u'806951', 'name': u'PlayRapid', 'zip': u'13150', 'phone': u'04 99 99 99 99', 'mobile': False, 'country': u'France', 'street2': False, 'support_city': u'Cavaillon PFC', 'street': u'210 Route des Cayades', 'password': u'PLAY', 'email': u'info@yourcompany.com'}

address = {'city': u'Saint Joseph', 'name': u'Marie STOURHNE', 'zip': u'97212', 'mobile': '', 'street2': '', 'street3': '', 'countryCode': u'MQ', 'phone': '', 'street': u'rue germain', 'email': ''}

option = {'ar': False, 'nm': True, 'ftd': False}

kwargs = {'logo': 'ACCES_OM', '_product_code': u'8Q'}

content = """/* Utf8 file encoded converted in CP1252 by python */
^XA
^LH30,30          /* initial position*/
^CI27       /* windows CP1252 decoding */
^CF0,22    /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN    /*FW:Default orientation*/
^BY3    /*BY:Bar Code Field Default*/

^FO80,01^XGE:ACCES_OM,1,1^FS

^FO0,100^GB770,1,4^FS

^FO10,130^A0,30^FDEXPEDITEUR
^FS
^FO450,130^FDRef Client: OUT/00022^FS
^FO0,160^GB360,160,4^FS     /*GB:graphic box|width,height,thickness*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO0,160^GD350,160,10,,R^FS
^FO0,160^GD350,160,10,,L^FS
^FO410,160^GB360,160,4^FS
/*^A0 /*A:font|font_type,orientation,size*/*/
^FO25,175^A0,30,30^FDPlayRapid^FS
^FO25,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
/* COLISS RULE Teleph expediteur si OM ou I */
/* COLISS RULE Pays expediteur si OM ou I */
^A0,24^FD210 Route des Cayades
\&
TEL: 04 99 99 99 99
\&13150 Tarascon
\&France
^FS

^FO420,170   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: 806951
\&SITE DE PRISE EN CHARGE:
\&Cavaillon PFC
\&N° Colis : 8Q 0000000002 4
\&Poids   : 6.3 Kg
\&Edité le : 13/07/2014
^FS


/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO40,345^PR2,2^BCN,230,Y,N,N^FD8Q0>50000000024^FS
^FO40,575^GB402,3,4^FS

^FO0,585^FDN° de colis :^FS


/* /!\ /_\ /!\ /_\ /!\ */
^FO570,350^XGE:NM,1,1^FS

^FO30,630^A0,30^FDDESTINATAIRE^FS

^FO5,660^GB450,200,4^FS
^FO30,675^A0,24,28^FDMarie STOURHNE^FS
^FO30,705^FB400,6,2,
^FDrue germain
\&
\&^FS
^FO30,755
^A0,40
^FD97212 Saint Joseph^FS

/* COLISS RULE Phone+country expediteur si Internationale */
^FO30,800^FDTEL: ^FS
^FO0,950^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
^FO70,880^BCN,230,Y,N,N^FD8Q197212>58069510630001029^FS
^FO100,1120^FDN° PCH:^FS
^FO0,1136^XGE:POSTE,1,1^FS
^FO720,1130^XGE:CAMERA,1,1^FS
^XZ
"""
