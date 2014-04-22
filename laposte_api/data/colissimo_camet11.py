# -*- coding: utf-8 -*-

delivery={'date': '09/04/2014', 'carrier_tracking_ref_bar': u'7Q5>53894000014', 'carrier_tracking_ref': u'7Q 53894 00001 4', 'weight': '5.0'}

sender={'city': u'Villeurbanne', 'account': u'123456', 'name': u'Akretion', 'zip': u'69100', 'support_city': u'LYON', 'country': u'France', 'phone': u'04.99.99.99.99', 'street': u'35B rue Montgolfier'}

address={'city': u'Fort de France', 'name': u'L\xe9on CAMET', 'zip': u'97200', 'mobile': '', 'street2': '', 'street3': '', 'phone': '', 'street': u"3 rue d'\xe0 c\xf4t\xe9", 'country_code': u'FR', 'email': ''}

option={'non_machinable': False, 'ar': False, 'ftd': True}

kwargs={'logo': 'EXPERT_OM', '_product_code': u'7Q'}

content="""/* Utf8 file encoded converted in CP1252 by python */

/* PARAMETERS VARIABLES : Search VARY in comments */

^XA

^LH30,30          /* initial position*/

^CI27       /* windows CP1252 decoding */

^CF0,22    /*CF:default font|font_type,size*/

/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */

^FWN    /*FW:Default orientation*/

^BY3    /*BY:Bar Code Field Default*/



^FO80,01^XGE:EXPERT_OM,1,1^FS



^FO0,100^GB770,1,4^FS



^FO10,130^A0,30^FDEXPEDITEUR

^FS

^FO450,130^FDRef Client: Akretion^FS

^FO0,160^GB360,160,4^FS     /*GB:graphic box|width,height,thickness*/

/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/

^FO0,160^GD350,160,10,,R^FS

^FO0,160^GD350,160,10,,L^FS

^FO410,160^GB360,160,4^FS

/*^A0 /*A:font|font_type,orientation,size*/*/

^FO25,175^A0,30,30^FDAkretion^FS

^FO25,205   /*FO:field origin|x,y*/

^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/

/* COLISS RULE Teleph expediteur si OM ou I */

/* COLISS RULE Pays expediteur si OM ou I */

^A0,24^FD35B rue Montgolfier

\&TEL: 04.99.99.99.99

\&69100 Villeurbanne

\&France

^FS



^FO420,170   /*FO:field origin|x,y*/

^FB400,6,3,

^FDCOMPTE CLIENT: 123456

\&SITE DE PRISE EN CHARGE:

\&LYON

\&N° Colis : 7Q 53894 00001 4

\&Poids   : 5.0 Kg

\&Edité le : 09/04/2014

^FS





/* ||| || |||| */

/* >5  => is subset C invocation code ; >6  => is subset B invocation code */

^FO40,345^PR2,2^BCN,230,Y,N,N^FD7Q5>53894000014^FS

^FO40,575^GB

402

,3,4^FS



^FO0,585^FDN° de colis :^FS





/* /!\ /_\ /!\ /_\ /!\ */

^FO570,550^XGE:FTD,1,1^FS



^FO30,630^A0,30^FDDESTINATAIRE

^FS



^FO5,660^GB450,200,4^FS

^FO30,675^A0,24,28^FDLéon CAMET^FS

^FO30,705^FB400,6,2,

^FD3 rue d'à côté

\&

\&^FS

^FO30,755

^A0,40

^FD97200 Fort de France^FS



/* COLISS RULE Phone+country expediteur si Internationale */

^FO0,950^A0B^FDSPECIFIQUE^FS



/* ||| || |||| */

^FO70,880^BCN,230,Y,N,N^FD7Q5>53894000014^FS

^FO100,1120^FDN° PCH:^FS

^FO0,1130^XGE:POSTE,1,1^FS

^FO720,1130^XGE:CAMERA,1,1^FS

^XZ

"""
