## -*- coding: utf-8 -*-
/* Utf8 file encoded converted in CP1252 by python */
/* PARAMETERS VARIABLES : Search VARY in comments */
^XA
^LH30,30        /* initial position*/
^CI27           /* windows CP1252 decoding */
^CF0,22         /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN            /*FW:Default orientation*/
^BY3            /*BY:Bar Code Field Default*/

^FO10,01^XGE:${signature},1,1^FS
^FO680,01^XGE:${logo},1,1^FS

% if _product_code != '':
^FO0,90^GB770,1,4^FS   /*ligne sous image du haut */
^FO470,110^A0,30^FDEXPEDITEUR^FS
^FO5,110^FDRef Client: ${d['custom_shipping_ref']}^FS
/*GB:graphic box|width,height,thickness*/
^FO460,145^GB310,160,4^FS     /*bloc expediteur*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO460,145^GD300,160,10,,R^FS
^FO460,145^GD300,160,10,,L^FS
/*^A0 /*A:font|font_type,orientation,size*/*/
^FO480,175^A0,30,30^FD${s['name']}^FS
^FO480,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
^A0,24^FD${s['street']}
\&${s['street2']}
\&${s['zip']} ${s['city']}^FS

^FO460,310^GB310,160,4^FS   /*bloc compte client*/
^FO470,320   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: ${s['account']}
\&SITE DE PRISE EN CHARGE:
\&${s['center_support_city']} PFC
\&N° Colis : ${d['suivi_barcode']}
\&Poids   : ${d['weight']} kg
\&Edité le : ${d['date']}
^FS

/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
% if len(d['suivi_barcode']) > 1 :
^FO25,140^PR2,2^BCN,230,N,N,N^FD${d['suivi_barcode'][:4].replace(' ','') + '>5'}${d['suivi_barcode'][4:].replace(' ','')}^FS
^FO25,370^GB402,3,4^FS  /*ligne sous code barre*/
% endif
^FO70,380^FDN° de colis : ${d['suivi_barcode']}^FS

/* /!\ /_\ /!\ /_\ /!\ */
% if o['nm']:
^FO580,505^XGE:NM,1,1^FS
% endif

^FO30,410^A0,30^FDDESTINATAIRE^FS

^FO5,440^GB450,200,4^FS
^FO25,450^A0,26,26^FD${ds['name']}^FS
^FO25,475^FB400,6,2,
^FD${a['name']}
\&${ds['street']}
\&${ds['street2']}
\&${ds['zip']} ${ds['city']}^FS
^FO25,575^A0,36,46^FD91500^FS
^FO155,585^A0,28,38^FDHUB RELAIS^FS
^FO25,610^A0,18^FDTel : ${a['mobile']}^FS

^FO0,715^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
/* >5  => is subset C invocation code  */
% if len(d['prise_en_charge_barcode']) > 1 :
^FO70,650^BCN,230,N,N,N^FD${d['prise_en_charge_barcode'][:9].replace(' ','') + '>5' + d['prise_en_charge_barcode'][9:].replace(' ','') or ''}^FS
^FO180,890^FDN° PCH:  ${d['prise_en_charge_barcode']}^FS
^FO0,890^XGE:POSTE,1,1^FS
^FO720,885^XGE:CAMERA,1,1^FS
%endif
% if len(routage_barcode) >1 :
^FO70,933^A0,60,80^FD${d['lot_routing']}^FS
% if len(d['lot_routing'])>3:
^FO265,948^A0,40,60^FDSA13 REL^FS
^FO520,940^A0,50,70^FD${d['distri_sort']}^FS
%else:
^FO220,948^A0,40,60^FDSA13 REL^FS
^FO480,940^A0,50,70^FD${d['distri_sort']}^FS
%endif
^FO35,978^BCN,170,N,N,N^FD>:%>5${routage_barcode_full[1:9]}>6M>5${routage_barcode_full[10:28]}^FS
^FO230,1150^FD${routage_barcode.replace('%','')}^FS
%endif
^FO35,978^GB695,1,4^FS
% else:
^FO30,630^A0,30^FDThere is non product code : no display is possible^FS
% endif
^XZ
