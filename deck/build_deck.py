"""Builds Oikos_Megatron_Deck.html from data/outline.json and data/slides_1_3_data.json.
Only slides 1-3 carry data. Every other slide is a labelled skeleton."""
import json, html, sys
from pathlib import Path

root = Path(__file__).parent
outline = json.loads((root / "data/outline.json").read_text())
d = json.loads((root / "data/slides_1_3_data.json").read_text())
D = json.loads((root / "data/deck_data.json").read_text())
esc = html.escape
fmt = lambda n: f"{n:,}".replace(",", ",")

FUNNELS = ["Discover", "Evaluate", "Buy"]
fun_vol = {f: sum(t["volume"] for t in d["topics"] if t["funnel"] == f) for f in FUNNELS}
total = d["total_volume"]
pct = lambda f: round(100 * fun_vol[f] / total)
top = max(d["topics"], key=lambda t: t["volume"])

def head(eyebrow, title, verdict):
    return f'<div class="sl">{esc(eyebrow)}</div><h2 class="sh">{esc(title)}</h2><p class="verdict">{esc(verdict)}</p>'

def insights(items):
    out = ""
    for i, (num, txt, src) in enumerate(items, 1):
        out += f'<div class="ins"><span class="n">0{i}</span><b>{esc(num)}</b><p>{esc(txt)}</p><small>{esc(src)}</small></div>'
    return f'<div class="insrow">{out}</div>'

def reco(text):
    return f'<div class="reco"><span>Our recommendation</span> {esc(text)}</div>'

def cover():
    kpis = [(fmt(d["keywords_unique"]), "unique keywords"), ("9", "topics in 3 funnel stages"),
            (fmt(d["prompts_total"]), "AI prompts listed"), (f'{total/1e6:.1f} M', "monthly searches (order of magnitude)")]
    k = "".join(f'<div class="kpi"><b>{a}</b><span>{esc(b)}</span></div>' for a, b in kpis)
    return f'''<div class="hero"><span class="badge">Holistic Search Study · November 2026</span>
<h1>Oikos Pro</h1><p class="sub">Google and AI search · United States</p><div class="kpis">{k}</div>
<div class="band"><b>Your question:</b> how does Oikos Pro show up in AI answers and in Google, especially when people ask about taste, texture, recipe change and price?</div>
<div class="agenda">{"".join(f'<span>{p["id"]:02d} · {esc(p["label"])}</span>' for p in outline["parts"])}</div></div>'''

def method():
    steps = [("1", "Keyword listing and classification", f'{fmt(d["keywords_total"])} keywords, 9 topics, 3 funnel stages'),
             ("2", "SEO matrix (SE Ranking)", "Share of voice per topic, Google USA"),
             ("3", "AI matrix (SE Visible)", "Prompts: 70% unbranded, 30% branded"),
             ("4", "Benchmark", "2 inspirational competitors, SEO and GEO")]
    s = "".join(f'<div class="step"><i>{a}</i><b>{esc(b)}</b><p>{esc(c)}</p></div>' for a, b, c in steps)
    return head("01 · Method", "How to read this study", "Four steps, one funnel, one question per slide.") + f'<div class="steps">{s}</div>' + \
        '<div class="note">Funnel: Discover (Moment, Recipe, Health), Evaluate (Ingredients, Testimonial), Buy (Product, Flavor, Packaging, Purchase). Branded and unbranded prompts are read separately. Competitor prompts are not tracked.</div>'

