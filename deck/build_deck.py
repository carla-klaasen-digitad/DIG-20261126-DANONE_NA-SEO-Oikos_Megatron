"""Builds Oikos_Megatron_Deck.html (35 slides) and Oikos_Megatron_Deck_20.html (core 20) from
data/outline.json, data/deck_data.json and data/slides_1_3_data.json. Structure follows the example decks
(see ../deck_analysis). Anything without data is a labelled blank."""
import json, html, base64, collections
from pathlib import Path

root = Path(__file__).parent
outline = json.loads((root / "data/outline.json").read_text())
d = json.loads((root / "data/slides_1_3_data.json").read_text())
D = json.loads((root / "data/deck_data.json").read_text())
esc = html.escape
fmt = lambda n: f"{n:,.0f}"

TOPICS = ["Moment","Recipe","Health","Ingredient","Testimonial","Product","Flavor","Packaging","Purchase"]
STAGES = {"Discover":["Moment","Recipe","Health"],"Evaluate":["Ingredient","Testimonial"],"Buy":["Product","Flavor","Packaging","Purchase"]}
FUNNEL_OF = {t:s for s,ts in STAGES.items() for t in ts}
LAB = {"Ingredient":"Ingredients"}
lab = lambda t: LAB.get(t, t)
SEO, AI, SEA = D["seo"], D["ai"], D["season"]
vol = {t["topic"]:t["volume"] for t in d["topics"]}
TOTAL_VOL = d["total_volume"]
stage_vol = {s:sum(vol[t] for t in ts) for s,ts in STAGES.items()}
tot_traffic = sum(SEO[t]["oikos_traffic_keywords"] for t in TOPICS)
brand_traffic = sum(SEO[t]["oikos_brand_kw_traffic"] for t in TOPICS)
tz_traffic = sum(SEO[t]["oikos_triplezero_traffic"] for t in TOPICS)
SOV_MAX, DEM_MAX = 12, 70
MN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# ---------- logos (embedded, same height) ----------
LOGOS = {}
for k, names in {"oikos":["Oikos","Oikos Pro"],"chobani":["Chobani"],"fairlife":["Fairlife","fairlife"],"premier":["Premier Protein"]}.items():
    b = base64.b64encode((root/f"assets/logo_{k}.png").read_bytes()).decode()
    for n in names: LOGOS[n] = b
def logo(name, text=True):
    b = LOGOS.get(name)
    if not b: return esc(name)
    return f'<span class="lg"><img src="data:image/png;base64,{b}" alt="{esc(name)}"></span>'

# ---------- building blocks ----------
CUR = [""]
STALE = '<span class="tagp stale">STALE · SE Ranking 22 Nov, old project</span>'
ONEWK = '<span class="tagp live">SE Visible · 111 prompts · 20-26 Nov</span>'
RECO_TBD = "[Recommendation to write after review: action, target, P1 / P2 / P3]"
def head(title, verdict, eyebrow=None):
    return f'<div class="sl">{esc(eyebrow or CUR[0])}</div><h2 class="sh">{esc(title)}</h2><p class="verdict">{esc(verdict)}</p>'
def insights(items):
    out = ""
    for i, (num, txt, src) in enumerate(items, 1):
        pend = " pend" if str(num) == "Pending" else ""
        out += f'<div class="ins{pend}"><span class="n">0{i}</span><b>{esc(num)}</b><p>{esc(txt)}</p><small>{esc(src)}</small></div>'
    return f'<div class="insrow">{out}</div>'
def reco(text=RECO_TBD): return f'<div class="reco"><span>Our recommendation</span> {esc(text)}</div>'
def pending(text): return f'<div class="ph small"><span class="tag">PENDING</span> {esc(text)}</div>'
def note(text): return f'<div class="note">{esc(text)}</div>'
def vis(title, inner, cls=""): return f'<div class="vis {cls}"><h4>{esc(title)}</h4>{inner}</div>'
def two(a, b): return f'<div class="two">{a}{b}</div>'
def axis(txt): return f'<div class="brow axis"><div></div><div class="ax"><span>0</span><span>{esc(txt)}</span></div><div></div></div>'
def bar(label, val, mx, txt, cls="", sub="", raw=False):
    w = 0 if not mx else max(0, min(100, 100*val/mx))
    l = label if raw else esc(label)
    return f'<div class="brow"><div class="bl">{l}<small>{esc(sub)}</small></div><div class="bt"><i class="{cls}" style="width:{w:.1f}%"></i></div><div class="bv">{esc(txt)}</div></div>'
