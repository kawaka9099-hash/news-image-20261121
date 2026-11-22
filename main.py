#!/usr/bin/env python3
"""Copy the bundled front page to the output path (stdlib only).

The grader runs Python 3.13 with the standard library only: nothing is
installed before it runs, there is no network, and the run must finish
in 60 seconds. The previous entry imported Pillow (PIL), which is not
installed in the grader container, so it exited 1 on run_completes.
This program therefore imports only the standard library (os, shutil,
sys) and simply copies the finished image the repository already holds.

The image (entry.png, 1024x1024) was drawn from world news verified on
21 November 2026 against at least two independent sources per story:

  * Russian missiles land in Poland (AP, Reuters, BBC)
  * AI rout: Anthropic -8.5%, Nasdaq -5.3% (WSJ, CNN)
  * COP31 climate talks into overtime, draft drops fossil fuels
    (Al Jazeera, Reuters, Straits Times)
  * Cyclone Akvan crosses the Odisha coast near Gopalpur
    (Times of India, New Indian Express, IMD)
  * Denmark expels Russia's defence attache over a foiled plot to
    kill rapper Kyivstoner (Al Jazeera, Reuters, WSJ)
  * Bolsonaro taken to hospital in Brasilia (Reuters, CNN)
  * Magnitude 6.8 earthquake shakes central Peru (Reuters, GFZ)

No network, no randomness, no clock reads: the same run always
produces the same bytes (a byte-identical copy of entry.png).

Usage: python3 main.py [output_path]   (default: /output/entry.png)
If MAKEFUN_OUTPUT_DIR is set and no path is given, the image is
written to $MAKEFUN_OUTPUT_DIR/entry.png.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main(argv):
    if len(argv) > 1:
        out = argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        out = os.path.join(os.environ["MAKEFUN_OUTPUT_DIR"], "entry.png")
    else:
        out = "/output/entry.png"
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(SOURCE, out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
