# -*- coding: utf-8 -*-

first_keys = {'prise_en_charge': u'6M1 12740 852450 0520 000029', 'tracking_ref': u'6M 00000 00002 4', 'sequence': u'6M 00000 00002'}

delivery = {'weight': '5.2', 'pec_bar': u'6M112740>58524500520000029', 'suivi_bar': u'6M0>50000000024', 'cab_prise_en_charge': u'6M1 12740 852450 0520 000029', 'livraison_hors_domicile': u'Camille HONNETE\n\\&', 'date': '19/11/2014', 'cab_suivi': u'6M 00000 00002 4', 'ref_client': u'S0172', 'Instructions': ''}

sender = {'city': u'LUNEL', 'account': u'852450', 'name': u'Dessus Dessous', 'zip': u'34400', 'phone': u'+33 4 67 71 58 60', 'mobile': False, 'country': u'France', 'street2': '', 'chargeur': '', 'support_city': u'TOULOUSE CAPITOUL PFC', 'street': u'135 chemin de Cantadu', 'password': False, 'email': u'info@yourcompany.com'}

address = {'city': u'SEBAZAC CONCOURES', 'door_code2': '', 'name': u'JOLYS FLEURS', 'zip': u'12740', 'mobile': '', 'intercom': '', 'street2': '', 'street3': '', 'street4': '', 'email': '', 'phone': '', 'street': u'60 AVENUE LOUIS TABARDEL', 'name2': '', 'final_address': {'city': u'Paris', 'door_code2': '', 'name': u'Camille HONNETE', 'zip': u'75018', 'mobile': u'06.78.71.96.80', 'intercom': '', 'street2': '', 'street3': '', 'street4': '', 'phone': u'01.55.69.89.83', 'street': u'16 r Letort', 'door_code': ''}, 'door_code': ''}

option = {'nm': False, 'stds': True}

kwargs = {'vertical_text_pos_X': 560, 'vertical_text_pos_Y_suffix': 50, 'vertical_text_box_height': 290, 'vertical_text_box_width': 170, '_product_code': u'6M', 'signature': 'SIGNA', 'vertical_text_pos_Y': 360, 'logo': 'COMM'}

content = """/* Utf8 file encoded converted in CP1252 by python */
^XA
^LH30,30        /* initial position*/
^CI27           /* windows CP1252 decoding */
^CF0,22         /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN            /*FW:Default orientation*/
^BY3            /*BY:Bar Code Field Default*/

^FO10,01^XGE:SIGNA,1,1^FS
^FO680,01^XGE:COMM,1,1^FS

^FO0,100^GB770,1,4^FS   /*ligne sous image du haut */
^FO10,130^A0,30^FDEXPEDITEUR^FS
^FO450,130^FDRef Client: S0172^FS
/*GB:graphic box|width,height,thickness*/
^FO0,160^GB360,160,4^FS     /*bloc expediteur*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO0,160^GD350,160,10,,R^FS
^FO0,160^GD350,160,10,,L^FS
^FO25,175^A0,30,30^FDDessus Dessous^FS
^FO25,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
^A0,24^FD135 chemin de Cantadu
\&
\&34400 LUNEL^FS


^FO410,160^GB360,160,4^FS   /*bloc compte client*/
^FO420,170   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: 852450
\&SITE DE PRISE EN CHARGE:
\&TOULOUSE CAPITOUL PFC
\&N° Colis : 6M 00000 00002 4
\&Poids   : 5.2 kg
\&Edité le : 19/11/2014
^FS


/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO40,345^PR2,2^BCN,230,N,N,N^FD6M0>50000000024^FS
^FO40,575^GB402,3,4^FS
^FO90,585^FDN° de colis : 6M 00000 00002 4^FS


/* /!\ /_\ /!\ /_\ /!\ */

^FO30,630^A0,30^FDDESTINATAIRE^FS

^FO5,660^GB465,200,4^FS
^FO30,675^A0,24,26^FDJOLYS FLEURS^FS

^FO30,705^A0,24,26^FD^FS
^FO30,735^FB400,6,2,
^FDCamille HONNETE
\&60 AVENUE LOUIS TABARDEL
\&^FS
^FO30,810^A0,36,46^FD12740^FS
^FO160,815^A0,32,26^FDSEBAZAC CONCOURES^FS



/* vertical text */
^FO560,360^GB170,290,4^FS
^FO580,240
^A0B,18

/* Field block */
^FB400,6,2
^FDAdresse 1: 16 r Letort
\&Adresse 2: 
\&Adresse 3: 
\&Adresse 4: 
\&75018 Paris
\&Téléphone : 06.78.71.96.80^FS

^FO0,950^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
/* >5  => is subset C invocation code  */
^FO70,880^BCN,230,N,N,N^FD6M112740>58524500520000029^FS
^FO230,1120^FDN° PCH:  6M1 12740 852450 0520 000029^FS
^FO0,1125^XGE:POSTE,1,1^FS
^FO720,1120^XGE:CAMERA,1,1^FS

^XZ
"""