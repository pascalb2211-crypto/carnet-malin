/* Moteur Thaï Malin : lit une page JSON + les faits partagés et dessine la page */
(function(){
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function fact(F,s){ if(typeof s!=='string'||s.indexOf('$')<0)return s;
  return s.replace(/\$([a-z0-9_.\-]+)/gi,function(_,p){var v=F;p.split('.').forEach(function(k){v=v&&v[k]});return v==null?'—':v})}
function head(b){var h=el('div','hd');h.style.setProperty('--c',b.color);
  h.appendChild(el('span','n',String(b.n)));var t=el('div','ht');t.appendChild(el('b','',b.title));t.appendChild(el('span','',b.sub));h.appendChild(t);return h}
function closeAll(){document.querySelectorAll('.card.open').forEach(function(c){c.classList.remove('open')});document.body.classList.remove('lock')}
window.TMclose=closeAll;
function wire(c){var x=el('button','xb','✕ Fermer');x.type='button';c.insertBefore(x,c.firstChild);c.querySelector('.hd').appendChild(el('span','more','Voir ›'));
  c.addEventListener('click',function(e){if(c.classList.contains('open')){if(e.target===x){history.back();e.stopPropagation()}return}
    closeAll();c.classList.add('open');document.body.classList.add('lock');c.scrollTop=0;try{history.pushState({o:1},'')}catch(_){}})}
window.TMrender=function(root,P,F){
  var pg=el('main','pg');var ban=el('div','ban');if(P.cover)ban.style.backgroundImage='url(img/'+P.cover+'.jpg)';pg.appendChild(ban);
  var top=el('header','top');top.appendChild(el('span','num',String(P.num)));
  var tt=el('div','tt');tt.appendChild(el('h1','',P.title));tt.appendChild(el('p','sb',P.subtitle));tt.appendChild(el('p','ld',P.lead));
  top.appendChild(tt);pg.appendChild(top);
  var grid=el('div','grid');
  P.blocks.forEach(function(b){b.sub=fact(F,b.sub);b.title=fact(F,b.title);
    var c=el('section','card');
    if(b.img){var ph=el('div','ph');ph.style.backgroundImage='url(img/'+b.img+'.jpg)';c.appendChild(ph);c.classList.add('hasimg')}
    c.appendChild(head(b));
    if(b.type==='card'){
      var ul=el('ul','ck');b.checks.forEach(function(x){ul.appendChild(el('li','',fact(F,x)))});c.appendChild(ul);
      if(b.links){var lk=el('div','lk');b.links.forEach(function(l){var a=el('a','',l.t);a.href=l.u;if(!/^tel:/.test(l.u)){a.target='_blank';a.rel='noopener'}lk.appendChild(a)});c.appendChild(lk)}
      var aw=null;if(b.agoda){aw=el('div','agw');var ab=el('button','agb','🔎 Chercher d\'autres hôtels à '+(b.agoda.dest||'')+' · Agoda');var ac=el('div','agc');aw.appendChild(ab);aw.appendChild(ac);
        ab.addEventListener('click',function(ev){ev.stopPropagation();if(ab.dataset.ok)return;ab.dataset.ok='1';ab.textContent='Chargement…';
          var id='adg'+Math.floor(Math.random()*1e9),d=document.createElement('div');d.id=id;ac.appendChild(d);
          var s=document.createElement('script');s.src='https://cdn0.agoda.net/images/sherpa/js/sherpa_init1_08.min.js';
          s.onload=function(){try{var g={};g.crt=b.agoda.crt||'';g.version='1.04';g.id=g.name=id;g.width='320px';g.height='420px';g.ReferenceKey=b.agoda.ref;g.Layout='SquareCalendar';g.Language='fr-fr';g.Cid=b.agoda.cid;g.DestinationName=b.agoda.dest||'';g.OverideConf=false;new AgdSherpa(g).initialize();ab.style.display='none';var hn=el('p','agh','Tape « '+(b.agoda.dest||'')+' » dans la recherche, puis choisis tes dates.');ac.parentNode.insertBefore(hn,ac)}catch(e){ab.textContent='Moteur indisponible';ac.textContent='Ouvre la liste Agoda : '+(b.agoda.url||'')}};
          s.onerror=function(){ab.dataset.ok='';ab.textContent='Connexion requise pour chercher';};
          document.head.appendChild(s)})}
      if(b.tip)c.appendChild(el('p','tip',b.tip));
      if(aw)c.appendChild(aw);
    }
    if(b.type==='routes'){
      var r=el('div','rt');b.items.forEach(function(i){var row=el('div','ro');
        row.appendChild(el('b','via',i.via));row.appendChild(el('span','ar','→'));row.appendChild(el('span','cie',i.cie));row.appendChild(el('em','',i.note));r.appendChild(row)});c.appendChild(r)}

    if(b.type==='bars'){
      var bw=el('div','bars');
      b.items.forEach(function(i){
        var r=el('div','br'+(i.direct?' dr':''));
        var top=el('div','bt');top.appendChild(el('b','',i.lbl));top.appendChild(el('span','tg',i.tag));r.appendChild(top);
        var tr=el('div','trk');var f=el('i','fl');
        f.style.left=(i.min/b.max*100)+'%';f.style.width=Math.max((i.max-i.min)/b.max*100,2.5)+'%';
        tr.appendChild(f);r.appendChild(tr);
        r.appendChild(el('span','tx',i.txt));bw.appendChild(r)});
      var sc=el('div','sc');sc.appendChild(el('span','','0 h'));sc.appendChild(el('span','','10 h'));sc.appendChild(el('span','',b.max+' h'));bw.appendChild(sc);
      c.appendChild(bw);
    }
    if(b.type==='seasons'){
      var sw=el('div','ss');
      b.items.forEach(function(i){
        var s=el('div','se');s.style.setProperty('--c',i.c);
        var h=el('div','sh');h.appendChild(el('span','si',i.ico));var t=el('div','');t.appendChild(el('b','',i.name));t.appendChild(el('small','',i.when));h.appendChild(t);s.appendChild(h);
        var p=el('div','sp');
        var a=el('div','pc');a.appendChild(el('em','','✈️ Vol direct'));a.appendChild(el('strong','',fact(F,i.direct)));p.appendChild(a);
        var d=el('div','pc alt');d.appendChild(el('em','','🔁 Avec escale'));d.appendChild(el('strong','',fact(F,i.escale)));p.appendChild(d);
        s.appendChild(p);sw.appendChild(s)});
      c.appendChild(sw);
      if(b.note)c.appendChild(el('p','note','💰 '+b.note));
      c.appendChild(el('p','src',F.vols&&F.vols._verifie?('Prix vérifiés le '+F.vols._verifie):'Prix indicatifs · édition 2026'));
    }
    if(b.type==='table'){
      var w=el('div','tw'),t=el('table'),th=el('tr');
      b.head.forEach(function(h){th.appendChild(el('th','',h))});t.appendChild(th);
      b.rows.forEach(function(row,ri){var tr=el('tr',(b.ref&&ri===0)?'ref':'');
        row.forEach(function(cell,ci){var td=el('td',(b.bold&&b.bold.indexOf(ci)>=0)?'bd':'',fact(F,cell));tr.appendChild(td)});t.appendChild(tr)});
      w.appendChild(t);c.appendChild(w);
      if(b.note)c.appendChild(el('p','note','💰 '+b.note));
      var src=F.vols&&F.vols._verifie?('Prix vérifiés le '+F.vols._verifie):'Prix indicatifs · édition 2026';
      if(b.bold)c.appendChild(el('p','src',src));
    }

    if(b.type==='meteo'){
      var wx=el('div','wx'),chips=el('div','chips'),out=el('div','wxo');wx.appendChild(chips);wx.appendChild(out);c.appendChild(wx);
      var more=c.querySelector('.more');
      var ICON=function(k){if(k===0)return['☀️','Dégagé'];if(k<=2)return['🌤️','Peu nuageux'];if(k===3)return['☁️','Couvert'];if(k<=48)return['🌫️','Brouillard'];if(k<=57)return['🌦️','Bruine'];if(k<=67)return['🌧️','Pluie'];if(k<=77)return['❄️','Neige'];if(k<=82)return['🌦️','Averses'];return['⛈️','Orage']};
      function draw(p,d,old){
        var cu=d.current,i=ICON(cu.weather_code);out.innerHTML='';
        var big=el('div','wbig');big.appendChild(el('span','wi',i[0]));var t=el('div','');t.appendChild(el('b','',Math.round(cu.temperature_2m)+'°C'));t.appendChild(el('small','',i[1]+' · humidité '+cu.relative_humidity_2m+'% · vent '+Math.round(cu.wind_speed_10m)+' km/h'));big.appendChild(t);out.appendChild(big);
        var row=el('div','wdays');d.daily.time.forEach(function(day,k){var q=ICON(d.daily.weather_code[k]);var x=el('div','wd');
          x.appendChild(el('em','',new Date(day+'T12:00').toLocaleDateString('fr-FR',{weekday:'short'})));x.appendChild(el('span','',q[0]));
          x.appendChild(el('b','',Math.round(d.daily.temperature_2m_max[k])+'°'));x.appendChild(el('small','',Math.round(d.daily.temperature_2m_min[k])+'°'));
          x.appendChild(el('small','rn','💧'+(d.daily.precipitation_probability_max[k]||0)+'%'));row.appendChild(x)});out.appendChild(row);
        out.appendChild(el('p','src',old?('Hors connexion · dernière mise à jour : '+old):'Prévisions Open-Meteo · mises à jour à chaque ouverture'));
        if(more)more.textContent=Math.round(cu.temperature_2m)+'° '+i[0];
      }
      function load(p){
        chips.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x.textContent===p.nom)});
        out.innerHTML='<p class=src>Chargement…</p>';
        var key='tmwx:'+p.lat+','+p.lon;
        var u='https://api.open-meteo.com/v1/forecast?latitude='+p.lat+'&longitude='+p.lon+'&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=5';
        fetch(u).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){try{localStorage.setItem(key,JSON.stringify({d:d,t:new Date().toLocaleString('fr-FR')}))}catch(_){}draw(p,d)}).catch(function(){
          try{var s=JSON.parse(localStorage.getItem(key));if(s){draw(p,s.d,s.t);return}}catch(_){}
          out.innerHTML='<p class=src>Météo indisponible sans connexion. Elle s\'affichera dès que vous aurez du réseau.</p>'});
      }
      b.places.forEach(function(p,k){var x=el('button','',p.nom);x.type='button';x.addEventListener('click',function(e){e.stopPropagation();load(p)});chips.appendChild(x)});
      load(b.places[0]);
    }
    if(b.type==='form'){
      var fm=el('form','fm');
      b.fields.forEach(function(f){var w=el('label','ff');w.appendChild(el('span','',f.label));var i;
        if(f.t==='select'){i=el('select');f.opts.forEach(function(o){var op=el('option','',o);op.value=o;i.appendChild(op)})}
        else if(f.t==='textarea'){i=el('textarea');i.rows=3}
        else{i=el('input');i.type=f.t||'text'}
        i.name=f.k;if(f.ph)i.placeholder=f.ph;if(f.req)i.required=true;w.appendChild(i);fm.appendChild(w)});
      var sb=el('button','fb',b.btn||'Envoyer');sb.type='submit';fm.appendChild(sb);var msg=el('p','fmsg');fm.appendChild(msg);
      fm.addEventListener('submit',function(e){e.preventDefault();var data={};Object.keys(b.hidden||{}).forEach(function(k){data[k]=b.hidden[k]});
        new FormData(fm).forEach(function(v,k){data[k]=v});sb.disabled=true;msg.textContent='Envoi…';
        fetch(b.endpoint,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},body:JSON.stringify(data)})
          .then(function(r){if(!r.ok)throw 0;msg.textContent=b.ok||'Merci, c\'est envoyé !';fm.reset()})
          .catch(function(){msg.textContent='Envoi impossible pour le moment. Écris-nous à contact@thaimalin.fr'})
          .then(function(){sb.disabled=false})});
      c.appendChild(fm);
    }
    wire(c);grid.appendChild(c);
  });
  pg.appendChild(grid);
  if(P.outro)pg.appendChild(el('p','outro',P.outro));
  root.appendChild(pg);
};
})();