def treemap():
    cols = ""
    for f in FUNNELS:
        ts = sorted([t for t in d["topics"] if t["funnel"] == f], key=lambda t: -t["volume"])
        blocks = "".join(f'<div class="tm" style="flex:{t["volume"]}" title="{t["keywords"]} keywords"><b>{esc(t["topic"])}</b><span>{fmt(t["volume"])} · {round(100*t["volume"]/total,1)}%</span></div>' for t in ts)
        cols += f'<div class="tmcol" style="flex:{fun_vol[f]}"><h4>{f} · {pct(f)}%</h4><div class="tmstack">{blocks}</div></div>'
    ins = [(f"{pct('Buy')}%", "of search demand sits in the Buy stage", "Keyword listing, monthly average"),
           (f"{round(100*top['volume']/total)}%", f"of all demand is the {top['topic']} topic", "Includes brand-name searches"),
           (f"{pct('Discover')}%", "is Discover: Moment, Recipe, Health", "Keyword listing"),
           (f"{pct('Evaluate')}%", "is Evaluate: Ingredients, Testimonial", "Keyword listing")]
    return head("02 · Global vision", "Where the demand is", f"Buy holds {pct('Buy')}% of demand, Discover {pct('Discover')}% and Evaluate {pct('Evaluate')}%.") + \
        insights(ins) + f'<div class="tmwrap">{cols}</div>' + \
        '<div class="note">Average monthly search volume, USA, last 48 months. Close variants and misspellings share one volume and are counted once. Volumes are orders of magnitude, not additive. Product includes brand-name searches such as "oikos protein shake".</div>' + \
        reco("To write once the SEO share of voice (slide 4) is in: pick the topics where demand is high and Oikos is weak.")

def todo(s):
    note = f'<div class="note">{esc(s["note"])}</div>' if s.get("note") else ""
    return head(f'{s["part"]}', s["name"], "[Verdict sentence, 15 words max, written when the data arrives]") + \
        insights([("[ ]", "[Insight, 12 words max]", "[source]")] * 4) + \
        f'<div class="ph"><span class="tag">DATA PENDING</span><h4>Planned visual</h4><p>{esc(s["visual"])}</p><h4>Needs</h4><p>{esc(s["needs"])}</p></div>{note}' + \
        reco("[Action, target, P1 / P2 / P3]")


TOPICS=["Moment","Recipe","Health","Ingredient","Testimonial","Product","Flavor","Packaging","Purchase"]
STAGE_TOPICS={"Discover":["Moment","Recipe","Health"],"Evaluate":["Ingredient","Testimonial"],"Buy":["Product","Flavor","Packaging","Purchase"]}
SEO=D["seo"]; AI=D["ai"]; SEA=D["season"]
vol={t["topic"]:t["volume"] for t in d["topics"]}
TOPIC_LABEL={"Ingredient":"Ingredients"}
lab=lambda t:TOPIC_LABEL.get(t,t)
tot_traffic=sum(SEO[t]["oikos_traffic_keywords"] for t in TOPICS)
brand_traffic=sum(SEO[t]["oikos_brand_kw_traffic"] for t in TOPICS)
tz_traffic=sum(SEO[t]["oikos_triplezero_traffic"] for t in TOPICS)
STALE='<span class="tagp stale">STALE · SE Ranking 22 Nov, old project</span>'
ONEWK='<span class="tagp live">SE Visible · 111 prompts · 20-26 Nov</span>'
RECO_TBD="[Recommendation to write after review: action, target, P1 / P2 / P3]"
def bar(label,val,mx,txt,cls="",sub=""):
    w=0 if not mx else max(0,min(100,100*val/mx))
    return f'<div class="brow"><div class="bl">{esc(label)}<small>{esc(sub)}</small></div><div class="bt"><i class="{cls}" style="width:{w:.1f}%"></i></div><div class="bv">{esc(txt)}</div></div>'
def rank_txt(o): return "outside top 20" if not o or o["rank"]>20 else f"#{o['rank']}"
def sov_txt(o): return f'{o["sov"]:.2f}% · {rank_txt(o)}' if o else "0% · outside top 20"
def ai_avg(topics,key="avg_visibility"):
    n=sum(AI[t]["n"] for t in topics); return sum(AI[t][key]*AI[t]["n"] for t in topics)/n
def ai_zero(topics): return sum(AI[t]["zero"] for t in topics), sum(AI[t]["n"] for t in topics)

