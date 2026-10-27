import json,os
from urllib.parse import quote,quote_plus
CJ="https://www.dpbolvw.net/click-101855269-12677526"
T='2026-10-27'
# ville: (nom, agoda_ville, trip_prefix, bandes, hotels)
# hotel: (tier, name, quartier, desc, booking, agoda, trip(id,slug)|None, [agoda_ville override])
V={}
V['chiang-mai']=('Chiang Mai','chiang-mai-th','chiang-mai',{'Économique':'≈ 400–900 THB/nuit','Confort':'≈ 1 000–2 500 THB/nuit','Premium':'≈ 3 000–7 000 THB/nuit','Luxe':'≈ 7 000–20 000 THB/nuit'},[
('Économique','BED Nimman','Nimman','Hôtel design pour adultes, quartier branché et café-friendly.','bed-nimman',None,('1337952','bed-nimman-hotel-adults-only')),
('Économique','Green Tiger House','Vieille ville','Petite maison d\'hôtes végétarienne, calme et accueillante.',None,'green-tiger-house_2',('2199385','green-tiger-vegetarian-house')),
('Confort','Burirattana Hotel','Vieille ville','Hôtel central à deux pas des remparts et du marché du dimanche.','burirattana-chiang-mai1',None,('94151725','burirattana-hotel')),
('Confort','Villa Klang Wiang','Vieille ville','Petit hôtel de charme avec jardin, dans la vieille ville.','villa-klang-wiang-chiang-mai','villa-klang-wiang',('24899774','villa-klang-wiang')),
('Premium','Ping Nakara Boutique Hotel & Spa','Rive de la Ping','Boutique-hôtel colonial raffiné avec spa.','ping-nakara-boutique-and-spa',None,('661352','ping-nakara-boutique-hotel-and-spa')),
('Luxe','137 Pillars House','Rive de la Ping','Ancienne maison de teck du 19e siècle, grand luxe discret.','one-three-seven-pillars-house','137-pillars-house',('997882','137-pillars-house')),
])
V['krabi']=('Krabi','krabi-th','krabi',{'Économique':'≈ 500–1 100 THB/nuit','Confort':'≈ 1 400–3 500 THB/nuit','Premium':'≈ 3 500–8 000 THB/nuit','Luxe':'≈ 8 000–30 000 THB/nuit'},[
('Économique','Pak-Up Hostel','Krabi Town','Auberge sociable et bien tenue, idéale pour rencontrer des voyageurs.','pak-up-hostel',None,('710497','pak-up-hostel')),
('Confort','Apasari Krabi','Ao Nang','Hôtel-boutique avec piscine, près de la plage.','amandari-krabi','apasari-krabi-hotel',('709770','apasari-krabi')),
('Confort','Sand Sea Resort','Railay','Bungalows tranquilles sur la plage de Railay West.','sand-sea-resort',None,('1516706','sand-sea-resort')),
('Confort','Aonang Cliff Beach Resort','Ao Nang','Resort en bord de falaise avec vue sur la baie.','aonang-cliff-beach-resort',None,('999071','aonang-cliff-beach-resort')),
('Premium','Railay Princess Resort & Spa','Railay','Resort entre deux plages, accessible en bateau.','railay-princess-resort-spa','railay-princess-resort-spa',('710552','railay-princess-resort-and-spa')),
('Premium','Centara Grand Beach Resort & Villas Krabi','Railay','Grand resort au pied des falaises de Railay.','grand-beach-resort-villas-krabi','centara-grand-beach-resort-villas-krabi_4',('709845','centara-grand-beach-resort-and-villas-krabi')),
('Luxe','Phulay Bay, a Ritz-Carlton Reserve','Nord d\'Ao Nang','Villas de luxe en bord de mer, expérience très privée.','phulay-bay-a-ritz-carlton-reserve',None,('979266','phulay-bay-a-ritz-carlton-reserve')),
])
V['phuket']=('Phuket','phuket-th','phuket',{'Économique':'≈ 600–1 400 THB/nuit','Confort':'≈ 1 800–4 000 THB/nuit','Premium':'≈ 4 000–9 000 THB/nuit','Luxe':'≈ 9 000–35 000 THB/nuit'},[
('Économique','The Expat Hotel','Patong','Hôtel simple et central, pratique pour sortir.',None,'expat-hotel',('702379','the-expat-hotel')),
('Économique','TRIBE Phuket Patong','Patong','Hôtel moderne et abordable, à deux pas de la plage.','tribe-phuket-patong','tribe-phuket-patong',('11604407','tribe-phuket-patong-by-accor')),
('Confort','Kalima Resort & Spa','Patong','Resort avec piscine sur les hauteurs de Patong.',None,'kalima-resort-spa',('702789','kalima-resort-and-spa-phuket')),
('Confort','Phuket Orchid Resort & Spa','Karon','Resort de bord de mer à Karon, bon rapport qualité-prix.','phuket-orchid-resort','phuket-orchid-resort',('998454','phuket-orchid-resort-and-spa')),
('Premium','Amari Phuket','Patong','Resort face à la baie de Patong, piscines et vue mer.',None,None,('756638','amari-phuket')),
('Premium','Holiday Inn Resort Phuket','Patong','Grand resort familial en bord de plage.','holiday-inn-resort-phuket',None,('1524907','holiday-inn-resort-phuket-by-ihg')),
('Luxe','Paresa Resort Phuket','Kamala','Resort perché sur une falaise, vue sur la mer d\'Andaman.','paresa','paresa-resort-phuket',('998312','paresa-resort-phuket')),
('Luxe','Keemala','Kamala','Villas originales dans la jungle, esprit « nid » et nature.',None,'keemala',('2620829','keemala')),
('Luxe','Rosewood Phuket','Emerald Bay','Resort ultra-luxe en baie privée.',None,None,('10521003','rosewood-phuket')),
])
V['koh-lanta']=('Koh Lanta','koh-lanta-th','ko-lanta',{'Économique':'≈ 500–1 200 THB/nuit','Confort':'≈ 1 500–3 500 THB/nuit','Premium':'≈ 4 000–10 000 THB/nuit','Luxe':'≈ 9 000–25 000 THB/nuit'},[
('Économique','Lanta Long Beach Hostel','Long Beach','Auberge simple et sociable à deux pas de la plage.','lanta-long-beach-hostel',None,('4548451','lanta-long-beach-hostel')),
('Confort','Lanta Sand Resort & Spa','Long Beach','Resort de plage avec piscine, ambiance détendue.','lanta-sand-resort-spa','lanta-sand-resort-spa',('1512657','lanta-sand-resort-and-spa-krabi')),
('Confort','Avani+ Koh Lanta Krabi Resort','Klong Dao','Resort de plage avec piscine et activités (anciennement Crown Lanta).','crown-lanta-resort-spa',None,None),
('Premium','Layana Resort & Spa','Long Beach','Resort pour adultes, spa et piscine en bord de mer.','layana-resort-spa','layana-resort-spa-adults-only',('710082','layana-resort-and-spa-adults-only')),
('Luxe','Pimalai Resort & Spa','Ba Kan Tiang','Grand resort sur une plage presque privée, côté sud.','pimalai-resort-and-spa',None,('996822','pimalai-resort-and-spa')),
])
V['koh-phi-phi']=('Koh Phi Phi','koh-phi-phi-th','phi-phi-islands',{'Économique':'≈ 500–1 200 THB/nuit','Confort':'≈ 2 000–4 500 THB/nuit','Premium':'≈ 4 500–10 000 THB/nuit','Luxe':'≈ 10 000–30 000 THB/nuit'},[
('Économique','Slumber Party Phi Phi','Tonsai','Auberge festive au cœur du village de Tonsai.',None,None,('129726368','slumber-party-phi-phi')),
('Confort','Phi Phi Cliff Beach Resort','Laem Hin','Bungalows sur la falaise, un peu à l\'écart de l\'agitation.','phi-phi-cliff-beach-resort',None,('2621511','phi-phi-cliff-beach-resort')),
('Confort','P.P. Erawan Palms Resort','Laem Tong','Resort calme au nord de l\'île, loin du bruit.','p-p-erawan-palms-resort','p-p-erawan-palms-resort',('999161','pp-erawan-palms-resort')),
('Premium','Phi Phi Holiday Resort','Laem Tong','Resort de plage au nord, tranquille et confortable.','holiday-inn-resort-phi-phi-island','holiday-inn-resort-phi-phi-island',('1273850','holiday-inn-resort-phi-phi-island')),
('Premium','SAii Phi Phi Island Village','Laem Tong','Grand resort de plage, bateau privé depuis Tonsai.','phiphiislandvillagebeachresortandspa','phi-phi-island-village-beach-resort',('998346','phi-phi-island-village-beach-resort')),
('Luxe','Zeavola Resort','Laem Tong','Resort de charme face à la mer, villas pieds dans le sable.',None,'zeavola-hotel',('991385','zeavola-resort')),
])
V['koh-samui']=('Koh Samui','koh-samui-th','koh-samui',{'Économique':'≈ 600–1 500 THB/nuit','Confort':'≈ 2 000–4 500 THB/nuit','Premium':'≈ 4 500–10 000 THB/nuit','Luxe':'≈ 10 000–40 000 THB/nuit'},[
('Économique','Lub d Koh Samui Chaweng Beach','Chaweng','Auberge-hôtel animée face à la plage de Chaweng.','lub-d-koh-samui-chaweng-beach','lub-d-koh-samui-chaweng-beach_2',('24168984','lub-d-koh-samui-chaweng-beach-beachfront-vibrant-social-vibe')),
('Économique','Crystal Lamai Hotel','Lamai','Petit hôtel simple à Lamai, près de la plage.','crystal-lamai','crystal-lamai-hotel',('5031984','crystal-lamai-hotel')),
('Confort','Casa de Mar','Chaweng','Hôtel de plage convivial à Chaweng.',None,None,('2381142','casa-de-mar-koh-samui')),
('Confort','Chaweng Regent Beach Resort','Chaweng','Resort de bord de plage, piscine et restaurant.','chaweng-regent-beach-resort','chaweng-regent-beach-resort',('998606','chaweng-regent-beach-resort-koh-samui')),
('Premium','Sheraton Samui Resort','Chaweng Noi','Grand resort sur une baie à l\'écart de Chaweng.','sheraton-ko-samui-resort',None,('1816638','sheraton-samui-resort')),
('Luxe','Santiburi Koh Samui','Mae Nam','Resort de luxe sur une plage tranquille du nord.','santiburi-beach-resort-golf-and-spa',None,('998605','santiburi-koh-samui')),
('Luxe','Nora Buri Resort & Spa','Chaweng','Resort de luxe au cœur de Chaweng, avec spa.',None,'nora-buri-resort-spa',('998627','nora-buri-resort-and-spa')),
])
V['pattaya']=('Pattaya','pattaya-th','pattaya',{'Économique':'≈ 400–1 000 THB/nuit','Confort':'≈ 1 200–3 000 THB/nuit','Premium':'≈ 3 000–7 000 THB/nuit','Luxe':'≈ 6 000–15 000 THB/nuit'},[
('Économique','Pattaya Backpackers Hostel','Centre','Auberge pour adultes, simple et bien située.',None,None,('23782821','pattaya-backpackers-hostel-adults-only')),
('Confort','Mercure Pattaya Ocean Resort','Pattaya Centre','Hôtel de plage avec piscine, bon confort.','mercure-pattaya-ocean-resort','mercure-pattaya-ocean-resort',('1379449','mercure-pattaya-ocean-resort')),
('Premium','Siam@Siam Design Hotel Pattaya','Pattaya Centre','Hôtel design avec piscine sur le toit.','siam-siam-design-pattaya','siam-siam-design-hotel-pattaya',('1195018','siamsiam-design-hotel-pattaya')),
('Premium','Hilton Pattaya','Pattaya Centre','Hôtel haut de gamme dans le centre commercial Central Marina.','hilton-pattaya','hilton-pattaya_7',('928353','hilton-pattaya')),
('Luxe','Royal Cliff Beach Hotel Pattaya','Pattaya Sud','Grand resort sur falaise, plusieurs piscines et plage privée.','royal-cliff-beach-resort',None,('1517944','royal-cliff-beach-hotel')),
])
V['hua-hin']=('Hua Hin','hua-hin-cha-am-th','hua-hin',{'Économique':'≈ 500–1 200 THB/nuit','Confort':'≈ 1 500–3 500 THB/nuit','Premium':'≈ 3 500–8 000 THB/nuit','Luxe':'≈ 7 000–20 000 THB/nuit'},[
('Confort','City Beach Resort','Centre','Resort proche de la plage et du marché de nuit.','city-beach-resort',None,('709420','city-beach-resort')),
('Premium','Hyatt Regency Hua Hin','Plage','Resort de plage élégant avec piscines.','hyatt-regency-hua-hin',None,('709480','hyatt-regency-hua-hin')),
('Premium','Hua Hin Marriott Resort & Spa','Plage','Resort de plage avec spa et plusieurs piscines.','hua-hin-marriott-resort-and-spa',None,('4125209','hua-hin-marriott-resort-and-spa')),
('Luxe','Centara Grand Beach Resort & Villas Hua Hin','Plage','Institution historique de Hua Hin, jardins en front de mer.','sofitelcentralhuahinresort','centara-grand-beach-resort-villas-hua-hin',('709400','centara-grand-beach-resort-and-villas-hua-hin')),
('Luxe','Anantara Hua Hin Resort','Plage','Resort de luxe en bord de mer, esprit thaï.','anantara-resort-hua-hin','anantara-hua-hin-resort',('996833','anantara-hua-hin-resort')),
])
V['ayutthaya']=('Ayutthaya','ayutthaya-th','phra-nakhon-si-ayutthaya',{'Économique':'≈ 400–900 THB/nuit','Confort':'≈ 900–2 000 THB/nuit','Premium':'≈ 2 500–6 000 THB/nuit','Luxe':'≈ 2 500–6 000 THB/nuit'},[
('Économique','Baan Lotus Guest House','Centre historique','Maison d\'hôtes familiale proche des temples.','baan-lotus-guest-house',None,None),
('Confort','Classic Kameo Hotel & Serviced Apartments','Centre','Hôtel confortable avec piscine, près du centre.','classic-kameo-amp-serviced-apartments-ayutthaya','classic-kameo-hotel-ayutthaya',('1623137','classic-kameo-hotel-and-serviced-apartments-ayutthaya')),
('Premium','Sala Ayutthaya','Bord du fleuve','Hôtel design face au temple Wat Ratchaburana, sur le fleuve.','sala-ayutthaya',None,('2192480','sala-ayutthaya')),
])
V['chiang-rai']=('Chiang Rai','chiang-rai-th','chiang-rai',{'Économique':'≈ 400–900 THB/nuit','Confort':'≈ 1 000–2 200 THB/nuit','Premium':'≈ 2 500–6 000 THB/nuit','Luxe':'≈ 5 000–12 000 THB/nuit'},[
('Économique','Baan Bua Guest House','Centre','Maison d\'hôtes simple et accueillante.','baan-bua-guest-house',None,('712422','baan-bua-guest-house')),
('Confort','Wiang Inn Hotel','Centre-ville','Hôtel central, pratique pour le marché de nuit.','wiang-inn',None,('712859','wiang-inn-hotel')),
('Premium','The Legend Chiang Rai Boutique River Resort & Spa','Rivière Kok','Resort de charme au bord de la rivière, style lanna.','the-legend-chiang-rai-boutique-river-resort-spa','the-legend-chiang-rai-hotel',('712838','the-legend-chiang-rai-boutique-river-resort-and-spa')),
('Premium','Le Méridien Chiang Rai Resort','Rivière Kok','Grand resort calme au bord de la rivière.','le-meridien-chiang-rai-resort',None,('1005264','le-meridien-chiang-rai-resort-thailand')),
])
V['khon-kaen']=('Khon Kaen','khon-kaen-th','khon-kaen',{'Économique':'≈ 400–900 THB/nuit','Confort':'≈ 1 000–2 000 THB/nuit','Premium':'≈ 2 000–4 500 THB/nuit','Luxe':'≈ 2 000–4 500 THB/nuit'},[
('Confort','Kosa Hotel & Wellness Center','Centre','Hôtel de centre-ville avec spa et centre commercial.','kosa',None,('711201','kosa-hotel-and-shopping-mall')),
('Premium','Charoen Thani Hotel Khon Kaen','Centre','Grand hôtel installé du centre-ville.','charoenthani-khon-kaen','charoenthanikhonkaen-hotel',('2486902','charoen-thani-hotel-khon-kaen')),
('Premium','Pullman Khon Kaen Raja Orchid','Centre','Hôtel haut de gamme avec piscine et rooftop.','sofitelrajaorchid',None,('2113194','pullman-khon-kaen-raja-orchid')),
])
V['koh-chang']=('Koh Chang','koh-chang-th','koh-chang',{'Économique':'≈ 500–1 200 THB/nuit','Confort':'≈ 1 500–3 000 THB/nuit','Premium':'≈ 3 000–7 000 THB/nuit','Luxe':'≈ 3 000–7 000 THB/nuit'},[
('Économique','Kaibae Hut Resort','Kai Bai','Bungalows simples au bord de la plage de Kai Bai.','kaibae-hut-resort',None,('709633','kai-bae-hut-resort')),
('Confort','Siam Beach Resort','Klong Prao','Bungalows en bord de plage, ambiance détendue.','siam-beach-resort',None,('709192','siam-beach-resort')),
('Premium','Centara Koh Chang Tropicana Resort','Klong Prao','Resort de plage avec piscine et grandes chambres.','koh-chang-tropicana-resort-spa','centara-koh-chang-tropicana-resort',('709691','centara-koh-chang-tropicana-resort')),
])
V['koh-phangan']=('Koh Phangan','koh-phangan-th','koh-phangan',{'Économique':'≈ 500–1 200 THB/nuit','Confort':'≈ 1 500–3 500 THB/nuit','Premium':'≈ 3 500–8 000 THB/nuit','Luxe':'≈ 8 000–25 000 THB/nuit'},[
('Confort','Sunrise Resort Koh Phangan','Haad Rin','Bungalows sur la plage de Haad Rin (Sunrise).','sunrise-resort-koh-phangan',None,('2504181','sunrise-resort-koh-phangan')),
('Premium','Panviman Resort Koh Phangan','Thong Nai Pan Noi','Resort perché sur une baie, vue mer superbe.','panviman-koh-phangan',None,('712119','panviman-koh-phangan')),
('Premium','Buri Rasa Village Phangan','Thong Nai Pan Noi','Village de bungalows face à la plage.','buri-rasa-koh-phangan',None,('712050','buri-rasa-koh-phangan')),
('Luxe','Anantara Rasananda Koh Phangan Villas','Thong Nai Pan Noi','Villas de luxe avec piscine privée.','rasananda','anantara-rasananda-koh-phangan-villas',('711145','anantara-rasananda-koh-phangan-villas')),
])
V['koh-tao']=('Koh Tao','koh-tao-th','koh-tao',{'Économique':'≈ 600–1 400 THB/nuit','Confort':'≈ 1 500–3 500 THB/nuit','Premium':'≈ 3 500–8 000 THB/nuit','Luxe':'≈ 8 000–20 000 THB/nuit'},[
('Confort','Ban\'s Diving Resort','Sairee','Resort de plongée, bungalows face à la plage de Sairee.','ban-s-diving-resort','ban-s-diving-resort',('709169','ban-s-diving-resort')),
('Confort','Charm Churee Villa','Chalok Baan Kao','Villas sur la colline, vue sur la baie de Chalok.','charm-churee-village',None,('709178','charm-churee-villa')),
('Premium','Haadtien Beach Resort','Haad Tien','Resort tranquille sur une plage isolée.','haadtien-beach-resort',None,('709185','haadtien-beach-resort')),
('Premium','Jamahkiri Dive Resort & Spa','Haad Tien','Resort de charme avec spa, vue sur la baie.','jamahkiri-resort-spa-koh-tao',None,('709189','jamahkiri-resort')),
])
def links(h,av,tp):
    n=h['name'];s=quote_plus(n+" "+h['ville'])
    bk=CJ+"?url="+quote("https://www.booking.com/hotel/th/"+h['booking']+".html" if h.get('booking') else "https://www.booking.com/searchresults.fr.html?ss="+s,safe='')
    ag=f"https://www.agoda.com/fr-fr/{h['agoda']}/hotel/{av}.html?cid=1972177" if h.get('agoda') else f"https://www.agoda.com/fr-fr/city/{av}.html?cid=1972177"
    tr=f"https://fr.trip.com/hotels/{tp}-hotel-detail-{h['trip'][0]}/{h['trip'][1]}/?Allianceid=9852508&SID=327644129&trip_sub3=D19106369&locale=fr-fr" if h.get('trip') else f"https://fr.trip.com/hotels/list?keyword={quote_plus(n)}&Allianceid=9852508&SID=327644129&trip_sub3=D19106369&locale=fr-fr"
    return bk,ag,tr
