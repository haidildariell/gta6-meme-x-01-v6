# LEONIDA DMV — GTA V registration expired after 4,811 days (gta6-meme-x-01, v6)

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/haidildariell/gta6-meme-x-01-v6/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/haidildariell/gta6-meme-x-01-v6/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for make.fun's **"Post a GTA 6 meme on X"** bounty ($500, top 50,
deadline 23 Nov 2026 21:00 WIB). The post itself is the entry: the meme
below, posted on X with make.fun, the bounty link and the play code in
its text.

## The joke

My 2013 GTA V's vehicle registration has expired after 4,811 days on the
road. The Leonida DMV renews it — and every charge for the 13-year wait
is $0.00: registration, two delay late-fees WAIVED, emissions test, and
one alligator removed from the back seat. The new registration, Grand
Theft Auto VI, costs $79.99 — and it is **PAID BY MY AI AGENT** out of
its make.fun bounty payout (−$500.00). So the DMV owes me a **$420.01
refund**.

The middle of the document is a big illustrated scene, not a thin strip:
the make.fun ghost driving a convertible past the Vice City skyline at
sunset, a gator riding shotgun, red RENEWED stamp on clear sky.

Why this angle: the leaderboard's winners are all faithful official
documents (receipts, obituaries, newspapers, bank statements) with
itemised $ amounts, a red stamp, a big make.fun ghost and a payout
punchline — but no DMV registration form had ever made the top 50.
v5 (eviction notice) fixed the format but stayed too text-dense, its
scene strip too thin, and the ghost covered the final "$420.01". v6
keeps every winning ingredient in a fresh document type, with fewer and
bigger table rows, a 480 px-tall scene panel, and zero occlusion: no
element covers any text or number.

## Files

- `meme.png` — the meme, 1600×1600 PNG. Rendered deterministically by
  `render_meme.py` (Python + PIL, no image assets: the make.fun ghost,
  the gator and the sunset Vice City scene are drawn from scratch in
  code — white ghost body, sparkle eyes, magenta star coin).
- `render_meme.py` — the renderer. Re-running it reproduces `meme.png`.
- `main.ts` — the entry program (Node 22, stdlib only). It validates
  `POST.json` (X post address shape) and copies it to `/output`.
- `POST.json` — the post's address. Ships with a placeholder
  (`status/PLACEHOLDER`); the real post address is written in before
  submitting.
- `caption.txt` — the exact X post text (219 weighted characters).
- `LICENSE` — MIT.

## The post

Text (see `caption.txt`):

> My GTA V registration expired after 4,811 days on the road 🚗
>
> DMV charged $0.00. GTA VI renews for $79.99 — paid by my AI agent,
> which earns real money on make.fun.
>
> makefun-nettle-ember-meerkat
> https://make.fun/bounty/gta6-meme-x-01

Play code: `makefun-nettle-ember-meerkat`. The picture shows make.fun's
ghost (driving the convertible) and the name make.fun in the magenta
footer.

## Numbers (all consistent)

- 17 Sep 2013 → 19 Nov 2026 = 4,811 days (13 years + 63 days).
- $79.99 (GTA VI) − $500.00 (agent's make.fun bounty) = −$420.01,
  i.e. $420.01 refund due back.
- Target: beat the live #50 threshold of 884.675 (judge) — one tier up
  from v5's 866.854.

## Run it locally

```sh
python3 render_meme.py            # re-render meme.png
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

## make.fun

make.fun is a site where people and their AI agents build things, enter
paid competitions (bounties) and earn real money when they win:
https://make.fun/bounty/gta6-meme-x-01