def table(headers, rows, cls="tbl"):
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{b}</table>'
def line_svg(values, labels, color="#B8001C", w=560, h=150):
    mx, mn = max(values), 0
    n = len(values); px = lambda i: 10 + i*(w-20)/(n-1); py = lambda v: h-24 - (v-mn)/(mx-mn or 1)*(h-44)
    pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(values))
    area = f"{px(0):.1f},{h-24} {pts} {px(n-1):.1f},{h-24}"
    pk = values.index(mx)
    return (f'<svg viewBox="0 0 {w} {h}" class="line"><polygon points="{area}" fill="{color}" opacity=".10"/><polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<circle cx="{px(pk):.1f}" cy="{py(mx):.1f}" r="4" fill="{color}"/><text x="{px(pk):.1f}" y="{py(mx)-8:.1f}" font-size="10" text-anchor="middle" fill="#2c2c2c">peak {fmt(mx)} · {esc(labels[pk])}</text>'
            f'<text x="10" y="{h-6}" font-size="10" fill="#6b6b6b">{esc(labels[0])}</text><text x="{w-10}" y="{h-6}" font-size="10" text-anchor="end" fill="#6b6b6b">{esc(labels[-1])}</text></svg>')
def heat(ts):
    hr = "<tr><th></th>"+"".join(f"<th>{m}</th>" for m in MN)+"<th>Peak</th></tr>"; hb = ""
    for t in ts:
        cells = "".join(f'<td class="hm{" peak" if MN[k]==SEA[t]["peak"] else ""}" style="background:rgba(184,0,28,{max(0,min(1,(v-0.7)/0.8)):.2f});color:{"#fff" if (v-0.7)/0.8>.55 else "#2c2c2c"}">{v:.2f}</td>' for k, v in enumerate(SEA[t]["index"]))
        hb += f'<tr><th>{lab(t)}</th>{cells}<td><b>{SEA[t]["peak"]}</b></td></tr>'
    return f'<table class="heat">{hr}{hb}</table>'
def oikos_sov(t):
    o = SEO[t]["oikos"]; return (o["sov"], o["rank"]) if o else (0.0, 99)
def rank_txt(r): return "outside top 20" if r > 20 else f"#{r}"
def derived_sov(ts, name):
    tot = sum(SEO[t]["total_traffic"] for t in ts); tr = 0
    for t in ts:
        o = SEO[t]["oikos"] if name == "Oikos" else SEO[t]["competitors"][name]
        tr += o["traffic"] if o else 0
    return 100*tr/tot
def ai_stats(ts):
    n = sum(AI[t]["n"] for t in ts)
    w = lambda k: sum(AI[t][k]*AI[t]["n"] for t in ts)/n
    sent = [AI[t]["avg_sentiment"]*AI[t]["n"] for t in ts if AI[t]["avg_sentiment"] is not None]
    return dict(n=n, vis=w("avg_visibility"), sov=w("avg_sov"), zero=sum(AI[t]["zero"] for t in ts), sent=sum(sent)/n)
def mentions(ts):
    c = collections.Counter()
    for t in ts:
        for k, v in AI[t]["mentions"].items(): c[k.lower()] += v
    return c
def plist(prompts, limit=12):
    rows = ""
    for p in sorted(prompts, key=lambda p: ((p["visibility"] or 0), (p["sentiment"] if p["sentiment"] is not None else 0)))[:limit]:
        sent = "" if p["sentiment"] is None else f'{p["sentiment"]:+.0f}'
        rows += f'<tr><td>{esc(p["prompt"])}</td><td>{"branded" if p["branded"]=="yes" else "unbranded"}</td><td>{p["visibility"]:.0f}%</td><td>{sent}</td><td>{esc(p["mentions"])}</td></tr>'
    return f'<table class="tbl"><tr><th>Prompt</th><th>Type</th><th>Visibility</th><th>Net sentiment</th><th>Brands mentioned</th></tr>{rows}</table>'

# ---------- Part 0: context and method ----------
def cover(s):
    kp = [(fmt(d["keywords_unique"]), "unique keywords"), ("9 · 3", "topics · funnel stages"), (f'{TOTAL_VOL/1e6:.1f} M', "monthly searches (order of magnitude)"), ("111", "AI prompts tracked in SE Visible")]
    k = "".join(f'<div class="kpi"><b>{a}</b><span>{esc(b)}</span></div>' for a, b in kp)
    cards = "".join(f'<div class="cc"><span class="cn">{p["id"]+1:02d}</span><b>{esc(p["label"])}</b><p>{esc(p["phrase"]) if p["phrase"] else ""}</p></div>' for p in OUT_PARTS)
    return f'<div class="hero"><span class="badge">Holistic search study · USA · November 2026</span><h1>Oikos Pro · Demand, competition and AI visibility</h1><p class="sub">SEO and GEO analysis of the search demand around Oikos Pro: the brand, then three funnel stages (Discover, Evaluate, Buy), then recommendations.</p><div class="kpis">{k}</div><div class="sl" style="margin-top:18px">Agenda</div><h3 class="h3">Structure of the study</h3><div class="cgrid">{cards}</div></div>'

