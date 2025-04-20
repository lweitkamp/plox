from .plox import Plox


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", type=Path)
    args = parser.parse_args()

    plox = Plox()

    if args.file:
        plox.run_file(args.file)
    else:
        plox.run_prompt()