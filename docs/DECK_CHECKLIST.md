# Deck checklist (2026-11-26): rebuilt from the structure of the example decks

Two versions are generated from the same outline (`deck/data/outline.json`, flag `core`):
- `Oikos_Megatron_Deck.html`: 35 slides, full structure.
- `Oikos_Megatron_Deck_20.html`: the 20 core slides (marked CORE below).

Structure (from `deck_analysis/DECK_ANALYSIS.md`): context and method, brand, global vision, then one block per funnel stage (the stage plays the role of the example decks' topic; the Oikos topics are the categories inside it), then recommendations. Funnel breakdown per the 24-25 Nov meeting.
Status: BUILT = filled with current data. PARTIAL = built with a PENDING box. BLANK = skeleton only. STALE = SE Ranking 22 Nov, old project. SE Visible = 111 prompts, one week.
No recommendations, priorities or matrix logic are written; recommendation boxes are placeholders.

| # | Part | Slide | CORE | Status | Pending in it |
|---|---|---|---|---|---|
| 1 | 0 Context | Cover and agenda | x | BUILT | |
| 2 | 0 Context | Context of the mandate | x | PARTIAL | Social and retail |
| 3 | 0 Context | Method in 4 steps | x | BUILT | |
| 4 | 0 Context | Glossary and limits | | BUILT | |
| 5 | 0 Context | Global data | | PARTIAL | Social mentions, reach, sentiment |
| 6 | 1 Brand | The demand that carries the Oikos name | x | PARTIAL | Google Ads clicks, impressions, CTR |
| 7 | 1 Brand | Oikos against competition on the brand | x | PARTIAL | Conquesting Ads, brand SERP |
| 8 | 2 Global | Where the demand is, by funnel stage | x | BUILT | |
| 9 | 2 Global | SEO and AI by funnel stage | x | PARTIAL (stale) | Sources and competitor exports |
| 10 | 3 Discover | Demand and categories | x | PARTIAL | Social mentions and engagement |
| 11 | 3 Discover | Trends | | BUILT | |
| 12 | 3 Discover | Attribute view | | PARTIAL | Coverage per attribute |
| 13 | 3 Discover | SEO competitive environment | x | PARTIAL (stale) | Fresh export, keyword positions |
| 14 | 3 Discover | Visibility in AI answers | x | PARTIAL | Cited sources |
| 15-20 | 4 Evaluate | Same 4 slides, plus taste and texture in AI answers (19) | 15, 18, 19, 20 | PARTIAL | Complaint themes need AI answer text |
| 21-26 | 5 Buy | Same 5 slides, plus retail platform demand (26, BLANK) | 21, 24, 25 | PARTIAL | Retail data (Thomas) |
| 27 | 6 Recs | Synthesis and prioritization | x | PARTIAL | Priority, uncaptured potential |
| 28 | 6 Recs | Content salience | | BLANK | Page analysis |
| 29-31 | 6 Recs | YouTube, Reddit, Meta | | PARTIAL (stale) | Social listening mentions (Thomas) |
| 32 | 6 Recs | Media sites | | BLANK | Thomas; typing of domains |
| 33 | 6 Recs | SEO and GEO prioritization matrix | x | BLANK | Data source of baseline matrix not confirmed |
| 34 | 6 Recs | Conclusion and growth perspectives | | BLANK | |
| 35 | 6 Recs | Next steps and production plan | x | BLANK | Recommendations, writer role email |

## Still needed
- How the baseline matrix (Oikos US Matrice de prio) data was produced; then the matching export.
- The 2 inspirational competitors.
- SE Visible competitors and sources exports; engine(s); answer text for sentiment themes.
- Fresh SE Ranking exports after the project rebuild (topic, Global, funnel).
- Thomas: social listening and retail data. Google Ads brand clicks, impressions and CTR if wanted.

## Findings worth checking
- The master labels brand misspellings (okies, orkos, ikos yogurt) as Non-branded: about 45,600 of Oikos Product traffic. The deck classifies them as branded with a token rule (build_data.py, isbrand).
- Brand tags for Quest, Ghost, Slate, Ensure, Boost, Greek Gods and Ratio carry volume from the everyday words, so they are excluded from brand charts and from the "leading query" per topic.
- Premier Protein is not a tracked brand in SE Visible, so it does not appear in the AI brand mentions.