def context(s):
    ins = [(fmt(d["keywords_unique"]), "unique keywords analysed, brand and non-brand", "Master keyword listing"),
           (f'{TOTAL_VOL/1e6:.1f} M', "monthly searches across 9 topics (order of magnitude)", "Google Ads, USA"),
           ("3 stages", "Discover, Evaluate, Buy, with 9 topics inside", "Funnel model"),
           ("Pending", "social conversation and retail platforms", "Thomas")]
    bv = sum(v["brand"] for v in D["brand"]["stage"].values())
    rows = bar("Oikos-name searches", bv, TOTAL_VOL, f"{100*bv/TOTAL_VOL:.1f}% of demand", "brandbar") + bar("All other searches", TOTAL_VOL-bv, TOTAL_VOL, f"{100*(TOTAL_VOL-bv)/TOTAL_VOL:.1f}% of demand", "slate")
    q = ["How does Oikos Pro show up in AI answers (ChatGPT, Gemini, Perplexity, AI Overviews) and in Google?",
         "What do people say about taste, texture, a perceived recipe change, shrinkflation and price?",
         "Does Oikos Pro appear when people ask category questions, without naming the brand?"]
    ql = "".join(f"<li>{esc(x)}</li>" for x in q)
    return head("Context of the mandate", "Understand how Oikos Pro is found, seen and understood, with and without the brand name.") + insights(ins) + \
        two(vis("What the client wants to know", f'<ul class="lim">{ql}</ul>'+note("Oikos Pro is an ultra-filtered milk cultured dairy product with 20 g protein and 0 g added sugar. It is not tracked as a Greek yogurt. Scope: USA, English.")), vis("Demand: brand vs everything else", axis("share of total demand")+rows))

def method(s):
    steps = [("1","Keyword listing and classification",f'{fmt(d["keywords_total"])} keywords, 9 topics, 3 funnel stages'),("2","SEO matrix (SE Ranking)","Share of voice per topic, Google USA"),("3","AI matrix (SE Visible)","Prompts: 70% unbranded, 30% branded"),("4","Benchmark and recommendations","Competitors, SEO and GEO, priorities")]
    st = "".join(f'<div class="step"><i>{a}</i><b>{esc(b)}</b><p>{esc(c)}</p></div>' for a, b, c in steps)
    return head("Method in 4 steps", "The same mechanics as the other holistic studies, applied to the Oikos Pro keyword and prompt set.") + f'<div class="steps">{st}</div>' + \
        two(vis("SEO and GEO: two views of the same topics", "<p class='p'>SEO counts where Oikos ranks in Google (SE Ranking share of voice). GEO counts how often Oikos is mentioned in AI answers (SE Visible visibility, share of voice and sentiment). A topic can be won in one and lost in the other.</p>"),
            vis("Reading the slides", "<p class='p'>Each funnel stage is read the same way: demand and categories, trends, attribute view, SEO competitive environment, AI answer visibility. Blank boxes marked PENDING are data not yet available.</p>"))

def glossary(s):
    gl = [("Search volume","Average monthly Google searches, USA, last 48 months. Close variants and misspellings counted once."),("Share of voice","A domain's share of the estimated traffic in a topic's keyword set (SE Ranking). Not additive across topics."),("Visibility (AI)","Share of runs of a prompt in which Oikos is mentioned (SE Visible)."),("AI share of voice","Oikos's share of brand mentions in the AI answers to a prompt (SE Visible)."),("Net sentiment","SE Visible's sentiment score per prompt. Definition not given in the export."),("Branded / unbranded","Branded = the Oikos name or a misspelling. Unbranded = category searches and questions."),("Funnel","Discover (Moment, Recipe, Health), Evaluate (Ingredients, Testimonial), Buy (Product, Flavor, Packaging, Purchase).")]
    g = "".join(f'<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>' for a, b in gl)
    lim = ["SE Ranking exports are from 22 Nov 2026, from the old project (includes Triple Zero and ambiguous keywords). Re-export pending.","SE Visible: 111 prompts, one week, 7 to 30 prompts per topic. Indicative only.","Competitors shown are candidates. The 2 inspirational competitors are not chosen yet.","Competitor positions per keyword, AI cited sources, coverage and social data are not available yet.","Attribute tags are rule-based and not yet validated."]
    l = "".join(f"<li>{esc(x)}</li>" for x in lim)
    return head("Glossary and limits", "What the terms mean, and what the figures do not cover.") + two(vis("Glossary", f'<table class="tbl">{g}</table>'), vis("Known limits", f'<ul class="lim">{l}</ul>'))

def globaldata(s):
    ins = [(fmt(d["keywords_total"]), f'keywords listed ({fmt(d["keywords_unique"])} unique)', "Master"), (f'{TOTAL_VOL/1e6:.1f} M', "monthly search volume", "Google Ads, USA"), ("9 + 111", "SE Ranking topic exports · SE Visible prompts", "Stale · one week"), ("Pending", "social mentions, reach and sentiment", "Social listening (Thomas)")]
    rows = []
    for st, ts in STAGES.items():
        kw = sum(1 for t in d["topics"] if t["funnel"] == st); k = sum(t["keywords"] for t in d["topics"] if t["funnel"] == st)
        B = D["brand"]["stage"][st]; a = ai_stats(ts)
        rows.append([f"<b>{st}</b>", fmt(k), fmt(stage_vol[st]), f"{100*stage_vol[st]/TOTAL_VOL:.0f}%", f'{100*B["brand"]/(B["brand"]+B["non"]):.1f}%', str(a["n"]), f'{a["vis"]:.0f}%'])
    t = table(["Funnel stage","Keywords","Monthly volume","Share of demand","Oikos-name share","AI prompts","AI visibility"], rows)
    return head("Global data", "Overview of the corpus, all topics together.") + insights(ins) + vis("The study in numbers, by funnel stage", t) + note("Volumes are monthly averages, canonical keywords only (close variants counted once), brand-name searches included.")