def sov():
    mx=max((SEO[t]["oikos"]["sov"] if SEO[t]["oikos"] else 0) for t in TOPICS)
    rows="".join(bar(lab(t),(SEO[t]["oikos"]["sov"] if SEO[t]["oikos"] else 0),mx,sov_txt(SEO[t]["oikos"]),"",
        f'{FUNNEL_OF[t]} · est. traffic {SEO[t]["oikos_traffic_keywords"]:,}') for t in TOPICS)
    ins=[(f"{round(100*brand_traffic/tot_traffic)}%","of Oikos estimated traffic comes from brand-name keywords and misspellings","Keywords in the Top 20, stale"),
         (f"{round(100*tz_traffic/tot_traffic)}%","of Oikos estimated traffic lands on Triple Zero pages","URL of ranking page, stale"),
         ("3 of 9","topics have Oikos outside the top 20 domains: Moment, Recipe, Purchase","Share of voice by topic, stale"),
         (f'{SEO["Flavor"]["oikos"]["sov"]}%',"share of voice in Flavor, where Oikos ranks #1","Share of voice, stale")]
    return head("02 · Global vision","Where Oikos wins and loses in Google",f"Oikos leads Flavor and Product, but almost entirely through brand-name searches.")+STALE+insights(ins)+\
        f'<div class="vis"><h4>Oikos share of voice by topic</h4>{rows}</div>'+\
        '<div class="note">Share of voice = share of estimated traffic in the topic keyword set, Google USA. Oikos in brand searches includes misspellings (okies, orkos, ikos). Old project: includes Triple Zero and ambiguous keywords. Re-export after the SE Ranking rebuild.</div>'+reco(RECO_TBD)

def season():
    MN=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    head_row="<tr><th></th>"+"".join(f"<th>{m}</th>" for m in MN)+"<th>Peak</th></tr>"
    body=""
    for t in TOPICS:
        ix=SEA[t]["index"]; cells=""
        for k,v in enumerate(ix):
            a=max(0,min(1,(v-0.7)/0.8)); star=" peak" if MN[k]==SEA[t]["peak"] else ""
            cells+=f'<td class="hm{star}" style="background:rgba(184,0,28,{a:.2f});color:{"#fff" if a>.55 else "#2c2c2c"}">{v:.2f}</td>'
        body+=f'<tr><th>{lab(t)}</th>{cells}<td><b>{SEA[t]["peak"]}</b></td></tr>'
    jan=sum(SEA[t]["peak"]=="Jan" for t in TOPICS)
    ins=[(f"{jan} of 9","topics peak in January","Google Ads, 48 months, USA"),
         (f'{SEA["Product"]["peak"]}',"is the peak month for Product",""),
         (f'{SEA["Flavor"]["peak"]}',"is the peak month for Flavor and Purchase",""),
         ("Index","1.00 = the topic's average month","Peak month = highest of 12")]
    return head("02 · Global vision","When the demand arrives",f"{jan} of 9 topics peak in January; Product peaks in {SEA['Product']['peak']}.")+insights(ins)+\
        f'<div class="vis"><table class="heat">{head_row}{body}</table></div>'+\
        '<div class="note">Seasonality index = average volume of each calendar month across the 48 months (Nov 2022 to Oct 2026) ÷ the topic\'s monthly mean. Close variants counted once. Brand-name searches included.</div>'+reco(RECO_TBD)

def ai_global():
    mx=100
    rows="".join(bar(lab(t),AI[t]["avg_visibility"],mx,f'{AI[t]["avg_visibility"]:.0f}% · {AI[t]["zero"]}/{AI[t]["n"]} prompts at zero',"",f'{AI[t]["n"]} prompts, {AI[t]["branded"]} branded') for t in TOPICS)
    men=D["ai_brand_mentions"]; mm=max(men.values())
    mrows="".join(bar(k.title() if k!="oikos pro" else "Oikos Pro",v,mm,f"in {v} of {D['ai_total']} prompts","brandbar" if k=="oikos pro" else "") for k,v in sorted(men.items(),key=lambda x:-x[1]))
    z=D["ai_zero"]; br=[p for t in TOPICS for p in AI[t]["prompts"] if p["branded"]=="yes"]; ub=[p for t in TOPICS for p in AI[t]["prompts"] if p["branded"]=="no"]
    avg=lambda l:sum((p["visibility"] or 0) for p in l)/len(l)
    ins=[(f'{z} of {D["ai_total"]}',"prompts show no Oikos mention at all","SE Visible prompts export"),
         (f'{avg(br):.0f}% vs {avg(ub):.0f}%',"average visibility, branded vs unbranded prompts","SE Visible"),
         (f'{men.get("chobani",0)}',f'prompts mention Chobani (Oikos Pro: {men.get("oikos pro",0)})',"Top Mentions column"),
         ("Pending","cited sources and competitor exports","SE Visible competitors / sources")]
    return head("02 · Global vision","Who answers in AI instead of Oikos",f"Oikos is absent from {z} of {D['ai_total']} tracked prompts; unbranded visibility is far lower.")+ONEWK+insights(ins)+\
        f'<div class="two"><div class="vis"><h4>Average visibility by topic</h4>{rows}</div><div class="vis"><h4>Brands mentioned (tracked brands only)</h4>{mrows}<div class="ph small"><span class="tag">PENDING</span> Cited sources by domain: needs the SE Visible sources export.</div></div></div>'+\
        '<div class="note">One week of data, 7 to 30 prompts per topic: indicative only. Engine(s) not stated in the export. Top Mentions only lists brands tracked in the project (Oikos Pro, Chobani, fairlife, Orgain, Nurri); Premier Protein is not tracked.</div>'+reco(RECO_TBD)