doutes=[]
for slug,(ville,av,tp,bandes,hs) in V.items():
    out=[];ex=[]
    for t in hs:
        tier,name,q,desc,bk,ag,tr=t
        h={"tier":tier,"style":"","name":name,"ville":ville,"quartier":q,"desc":desc,"price":""}
        if ag:h["agoda"]=ag
        if tr:h["trip"]=list(tr)
        if bk:h["booking"]=bk
        h["statut"]="brouillon-ia";h["verifie"]=T
        out.append(h)
        b,a,r=links(h,av,tp)
        ex.append({"tier":tier,"name":name,"desc":desc,"price":bandes.get(tier,""),"bookingUrl":b,"agodaUrl":a,"tripUrl":r})
        m=[p for p,v in (("Booking",bk),("Agoda",ag),("Trip",tr)) if not v]
        if m:doutes.append(f"{ville} – {name} : lien direct manquant sur {', '.join(m)} (recherche/ville à la place)")
    json.dump({"ville":ville,"agoda_ville":av,"trip_ville":{"ville":tp,"id":""},"bandes":bandes,
      "_meta":{"statut":"brouillon-ia","date":T,"sources":[{"t":"Pages hôtels Booking, Agoda et Trip.com (liens vérifiés par recherche)","u":""},{"t":"Sélection Premium Thaï Malin (base de Pascal)","u":"(base de Pascal)"}]},
      "hotels":out},open(f'hotels/{slug}.json','w'),ensure_ascii=False,indent=1)
    json.dump({"hotels":ex},open(f'export-premium/extras-{slug}-hotels.json','w'),ensure_ascii=False,indent=1)
open('DOUTES-hotels.txt','w').write("\n".join(doutes))
print(len(V),'villes',sum(len(v[4]) for v in V.values()),'hôtels',len(doutes),'doutes')
