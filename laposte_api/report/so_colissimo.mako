## -*- coding: utf-8 -*-
/* Utf8 file encoded converted in CP1252 by python */
^XA
^LH30,30        /* initial position*/
^CI27           /* windows CP1252 decoding */
^CF0,22         /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN            /*FW:Default orientation*/
^BY3            /*BY:Bar Code Field Default*/

^FO10,01^XGE:${signature},1,1^FS
^FO680,01^XGE:${logo},1,1^FS

^FO0,100^GB770,1,4^FS   /*ligne sous image du haut */
^FO10,130^A0,30^FDEXPEDITEUR^FS
^FO450,130^FDRef Client: ${d['ref_client']}^FS
/*GB:graphic box|width,height,thickness*/
^FO0,160^GB360,160,4^FS     /*bloc expediteur*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO0,160^GD350,160,10,,R^FS
^FO0,160^GD350,160,10,,L^FS
^FO25,175^A0,30,30^FD${s['name']}^FS
^FO25,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
^A0,24^FD${s['street']}
\&${s['street2']}
\&${s['zip']} ${s['city']}^FS


^FO410,160^GB360,160,4^FS   /*bloc compte client*/
^FO420,170   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: ${s['account']}
\&SITE DE PRISE EN CHARGE:
\&${s['support_city']}
\&N° Colis : ${d['cab_suivi']}
\&Poids   : ${d['weight']} kg
\&Edité le : ${d['date']}
^FS


/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
% if len(d['suivi_bar']) >1 :
^FO40,345^PR2,2^BCN,230,N,N,N^FD${d['suivi_bar']}^FS
^FO40,575^GB402,3,4^FS
^FO90,585^FDN° de colis : ${d['cab_suivi']}^FS

% if _product_code == '6J':
^FO670,370^BY3,,80^BCR,100,N,N,N^FD>:${s['chargeur'][0:1] + '>5'}${s['chargeur'][1:]}^FS
^FO650,460^A0B,18^FD${s['chargeur']}^FS
% endif
% endif

/* /!\ /_\ /!\ /_\ /!\ */
% if o['nm']:
^FO400,590^XGE:NM,1,1^FS
% endif

^FO30,630^A0,30^FDDESTINATAIRE^FS

% if _product_code in ['6C','6A', '6K']:
^FO5,660^GB465,200,4^FS
^FO30,675^A0,24,28
^FD${a['final_address']['name']}^FS
^FO30,705^FB400,6,2,
^FD${a['final_address']['street']}
\&${a['final_address']['street2'] or ''}^FS
^FO30,780^A0,40^FD${a['final_address']['zip']} ${a['final_address']['city']}^FS
%else:
^FO5,660^GB465,200,4^FS
^FO30,675^A0,24,26^FD${a['name']}^FS
%if 'name2' in a:

^FO30,705^A0,24,26^FD${a['name2']}^FS
^FO30,735^FB400,6,2,
^FD${d['livraison_hors_domicile']}${a['street']}
\&${a['street2'] or ''}^FS
^FO30,810^A0,36,46^FD${a['zip']}^FS
^FO160,815^A0,32,26^FD${a['city']}^FS

%else:

^FO30,705^FB400,6,2,
^FD${d['livraison_hors_domicile']}${a['street']}
\&${a['street2'] or ''}^FS
^FO30,780^A0,36,46^FD${a['zip']}^FS
^FO160,785^A0,32,26^FD${a['city']}^FS
%endif

%endif

/* vertical text */
^FO${vertical_text_pos_X},${vertical_text_pos_Y}^GB${vertical_text_box_width},${vertical_text_box_height},4^FS
^FO${vertical_text_pos_X + 20},${vertical_text_pos_Y - vertical_text_box_width + vertical_text_pos_Y_suffix}
^A0B,18

/* Field block */
^FB400,6,2
% if _product_code in ['6C','6A', '6K']:
^FDCode porte : ${a['final_address']['door_code']}
\&Code porte2 : ${a['final_address']['door_code2']}
\&Interphone : ${a['final_address']['intercom']}
\&Tél. Portable: ${a['final_address']['mobile']}
\&Téléphone : ${a['final_address']['phone']}^FS
% elif _product_code in ['6H', '6M', '6J']:
^FDAdresse 1: ${a['final_address']['street']}
\&Adresse 2: ${a['final_address']['street2']}
\&Adresse 3: ${a['final_address']['street3']}
\&Adresse 4: ${a['final_address']['street4']}
\&${a['final_address']['zip']} ${a['final_address']['city']}
\&Téléphone : ${a['final_address']['mobile']}^FS
% endif

^FO0,950^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
/* >5  => is subset C invocation code  */
% if len(d['pec_bar']) > 1:
^FO70,880^BCN,230,N,N,N^FD${d['pec_bar']}^FS
^FO230,1120^FDN° PCH:  ${d['cab_prise_en_charge']}^FS
^FO0,1125^XGE:POSTE,1,1^FS
^FO720,1120^XGE:CAMERA,1,1^FS
% endif

^XZ