# ---------- Part 1: brand ----------
def brand1(s):
    B = D["brand"]; bs = D["brand_split"]; bv = sum(bs.values())
    palette = ["#B8001C","#364457","#5A6B80","#7C8A9B","#B6BEC8","#D8DDE3"]
    seg = "".join(f'<i style="width:{100*v/bv:.1f}%;background:{palette[i%6]}" title="{esc(k)}"></i>' for i, (k, v) in enumerate(bs.items()))
    leg = "".join(f'<span class="lgd"><i style="background:{palette[i%6]}"></i>{esc(k)} {100*v/bv:.0f}% · {fmt(v)}</span>' for i, (k, v) in enumerate(bs.items()))
    spell = [x for x in B["top_branded"] if any(w in x["kw"] for w in ("oikos yogurt","okio yogurt","okios protein yogurt"))][:3]
    ins = [(fmt(bv), "monthly searches carry the Oikos name (brand and misspellings)", "Keyword listing"), (f"{100*bv/TOTAL_VOL:.1f}%", "of all demand in the study", "Keyword listing"),
           (f'{100*bs["Oikos (general)"]/bv:.0f}%', "of brand demand is the generic Oikos name, before any sub-brand", "Keyword listing"), ("Pending", "Google Ads clicks, impressions and CTR on the brand", "Google Ads (not exported)")]
    top = table(["Query","Volume / month"], [[esc(x["kw"]), fmt(x["vol"])] for x in B["top_branded"]])
    return head("The demand that carries the Oikos name", f"{fmt(bv)} searches a month name Oikos, {100*bv/TOTAL_VOL:.1f}% of all demand in the study.") + insights(ins) + \
        vis("Split of brand demand by sub-brand", f'<div class="stackb">{seg}</div><div class="legend">{leg}</div>') + \
        two(vis("Brand search volume trend (48 months)", line_svg(D["brand_trend"], D["trend_labels"], w=520, h=180)), vis("Top 10 Oikos-name queries", top)) + \
        note("Misspellings (okio, oiko, orkos) are counted as Oikos. Google merges close variants, so several spellings carry the same volume and are counted once. Sub-brand split is a keyword-text rule: Triple Zero, Fusion, Remix, shakes and drinks, Oikos Pro, otherwise generic.") + reco()

def brand2(s):
    B = D["brand"]["brands"]; comp = [b for b in B if not b["brand"].startswith("Oikos")]; oi = [b for b in B if b["brand"] == "Oikos"][0]["vol"]
    mx = max(b["vol"] for b in B); ctot = sum(b["vol"] for b in comp)
    rows = bar(logo("Oikos"), oi, mx, f"{fmt(oi)} / mo", "brandbar", raw=True) + "".join(bar(logo(b["brand"]), b["vol"], mx, f'{fmt(b["vol"])} / mo', "slate", raw=True) for b in comp[:9])
    top2 = (comp[0]["vol"]+comp[1]["vol"])/ctot
    ins = [(f'{comp[0]["brand"]}', f'is the largest competitor brand ({fmt(comp[0]["vol"])}/mo)', "Keyword listing brand tag"), (f"{100*top2:.0f}%", f'of competitor brand demand sits with {comp[0]["brand"]} and {comp[1]["brand"]}', "Brands listed here"),
           (f'{oi/comp[0]["vol"]:.1f}x', f'Oikos brand volume vs {comp[0]["brand"]}', "Keyword listing"), ("Pending", "Ads conquesting and who occupies the brand SERP", "Google Ads, SE Ranking")]
    return head("Oikos against competition on the brand", f"Oikos and {comp[0]['brand']} carry similar brand-name demand; the next competitor is about half the size.") + insights(ins) + \
        two(vis("Brand-name search volume", rows), vis("Not available yet", pending("Who occupies the demand for the Oikos name outside Oikos (SERP of brand queries).") + pending("Competitor advertising on Oikos brand queries (conquesting).") + pending("Competitor brand-name Google Ads clicks and impressions."))) + \
        note("Brands whose name is also an everyday word (Quest, Ghost, Slate, Ensure, Boost, Greek Gods, Ratio) are left out because their volume is not brand demand. Tags are rule-based and not yet validated.") + reco()