def stage_seo(s):
    st=s["stage"]; ts=STAGE_TOPICS[st]
    stv=sum(vol[t] for t in ts); mxv=max(vol[t] for t in ts); mxs=max((SEO[t]["oikos"]["sov"] if SEO[t]["oikos"] else 0) for t in ts)
    vrows="".join(bar(lab(t),vol[t],mxv,f"{vol[t]:,} / month","slate") for t in ts)
    srows="".join(bar(lab(t),(SEO[t]["oikos"]["sov"] if SEO[t]["oikos"] else 0),mxs,sov_txt(SEO[t]["oikos"]),"",f'est. traffic {SEO[t]["oikos_traffic_keywords"]:,}') for t in ts)
    best=max(ts,key=lambda t:(SEO[t]["oikos"]["sov"] if SEO[t]["oikos"] else 0))
    weak=[lab(t) for t in ts if not SEO[t]["oikos"] or SEO[t]["oikos"]["rank"]>10]
    ins=[(f'{round(100*stv/d["total_volume"])}%',f"of total search demand is {st}","Keyword listing"),
         (f'{SEO[best]["oikos"]["sov"]}%' if SEO[best]["oikos"] else "0%",f"best share of voice: {lab(best)} ({rank_txt(SEO[best]['oikos'])})","Share of voice, stale"),
         (str(len(weak)),f"topics with Oikos outside the top 10: {', '.join(weak) or 'none'}","Share of voice, stale"),
         (f'{sum(SEO[t]["oikos_traffic_keywords"] for t in ts):,}',"Oikos estimated monthly traffic in this stage","Keywords in the Top 20, stale")]
    ver=f'In {st}, Oikos is strongest in {lab(best)}' + (f' and outside the top 10 in {", ".join(weak)}.' if weak else '.')
    return head(f"0{s['part'][1]} · {st}" if False else s["part"],s["name"],ver)+STALE+insights(ins)+\
        f'<div class="two"><div class="vis"><h4>Search demand (avg monthly volume)</h4>{vrows}</div><div class="vis"><h4>Oikos share of voice (rank among domains)</h4>{srows}</div></div>'+\
        '<div class="note">Demand includes brand-name searches. Rank is among the top 20 domains per topic. Share of voice is not additive across topics.</div>'+reco(RECO_TBD)

