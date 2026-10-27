# Génère un mini-guide sur mesure (JSON + moteur) à partir d'une demande voyageur
import json,sys,os,shutil,re
D=json.load(open(sys.argv[1],encoding='utf-8'));OUT=sys.argv[2]
SRC='app'
C={
'Chiang Rai':('Temple blanc et nature du Nord',2,'nord',['culture','nature','hors'],19.91,99.83),
'Chiang Mai':('Culture, cuisine et montagnes',3,'nord',['culture','nature','street','aventure'],18.79,98.98),
'Sukhothai':("Ruines d'un ancien royaume",1,'nord',['culture','hors'],17.01,99.82),
'Isan':('La Thaïlande authentique',3,'centre',['culture','hors','street'],16.44,102.83),
'Ayutthaya':('Ancienne capitale et temples en briques',1,'centre',['culture','hors'],14.35,100.57),
'Bangkok':('Temples, street food et vertige urbain',3,'centre',['culture','street','fetes'],13.75,100.50),
'Hua Hin':('Plage paisible près de Bangkok',2,'golfe',['plages','spa','famille'],12.57,99.96),
'Pattaya':('Plages et animation à 2 h de Bangkok',2,'est',['plages','fetes'],12.93,100.88),
'Koh Samet':('Île proche aux plages claires',2,'est',['plages'],12.57,101.45),
'Koh Chang':('Jungle et plages tranquilles',3,'est',['plages','nature','famille'],12.05,102.34),
'Koh Kood':('Île sauvage et paisible',3,'est',['plages','hors','spa'],11.65,102.55),
'Khao Sok':('Jungle et lacs de calcaire',2,'andaman',['nature','aventure','hors'],8.92,98.53),
'Koh Tao':('Plongée et eaux turquoise',3,'golfe',['plages','aventure'],10.10,99.84),
'Koh Phangan':('Plages, yoga et fêtes',3,'golfe',['plages','fetes','spa'],9.74,100.03),
'Koh Samui':('Plages, resorts et détente',4,'golfe',['plages','spa','famille'],9.51,100.01),
'Krabi':('Falaises, lagons et îles',4,'andaman',['plages','aventure','nature'],8.09,98.91),
'Koh Phi Phi':('Îles de carte postale et lagons',2,'andaman',['plages','aventure','fetes'],7.74,98.78),
'Koh Lanta':('Île calme et plages sauvages',3,'andaman',['plages','hors','spa'],7.62,99.04),
'Phuket':('Plages, nuits animées et excursions',4,'andaman',['plages','fetes','famille'],7.88,98.39)}
ORDRE=list(C)
SLUG={'Isan':'khon-kaen'}
slug=lambda c:SLUG.get(c,c.lower().replace(' ','-'))
IMGC={'nord':'temple-jour','centre':'bangkok-coucher','golfe':'plage-palmier','est':'plage-coucher','andaman':'baie-bateaux'}
IMGV={'Bangkok':'bangkok-coucher','Chiang Mai':'temple-jour','Chiang Rai':'temple-jour','Sukhothai':'ruines-coucher','Krabi':'baie-bateaux','Phuket':'baie-panoramique','Koh Tao':'tortue-snorkeling','Khao Sok':'cascade'}
MOIS={'Janvier':'Saison sèche et agréable : idéal presque partout.','Février':'Saison sèche : très belle période.','Mars':'Il commence à faire très chaud, surtout dans le nord.','Avril':'Période la plus chaude, Songkran mi-avril.','Mai':'Chaud et humide, les pluies arrivent.','Juin':'Saison des pluies, le golfe reste souvent plus clément.','Juillet':'Saison des pluies, le golfe est souvent plus sûr que la côte Andaman.','Août':'Saison des pluies, belles promos et peu de monde.','Septembre':'Pluies marquées, nature luxuriante.','Octobre':'Fin des pluies, la saison sèche approche.','Novembre':'Début de la haute saison, Loy Krathong.','Décembre':'Haute saison : réserve tôt.'}
def alerte(m,cote):
    if cote=='andaman' and m in ('Mai','Juin','Juillet','Août','Septembre','Octobre'):return "Côte Andaman en saison des pluies : mer parfois agitée, certaines excursions suspendues."
    if cote=='golfe' and m in ('Octobre','Novembre','Décembre'):return "Golfe de Thaïlande : saison des pluies à cette période."
    return ''
