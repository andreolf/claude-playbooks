#!/usr/bin/env python3
# ============================================================================
# Claude Playbooks v2.0
# Turn messy inputs like diffs, contracts, and notes into consistent prompts
# ============================================================================

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

ROOT = Path(__file__).resolve().parent
PLAYBOOKS_DIR = ROOT / "playbooks"
PACKS_DIR = ROOT / "packs"
HOOKS_DIR = ROOT / "hooks"
OUT_DIR = ROOT / "out"

VAR_PATTERN = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")

# ============================================================================
# CORE UTILITIES (unchanged from v1)
# ============================================================================

def parse_vars(pairs):
    """Parse key=value pairs into dictionary."""
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
    """Execute a hook script if it exists."""
    if not path.exists():
        return
    if not os.access(path, os.X_OK):
        # try to run with bash anyway
        subprocess.run(["bash", str(path)], check=True, env=env)
        return
    subprocess.run([str(path)], check=True, env=env)

def render(template: str, vars_dict: dict) -> str:
    """Substitute {{variables}} in template with values from vars_dict."""
    def repl(m):
        key = m.group(1)
        return vars_dict.get(key, m.group(0))
    return VAR_PATTERN.sub(repl, template)

# ============================================================================
# PACK MANAGEMENT
# ============================================================================

def load_manifest(pack_name: str) -> dict:
    """Load and parse pack manifest.json."""
    manifest_path = PACKS_DIR / pack_name / "meta" / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Pack '{pack_name}' not found.\n"
            f"Expected manifest at: {manifest_path}\n"
            f"Available packs: {', '.join(discover_packs()) or 'none'}"
        )

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {manifest_path}: {e}")

def validate_manifest(manifest: dict, pack_name: str):
    """Validate pack manifest structure."""
    required_fields = ["name", "version", "playbooks"]
    for field in required_fields:
        if field not in manifest:
            raise ValueError(
                f"Pack '{pack_name}' manifest missing required field: {field}\n"
                f"Required fields: {', '.join(required_fields)}"
            )

    if not isinstance(manifest["playbooks"], list):
        raise ValueError(
            f"Pack '{pack_name}' manifest field 'playbooks' must be an array"
        )

    if manifest["name"] != pack_name:
        print(
            f"Warning: Pack directory name '{pack_name}' "
            f"doesn't match manifest name '{manifest['name']}'",
            file=sys.stderr
        )

def check_license(manifest: dict, pack_name: str):
    """Check if pack requires license and validate."""
    if not manifest.get("requires_license", False):
        return

    license_env = manifest.get("license_env", "PLAYBOOK_LICENSE_KEY")
    if not os.environ.get(license_env):
        license_url = manifest.get("license_url", "")
        print(f"\nError: Pack '{pack_name}' requires a license.", file=sys.stderr)
        print(f"Set environment variable: {license_env}", file=sys.stderr)
        if license_url:
            print(f"Get a license at: {license_url}", file=sys.stderr)
        print(f"\nExample: export {license_env}=\"your-license-key\"", file=sys.stderr)
        sys.exit(1)

def discover_packs() -> list:
    """Return list of available pack names."""
    if not PACKS_DIR.exists():
        return []
    return [p.name for p in PACKS_DIR.iterdir() if p.is_dir() and (p / "meta" / "manifest.json").exists()]

# ============================================================================
# PLAYBOOK LOADING
# ============================================================================

def load_playbook(name: str, pack: str = None) -> str:
    """Load playbook template from core or pack."""
    if pack:
        # Load from pack
        manifest = load_manifest(pack)
        validate_manifest(manifest, pack)
        check_license(manifest, pack)

        # Check if playbook is in manifest whitelist
        if name not in manifest["playbooks"]:
            raise FileNotFoundError(
                f"Playbook '{name}' not available in pack '{pack}'.\n"
                f"Available playbooks: {', '.join(manifest['playbooks'])}"
            )

        pb_path = PACKS_DIR / pack / "playbooks" / f"{name}.md"
    else:
        # Load from core
        pb_path = PLAYBOOKS_DIR / f"{name}.md"

    if not pb_path.exists():
        raise FileNotFoundError(f"Playbook not found: {pb_path}")

    return pb_path.read_text(encoding="utf-8")

