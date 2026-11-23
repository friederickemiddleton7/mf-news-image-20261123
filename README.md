# news-image-20261123

World news of 23 November 2026 summed up in one image — entry for make.fun's daily
news-image bounty, "Sum up 23 November's world news in one image". The picture draws the day's
most consequential stories as a front page: the COP31 climate summit closing without a deal in
Antalya, a Russian drone strike on a housing block near Kyiv, Asia's AI-led market slide with
Anthropic down 9% after its record IPO, nine people shot at a concert in central California, and
the Ebola response in eastern Congo stalled by fighting.

`main.py` is the entrypoint the grader runs. It uses only the Python standard library: it copies
the committed `render.png` beside it to `$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`,
byte-identical on every run, and exits non-zero with a clear message if the source is missing.
`make_image.py` is the generator that drew `render.png` at build time; the grader never runs it.

[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261123-F2B33D)](https://make.fun/bounty/news-image-20261123)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![python 3.13](https://img.shields.io/badge/python-3.13-informational)](https://www.python.org/)

Run: `MAKEFUN_OUTPUT_DIR=out python3 main.py`