TIER={'Routard':35,'Confort':70,'Premium':140}
VT={'Plages & îles':'plages','Culture & temples':'culture','Nature & jungle':'nature','Street food':'street','Fêtes & soirées':'fetes','Détente & spa':'spa','Aventure':'aventure','Hors sentiers battus':'hors','En couple':'couple','En famille':'famille','En solo':'solo'}
tags={VT[e] for e in D['envies'] if e in VT}
d=D['jours'];sel0=[c for c in ORDRE if c in D['destinations']];nordc=sorted([c for c in sel0 if C[c][4]>13.76],key=lambda c:C[c][4]);sel=(['Bangkok']+nordc+[c for c in sel0 if c!='Bangkok' and c not in nordc]) if 'Bangkok' in sel0 else sel0;n=D['voyageurs']
tot=sum(C[c][1] for c in sel);raw={c:C[c][1]*d/tot for c in sel};alloc={c:max(1,int(raw[c])) for c in sel}
while sum(alloc.values())<d:c=max(sel,key=lambda x:raw[x]-alloc[x]);alloc[c]+=1
while sum(alloc.values())>d:c=max(sel,key=lambda x:alloc[x]);alloc[c]-=1
fm=lambda x:f"{round(x/50)*50:,}".replace(',',' ')
V=json.load(open(SRC+'/data/vols.json'))
france=not D['depart'].lower().startswith('la réunion')
rk='fra-bkk' if france else 'run-bkk'
saison=next((s for s,ms in V['_routes'][rk]['mois'].items() if D['mois'] in ms),'moyenne')
vol=V[rk][saison];maj=V['_routes'][rk].get('maj') or V.get('_maj')
base=TIER[D['style']]*d*n
nom=D['name']
# ---- pages
P=[]
cov=IMGV.get(sel[0],IMGC[C[sel[0]][2]])
blocks=[]
blocks.append({"type":"card","n":1,"color":"#e91e8c","title":"Ton voyage en un coup d'œil","sub":f"{d} jours · {n} voyageur(s)","img":cov,"checks":[f"Départ : {D['depart']}, en {D['mois']}.",f"Style de voyage : {D['style']}.","Tes envies : "+", ".join(D['envies'])+".","Étapes : "+" → ".join(sel)+"."]+([f"Ta demande : « {D['note']} »"] if D.get('note') else [])})
al=[f"{c} : {alerte(D['mois'],C[c][2])}" for c in sel if alerte(D['mois'],C[c][2])]
blocks.append({"type":"card","n":2,"color":"#fb8c00","title":f"Ta période : {D['mois']}","sub":"ce qu'il faut savoir","img":"fete-lanternes" if D['mois'] in('Novembre',) else "plage-coucher","checks":[MOIS[D['mois']]]+al,"tip":"Pense à vérifier la météo juste avant le départ."})
blocks.append({"type":"card","n":3,"color":"#00a67e","title":"Budget indicatif","sub":"séjour sur place + vols","img":"hebergement-piscine","checks":[f"Sur place : environ {fm(base*0.85)} à {fm(base*1.2)} € pour {n} voyageur(s) ({TIER[D['style']]} €/jour/pers.), hors vols.",f"Vols aller-retour depuis {'la France' if france else 'La Réunion'} ({saison} saison) : direct {vol['direct']}, avec escale {vol['escale']} par personne.","Prix indicatifs, vérifiés"+(f" le {maj.split('-')[1]}/{maj.split('-')[0]}" if maj else " (édition 2026)")+"."],"tip":"Le bouton « Prix vols » en bas donne toutes les saisons."})
P.append({"id":"ton-voyage","title":f"Ton voyage sur mesure, {nom}","subtitle":"Préparé rien que pour toi","lead":f"{d} jours en Thaïlande","cover":cov,"blocks":blocks,"outro":"Le voyage i commence ici — bon départ !"})
def leg(a,b):
    ra,rb=C[a][2],C[b][2]
    s={ra,rb}
    if a=='Bangkok' and rb=='nord' or b=='Bangkok' and ra=='nord':return "Vol (environ 1 h 20) ou train de nuit (environ 12 h)"
    if s=={'centre','andaman'}:return "Vol (environ 1 h 30)"
    if s=={'nord','andaman'}:return "Vol, le plus souvent avec une correspondance à Bangkok (compter 3 à 4 h au total)"
    if s=={'centre','golfe'}:return "Vol (environ 1 h) puis ferry si besoin"
    if s=={'nord','golfe'}:return "Vol avec correspondance à Bangkok (compter 3 à 4 h au total), puis ferry si besoin"
    if s=={'centre','est'}:return "Minivan ou bus (environ 2 à 5 h selon la destination)"
    if ra==rb=='andaman':return "Minivan et/ou ferry : prévoir 2 à 3 h"
    if ra==rb=='golfe':return "Ferry ou bateau rapide : prévoir 1 à 3 h"
    if ra==rb=='nord':return "Bus ou minivan : prévoir 3 à 4 h"
    return "Vol intérieur ou minivan, selon la distance"
