"""Computes data/deck_data.json from the stale SE Ranking exports, the SE Visible prompts export and the master workbook.
No matrix logic (potential / coverage) is computed here."""
import csv, io, glob, json, re, collections, statistics
from pathlib import Path
import openpyxl

root = Path(__file__).resolve().parent
proj = root.parent
TOPICS = ["Moment","Recipe","Health","Ingredient","Testimonial","Product","Flavor","Packaging","Purchase"]
FUNNEL = {"Moment":"Discover","Recipe":"Discover","Health":"Discover","Ingredient":"Evaluate","Testimonial":"Evaluate",
          "Product":"Buy","Flavor":"Buy","Packaging":"Buy","Purchase":"Buy"}
SOVDIR = {"Moment":"moment","Recipe":"recipe","Health":"health","Ingredient":"ingredients","Testimonial":"testimonial",
          "Product":"product","Flavor":"flavor","Packaging":"packaging","Purchase":"purchase"}
num = lambda x: float(x) if str(x).replace('.','',1).replace('-','',1).isdigit() else None
_BT = re.compile(r"^(oik\w*|okio\w*|oyko\w*|oiko\w*|orkos?|\w*ikos|okos|oyks|okai|okies?)$")
class _BR:
    @staticmethod
    def search(k): return any(_BT.match(w) for w in k.split())
BRAND_RE=_BR
COMP = {"Chobani":"chobani.com","fairlife":"fairlife.com","Premier Protein":"premierprotein.com"}

def sections(path):
    cur=None; out={}; hdr=None
    for line in open(path, encoding='utf-8-sig'):
        line=line.strip()
        if not line: continue
        if 'Google USA, 20' in line and line.startswith('"'):
            cur=line.strip('"').split(',')[0]; out[cur]=[]; continue
        if line.startswith('Keyword,'): hdr=next(csv.reader([line])); continue
        if cur and hdr:
            r=next(csv.reader([line]))
            if len(r)==len(hdr): out[cur].append(dict(zip(hdr,r)))
    return out

import difflib
_wb=openpyxl.load_workbook(proj/'Masterlist_Oikos_Megatron_MASTER.xlsx',read_only=True)
_it=_wb['Keywords Listing Updated'].iter_rows(values_only=True); next(_it)
BM={str(r[1]).strip().lower():(r[26],str(r[18] or '')) for r in _it if r[1]}
EXTRA={'ozark','oak','oaks','ocos','yogurt that starts with o','triple o','tripple zero','triple zero'}
def isbrand(k):
    # brand = master says Branded, or the keyword contains Oikos / a close misspelling (token similarity >= 0.8)
    k=k.strip().lower()
    lab_,tag=BM.get(k,(None,''))
    if (lab_=='Branded' and 'oikos' in tag.lower()) or BRAND_RE.search(k): return True
    if any(difflib.SequenceMatcher(None,w,'oikos').ratio()>=0.8 for w in k.split()): return True
    return any(e in k for e in EXTRA)
seo={}
for t in TOPICS:
    d=SOVDIR[t]
    sovf=[f for f in glob.glob(str(proj/'share_of_voice_exports'/d/'Share of Voice*.csv'))][0]
    lines=open(sovf,encoding='utf-8-sig').read().split('\n')
    first=[]
    for ln in lines[1:]:
        if not ln.strip(): break
        first.append(ln)
    rows=list(csv.DictReader(io.StringIO('\n'.join(first))))
    total_traffic=float(re.search(r'Total traffic forecast"?\s*\n"?Traffic forecast"?,Dynamics\s*\n([\d.]+)','\n'.join(lines)).group(1))
    doms=[{"domain":r['Domain'],"sov":float(r['Share of Voice']),"traffic":float(r['Traffic forecast']),"rank":i+1} for i,r in enumerate(rows)]
    oi=[x for x in doms if 'oikos.com' in x['domain']]
    o=oi[0] if oi else None
    sec=sections(str(proj/'share_of_voice_exports'/d/'Keywords in the Top 20.csv'))
    okrows=[r for k,v in sec.items() if 'oikos.com' in k for r in v]
    tr=lambda rs:sum(float(r['Traffic forecast'] or 0) for r in rs)
    tot=tr(okrows)
    tz=tr([r for r in okrows if 'triple-zero' in r['URL'].lower()])
    br=tr([r for r in okrows if isbrand(r['Keyword'])])
    comps={}
    for name,dom in COMP.items():
        m=[x for x in doms if dom in x['domain']]
        comps[name]=({"sov":m[0]['sov'],"rank":m[0]['rank'],"traffic":m[0]['traffic']} if m else None)
    seo[t]={"total_traffic":total_traffic,"topic":t,"funnel":FUNNEL[t],"n_domains":len(doms),"top5":doms[:5],
            "oikos":o,"oikos_traffic_keywords":round(tot),"oikos_triplezero_traffic":round(tz),"oikos_brand_kw_traffic":round(br),
            "competitors":comps}

# seasonality: topic x calendar month index (all months, canonical keywords)
wb=openpyxl.load_workbook(proj/'Masterlist_Oikos_Megatron_MASTER.xlsx',read_only=True)
it=wb['Keywords Listing Updated'].iter_rows(values_only=True); h=next(it)
months=[(i,str(h[i])) for i in range(45,93)]
MN=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def cal(lbl):
    for k,m in enumerate(MN):
        if str(lbl).startswith(m): return k
    return None
acc={t:[0.0]*12 for t in TOPICS}; cnt={t:[0]*12 for t in TOPICS}
for r in it:
    if not r[1] or r[3] not in acc: continue
    if r[43] and not str(r[43]).startswith('Canonical'): continue
    for i,lbl in months:
        v=r[i]
        k=cal(h[i])
        if isinstance(v,(int,float)) and k is not None: acc[r[3]][k]+=v; cnt[r[3]][k]+=1
