# Oikos Megatron: where the project is (2026-11-25)

Holistic search study (SEO + GEO) for Oikos Pro, Danone North America, USA. Lead: Carla. With: Thomas Joachim.

## Goal
Understand how Oikos Pro appears in AI search and Google: how it is described (taste, texture, recipe change, shrinkflation, price), which answers surface for generic questions, and whether Oikos shows up unprompted.

## Source of truth
- `Masterlist_Oikos_Megatron_UPDATED.xlsx` is the base (built 2026-11-24).
- `Masterlist_Oikos_Megatron_MASTER.xlsx` is the working version (31 tabs, also on Drive).

## What is in the master
| Tab group | Content |
|---|---|
| Keywords Listing Updated | 5,838 keywords, 98 columns, CPC, seasonality, 48 monthly volumes, funnel/topic/brand type |
| Prompt Listing | 1,425 prompts: 854 unbranded, 571 branded. Load tier A1 = first 1,100 (70/30), A = ~1,220, B = branded kept, not loaded |
| Removed prompts / Branded retail (removed) | 256 competitor prompts and the retail-worded branded prompts |
| Prompt Review (AI search) | Advisory verdicts for every prompt (not applied, by decision) |
| CR and GA tabs (grey) | Classification review and gap analysis from 2026-11-24, historical |

Open item: Settings!B4 (CAD to USD rate) is empty, so USD CPC columns stay blank.

## Decisions
- Prompts are Brand or Unbranded only. No competitor prompts.
- 70/30 unbranded/branded in the load.
- Low-winnability, duplicate, leading and medical-framing prompts are kept on purpose.
- Branded prompts with retail wording were removed and replaced.
- Funnel: Discover (Moment, Recipe, Health), Evaluate (Ingredient, Testimonial), Buy (Product, Flavor, Packaging, Purchase).

## SE Ranking
- Google USA. 2,306 keyword slots.
- Re-setup files in `SE_Ranking_setup/`: all (2,306), 3 funnel files, 9 topic files.
- The Data API is blocked for billing, so only UI exports work.
- Share of voice exports for 9 topics are in `share_of_voice_exports/`. Overview: `Oikos_Pro_Share_of_Voice_Overview.xlsx`.
- Finding: about 99% of Oikos share of voice is brand search. Non-brand is near zero. Triple Zero pages hold 52 to 62% in several topics.

## Next steps (from the meeting)
| Step | Owner | Status |
|---|---|---|
| Refine prompt classification (brand vs unbranded) | Carla | Done |
| Add Buy/Discover/Evaluate to master and SE Ranking | Carla | Master done, SE Ranking files ready, needs loading |
| Export SE Visible and SE Ranking data | Carla | SE Ranking share of voice per topic done. SE Visible not done. Still needed: global and funnel share of voice, rank tracker export, competitor data |
| SEO/GEO prioritization matrix with two inspirational competitors | Carla | Not started. Candidates: Chobani, fairlife, Premier Protein |
| Presentation outline (send for review before the deck) | Carla | Not started |
| Social listening and retail data | Thomas | Pending |
| Writer role email | Thomas | Pending |

## Blockers
- SE Visible exports need the prompts loaded and run first.
- Competitor exports need the two competitors chosen.
- SE Ranking API billing.

## Reference
Previous studies (Econofitness, Nespresso, Télé-Québec, Tanguay) are in the Drive folder `1OW_ltyNhC7Jmp5Z6MbkzyYNGoD3MlkhZ`. The Télé-Québec brief describes the deck structure (about 58 pages). The new deck should be simpler: global vision, funnel stages, recommendations.