dep=D['depart'];last=sel[-1]
ov=[f"Arrivée à Bangkok : tous les vols internationaux atterrissent là (vol depuis {dep})."]
j=1
for c in sel:
    k=alloc[c];ov.append(f"Jours {j}"+(f" à {j+k-1}" if k>1 else "")+f" : {c} — {C[c][0]}.");j+=k
if 'Bangkok' not in sel0:ov.insert(1,"Prévois au moins une nuit à Bangkok à l'arrivée pour récupérer du vol.")
ov.append(f"Retour : de {last} vers Bangkok (ou directement vers l'aéroport international), puis vol vers {dep}.")
tr=[f"{sel[i]} → {sel[i+1]} : {leg(sel[i],sel[i+1])}." for i in range(len(sel)-1)]
if last!='Bangkok':tr.append(f"{last} → Bangkok (retour) : "+("route ou ferry jusqu'à l'aéroport de Krabi ou de Phuket, puis vol vers Bangkok (environ 1 h 30)." if C[last][2]=='andaman' else leg(last,'Bangkok')+"."))
note=[]
al=[f"{c} : {alerte(D['mois'],C[c][2])}" for c in sel if alerte(D['mois'],C[c][2])]
cb=[{"type":"card","n":1,"color":"#e91e8c","title":"Ton circuit en un coup d'œil","sub":f"{d} jours, de l'arrivée au retour","img":IMGC[C[sel[0]][2]],"checks":ov,"tip":"Ton guide suit cet ordre, étape par étape."},
 {"type":"card","n":2,"color":"#1e88e5","title":"Tes déplacements","sub":"d'une étape à l'autre","img":"tuktuk-bangkok","checks":tr,"tip":"Durées indicatives : confirme les horaires au moment de réserver."},
 {"type":"card","n":3,"color":"#fb8c00","title":"Le jour du retour","sub":"pour ne rien rater","img":"aeroport-avion-blanc","checks":[f"Arrive à l'aéroport international 3 h avant ton vol vers {dep}.","Si tu prends un vol intérieur la veille, garde une marge de sécurité.","Évite de réserver un vol intérieur le jour même du vol international.","Garde ton billet de sortie et ton passeport à portée de main."]}]
P.append({"id":"circuit","title":"Ton circuit","subtitle":"De l'arrivée au retour","lead":"Étapes, déplacements et jour du départ","cover":IMGC[C[sel[0]][2]],"blocks":cb,"outro":"Touche chaque étape dans le sommaire : à voir, où dormir, où manger, budget."})

# ---- pages d'étapes (contenu Premium)
import re
def short(t,n=150):
    t=(t or '').strip().replace('\n',' ')
    m=re.match(r'(.+?[.!?])(\s|$)',t)
    s=m.group(1) if m else t
    return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+'…'
STY={'Routard':{'Économique'},'Confort':{'Confort','Milieu de gamme','Boutique'},'Premium':{'Premium','Luxe','Haut de gamme'}}
BUD={'Routard':'Petit budget','Confort':'Budget moyen','Premium':'Budget élevé'}
PRIX={'Routard':{'€','€€'},'Confort':{'€€','€€€'},'Premium':{'€€€','€€€€'}}
COL=["#e91e8c","#1e88e5","#fb8c00","#00a67e","#8e24aa","#e53935","#5e35b1"]