# ---------- Part 2: global vision ----------
def treemap(s):
    cols = ""
    for st, ts in STAGES.items():
        tt = sorted([x for x in d["topics"] if x["funnel"] == st], key=lambda x: -x["volume"])
        blocks = "".join(f'<div class="tm" style="flex:{x["volume"]}"><b>{esc(lab(x["topic"]))}</b><span>{fmt(x["volume"])} · {100*x["volume"]/TOTAL_VOL:.1f}%</span></div>' for x in tt)
        cols += f'<div class="tmcol" style="flex:{stage_vol[st]}"><h4>{st} · {100*stage_vol[st]/TOTAL_VOL:.0f}%</h4><div class="tmstack">{blocks}</div></div>'
    top = max(d["topics"], key=lambda x: x["volume"])
    ins = [(f"{100*stage_vol['Buy']/TOTAL_VOL:.0f}%", "of search demand sits in the Buy stage", "Keyword listing"), (f"{100*top['volume']/TOTAL_VOL:.0f}%", f"of all demand is the {top['topic']} topic", "Includes brand-name searches"), (f"{100*stage_vol['Discover']/TOTAL_VOL:.0f}%", "is Discover: Moment, Recipe, Health", "Keyword listing"), (f"{100*stage_vol['Evaluate']/TOTAL_VOL:.0f}%", "is Evaluate: Ingredients, Testimonial", "Keyword listing")]
    return head("Where the demand is, by funnel stage", f"Buy holds {100*stage_vol['Buy']/TOTAL_VOL:.0f}% of demand, Discover {100*stage_vol['Discover']/TOTAL_VOL:.0f}% and Evaluate {100*stage_vol['Evaluate']/TOTAL_VOL:.0f}%.") + insights(ins) + f'<div class="tmwrap">{cols}</div>' + \
        note("Average monthly search volume, USA, last 48 months. Close variants counted once. Volumes are orders of magnitude, not additive. Product includes brand-name searches such as \"oikos protein shake\".") + reco()

def stage_compare(s):
    comps = ["Chobani","fairlife","Premier Protein"]; names = ["Oikos"]+comps
    rows = []
    for st, ts in STAGES.items():
        a = ai_stats(ts)
        rows.append([f"<b>{st}</b>"] + [f"{derived_sov(ts, n):.1f}%" for n in names] + [f'{a["vis"]:.0f}%', f'{a["zero"]} of {a["n"]}'])
    hdr = ["Funnel stage"] + [logo(n) for n in names] + ["Oikos AI visibility","Prompts at zero"]
    best_seo = max(STAGES, key=lambda st: derived_sov(STAGES[st], "Oikos")); best_ai = max(STAGES, key=lambda st: ai_stats(STAGES[st])["vis"])
    ins = [(f"{derived_sov(STAGES[best_seo],'Oikos'):.1f}%", f"Oikos share of voice in {best_seo}, its best stage in Google", "Derived, stale"), (f"{ai_stats(STAGES[best_ai])['vis']:.0f}%", f"Oikos AI visibility in {best_ai}, its best stage in AI answers", "SE Visible"),
           (f"{D['ai_zero']} of {D['ai_total']}", "AI prompts with no Oikos mention", "SE Visible"), ("Pending", "SEO and AI winners per stage need the competitors and sources exports", "SE Visible, SE Ranking")]
    return head("SEO and AI by funnel stage", f"Oikos is strongest in Google in {best_seo} and in AI answers in {best_ai}.") + STALE + insights(ins) + \
        vis("Share of voice in Google (derived) and Oikos visibility in AI, by funnel stage", table(hdr, rows)) + \
        note("Stage share of voice is derived: summed traffic of the domain across the stage topics divided by summed topic traffic. A competitor outside a topic's top 20 counts as 0 there, so its figure is understated. Competitors are candidates, not chosen.") + reco()

# ---------- Parts 3-5: per funnel stage ----------
def demand_cat(s):
    st = s["stage"]; ts = STAGES[st]; sv = stage_vol[st]
    best = max(ts, key=lambda t: vol[t]); q = D["queen"][best]
    ins = [(fmt(sv), f"searches a month in {st}, {100*sv/TOTAL_VOL:.0f}% of all demand", "Keyword listing"), (q["kw"], f'is the leading non-brand query in {lab(best)} ({fmt(q["vol"])}/mo)', "Keyword listing"),
           (f"{100*vol[best]/sv:.0f}%", f"of {st} demand is {lab(best)}, the largest topic", "Keyword listing"), ("Pending", "social mentions and engagement (7 days)", "Social listening (Thomas)")]
    left = "".join(bar(lab(t), vol[t], sv, f"{100*vol[t]/sv:.0f}% of {st} · {fmt(vol[t])}/mo", "", f'leading query: {D["queen"][t]["kw"]}') for t in ts)
    sub = D["subcats"][st]; sm = sub[0]["vol"]
    right = "".join(bar(x["v"], x["vol"], sm, f'{fmt(x["vol"])}/mo', "slate") for x in sub)
    return head("Demand and categories", f"{fmt(sv)} searches a month, led by {lab(best)} ({100*vol[best]/sv:.0f}% of {st}).") + insights(ins) + \
        two(vis(f"Topics in {st}: share of the stage's demand", axis("100% of the stage") + left), vis("Top sub-categories, non-brand searches (relative to the largest)", right)) + \
        vis("Search vs social weight of the topics", pending("Social mentions and engagement (7 days) per topic, as in the Econofitness decks. Needs the social listening data from Thomas.")) + \
        note("Topic bars use a fixed scale (0 to 100% of the stage). Sub-categories come from the keyword listing and are rule-based; they exclude brand and competitor-brand searches.") + reco()

