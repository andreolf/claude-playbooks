#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAYBOOKS_DIR = ROOT / "playbooks"
HOOKS_DIR = ROOT / "hooks"
OUT_DIR = ROOT / "out"

VAR_PATTERN = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")

def parse_vars(pairs):
    vars_dict = {}
    for p in pairs or []:
        if "=" not in p:
            raise ValueError(f"Invalid --vars entry: {p}. Use key=value")
        k, v = p.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise ValueError(f"Invalid --vars entry: {p}. Key is empty")
        vars_dict[k] = v
    return vars_dict

def run_hook(path: Path, env: dict):
    if not path.exists():
        return
    if not os.access(path, os.X_OK):
        # try to run with bash anyway
        subprocess.run(["bash", str(path)], check=True, env=env)
        return
    subprocess.run([str(path)], check=True, env=env)

def load_playbook(name: str) -> str:
    pb_path = PLAYBOOKS_DIR / f"{name}.md"
    if not pb_path.exists():
        raise FileNotFoundError(f"Playbook not found: {pb_path}")
    return pb_path.read_text(encoding="utf-8")

def render(template: str, vars_dict: dict) -> str:
    def repl(m):
        key = m.group(1)
        return vars_dict.get(key, m.group(0))
    return VAR_PATTERN.sub(repl, template)

def main():
    parser = argparse.ArgumentParser(prog="playbook", description="Generate Claude playbook prompts")
    parser.add_argument("name", help="Playbook name (file in ./playbooks without .md)")
    parser.add_argument("--input", help="Optional input file to inject as {{input}}")
    parser.add_argument("--vars", action="append", help="Variables key=value. Repeatable.", default=[])
    parser.add_argument("--print-only", action="store_true", help="Do not save to out/")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    vars_dict = parse_vars(args.vars)

    if args.input:
        input_path = Path(args.input).expanduser().resolve()
        vars_dict["input"] = input_path.read_text(encoding="utf-8")

    # Add standard vars
    vars_dict.setdefault("date", datetime.utcnow().strftime("%Y-%m-%d"))
    vars_dict.setdefault("time_utc", datetime.utcnow().strftime("%H:%M:%S"))

    # Prepare env for hooks
    env = os.environ.copy()
    env["PLAYBOOK_NAME"] = args.name
    for k, v in vars_dict.items():
        env[f"PB_{k.upper()}"] = v

    # Run pre hook
    run_hook(HOOKS_DIR / "pre.sh", env)

    template = load_playbook(args.name)
    rendered = render(template, vars_dict)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_file = OUT_DIR / f"{timestamp}_{args.name}.prompt.txt"

    if not args.print_only:
        out_file.write_text(rendered, encoding="utf-8")

    # Run post hook (can read OUT_FILE)
    env["OUT_FILE"] = str(out_file)
    run_hook(HOOKS_DIR / "post.sh", env)

    print(rendered)

if __name__ == "__main__":
    main()