from urllib.parse import quote,quote_plus
CJ="https://www.dpbolvw.net/click-101855269-12677526"
def lab(n):
    n=n.replace(' Sukhothai','').replace(' Resort','').replace(' Hotel','').replace(' Bangkok','')
    if len(n)<=20:return n
    c=n[:20];return c[:c.rfind(' ')] if ' ' in c else c
def hlinks(h):
    n=h.get('q') or h['name'];v=h.get('ville','Thaïlande');s=quote_plus(n+" "+v)
    if h.get('booking'):bk=CJ+"?url="+quote("https://www.booking.com/hotel/th/"+h['booking']+".html",safe='')
    else:bk=CJ+"?url="+quote("https://www.booking.com/searchresults.fr.html?ss="+s,safe='')
    return [("Booking",bk),
            ("Agoda",(f"https://www.agoda.com/fr-fr/{h['agoda']}/hotel/{h.get('agoda_ville','')}.html?cid=1972177" if h.get('agoda') else f"https://www.agoda.com/fr-fr/city/{h.get('agoda_ville','')}.html?cid=1972177")),
            ("Trip.com",(f"https://fr.trip.com/hotels/{h['tvil']}-hotel-detail-{h['trip'][0]}/{h['trip'][1]}/?Allianceid=9852508&SID=327644129&trip_sub3=D19106369&locale=fr-fr" if h.get('trip') else f"https://fr.trip.com/hotels/list?keyword={quote_plus(h.get('q') or h['name'])}&Allianceid=9852508&SID=327644129&trip_sub3=D19106369&locale=fr-fr"))]
