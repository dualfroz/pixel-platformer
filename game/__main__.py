import argparse
import os
import sys


def main(argv):
    parser = argparse.ArgumentParser(prog="game")
    parser.add_argument("--screenshot")
    parser.add_argument("--frames", type=int, default=60)
    args = parser.parse_args(argv)

    if args.screenshot:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        from .render.app import runScreenshot

        runScreenshot(args.screenshot, args.frames)
    else:
        from .render.app import runPlay

        runPlay()


if __name__ == "__main__":
    main(sys.argv[1:])
