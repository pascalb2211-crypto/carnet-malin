
(function(){
var root=document.getElementById('app'),sheet=document.getElementById('sheet'),bt=document.getElementById('bt'),D={};
function j(u){return fetch(u).then(function(r){return r.json()})}
function show(id){
  var i=D.idx.findIndex(function(p){return p.id===id});if(i<0){i=0;id=D.idx[0].id}
  if(window.TMclose)TMclose();
  j('data/pages/'+id+'.json').then(function(P){
    root.innerHTML='';TMrender(root,P,D.facts);bt.textContent=P.title;document.title=P.title+' · Thaï Malin';
    var n=document.createElement('nav');n.className='nav';
    var pv=D.idx[i-1],nx=D.idx[i+1];
    function nb(p,l,cl){return '<a class="nb '+cl+'" href="#/'+p.id+'" style="background-image:url(img/'+p.cover+'.jpg)"><span><small>'+l+'</small><b>'+p.title+'</b></span><i>'+(cl==='pv'?'‹':'›')+'</i></a>'}
    n.innerHTML=(nx?nb(nx,'Page suivante','nx'):'')+(pv?nb(pv,'Page précédente','pv'):'')+'<p class=pn>Page '+(i+1)+' sur '+D.idx.length+'</p>';
    root.appendChild(n);window.scrollTo(0,0);closeSheet()});
}
function route(){markMenu();show((location.hash||'').replace(/^#\/?/,''))}
function openVols(){var V=D.vols,rs=Object.keys((V&&V._routes)||{}),vs=document.getElementById('vsheet');if(!rs.length)return;
  function draw(k){var r=V[k],h='<button class=x id=vx>✕</button><h2>✈️ Prix indicatifs des vols</h2>';
    h+='<div class=chips>'+rs.map(function(q){return '<button data-r="'+q+'" class="'+(q===k?'on':'')+'">'+V._routes[q].nom+'</button>'}).join('')+'</div>';
    ['basse','moyenne','haute'].forEach(function(s){var S=((V._routes[k].saisons)||V._saisons)[s],x=r[s];if(!x)return;
      h+='<div class=vs style="--c:'+S.c+'"><div class=vh><span>'+S.ico+'</span><div><b>'+S.nom+'</b><small>'+S.quand+'</small></div></div><div class=vp><div><em>✈️ Vol direct</em><strong>'+x.direct+'</strong></div><div><em>🔁 Avec escale</em><strong>'+x.escale+'</strong></div></div></div>'});
    var R=V._routes[k],mj=R.maj||V._maj;h+='<p class=vn>'+(mj?('Prix vérifiés le '+mj.split('-').reverse().join('/')):'Prix indicatifs · édition 2026')+' · aller-retour par personne. Ils varient selon la date et la compagnie : comparez avant de réserver.'+(R.note?'<br>'+R.note:'')+'</p>';
    if(R.sources)h+='<p class=vn>Sources : '+R.sources.map(function(s){return '<a href="'+s.u+'" target=_blank rel=noopener style="color:#f5c542">'+s.t+'</a>'}).join(' · ')+'</p>';
    h+='<div class=lk2>'+(V._liens||[]).map(function(l){return '<a href="'+l.u+'" target=_blank rel=noopener>'+l.t+'</a>'}).join('')+'</div>';
    vs.innerHTML=h;vs.classList.add('on');
    document.getElementById('vx').onclick=function(){vs.classList.remove('on')};
    vs.querySelectorAll('.chips button').forEach(function(b){b.onclick=function(){draw(b.getAttribute('data-r'))}})}
  draw(rs[0])}
function openSheet(){sheet.classList.add('on')}function closeSheet(){sheet.classList.remove('on')}
function markMenu(){var id=(location.hash||'').replace(/^#\/?/,'')||D.idx[0].id;var f=false;document.querySelectorAll('#tabs a').forEach(function(a){var m=!f&&a.getAttribute('data-go')===id;if(m)f=true;a.classList.toggle('on',m)})}
Promise.all([j('data/pages.json'),j('data/facts.json'),j('data/vols.json').catch(function(){return null}),j('data/menu.json').catch(function(){return[{ico:'📖',label:'Sommaire',sommaire:true}]})]).then(function(r){
  D.idx=r[0];D.facts=r[1];D.facts.vols=r[2]||{};D.vols=r[2];
  var t=document.getElementById('tabs');t.innerHTML=r[3].map(function(m){return m.vols?'<a href="#" id="vol" role="button"><i>'+m.ico+'</i><span>'+m.label+'</span></a>':m.sommaire?'<a href="#" id="som" role="button"><i>'+m.ico+'</i><span>'+m.label+'</span></a>':'<a href="#/'+m.go+'" data-go="'+m.go+'"><i>'+m.ico+'</i><span>'+m.label+'</span></a>'}).join('');
  sheet.innerHTML='<button class=x id=sx>✕</button><h2>Sommaire</h2>'+D.idx.map(function(p){return '<a href="#/'+p.id+'"><i style="background-image:url(img/'+p.cover+'.jpg)"></i><div><b>'+p.num+'. '+p.title+'</b><span>'+p.sub+'</span></div></a>'}).join('');
  document.getElementById('sx').onclick=closeSheet;
  var vb=document.getElementById('vol');if(vb)vb.onclick=function(e){e.preventDefault();openVols()};var sm=document.getElementById('som');if(sm)sm.onclick=function(e){e.preventDefault();openSheet()};
  window.addEventListener('hashchange',route);route();
});
window.addEventListener('popstate',function(){if(window.TMclose)TMclose()});
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(function(){});
})();