def pg_etape(c,j,k):
    f=f'contenu/{slug(c)}.json'
    if not os.path.exists(f):return None
    X=json.load(open(f));img=IMGV.get(c,IMGC[C[c][2]]);B=[]
    HB=f'hotels/{slug(c)}.json'
    if os.path.exists(HB):
        HD=json.load(open(HB));X['hotels']=HD['hotels'];X['bandes']=HD.get('bandes',{});X['agoda_ville']=HD.get('agoda_ville','');X['trip_ville']=HD.get('trip_ville',{})
        X['_hotels_meta']=HD.get('_meta')
    st=D['style']
    def add(title,sub,im,checks,tip=None,links=None):
        if not checks:return
        b={"type":"card","n":len(B)+1,"color":COL[len(B)%7],"title":title,"sub":sub,"img":im,"checks":checks}
        if tip:b["tip"]=tip
        if links:b["links"]=links
        B.append(b)
    if X.get('districts'):
        add("Où te poser","les quartiers à connaître",img,[f"{d['name']} : {short(d.get('desc'))}" for d in X['districts'][:4]])
    S=X.get('sites',[])
    add("À ne pas manquer","les incontournables",img,[f"{s['name']} : {short(s.get('desc'))}"+(f" ({s['price']})" if s.get('price') else '') for s in S[:5]],("Astuce : "+short(S[0]['tip'],140)) if S and S[0].get('tip') else None)
    if X.get('beaches') and 'plages' in tags:
        add("Les plages","pour se baigner et se détendre","plage-palmier",[f"{b['name']} : {b.get('vibe') or short(b.get('desc'))}"+(" · idéale en famille" if 'famille' in tags and b.get('family','').startswith('Oui') else '') for b in X['beaches'][:4]])
    if X.get('excursions'):
        add("Excursions","à réserver sur place","bateau-gros-plan",[f"{e['name']} : {e.get('duration','')} · {e.get('price','')}".strip(' :·') for e in X['excursions'][:3]],("Saison : "+short(X['excursions'][0].get('season'),110)) if X['excursions'][0].get('season') else None)
    H=[h for h in X.get('hotels',[]) if h.get('tier') in STY[st]] or X.get('hotels',[])
    lk=[]
    for h in H[:2]:
        if h.get('q') or h.get('trip') or h.get('agoda') or h.get('booking'):
            h.setdefault('agoda_ville',X.get('agoda_ville',''));h.setdefault('tvil',X.get('trip_ville',{}).get('ville',''));h.setdefault('tid',X.get('trip_ville',{}).get('id',''))
            lk+=[{"t":f"🛏️ {lab(h['name'])} · {w}","u":u} for w,u in hlinks(h)]
        elif h.get('bookingUrl'):lk.append({"t":"🛏️ "+h['name'][:26],"u":h['bookingUrl']})
    add("Où dormir",f"selon ton style : {st}","hebergement-piscine",[f"{h['name']}"+(f" ({h.get('price') or X.get('bandes',{}).get(h.get('tier'),'')})" if (h.get('price') or X.get('bandes',{}).get(h.get('tier'))) else '')+(f" · {h['quartier']}" if h.get('quartier') else '')+f" : {short(h.get('desc'),110)}" for h in H[:3]],"Les prix sont des fourchettes indicatives. Les boutons Booking, Agoda et Trip.com affichent les offres et les tarifs du moment : compare-les avant de réserver.",lk)
    if B and B[-1]['title']=='Où dormir':B[-1]['agoda']={'cid':'1972177','ref':'1qLHTvK4/AiYf/W4zM1iJQ==','crt':'6120966568255','dest':c}
    R=X.get('restaurants',[]);pref=[r for r in R if r.get('price') in PRIX[st]] or R
    want=[]
    if 'street' in tags:want.append('street')
    if tags&{'fetes','couple'}:want.append('rooftop')
    if st=='Premium':want.append('gastro')
    pref.sort(key=lambda r:0 if r.get('cat') in want else 1)
    add("Où manger","bonnes adresses","marche-nuit",[f"{r['name']}"+(f" ({r['price']})" if r.get('price') else '')+f" : {r.get('spec') or short(r.get('desc'),90)}"+(f" · {r.get('zone') or r.get('station')}" if (r.get('zone') or r.get('station')) else '') for r in pref[:5]])
    add("Se déplacer","les bons réflexes","tuktuk-bangkok",[f"{t['title']} : {t.get('price','')}".strip(' :') for t in X.get('transport',[])[:4]],("Astuce : "+short(X['tips'][0],150)) if X.get('tips') else None)
    bu=[b for b in X.get('budget',[]) if b.get('tier')==BUD[st]]
    if bu:
        b=bu[0];det=[l.strip() for l in (b.get('detail') or '').split('\n') if l.strip()][:5]
        add("Budget sur place",f"{b['tier']} : {b['price']}","rooftop",[short(b.get('desc'),140)]+det)
    out="Profite bien de cette étape !"
    if X.get('_meta'):
        M=X['_meta'];add("Sources de cette page","page préparée à partir du web",img,["Cette page a été préparée à partir de sources web récentes (liste ci-dessous). Prix et horaires sont à confirmer sur place."],None,[{"t":s['t'][:34],"u":s['u']} for s in M['sources'][:4]])
        out="Page courte, à confirmer sur place avant de réserver."
    return {"id":"etape-"+slug(c),"title":f"{c}","subtitle":f"Jour {j}"+(f" à {j+k-1}" if k>1 else ""),"lead":C[c][0],"cover":img,"blocks":B,"outro":out}
etapes=[];j=1
for c in sel:
    k=alloc[c];p=pg_etape(c,j,k)
    if p:etapes.append(p)
    j+=k
P.extend(etapes)
P.append({"id":"meteo","title":"Météo de ton voyage","subtitle":"Prévisions en direct","lead":"Pour chaque étape","cover":"plage-coucher","blocks":[
 {"type":"meteo","n":1,"color":"#e91e8c","title":f"Météo {D['depart']}","sub":"avant de partir","img":"aeroport-avion-blanc","places":[{"nom":"Saint-Denis","lat":-20.88,"lon":55.45}] if not france else [{"nom":"Paris","lat":48.85,"lon":2.35},{"nom":"Lyon","lat":45.76,"lon":4.84},{"nom":"Marseille","lat":43.30,"lon":5.37}]},
 {"type":"meteo","n":2,"color":"#00a67e","title":"Météo de tes étapes","sub":"pendant le voyage","img":"baie-panoramique","places":[{"nom":c,"lat":C[c][4],"lon":C[c][5]} for c in sel]}],"outro":"Les prévisions couvrent 5 jours : reviens les consulter avant de partir."})
