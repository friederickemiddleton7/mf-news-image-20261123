# World News — 23 November 2026

This repository contains a single 1024×1024 PNG poster that sums up the world news of **23 November 2026**. The image names that day prominently and presents the day's most consequential stories across regions and fields — the COP31 climate summit ending without a deal, the drone attack near Kyiv, Asia's stock slide on AI fears, the California concert shooting, and the stalled Ebola response in Congo — with short labels and clean pictograms so a viewer who missed the day can tell what happened.

`main.py` is the standard-library-only entrypoint: it copies the committed `render.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`) byte-identically, verifying the PNG signature and 1 MiB size cap. `make_image.py` drew `render.png` at build time using Pillow and is never run by the grader.

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/friederickemiddleton7/mf-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/friederickemiddleton7/mf-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

[![license: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Run: `MAKEFUN_OUTPUT_DIR=out python3 main.py`

Bounty page: https://make.fun/bounty/news-image-20261123