def trends(s):
    st = s["stage"]; ts = STAGES[st]; v = D["trend"][st]
    last, prev = sum(v[-12:]), sum(v[-24:-12]); chg = 100*(last/prev-1)
    peaks = {}
    for t in ts: peaks[SEA[t]["peak"]] = peaks.get(SEA[t]["peak"], 0)+1
    pkm = max(peaks, key=peaks.get)
    ins = [(f"{chg:+.1f}%", "change in total monthly volume, last 12 months vs the 12 before", "Google Ads, 48 months"), (fmt(sum(v[-12:])/12), "average monthly volume, last 12 months", "Google Ads"), (pkm, f"is the most common peak month across {st} topics", "Seasonality index"), (MN[min(range(12), key=lambda k: sum(SEA[t]["index"][k] for t in ts))], "is the lowest month for the stage", "Seasonality index")]
    return head("Trends", f"{st} demand is {'flat' if abs(chg)<1 else format(chg,'+.0f')+'%'} over the last year ({chg:+.1f}%) and peaks mostly in {pkm}.") + insights(ins) + \
        vis(f"Monthly search volume in {st} (sum of keywords, 48 months)", line_svg(v, D["trend_labels"], w=1060, h=190)) + \
        vis("Seasonality index by topic (1.00 = the topic's average month)", heat(ts)) + \
        note("Sum of monthly volumes of all canonical keywords in the stage; keywords with no volume in a month count as 0, so early months can be understated. Seasonality index = average of each calendar month across the years divided by the topic's monthly mean.") + reco()

def attrs(s):
    st = s["stage"]; sv = stage_vol[st]; ts = STAGES[st]
    blocks = ""
    for an, vals in D["attrs"][st].items():
        blocks += vis(an, "".join(bar(x["v"], x["vol"], sv, f'{100*x["vol"]/sv:.1f}% of {st} · {fmt(x["vol"])}/mo', "slate") for x in vals))
    first = list(D["attrs"][st].items())
    top = max(((an, x) for an, vs in first for x in vs), key=lambda p: p[1]["vol"])
    ins = [(top[1]["v"], f'is the largest attribute value in {st} ({top[0].lower()}, {100*top[1]["vol"]/sv:.0f}% of the stage)', "Rule-based tags")] + \
          [(first[i][1][0]["v"], f'leads {first[i][0].lower()} ({100*first[i][1][0]["vol"]/sv:.0f}% of the stage)', "Rule-based tags") for i in range(1,3)] + [("Pending", "coverage of each attribute (share of voice by attribute)", "Needs keyword-level positions")]
    return head("Attribute view", f"In {st}, {top[1]['v'].lower()} is the dominant attribute ({100*top[1]['vol']/sv:.0f}% of the stage).") + insights(ins) + \
        f'<div class="three">{blocks}</div>' + \
        note("Attributes are rule-based tags on the keyword listing, not yet validated. A keyword can carry several values, so shares do not add to 100%. Bars use the stage's total demand as 100%.") + reco()

def seo_env(s):
    st = s["stage"]; ts = STAGES[st]
    blocks = ""
    for t in ts:
        S = SEO[t]; sv, rk = oikos_sov(t); doms = S["domains"][:5]
        rows = "".join(bar(x["domain"].replace("www.", ""), x["sov"], 40, f'{x["sov"]:.1f}%', "brandbar" if "oikos.com" in x["domain"] else "slate") for x in doms)
        if not any("oikos.com" in x["domain"] for x in doms): rows += bar("oikos.com", sv, 40, f'{sv:.1f}% · {rank_txt(rk)}', "brandbar")
        blocks += vis(f"{lab(t)}: Oikos {rank_txt(rk)}, {sv:.1f}% share of voice, est. traffic {fmt(S['oikos_traffic_keywords'])}", rows)
    comps = ["Chobani","fairlife","Premier Protein"]
    ctab = table(["Topic", logo("Oikos")] + [logo(c) for c in comps], [[lab(t), f'{oikos_sov(t)[0]:.1f}%'] + [(f'{SEO[t]["competitors"][c]["sov"]:.1f}% (#{SEO[t]["competitors"][c]["rank"]})' if SEO[t]["competitors"][c] else "not in top 20") for c in comps] for t in ts])
    top5 = sum(1 for t in ts if oikos_sov(t)[1] <= 5); firsts = collections.Counter(SEO[t]["domains"][0]["domain"].replace("www.", "") for t in ts)
    ins = [(f"{derived_sov(ts,'Oikos'):.1f}%", f"Oikos share of voice across {st} (derived)", "Share of voice, stale"), (f"{top5} of {len(ts)}", "topics where Oikos is in the top 5 domains", "Share of voice, stale"), (firsts.most_common(1)[0][0], f"is the first domain in {firsts.most_common(1)[0][1]} of {len(ts)} {st} topics", "Share of voice, stale"), ("Pending", "fresh export and per-keyword competitor positions", "SE Ranking")]
    return head("SEO competitive environment", f"In {st}, Oikos is in the top 5 domains in {top5} of {len(ts)} topics.") + STALE + insights(ins) + \
        f'<div class="two">{blocks}</div>' + vis("Candidate competitors: share of voice and rank by topic", ctab) + \
        note("Share of voice is a domain's share of estimated traffic in the topic keyword set (top 20 domains shown by SE Ranking). Bars use a fixed 0 to 40% scale. Old project: includes Triple Zero and ambiguous keywords. Competitors are candidates.") + reco()

