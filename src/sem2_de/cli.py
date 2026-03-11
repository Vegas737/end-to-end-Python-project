from __future__ import annotations
import argparse
from pathlib import Path
from sem2_de.config import load_config

def cmd_extract(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    print(f"variant={cfg.variant_id} source_type={cfg.source_type}")
    print("TODO: реализуйте извлечение данных")
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sem2_de")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_ex = sub.add_parser("extract", help="Extract data from API")
    p_ex.add_argument("--config", required=True, help="Path to variant_XX.yml")
    p_ex.set_defaults(func=cmd_extract)

    return p

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
