const parts=[...document.querySelectorAll('.part')],pills=[...document.querySelectorAll('.pill')];
let P=0,S=0;const seen=new Set();
const subs=p=>[...parts[p].querySelectorAll('.ss')];
function show(p,s){P=Math.max(0,Math.min(parts.length-1,p));S=Math.max(0,Math.min(subs(P).length-1,s));seen.add(P);
 parts.forEach((x,i)=>x.classList.toggle('on',i===P));
 subs(P).forEach((x,i)=>x.classList.toggle('on',i===S));subs(P)[S].scrollTop=0;
 pills.forEach((x,i)=>{x.classList.toggle('on',i===P);x.classList.toggle('seen',seen.has(i)&&i!==P)});
 const n=subs(P).length;document.getElementById('dots').innerHTML=subs(P).map((_,i)=>`<i class="${i===S?'on':''}" data-i="${i}"></i>`).join('');
 document.getElementById('lab').textContent=`${subs(P)[S].dataset.name} · ${S+1} / ${n}`;
 document.getElementById('prevP').disabled=P===0;document.getElementById('nextP').disabled=P===parts.length-1;
 location.hash=`p${P}-s${S}`}
function next(){S<subs(P).length-1?show(P,S+1):P<parts.length-1&&show(P+1,0)}
function prev(){S>0?show(P,S-1):P>0&&show(P-1,subs(P-1).length-1)}
pills.forEach((b,i)=>b.onclick=()=>show(i,0));
document.getElementById('nextS').onclick=next;document.getElementById('prevS').onclick=prev;
document.getElementById('nextP').onclick=()=>show(P+1,0);document.getElementById('prevP').onclick=()=>show(P-1,0);
document.getElementById('dots').onclick=e=>{if(e.target.dataset.i)show(P,+e.target.dataset.i)};
document.onkeydown=e=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();next()}else if(e.key==='ArrowLeft')prev();
 else if(e.key==='f')document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()};
const m=location.hash.match(/p(\d+)-s(\d+)/);m?show(+m[1],+m[2]):show(0,0);