season={}
for t in TOPICS:
    vals=[acc[t][k]/max(1,cnt[t][k]) if cnt[t][k] else 0 for k in range(12)]
    # months counted per calendar month differ by one year (4 or 3 years): use mean of per-year monthly totals
    nyears=[len({str(h[i])[-4:] for i,l in months if cal(h[i])==k}) for k in range(12)]
    tot=[acc[t][k]/nyears[k] for k in range(12)]
    mean=sum(tot)/12
    season[t]={"index":[round(x/mean,2) for x in tot],"peak":MN[tot.index(max(tot))]}
hdrs=[str(h[i]) for i,_ in months]

# SE Visible
sv=list(csv.DictReader(open(proj/'sevisibleexport.csv',encoding='utf-8-sig')))
def topic_of(s): return s.split(':')[0].strip()
fn=lambda x:(float(str(x).replace('%','')) if str(x).replace('%','').replace('.','',1).replace('-','',1).isdigit() else None)
ai={}
for t in TOPICS:
    rs=[r for r in sv if topic_of(r['Topic'])==t]
    vis=[fn(r['Visibility']) or 0 for r in rs]
    pos=[fn(r['Avg. Position']) for r in rs if fn(r['Visibility']) and fn(r['Avg. Position'])]
    sent=[fn(r['Net Sentiment']) for r in rs if fn(r['Net Sentiment']) is not None]
    men=collections.Counter(m.strip() for r in rs for m in r['Top Mentions'].split(',') if m.strip())
    ai[t]={"topic":t,"funnel":FUNNEL[t],"n":len(rs),"branded":sum(r['Is Branded']=='yes' for r in rs),
        "avg_visibility":round(sum(vis)/len(vis),1),"zero":sum(v==0 for v in vis),
        "avg_sentiment":round(sum(sent)/len(sent),1) if sent else None,
        "avg_position":round(sum(pos)/len(pos),1) if pos else None,
        "mentions":dict(men),
        "prompts":[{"prompt":r['Prompt'],"visibility":fn(r['Visibility']),"sov":r['SoV'],"position":r['Avg. Position'],
                    "sentiment":fn(r['Net Sentiment']),"mentions":r['Top Mentions'],"branded":r['Is Branded']} for r in rs]}
allmen=collections.Counter(m.strip().lower() for r in sv for m in r['Top Mentions'].split(',') if m.strip())
out={"seo":seo,"season":season,"season_cols":hdrs[:2],"ai":ai,"ai_brand_mentions":dict(allmen),
     "ai_total":len(sv),"ai_zero":sum((fn(r['Visibility']) or 0)==0 for r in sv)}
(root/'data/deck_data.json').write_text(json.dumps(out,indent=1))
for t in TOPICS:
    s=seo[t]; o=s['oikos']
    print(t, 'SOVrank',o['rank'] if o else None, o['sov'] if o else None, 'kwTraffic',s['oikos_traffic_keywords'],'TZ',s['oikos_triplezero_traffic'],'brandKW',s['oikos_brand_kw_traffic'], '| peak',season[t]['peak'],'| AI',ai[t]['n'],ai[t]['avg_visibility'],ai[t]['zero'])
print(allmen)

# --- brand demand and attributes (master, canonical keywords only)
ATTR_BY_STAGE={"Discover":[("Moments",24),("Recipes",25),("Benefits",21)],
               "Evaluate":[("Ingredient",17),("Testimonials",22),("Benefits",21)],
               "Buy":[("Taste",15),("Packaging",16),("Yogurt types",14)]}
BRAND_OK=["Oikos","Premier Protein","Fairlife","Chobani","Good Culture","Oikos Pro","OWYN","Orgain","Muscle Milk","Noosa"]
bd={"stage":{s:{"brand":0.0,"non":0.0} for s in ("Discover","Evaluate","Buy")},"top_branded":[],"brands":collections.Counter()}
attrs={st:{a:collections.Counter() for a,_ in L} for st,L in ATTR_BY_STAGE.items()}
_it=_wb['Keywords Listing Updated'].iter_rows(values_only=True); next(_it)
topbr=[]
for r in _it:
    if not r[1] or r[3] not in FUNNEL: continue
    if r[43] and not str(r[43]).startswith('Canonical'): continue
    v=[x for x in r[45:93] if isinstance(x,(int,float))]; a=sum(v)/len(v) if v else (r[44] if isinstance(r[44],(int,float)) else 0)
    st=FUNNEL[r[3]]
    if isbrand(str(r[1])): bd["stage"][st]["brand"]+=a; topbr.append((a,str(r[1])))
    else: bd["stage"][st]["non"]+=a
    if r[18]:
        for b in str(r[18]).split(','):
            if b.strip() in BRAND_OK: bd["brands"][b.strip()]+=a
    for an,ci in ATTR_BY_STAGE[st]:
        if r[ci]:
            for val in str(r[ci]).split(','): attrs[st][an][val.strip()]+=a
topbr.sort(reverse=True)
bd["top_branded"]=[{"kw":k,"vol":round(a)} for a,k in topbr[:10]]
bd["brands"]=[{"brand":k,"vol":round(v)} for k,v in bd["brands"].most_common()]
bd["stage"]={k:{x:round(y) for x,y in v.items()} for k,v in bd["stage"].items()}
out["brand"]=bd
out["attrs"]={st:{a:[{"v":k,"vol":round(x)} for k,x in c.most_common(4)] for a,c in d_.items()} for st,d_ in attrs.items()}
(root/'data/deck_data.json').write_text(json.dumps(out,indent=1))
print(bd["stage"]); print(bd["top_branded"][:6])