def ai_vis(s):
    st = s["stage"]; ts = STAGES[st]; a = ai_stats(ts); men = mentions(ts)
    rank = sorted(men.items(), key=lambda x: -x[1]); orank = [k for k, _ in rank].index("oikos pro")+1 if "oikos pro" in men else None
    rows = [[lab(t), str(AI[t]["n"]), str(AI[t]["branded"]), f'{AI[t]["avg_visibility"]:.0f}%', f'{AI[t]["avg_sov"]:.0f}%', "" if AI[t]["avg_sentiment"] is None else f'{AI[t]["avg_sentiment"]:+.0f}', f'{AI[t]["zero"]}'] for t in ts]
    tab = table(["Topic","Prompts","Branded","Visibility","AI share of voice","Net sentiment","At zero"], rows)
    mm = max(men.values()); mrows = "".join(bar(logo(k.title() if k != "oikos pro" else "Oikos Pro"), v, mm, f'in {v} of {a["n"]} prompts', "brandbar" if k == "oikos pro" else "slate", raw=True) if (k.title() in LOGOS or k == "oikos pro") else bar(k.title(), v, mm, f'in {v} of {a["n"]} prompts', "slate") for k, v in rank)
    low = [p for t in ts for p in AI[t]["prompts"] if (p["visibility"] or 0) == 0]
    ins = [(f"#{orank}" if orank else "n/a", f"Oikos Pro rank by mentions among tracked brands in {st} prompts", "SE Visible, tracked brands only"), (f'{a["vis"]:.0f}%', "average visibility", "SE Visible"), (f'{a["sov"]:.0f}%', "average AI share of voice", "SE Visible"), (f'{a["sent"]:+.0f}', "average net sentiment", "SE Visible")]
    extra = vis(f"Prompts with zero visibility ({len(low)})", plist(low, 10)) if st != "Buy" else vis("Price and shrinkflation prompts (Purchase)", plist(AI["Purchase"]["prompts"], 8))
    return head("Visibility in AI answers", f"Oikos is mentioned in {a['vis']:.0f}% of {st} prompt runs; {a['zero']} of {a['n']} prompts show no mention.") + ONEWK + insights(ins) + \
        two(vis("By topic", tab), vis("Brands mentioned (tracked brands only)", mrows + pending("Cited sources by domain: needs the SE Visible sources export."))) + extra + \
        note("One week of data and few prompts per topic: indicative only. Engine(s) not stated in the export. Top Mentions lists only the brands tracked in the project; Premier Protein is not tracked.") + reco()

def sentiment(s):
    P = AI["Testimonial"]["prompts"]; neg = [p for p in P if p["sentiment"] is not None and p["sentiment"] < 0]
    ins = [(f'{AI["Testimonial"]["avg_visibility"]:.0f}%', "average visibility in Testimonial prompts", "SE Visible"), (str(len(neg)), "Testimonial prompts with negative net sentiment: " + "; ".join(f'"{p["prompt"]}" ({p["sentiment"]:+.0f})' for p in neg[:2]), "SE Visible"), (str(AI["Testimonial"]["zero"]), "Testimonial prompts with zero visibility", "SE Visible"), ("Pending", "complaint themes (thin, grainy, sour, chalky)", "Needs AI answer text")]
    return head("Taste and texture in AI answers", "Sentiment scores exist per prompt; the complaint themes need the AI answer text.") + ONEWK + insights(ins) + vis("All 30 Testimonial prompts, lowest visibility first", plist(P, 30)) + pending("Complaint theme chart (thin, grainy, sour, chalky, recipe change): blank until answer text or sources are exported.") + reco()

