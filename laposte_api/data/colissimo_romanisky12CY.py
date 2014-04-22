# -*- coding: utf-8 -*-

delivery={'date': '10/04/2014', 'carrier_tracking_ref_bar': u'CY0>500000045>6FR', 'carrier_tracking_ref': u'CY 0000 0004 5 FR', 'weight': '8.7'}

sender={'city': u'Villeurbanne', 'account': u'123456', 'name': u'Akretion', 'zip': u'69100', 'support_city': u'LYON', 'country': u'France', 'phone': u'04.99.99.99.99', 'street': u'35B rue Montgolfier'}

address={'city': u'Budapest', 'name': u'Sylvie ROMANISKY', 'zip': u'1062', 'mobile': '', 'street2': u'Lendway ut ca 27,', 'street3': '', 'phone': '', 'street': u'Ambassade de France', 'country_code': u'HU', 'email': ''}

option={'non_machinable': False, 'ar': False, 'ftd': False}

kwargs={'logo': 'EXPERT_I', '_product_code': 'CY'}

content="""/* Utf8 file encoded converted in CP1252 by python */
/* PARAMETERS VARIABLES : Search VARY in comments */
^XA
^LH30,30          /* initial position*/
^CI27       /* windows CP1252 decoding */
^CF0,22    /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN    /*FW:Default orientation*/
^BY3    /*BY:Bar Code Field Default*/

^FO80,01^XGE:EXPERT_I,1,1^FS

^FO0,100^GB770,1,4^FS

^FO10,130^A0,30^FDEXPEDITEUR
/ SENDER
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
\&N° Colis : CY 0000 0004 5 FR
\&Poids   : 8.7 Kg
\&Edité le : 10/04/2014
^FS

^FO30,330^FDAttention : le colis peut etre ouvert d'office^FS

/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO40,345^PR2,2^BCN,230,Y,N,N^FDCY0>500000045>6FR^FS
^FO40,575^GB
468
,3,4^FS

^FO0,585^FDN° de colis :^FS


/* /!\ /_\ /!\ /_\ /!\ */

^FO30,630^A0,30^FDDESTINATAIRE
 / ADDRESSEE
^FS

^FO5,660^GB450,200,4^FS
^FO30,675^A0,24,28^FDSylvie ROMANISKY^FS
^FO30,705^FB400,6,2,
^FDAmbassade de France
\&Lendway ut ca 27,
\&^FS
^FO30,755
^FD1062 Budapest^FS

/* COLISS RULE Phone+country expediteur si Internationale */
/* only for Y ?*/
^FO30,780^FDTEL: ^FS
^A0,40^FO30,810^FDSylvie ROMANISKY - HU^FS
^FO0,950^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
^FO70,880^BCN,230,Y,N,N^FDCY0>500000045>6FR^FS
^FO100,1120^FDN° PCH:^FS
^FO0,1130^XGE:POSTE,1,1^FS
^FO720,1130^XGE:CAMERA,1,1^FS
^XZ
"""