# pages communes
shared=[('comment-aller-france' if france else 'comment-aller-reunion'),'formalites','arrivee','conseils','numeros']
os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT):
    pth=os.path.join(OUT,f);shutil.rmtree(pth) if os.path.isdir(pth) else os.remove(pth)
for it in os.listdir(SRC):
    s=os.path.join(SRC,it)
    if it=='data':continue
    shutil.copytree(s,os.path.join(OUT,it)) if os.path.isdir(s) else shutil.copy(s,os.path.join(OUT,it))
os.makedirs(OUT+'/data/pages');shutil.copy(SRC+'/data/facts.json',OUT+'/data/facts.json')
for fn in ('menu.json',):shutil.copy(SRC+'/data/'+fn,OUT+'/data/'+fn)
# vols: route du voyageur en premier
rv={k:V['_routes'][k] for k in ([rk]+[x for x in V['_routes'] if x!=rk])};V['_routes']=rv
json.dump(V,open(OUT+'/data/vols.json','w'),ensure_ascii=False,indent=1)
pages={p['id']:p for p in P}
for sid in shared:pages[sid]=json.load(open(f'{SRC}/data/pages/{sid}.json'))
ca=shared[0]
order=['ton-voyage',ca,'formalites','arrivee','circuit']+[p['id'] for p in etapes]+['meteo','conseils','numeros']
idx=[];num=1
for pid in order:
    p=pages[pid];p['num']=num;json.dump(p,open(f"{OUT}/data/pages/{pid}.json",'w'),ensure_ascii=False,indent=1)
    idx.append({"id":pid,"num":num,"title":p['title'],"sub":p['subtitle'],"cover":p['cover']});num+=1
json.dump(idx,open(OUT+'/data/pages.json','w'),ensure_ascii=False,indent=1)
menu=[{"ico":"🏠","label":"Début","go":"ton-voyage"},{"ico":"📖","label":"Sommaire","sommaire":True},{"ico":"🌤️","label":"Météo","go":"meteo"},{"ico":"✈️","label":"Prix vols","vols":True}]
json.dump(menu,open(OUT+'/data/menu.json','w'),ensure_ascii=False,indent=1)
# images utiles uniquement
used=set()
for p in idx:
    pg=json.load(open(f"{OUT}/data/pages/{p['id']}.json"));used.add(pg['cover']);[used.add(b['img']) for b in pg['blocks'] if 'img' in b]
used|={'bateau-gros-plan','plage-coucher'}
from PIL import Image
for u in used:
    if not os.path.exists(f'{OUT}/img/{u}.jpg'):
        im=Image.open(f'bibliotheque/img/{u}.jpg').convert('RGB');im.thumbnail((720,1400));im.save(f'{OUT}/img/{u}.jpg',quality=76,optimize=True)
for f in os.listdir(OUT+'/img'):
    if f[:-4] not in used:os.remove(OUT+'/img/'+f)
files=['index.html','style.css','moteur.js','app.js','manifest.webmanifest','data/pages.json','data/facts.json','data/menu.json','data/vols.json','icons/i192.png','icons/i512.png']+['data/pages/'+f for f in sorted(os.listdir(OUT+'/data/pages'))]+['img/'+f for f in sorted(os.listdir(OUT+'/img'))]
sw=open(SRC+'/sw.js').read();rest=sw[sw.index("\nself.addEventListener('install'"):]
rest=rest.replace("k.filter(function(x){return x!==V})","k.filter(function(x){return x.indexOf('tm-sm-')===0&&x!==V})")
open(OUT+'/sw.js','w').write("var V='tm-sm-v1',F=%s;"%json.dumps(files)+rest)
m=json.load(open(OUT+'/manifest.webmanifest'));m['name']=f"Voyage sur mesure — {nom}";m['short_name']="Mon voyage";json.dump(m,open(OUT+'/manifest.webmanifest','w'),ensure_ascii=False)
h=open(OUT+'/index.html').read().replace("Thaï Malin · Guide test",f"Voyage sur mesure — {nom}");open(OUT+'/index.html','w').write(h)
print(alloc,rk,saison,vol)