def discover_playbooks(pack: str = None) -> list:
    """Discover available playbooks from core or pack."""
    if pack:
        # List playbooks from pack manifest
        manifest = load_manifest(pack)
        validate_manifest(manifest, pack)
        return manifest["playbooks"]
    else:
        # List core playbooks
        if not PLAYBOOKS_DIR.exists():
            return []
        return sorted([
            p.stem for p in PLAYBOOKS_DIR.glob("*.md")
        ])

# ============================================================================
# INPUT/OUTPUT UTILITIES
# ============================================================================

def read_stdin() -> str:
    """Read content from stdin if available."""
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""

def copy_to_clipboard(content: str) -> bool:
    """Copy content to system clipboard."""
    # Try pbcopy (macOS)
    try:
        subprocess.run(
            ["pbcopy"],
            input=content.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Try xclip (Linux)
    try:
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=content.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Try xsel (Linux)
    try:
        subprocess.run(
            ["xsel", "--clipboard", "--input"],
            input=content.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    print(
        "Warning: Could not copy to clipboard. "
        "Install pbcopy (macOS), xclip, or xsel (Linux).",
        file=sys.stderr
    )
    return False

# ============================================================================
# SUBCOMMAND IMPLEMENTATIONS
# ============================================================================

def cmd_run(args):
    """Execute playbook run subcommand."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Parse variables
    vars_dict = parse_vars(args.vars)

    # Handle input (stdin takes precedence over file)
    if args.stdin:
        stdin_content = read_stdin()
        if stdin_content:
            vars_dict["input"] = stdin_content
        elif not args.input:
            print("Warning: --stdin specified but no input on stdin", file=sys.stderr)

    if args.input and "input" not in vars_dict:
        input_path = Path(args.input).expanduser().resolve()
        vars_dict["input"] = input_path.read_text(encoding="utf-8")

    # Add standard vars
    vars_dict.setdefault("date", datetime.utcnow().strftime("%Y-%m-%d"))
    vars_dict.setdefault("time_utc", datetime.utcnow().strftime("%H:%M:%S"))

    # Prepare env for hooks
    env = os.environ.copy()
    env["PLAYBOOK_NAME"] = args.name
    if args.pack:
        env["PB_PACK"] = args.pack
    for k, v in vars_dict.items():
        env[f"PB_{k.upper()}"] = v

    # Run pre hook
    run_hook(HOOKS_DIR / "pre.sh", env)

    # Load and render template
    template = load_playbook(args.name, pack=args.pack)
    rendered = render(template, vars_dict)

    # Create timestamped output filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    pack_suffix = f"_{args.pack}" if args.pack else ""
    out_file = OUT_DIR / f"{timestamp}_{args.name}{pack_suffix}.prompt.txt"

    # Save output (unless --print-only)
    if not args.print_only:
        out_file.write_text(rendered, encoding="utf-8")

    # Run post hook (can read OUT_FILE)
    env["OUT_FILE"] = str(out_file)
    run_hook(HOOKS_DIR / "post.sh", env)

    # Copy to clipboard if requested
    if args.copy:
        if copy_to_clipboard(rendered):
            print("[Copied to clipboard]", file=sys.stderr)

    # Print to stdout
    print(rendered)

def cmd_list(args):
    """List available playbooks."""
    try:
        if args.pack:
            playbooks = discover_playbooks(pack=args.pack)
            print(f"Playbooks in pack '{args.pack}':")
        else:
            playbooks = discover_playbooks()
            print("Core playbooks:")

        if not playbooks:
            print("  (none)")
        else:
            for pb in playbooks:
                print(f"  {pb}")

        # Show available packs if listing core
        if not args.pack:
            packs = discover_packs()
            if packs:
                print(f"\nAvailable packs: {', '.join(packs)}")
                print("Use: playbook list --pack <name>")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_init(args):
    """Initialize new playbook or pack."""
    target_path = Path(args.path).resolve()

    if args.with_pack:
        # Create pack structure
        pack_name = args.with_pack
        pack_dir = PACKS_DIR / pack_name

        if pack_dir.exists():
            print(f"Error: Pack directory already exists: {pack_dir}", file=sys.stderr)
            sys.exit(1)

        # Create directories
        (pack_dir / "meta").mkdir(parents=True, exist_ok=True)
        (pack_dir / "playbooks").mkdir(parents=True, exist_ok=True)

        # Create manifest
        manifest = {
            "name": pack_name,
            "version": "1.0.0",
            "description": "Custom playbook pack",
            "playbooks": ["example"],
            "requires_license": False,
            "license_env": "PLAYBOOK_LICENSE_KEY"
        }
        manifest_path = pack_dir / "meta" / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        # Create example playbook
        example_pb = pack_dir / "playbooks" / "example.md"
        example_pb.write_text("""SYSTEM
You are an AI assistant. You are helpful and concise.

CONTEXT
Task: {{task}}
Context: {{context}}
Date: {{date}} (UTC {{time_utc}})

INPUT
{{input}}

TASK
Complete the task described in the context.

RULES
- If information is missing or unknown, state "Unknown" explicitly
- State all assumptions clearly
- Be deterministic: same input should produce consistent output structure

OUTPUT SCHEMA
1) Task understanding

2) Approach