def bench(s):
    st=s["stage"]; ts=STAGE_TOPICS[st]
    def cell(o): return "not in top 20" if not o else f'{o["sov"]:.1f}% (#{o["rank"]})'
    rows=""
    for t in ts:
        S=SEO[t]; lead=S["top5"][0]
        rows+=f'<tr><th>{lab(t)}</th><td class="b">{sov_txt(S["oikos"]) if S["oikos"] else "0%"}</td><td>{cell(S["competitors"]["Chobani"])}</td><td>{cell(S["competitors"]["fairlife"])}</td><td>{cell(S["competitors"]["Premier Protein"])}</td><td>{esc(lead["domain"].replace("www.",""))} {lead["sov"]:.1f}%</td></tr>'
    appear=lambda c:sum(1 for t in ts if SEO[t]["competitors"][c])
    ins=[(f'{appear("Chobani")} of {len(ts)}',"topics where Chobani is in the top 20 domains","Share of voice, stale"),
         (f'{appear("fairlife")} of {len(ts)}',"topics where fairlife is in the top 20","Share of voice, stale"),
         (f'{appear("Premier Protein")} of {len(ts)}',"topics where Premier Protein is in the top 20","Share of voice, stale"),
         ("Pending","the two inspirational competitors are not chosen yet","Thomas to confirm")]
    return head(s["part"],s["name"],f"Share of voice of Oikos and three candidate competitors in {st} topics.")+STALE+insights(ins)+\
        f'<div class="vis"><table class="tbl"><tr><th>Topic</th><th>Oikos</th><th>Chobani</th><th>fairlife</th><th>Premier Protein</th><th>Domain ranked #1</th></tr>{rows}</table></div>'+\
        '<div class="note">Candidates only: the 2 inspirational competitors are not chosen. Share of voice (rank). Per-keyword competitor positions are not in these exports.</div>'+reco(RECO_TBD)

def plist(prompts,limit=12,sort="visibility"):
    rows=""
    for p in sorted(prompts,key=lambda p:((p["visibility"] or 0),(p["sentiment"] if p["sentiment"] is not None else 0)))[:limit]:
        sent="" if p["sentiment"] is None else f'{p["sentiment"]:+.0f}'
        rows+=f'<tr><td>{esc(p["prompt"])}</td><td>{"branded" if p["branded"]=="yes" else "unbranded"}</td><td>{p["visibility"]:.0f}%</td><td>{sent}</td><td>{esc(p["mentions"])}</td></tr>'
    return f'<table class="tbl"><tr><th>Prompt</th><th>Type</th><th>Visibility</th><th>Net sentiment</th><th>Brands mentioned</th></tr>{rows}</table>'

def ai_stage(s):
    st=s["stage"]; ts=STAGE_TOPICS[st]
    rows="".join(bar(lab(t),AI[t]["avg_visibility"],100,f'{AI[t]["avg_visibility"]:.0f}% · {AI[t]["zero"]}/{AI[t]["n"]} at zero',"",f'{AI[t]["n"]} prompts, {AI[t]["branded"]} branded') for t in ts)
    z,n=ai_zero(ts); allp=[p for t in ts for p in AI[t]["prompts"]]
    low=[p for p in allp if (p["visibility"] or 0)==0]
    ins=[(f"{ai_avg(ts):.0f}%","average visibility across the stage's prompts","SE Visible"),
         (f"{z} of {n}","prompts with zero visibility","SE Visible"),
         (f'{sum(AI[t]["mentions"].get("Chobani",0) for t in ts)}',"prompts mention Chobani","Top Mentions"),
         (f"{ai_avg(ts,'avg_sentiment'):+.0f}" if all(AI[t]["avg_sentiment"] is not None for t in ts) else "n/a","average net sentiment","SE Visible")]
    extra=""
    if st=="Buy":
        pp=[p for p in AI["Purchase"]["prompts"]]
        extra=f'<h4 class="sub">Price and shrinkflation prompts (Purchase)</h4>{plist(pp,8)}'
    else:
        extra=f'<h4 class="sub">Prompts with zero visibility ({len(low)})</h4>{plist(low,10)}'
    return head(s["part"],s["name"],f"Oikos averages {ai_avg(ts):.0f}% visibility in {st} prompts; {z} of {n} show no mention.")+ONEWK+insights(ins)+\
        f'<div class="vis"><h4>Average visibility by topic</h4>{rows}</div>{extra}'+\
        '<div class="note">Indicative: one week and few prompts per topic. Net sentiment is SE Visible\'s score (definition not in the export). Cited sources are not included.</div>'+reco(RECO_TBD)