# ---------- Part 6: recommendations ----------
def synthesis(s):
    rows = []
    for st, ts in STAGES.items():
        for t in ts:
            sv, rk = oikos_sov(t)
            rows.append([st, lab(t), f'{100*vol[t]/TOTAL_VOL:.1f}%', f'{sv:.1f}% · {rank_txt(rk)}', f'{AI[t]["avg_visibility"]:.0f}%', f'{AI[t]["zero"]}/{AI[t]["n"]}', '<span class="tbd">[P1 / P2 / P3]</span>'])
    top5 = sum(1 for t in TOPICS if oikos_sov(t)[1] <= 5)
    ins = [(f"{TOTAL_VOL/1e6:.1f} M", "monthly searches in the study", "Keyword listing"), (f"{top5} of 9", "topics where Oikos is in the top 5 domains in Google", "Share of voice, stale"), (f'{D["ai_zero"]} of {D["ai_total"]}', "AI prompts with no Oikos mention", "SE Visible"), ("Pending", "potential not captured, and the topics not to prioritize", "Matrix data")]
    return head("Synthesis and prioritization", "[Verdict to write once the slides are reviewed]") + insights(ins) + vis("All topics: demand, Google and AI", table(["Stage","Topic","Share of demand","Oikos share of voice (stale)","AI visibility","AI prompts at zero","Priority"], rows)) + note("The priority column is intentionally blank: no recommendations or priority rule written yet.") + reco()

def platform(s):
    dom = s["platform"]; rows = []; found = 0
    for t in TOPICS:
        m = [x for x in SEO[t]["domains"] if dom in x["domain"]]
        if m:
            found += 1; r = SEO[t]["domains"].index(m[0])+1; rows.append([lab(t), FUNNEL_OF[t], f'{m[0]["sov"]:.1f}%', f"#{r}"])
        else: rows.append([lab(t), FUNNEL_OF[t], "not in top 20", ""])
    ins = [(f"{found} of 9", f'topics where {s["label"]} is in the top 20 domains', "Share of voice, stale"), ("Pending", f'{s["label"]} social listening mentions, reach and sentiment', "Thomas"), ("Pending", "Oikos presence on the platform", "Thomas"), ("Pending", "verdict: target, watch or ignore", "To write")]
    return head(s["name"], f"{s['label']} is in the top 20 Google domains for {found} of 9 topics.") + STALE + insights(ins) + vis(f"{s['label']} share of voice in Google, by topic", table(["Topic","Funnel stage","Share of voice","Rank"], rows)) + pending(f"{s['label']} social listening mentions and Oikos presence, as in the Econofitness decks.") + reco()

def todo(s):
    return head(s["name"], "[Verdict sentence, 15 words max, written when the data arrives]") + insights([("[ ]", "[Insight, 12 words max]", "[source]")]*4) + f'<div class="ph"><span class="tag">BLANK · DATA PENDING</span><h4>Planned content</h4><p>{esc(s["visual"])}</p><h4>Needs</h4><p>{esc(s["needs"])}</p></div>' + reco()

TPL = dict(cover=cover, context=context, method=method, glossary=glossary, globaldata=globaldata, brand1=brand1, brand2=brand2, treemap=treemap, stage_compare=stage_compare,
           demand_cat=demand_cat, trends=trends, attrs=attrs, seo_env=seo_env, ai_vis=ai_vis, sentiment=sentiment, synthesis=synthesis, platform=platform, todo=todo)

def build(core_only, outname):
    global OUT_PARTS
    parts = []
    for p in outline["parts"]:
        sl = [s for s in p["slides"] if s["core"] or not core_only]
        if sl: parts.append({**p, "slides": sl})
    OUT_PARTS = parts; total = sum(len(p["slides"]) for p in parts); n = 0
    hp, pills = "", ""
    for pi, p in enumerate(parts):
        pills += f'<button class="pill" data-p="{pi}" title="{esc(p["label"])}">{pi:02d}</button>'
        subs = []
        CUR[0] = f'{pi:02d} · {p["label"]}'
        if p["phrase"]:
            subs.append((f"Part {pi:02d} · {p['label']}", f'<div class="divider"><div class="sl">Part {pi:02d}</div><h2>{esc(p["label"])}</h2><p>{esc(p["phrase"])}</p></div>'))
        for s in p["slides"]:
            n += 1; s["part"] = CUR[0]
            subs.append((f'Slide {n} of {total} · {s["name"]}', f'<div class="slide-in">{TPL[s["tpl"]](s)}</div>'))
        hp += f'<div class="part" data-p="{pi}"><div class="track">' + "".join(f'<section class="ss" data-name="{esc(nm)}">{b}</section>' for nm, b in subs) + '</div></div>'
    css = (root/"deck.css").read_text(); js = (root/"deck.js").read_text()
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(outline["title"])}</title><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet"><style>{css}</style></head><body>
<header class="top"><b>Digitad</b><i></i><span>Oikos Pro</span><em>Holistic Search Study</em><u>Confidential</u></header><nav class="prog">{pills}</nav><main>{hp}</main>
<footer class="foot"><button id="prevP">← Previous section</button><div class="dots" id="dots"></div><span id="lab"></span><button id="nextP">Next section →</button></footer>
<button class="arr l" id="prevS">‹</button><button class="arr r" id="nextS">›</button><script>{js}</script></body></html>'''
    (root/outname).write_text(page, encoding="utf-8"); print(outname, total, "slides", len(page)//1024, "KB")

OUT_PARTS = []
build(False, "Oikos_Megatron_Deck.html")
build(True, "Oikos_Megatron_Deck_20.html")
