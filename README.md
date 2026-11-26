# Oikos Megatron: holistic search study (Oikos Pro, Danone North America, USA)

Holistic SEO + GEO (AI search) study for Oikos Pro. Lead: Carla Klaasen. With: Thomas Joachim.

## Masterlist (source of truth)
Google Sheet: https://docs.google.com/spreadsheets/d/1TrsKv4d0MN-JC99i5qtNsW1Wj8DjR8W5MTOJ5i008AE/edit?usp=sharing
(keywords, prompts, Settings). The workbook itself is not stored in this repo.

## Contents
| Folder | What it is |
|---|---|
| share_of_voice_exports_STALE/ | SE Ranking share of voice exports per topic (3 files each), exported 2026-11-22 from the OLD project. Files are prefixed STALE_: re-export after the SE Ranking project is rebuilt. |
| deck/ | Deck generator: data/outline.json + deck.css + deck.js -> `python3 build_deck.py` -> Oikos_Megatron_Deck_20.html (core slides; the 35-slide version is built locally and not tracked) |
| docs/ | Project status and the share of voice overview workbook (stale). |

## How to use
1. Open `deck/Oikos_Megatron_Deck_20.html` in Chrome or Safari (arrow keys, F for full screen).
2. Edit `deck/data/outline.json` or the data files, then run `python3 build_deck.py` from the `deck/` folder.
3. Share HTML with colleagues or the client through DigiShare (`/digitad.share`), never Netlify Drop or a personal link.

## Export naming
`STALE_<original SE Ranking file name>` = old data. New exports drop the prefix and go in `share_of_voice_exports/`.