def sentiment():
    P=AI["Testimonial"]["prompts"]; neg=[p for p in P if p["sentiment"] is not None and p["sentiment"]<0]
    brp=[p for p in P if p["branded"]=="yes"]
    ins=[(f'{AI["Testimonial"]["avg_visibility"]:.0f}%',"average visibility in Testimonial prompts","SE Visible"),
         (f'{len(neg)}',"Testimonial prompts with negative net sentiment: "+"; ".join(f'"{p["prompt"]}" ({p["sentiment"]:+.0f})' for p in neg[:2]),"SE Visible"),
         (f'{AI["Testimonial"]["zero"]}',"Testimonial prompts with zero visibility","SE Visible"),
         ("Pending","complaint themes (thin, grainy, sour, chalky)","needs AI answer text")]
    return head(s_part("Evaluate"),"Taste and texture sentiment","Sentiment scores exist per prompt; the complaint themes need the AI answer text.")+ONEWK+insights(ins)+\
        f'<h4 class="sub">All 30 Testimonial prompts, lowest visibility first</h4>{plist(P,30)}'+\
        '<div class="ph small"><span class="tag">PENDING</span> Complaint theme chart (thin, grainy, sour, chalky, recipe change): blank until answer text or sources are exported.</div>'+reco(RECO_TBD)
def s_part(st): return "03 · Evaluate"

def summary():
    rows=""
    for st,ts in STAGE_TOPICS.items():
        z,n=ai_zero(ts); sv=sum(vol[t] for t in ts); bs=max(ts,key=lambda t:(SEO[t]["oikos"]["sov"] if SEO[t]["oikos"] else 0))
        rows+=f'<tr><th>{st}</th><td>{round(100*sv/d["total_volume"])}%</td><td>{lab(bs)} {SEO[bs]["oikos"]["sov"] if SEO[bs]["oikos"] else 0}%</td><td>{ai_avg(ts):.0f}%</td><td>{z}/{n}</td><td class="tbd">[P1 / P2 / P3]</td></tr>'
    return head("06 · Recommendations","Summary: verdict per funnel stage","[Verdict to write once all slides are reviewed]")+\
        f'<div class="vis"><table class="tbl"><tr><th>Stage</th><th>Share of demand</th><th>Best Oikos share of voice (stale)</th><th>AI visibility</th><th>Prompts at zero</th><th>Priority</th></tr>{rows}</table></div>'+\
        '<div class="note">Data columns are filled from slides 3 to 16. The priority column is intentionally blank: no recommendations or priority rule written yet.</div>'+reco(RECO_TBD)

FUNNEL_OF={t:f for f,ts in STAGE_TOPICS.items() for t in ts}

parts_html, pills = "", ""
for p in outline["parts"]:
    pills += f'<button class="pill" data-p="{p["id"]}" title="{esc(p["label"])}">{p["id"]:02d}</button>'
    subs = []
    if p["phrase"]:
        subs.append(("Introduction", f'<div class="divider"><div class="sl">Part {p["id"]:02d}</div><h2>{esc(p["label"])}</h2><p>{esc(p["phrase"])}</p></div>'))
    for s in p["slides"]:
        s["part"] = f'{p["id"]:02d} · {p["label"]}'
        body = {"cover": cover, "method": method, "treemap": treemap, "sov": sov, "season": season, "ai_global": ai_global, "sentiment": sentiment, "summary": summary, "stage_seo": lambda: stage_seo(s), "bench": lambda: bench(s), "ai_stage": lambda: ai_stage(s)}.get(s["tpl"], lambda: todo(s))()
        subs.append((f'{s["n"]}. {s["name"]}', f'<div class="slide-in">{body}</div>'))
    sl = "".join(f'<section class="ss" data-name="{esc(n)}">{b}</section>' for n, b in subs)
    parts_html += f'<div class="part" data-p="{p["id"]}"><div class="track">{sl}</div></div>'

css = (root / "deck.css").read_text()
js = (root / "deck.js").read_text()
out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(outline["title"])}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="top"><b>Digitad</b><i></i><span>Oikos Pro</span><em>Holistic Search Study</em><u>Confidential</u></header>
<nav class="prog">{pills}</nav>
<main>{parts_html}</main>
<footer class="foot"><button id="prevP">← Previous section</button><div class="dots" id="dots"></div><span id="lab"></span><button id="nextP">Next section →</button></footer>
<button class="arr l" id="prevS">‹</button><button class="arr r" id="nextS">›</button>
<script>{js}</script></body></html>'''
(root / "Oikos_Megatron_Deck.html").write_text(out, encoding="utf-8")
print("slides:", sum(len(p["slides"]) for p in outline["parts"]), "bytes:", len(out))
