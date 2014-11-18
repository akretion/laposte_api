# -*- coding: utf-8 -*-

delivery={'weight': '13.9', 'pec_bar': u'9L169001>59647441390000023', 'suivi_bar': u'9L0>50000000024', 'cab_prise_en_charge': u'9L1 69001 964744 1390 000023', 'date': '12/05/2014', 'cab_suivi': u'9L 00000 00002 4', 'ref_client': u'OUT/00002', 'Instructions': ''}

sender={'city': u'city', 'account': u'964744', 'name': u'Your Company', 'zip': u'zip', 'phone': u'599', 'country': u'France', 'support_city': u'Gennevilliers PFC', 'street': u'rue', 'password': u'123456'}

address={'city': u'Lyon', 'name': u'Jim NHASTIC', 'zip': u'69001', 'mobile': '', 'street2': '', 'street3': '', 'countryCode': u'FR', 'phone': '', 'street': u'150 rue Vauban', 'email': ''}

option={'ar': False, 'nm': False, 'ftd': False}

kwargs={'logo': 'ACCESS_F', '_product_code': u'9L'}

content="""/* Utf8 file encoded converted in CP1252 by python */
^XA
^LH30,30          /* initial position*/
^CI27       /* windows CP1252 decoding */
^CF0,22    /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN    /*FW:Default orientation*/
^BY3    /*BY:Bar Code Field Default*/

^FO80,01^XGE:ACCESS_F,1,1^FS

^FO0,100^GB770,1,4^FS

^FO10,130^A0,30^FDEXPEDITEUR
^FS
^FO450,130^FDRef Client: OUT/00002^FS
^FO0,160^GB360,160,4^FS     /*GB:graphic box|width,height,thickness*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO0,160^GD350,160,10,,R^FS
^FO0,160^GD350,160,10,,L^FS
^FO410,160^GB360,160,4^FS
/*^A0 /*A:font|font_type,orientation,size*/*/
^FO25,175^A0,30,30^FDYour Company^FS
^FO25,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
/* COLISS RULE Teleph expediteur si OM ou I */
/* COLISS RULE Pays expediteur si OM ou I */
^A0,24^FDrue
\&
\&zip city
^FS

^FO420,170   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: 964744
\&SITE DE PRISE EN CHARGE:
\&Gennevilliers PFC
\&N° Colis : 9L 00000 00002 4
\&Poids   : 13.9 Kg
\&Edité le : 12/05/2014
^FS


/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO40,345^PR2,2^BCN,230,Y,N,N^FD9L0>50000000024^FS
^FO40,575^GB402,3,4^FS

^FO0,585^FDN° de colis :^FS


/* /!\ /_\ /!\ /_\ /!\ */

^FO30,630^A0,30^FDDESTINATAIRE^FS

^FO5,660^GB450,200,4^FS
^FO30,675^A0,24,28^FDJim NHASTIC^FS
^FO30,705^FB400,6,2,
^FD150 rue Vauban
\&
\&^FS
^FO30,755
^A0,40
^FD69001 Lyon^FS

/* COLISS RULE Phone+country expediteur si Internationale */
^FO30,800^FDTEL: ^FS
^FO0,950^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
^FO70,880^BCN,230,Y,N,N^FD9L169001>59647441390000023^FS
^FO100,1120^FDN° PCH:^FS
^FO0,1136^XGE:POSTE,1,1^FS
^FO720,1130^XGE:CAMERA,1,1^FS
^XZ
"""
