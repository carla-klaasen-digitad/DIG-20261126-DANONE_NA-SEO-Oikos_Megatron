"""Builds Oikos_Megatron_Deck.html from data/outline.json and data/slides_1_3_data.json.
Only slides 1-3 carry data. Every other slide is a labelled skeleton."""
import json, html, sys
from pathlib import Path

root = Path(__file__).parent
outline = json.loads((root / "data/outline.json").read_text())
d = json.loads((root / "data/slides_1_3_data.json").read_text())
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

parts_html, pills = "", ""
for p in outline["parts"]:
    pills += f'<button class="pill" data-p="{p["id"]}" title="{esc(p["label"])}">{p["id"]:02d}</button>'
    subs = []
    if p["phrase"]:
        subs.append(("Introduction", f'<div class="divider"><div class="sl">Part {p["id"]:02d}</div><h2>{esc(p["label"])}</h2><p>{esc(p["phrase"])}</p></div>'))
    for s in p["slides"]:
        s["part"] = f'{p["id"]:02d} · {p["label"]}'
        body = {"cover": cover, "method": method, "treemap": treemap}.get(s["tpl"], lambda: todo(s))()
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
