## -*- coding: utf-8 -*-
/* Utf8 file encoded converted in CP1252 by python */
/* PARAMETERS VARIABLES : Search VARY in comments */
^XA
^LH30,30          /* initial position*/
^CI27       /* windows CP1252 decoding */
^CF0,22    /*CF:default font|font_type,size*/
/*Fonts : P,Q,R,S,T fonts are the same with Zebra GX420t, only size change font '0' seems to be functionnal for general purpose */
^FWN    /*FW:Default orientation*/
^BY3    /*BY:Bar Code Field Default*/

^FO80,01^XGE:${logo},1,1^FS

^FO0,100^GB770,1,4^FS

^FO10,130^A0,30^FDEXPEDITEUR
% if _product_code[1:] == 'Y':
/ SENDER
% endif
^FS
% if _product_code in ['9L', '9V', '7Q', '8R', 'CY', 'EY']:
^FO450,130^FDRef Client: ${d['ref_client']}^FS
% endif
^FO0,160^GB360,160,4^FS     /*GB:graphic box|width,height,thickness*/
/*graphic diagonal line:width,height,border_thickness,,orientation(R=right diagonal)*/
^FO0,160^GD350,160,10,,R^FS
^FO0,160^GD350,160,10,,L^FS
^FO410,160^GB360,160,4^FS
/*^A0 /*A:font|font_type,orientation,size*/*/
^FO25,175^A0,30,30^FD${s['name']}^FS
^FO25,205   /*FO:field origin|x,y*/
^FB400,5,3,  /*FB:field block|width text,line number,space beetween lines*/
/* COLISS RULE Teleph expediteur si OM ou I */
/* COLISS RULE Pays expediteur si OM ou I */
^A0,24^FD${s['street']}
\&
% if _product_code in ['EY', 'CY', '7Q']:
TEL: ${s['phone']}
% endif
\&${s['zip']} ${s['city']}
% if _product_code in ['EY', 'CY', '7Q']:
\&${s['country']}
% endif
^FS

^FO420,170   /*FO:field origin|x,y*/
^FB400,6,3,
^FDCOMPTE CLIENT: ${s['account']}
\&SITE DE PRISE EN CHARGE:
\&${s['support_city']}
\&N° Colis : ${d['cab_suivi']}
\&Poids   : ${d['weight']} Kg
\&Edité le : ${d['date']}
^FS

% if _product_code[1:] == 'Y':
^FO30,330^FDAttention : le colis peut etre ouvert d'office^FS
% endif

/* ||| || |||| */
/* >5  => is subset C invocation code ; >6  => is subset B invocation code */
^FO40,345^PR2,2^BCN,230,Y,N,N^FD${d['suivi_bar']}^FS
^FO40,575^GB
% if _product_code[1:] == 'Y':
468
% else:
402
% endif
,3,4^FS

^FO0,585^FDN° de colis :^FS

% if _product_code == 'EY':
^FO470,600^FDEn cas de non livraison,^FS
/* VARY : you may switch to this mention "renvoyer à l'expéditeur en prioritaire." */
^FO470,630^FDtraiter le colis abandonné,^FS
% endif

/* /!\ /_\ /!\ /_\ /!\ */
% if o['nm']:
^FO570,350^XGE:NM,1,1^FS
% endif
% if o['ar'] and _product_code in ['7Q', 'CY']:
^FO570,450^XGE:AR,1,1^FS
% endif
% if o['ftd'] and _product_code == '7Q':
^FO570,550^XGE:FTD,1,1^FS
% endif
% if 1 == False:
/*TODO : Change this condition*/
^FO680,350^XGE:CRBT,1,1^FS
% endif
% if _product_code == 'EY':
^FO570,700^XGE:KPGEMS,1,1^FS
% endif

^FO30,630^A0,30^FDDESTINATAIRE
% if _product_code[1:] == 'Y':
 / ADDRESSEE
% endif
^FS

^FO5,660^GB450,200,4^FS
^FO30,675^A0,24,28^FD${a['name']}^FS
^FO30,705^FB400,6,2,
^FD${a['street']}
\&${a['street2']}
\&${a['street3']}^FS
^FO30,755
% if _product_code[1:] != 'Y':
^A0,40
% endif
^FD${a['zip']} ${a['city']}^FS

/* COLISS RULE Phone+country expediteur si Internationale */
% if _product_code[1:] == 'Y':
/* only for Y ?*/
^FO30,780^FDTEL: ${a['phone']}^FS
% endif
% if _product_code[1:] == 'Y':
^A0,40^FO30,810^FD${a['name']} - ${a['countryCode']}^FS
% endif
^FO0,950^A0B^FDSPECIFIQUE^FS

/* ||| || |||| */
^FO70,880^BCN,230,Y,N,N^FD${d['pec_bar']}^FS
^FO100,1120^FDN° PCH:^FS
^FO0,1136^XGE:POSTE,1,1^FS
^FO720,1130^XGE:CAMERA,1,1^FS
^XZ