3) Output
""")

        print(f"Created pack: {pack_dir}")
        print(f"  {manifest_path}")
        print(f"  {example_pb}")
        print(f"\nNext steps:")
        print(f"  1. Edit {manifest_path}")
        print(f"  2. Add playbooks to {pack_dir / 'playbooks'}/")
        print(f"  3. Update manifest 'playbooks' array with playbook names")
        print(f"  4. Test: playbook run example --pack {pack_name} --vars task=\"test\"")

    else:
        # Create single playbook
        if target_path.exists():
            print(f"Error: File already exists: {target_path}", file=sys.stderr)
            sys.exit(1)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("""SYSTEM
You are an AI assistant. You are helpful, practical, and specific.

CONTEXT
Project: {{project}}
Goal: {{goal}}
Date: {{date}} (UTC {{time_utc}})

INPUT
{{input}}

TASK
[Describe what needs to be done]

RULES
- If information is missing or unknown, state "Unknown" explicitly
- State all assumptions clearly in the Assumptions section
- Do not fabricate or hallucinate facts
- Be deterministic: same input should produce consistent output structure

OUTPUT SCHEMA
1) Clarifying questions (only if needed)
- Q1:
- Q2:
- Q3:

2) Assumptions

3) Analysis

4) Recommendations
""")

        print(f"Created playbook: {target_path}")
        print(f"\nNext steps:")
        print(f"  1. Edit the template")
        print(f"  2. Test: playbook run {target_path.stem} --vars project=\"test\" --vars goal=\"test\"")

# ============================================================================
# ARGUMENT PARSER SETUP
# ============================================================================

def setup_parser() -> argparse.ArgumentParser:
    """Configure argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="playbook",
        description="Turn messy inputs into consistent, reusable Claude prompts"
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Available commands")

    # playbook run
    run_parser = subparsers.add_parser(
        "run",
        help="Execute a playbook"
    )
    run_parser.add_argument("name", help="Playbook name (without .md extension)")
    run_parser.add_argument("--input", help="File to inject as {{input}}")
    run_parser.add_argument("--stdin", action="store_true", help="Read from stdin as {{input}}")
    run_parser.add_argument("--vars", action="append", default=[], help="Variables as key=value (repeatable)")
    run_parser.add_argument("--pack", help="Load playbook from pack")
    run_parser.add_argument("--print-only", action="store_true", help="Print only, don't save")
    run_parser.add_argument("--copy", action="store_true", help="Copy output to clipboard")

    # playbook list
    list_parser = subparsers.add_parser(
        "list",
        help="List available playbooks"
    )
    list_parser.add_argument("--pack", help="List playbooks in specific pack")

    # playbook init
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize new playbook or pack"
    )
    init_parser.add_argument("path", help="Path for new playbook file")
    init_parser.add_argument("--with-pack", help="Create pack structure instead", metavar="NAME")

    return parser

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main CLI entry point with legacy support."""
    # Check for legacy syntax (no subcommand)
    if len(sys.argv) > 1 and sys.argv[1] not in ["run", "list", "init", "--help", "-h"]:
        # Legacy syntax detected
        print(
            f"Warning: Legacy syntax deprecated. Use: playbook run {sys.argv[1]} [options]",
            file=sys.stderr
        )
        print(
            "See: playbook run --help",
            file=sys.stderr
        )
        print(file=sys.stderr)
        # Convert to new syntax
        sys.argv.insert(1, "run")

    # Parse arguments
    parser = setup_parser()

    # Show help if no subcommand
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Route to subcommand
    try:
        if args.subcommand == "run":
            cmd_run(args)
        elif args.subcommand == "list":
            cmd_list(args)
        elif args.subcommand == "init":
            cmd_init(args)
        else:
            parser.print_help()
            sys.exit(1)

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
