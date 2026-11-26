# Deck checklist (2026-11-26): 20-slide version matching the example decks

Structure follows the example decks (Econofitness, Nespresso, Tanguay, Télé-Québec): context and method, brand, one block per category (here: per funnel stage, per the 24-25 Nov meeting), then recommendations.
Meeting notes: fewer slides; global vision, funnel stages, recommendations; SEO and GEO benchmark with 2 inspirational competitors; prioritization matrix; social listening and retail from Thomas.

Status: BUILT = filled with current data. PARTIAL = built with a blank part. BLANK = skeleton only.
Stale: SE Ranking exports of 22 Nov 2026, old project. SE Visible: 111 prompts, 20-26 Nov, one week.
No recommendations, priority levels or matrix logic are written. Recommendation boxes are placeholders.

| # | Part | Slide | Status | Data used | What is blank |
|---|---|---|---|---|---|
| 1 | 0 Context | Cover, mandate and agenda | BUILT | Master | |
| 2 | 0 Context | Method, glossary and limits | BUILT | Master | |
| 3 | 1 Global vision | Where the demand is | BUILT | Master volumes | Recommendation |
| 4 | 1 Global vision | Oikos against competitors in Google | BUILT (stale) | Share of voice: Oikos, Chobani, fairlife, Premier Protein | Recommendation. Competitors are candidates. |
| 5 | 1 Global vision | The demand that carries the Oikos name (brand) | BUILT (stale part) | Master brand tags, SE Ranking keywords | Recommendation |
| 6 | 1 Global vision | Who answers in AI instead of Oikos | PARTIAL | SE Visible prompts (branded toggle) | Cited sources, competitors export |
| 7 | 2 Discover | Demand, trends and attributes | BUILT | Master (volumes, seasonality, rule-based tags) | Recommendation |
| 8 | 2 Discover | SEO competitive environment | PARTIAL (stale) | Share of voice, top 3 domains per topic | 2 competitors not chosen; no per-keyword positions |
| 9 | 2 Discover | Visibility in AI answers | PARTIAL | SE Visible | Sources, prompts to target |
| 10 | 3 Evaluate | Demand, trends and attributes | BUILT | Master | Recommendation |
| 11 | 3 Evaluate | SEO competitive environment | PARTIAL (stale) | Share of voice | Same as 8 |
| 12 | 3 Evaluate | Taste and texture in AI answers | PARTIAL | SE Visible net sentiment | Complaint themes (need AI answer text) |
| 13 | 3 Evaluate | Visibility in AI answers | PARTIAL | SE Visible | Same as 9 |
| 14 | 4 Buy | Demand, trends and attributes | BUILT | Master | Recommendation |
| 15 | 4 Buy | SEO competitive environment | PARTIAL (stale) | Share of voice | Same as 8 |
| 16 | 4 Buy | Visibility in AI answers, price and shrinkflation | PARTIAL | SE Visible (Purchase prompts) | Sources |
| 17 | 5 Recommendations | Social signals and retail platforms | BLANK | | Thomas's data |
| 18 | 5 Recommendations | Synthesis and prioritization | PARTIAL | Figures from slides 3 to 16 | Verdicts, P1/P2/P3 |
| 19 | 5 Recommendations | SEO and GEO prioritization matrix | BLANK | | Source of baseline matrix data not confirmed; 2 competitors not chosen |
| 20 | 5 Recommendations | Next steps and production plan | BLANK | | Recommendations, writer role email |

## Left out of the 20 (examples have them)
- Content salience (entity salience per page): needs a page-level NLP analysis, no data.
- Positioning matrix by sub-category (Tanguay): needs the matrix data source.
- Per-category slides for each of the 9 topics: merged into 3 funnel stages to keep 20 slides.
- Standalone seasonality slide (Télé-Québec only): folded into the stage demand slides.

## Still needed
- How the baseline matrix (Oikos US Matrice de prio) data was produced; then the matching export.
- The 2 inspirational competitors.
- SE Visible competitors and sources exports; engine(s); answer text for sentiment themes.
- Fresh SE Ranking exports after the project rebuild (topic, Global, funnel).
- Thomas: social listening and retail data.

## Findings worth checking
- The master labels brand misspellings (okies, orkos, ikos yogurt) as Non-branded: about 45,600 of Oikos Product traffic. The deck classifies them as branded with a token-similarity rule (build_data.py, isbrand).
- Brand tags for Quest, Ghost, Slate, Ensure, Boost, Greek Gods and Ratio carry volume from the everyday words, so they are excluded from the brand chart.
