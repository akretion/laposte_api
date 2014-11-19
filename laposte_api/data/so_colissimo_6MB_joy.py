# -*- coding: utf-8 -*-

first_keys = {'prise_en_charge': u'6M1 91500 852450 0130 000037', 'tracking_ref': u'6M 00000 00003 1', 'sequence': u'6M 00000 00003'}

delivery = {'suivi_bar': u'6M0>50000000031', 'routage_barcode_full': u'%00932206M000000000310849250Y', 'weight': '1.3', 'pec_bar': u'6M191500>58524500130000037', 'routage_barcode': u'%0093 2206 M000 0000 0031 0849 250Y', 'cab_prise_en_charge': u'6M1 91500 852450 0130 000037', 'livraison_hors_domicile': u'Elvire DEBORD\n\\&', 'date': '19/11/2014', 'cab_suivi': u'6M 00000 00003 1', 'ref_client': u'S0173', 'Instructions': ''}

sender = {'city': u'LUNEL', 'account': u'852450', 'name': u'Dessus Dessous', 'zip': u'34400', 'phone': u'+33 4 67 71 58 60', 'mobile': False, 'country': u'France', 'street2': '', 'chargeur': '', 'support_city': u'TOULOUSE CAPITOUL PFC', 'street': u'135 chemin de Cantadu', 'password': False, 'email': u'info@yourcompany.com'}

address = {'city': u'GAGNY', 'door_code2': '', 'name': u'JOYSUN', 'zip': u'93220', 'mobile': '', 'intercom': '', 'street2': '', 'street3': '', 'street4': '', 'email': '', 'phone': '', 'street': u'16 PLACE DU GENERAL DE GAULLE', 'name2': '', 'distri_sort': u'93V12', 'lot_routing': u'BBY0', 'final_address': {'city': u'Paris', 'door_code2': '', 'name': u'Elvire DEBORD', 'zip': u'75018', 'mobile': u'06.78.71.96.72', 'intercom': '', 'street2': '', 'street3': '', 'street4': '', 'phone': u'01.55.69.89.75', 'street': u'3 r Dancourt', 'door_code': ''}, 'door_code': '', '_specific_label': True}

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
^FO5,110^FDRef Client: S0173^FS
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
\&N° Colis : 6M 00000 00003 1
\&Poids   : 1.3 kg
\&Edité le : 19/11/2014
^FS

/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO25,140^PR2,2^BCN,230,N,N,N^FD6M0>50000000031^FS
^FO25,370^GB402,3,4^FS  /*ligne sous code barre*/
^FO70,380^FDN° de colis : 6M 00000 00003 1^FS

/* /!\ /_\ /!\ /_\ /!\ */

^FO30,410^A0,30^FDDESTINATAIRE^FS

^FO5,440^GB450,200,4^FS
^FO25,450^A0,26,26^FDJOYSUN^FS
^FO25,475^FB400,6,2,
^FDElvire DEBORD
\&16 PLACE DU GENERAL DE GAULLE
\&
\&93220 GAGNY^FS
^FO25,575^A0,36,46^FD91500^FS
^FO155,585^A0,28,38^FDHUB RELAIS^FS
^FO25,610^A0,18^FDTel mobile: 06.78.71.96.72^FS

^FO0,715^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
/* >5  => is subset C invocation code  */
^FO70,650^BCN,230,N,N,N^FD6M191500>58524500130000037^FS
^FO180,890^FDN° PCH:  6M1 91500 852450 0130 000037^FS
^FO0,890^XGE:POSTE,1,1^FS
^FO720,885^XGE:CAMERA,1,1^FS
^FO70,933^A0,60,80^FDBBY0^FS
^FO265,948^A0,40,60^FDSA13 REL^FS
^FO520,940^A0,50,70^FD93V12^FS
^FO35,978^BCN,170,N,N,N^FD>:%>500932206>6M>5000000000310849250^FS
^FO230,1150^FD0093 2206 M000 0000 0031 0849 250Y^FS
^FO35,978^GB695,1,4^FS
^XZ
"""