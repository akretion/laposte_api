# -*- coding: utf-8 -*-

first_keys = {'prise_en_charge': u'6M1 91500 852450 0390 000013', 'tracking_ref': u'6M 00000 00001 7', 'sequence': u'6M 00000 00001'}

delivery = {'suivi_bar': u'6M0>50000000017', 'routage_barcode_full': u'%00101006M0000000001708492508', 'weight': '3.9', 'pec_bar': u'6M191500>58524500390000013', 'routage_barcode': u'%0010 1006 M000 0000 0017 0849 2508', 'cab_prise_en_charge': u'6M1 91500 852450 0390 000013', 'livraison_hors_domicile': u'Ella DUBOL\n\\&', 'date': '19/11/2014', 'cab_suivi': u'6M 00000 00001 7', 'ref_client': u'S0171', 'Instructions': ''}

sender = {'city': u'LUNEL', 'account': u'852450', 'name': u'Dessus Dessous', 'zip': u'34400', 'phone': u'+33 4 67 71 58 60', 'mobile': False, 'country': u'France', 'street2': '', 'chargeur': '', 'support_city': u'TOULOUSE CAPITOUL PFC', 'street': u'135 chemin de Cantadu', 'password': False, 'email': u'info@yourcompany.com'}

address = {'city': u'ROMILLY SUR SEINE', 'door_code2': '', 'name': u'JE CONSOLE', 'zip': u'10100', 'mobile': '', 'intercom': '', 'street2': '', 'street3': '', 'street4': '', 'email': '', 'phone': '', 'street': u'33 RUE DE LA BOULE D OR', 'name2': '', 'distri_sort': u'10R60', 'lot_routing': u'TOY', 'final_address': {'city': u'Paris', 'door_code2': '', 'name': u'Ella DUBOL', 'zip': u'75015', 'mobile': u'06.78.71.96.86', 'intercom': '', 'street2': '', 'street3': '', 'street4': '', 'phone': u'01.55.69.89.89', 'street': u'25 r Oscar Roty', 'door_code': ''}, 'door_code': '', '_specific_label': True}

option = {'nm': False, 'stds': True}

kwargs = {'vertical_text_pos_X': 560, 'vertical_text_pos_Y_suffix': 50, 'vertical_text_box_height': 290, 'vertical_text_box_width': 170, '_product_code': u'6M', 'signature': 'SIGNA', 'vertical_text_pos_Y': 360, 'logo': 'COMM'}

content = """/* Utf8 file encoded converted in CP1252 by python */
/* 6MA */
^XA
^LH30,30        /* initial position*/
^CI27           /* windows CP1252 decoding */
^CF0,22         /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN            /*FW:Default orientation*/
^BY3            /*BY:Bar Code Field Default*/

^FO10,01^XGE:SIGNA,1,1^FS
^FO680,01^XGE:COMM,1,1^FS

^FO0,90^GB770,1,4^FS   /*ligne sous image du haut */
^FO470,110^A0,30^FDEXPEDITEUR^FS
^FO5,110^FDRef Client: S0171^FS
/*GB:graphic box|width,height,thickness*/
^FO460,145^GB310,160,4^FS     /*bloc expediteur*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO460,145^GD300,160,10,,R^FS
^FO460,145^GD300,160,10,,L^FS
/*^A0 /*A:font|font_type,orientation,size*/*/
^FO480,175^A0,30,30^FDDessus Dessous^FS
^FO480,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
^A0,24^FD135 chemin de Cantadu
\&
\&34400 LUNEL^FS

^FO460,310^GB310,160,4^FS   /*bloc compte client*/
^FO470,320   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: 852450
\&SITE DE PRISE EN CHARGE:
\&TOULOUSE CAPITOUL PFC
\&N° Colis : 6M 00000 00001 7
\&Poids   : 3.9 kg
\&Edité le : 19/11/2014
^FS

/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO25,140^PR2,2^BCN,230,N,N,N^FD6M0>50000000017^FS
^FO25,370^GB402,3,4^FS  /*ligne sous code barre*/
^FO70,380^FDN° de colis : 6M 00000 00001 7^FS

/* /!\ /_\ /!\ /_\ /!\ */

^FO30,410^A0,30^FDDESTINATAIRE^FS

^FO5,440^GB450,200,4^FS
^FO25,450^A0,26,26^FDJE CONSOLE^FS
^FO25,475^FB400,6,2,
^FDElla DUBOL
\&33 RUE DE LA BOULE D OR
\&
\&10100 ROMILLY SUR SEINE^FS
^FO25,575^A0,36,46^FD91500^FS
^FO155,585^A0,28,38^FDHUB RELAIS^FS
^FO25,610^A0,18^FDTel mobile: 06.78.71.96.86^FS

^FO0,715^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
/* >5  => is subset C invocation code  */
^FO70,650^BCN,230,N,N,N^FD6M191500>58524500390000013^FS
^FO180,890^FDN° PCH:  6M1 91500 852450 0390 000013^FS
^FO0,890^XGE:POSTE,1,1^FS
^FO720,885^XGE:CAMERA,1,1^FS
^FO70,933^A0,60,80^FDTOY^FS
^FO220,948^A0,40,60^FDSA13 REL^FS
^FO480,940^A0,50,70^FD10R60^FS
^FO35,978^BCN,170,N,N,N^FD>:%>500101006>6M>5000000000170849250^FS
^FO230,1150^FD0010 1006 M000 0000 0017 0849 2508^FS
^FO35,978^GB695,1,4^FS
^XZ
"""