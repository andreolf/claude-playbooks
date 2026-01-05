# Claude Playbooks

**Turn messy inputs like diffs, contracts, and notes into consistent, reusable prompts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

> Production-grade CLI for generating structured Claude prompts from templates. Zero dependencies, infinite extensibility.

## Why Claude Playbooks?

You keep writing similar prompts for audits, PR reviews, and content creation. Each time you:
- Reconstruct the structure from memory
- Copy-paste from old prompts
- Forget key sections or variables
- Get inconsistent results

**Claude Playbooks fixes this:**
- ✅ Write prompt structure once as a template
- ✅ Inject context-specific data via variables
- ✅ Get consistent, deterministic outputs
- ✅ Build shareable prompt libraries (core + packs)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/andreolf/claude-playbooks.git
cd claude-playbooks

# Install
./install.sh

# List available playbooks
playbook list

# Run your first playbook
playbook run audit_contract \
  --vars project="MyDeFi" \
  --vars chain="Ethereum" \
  --vars scope="Staking contract" \
  --vars threat_model="Reentrancy, access control" \
  --vars risk="High" \
  --input contracts/Staking.sol
```

**Output**: A structured audit prompt with your contract code embedded, saved to `out/` and printed to your terminal.

---

## Core vs Packs

Claude Playbooks has two types of playbooks:

### Core Playbooks (Free, MIT License)

Located in `playbooks/` - general-purpose templates included with installation:

| Playbook | Purpose |
|----------|---------|
| `audit_contract` | Smart contract security audit with severity ratings |
| `review_pr` | Pull request code review with risk categorization |
| `release_notes` | Generate changelog and announcements from changes |
| `ship_blog` | Technical blog post with title options and X thread |
| `token_launch_checklist` | Web3 token launch planning and failure modes |
| `panel_questions_web3` | Conference panel discussion questions |

### Playbook Packs (Optional, Can be Licensed)

Located in `packs/<pack-name>/` - specialized, domain-specific templates:

```
packs/
├── security-audits/        # Advanced audit playbooks
│   ├── meta/manifest.json
│   └── playbooks/*.md
└── custom-pack/
    ├── meta/manifest.json
    └── playbooks/*.md
```

**Using Packs:**

```bash
# List playbooks in a pack
playbook list --pack security-audits

# Run playbook from pack
playbook run deep_audit --pack security-audits --vars project="DeFi"

# Pack requires license? Set environment variable:
export SECURITY_PACK_LICENSE="your-license-key"
```

**Creating Packs:**

```bash
# Initialize new pack structure
playbook init my-pack --with-pack my-pack

# Creates:
# packs/my-pack/meta/manifest.json
# packs/my-pack/playbooks/example.md
```

**Monetization Path:**

Build specialized pack libraries and distribute with license keys. Claude Playbooks handles license checking automatically via environment variables.

---

## Command Reference

### playbook run

Execute a playbook with variables and optional input.

```bash
playbook run <name> [options]

Options:
  --input <file>       Inject file content as {{input}}
  --stdin              Read from stdin as {{input}}
  --vars key=value     Set template variable (repeatable)
  --pack <name>        Load playbook from pack
  --print-only         Print only, don't save to out/
  --copy               Copy output to clipboard (macOS/Linux)

Examples:
  # Basic usage
  playbook run review_pr --input changes.diff

  # Multiple variables
  playbook run audit_contract \
    --vars project="DeFi" \
    --vars chain="Base" \
    --vars scope="Staking changes" \
    --vars threat_model="Economic attacks" \
    --vars risk="High" \
    --input contracts/

  # Read from stdin
  git diff | playbook run review_pr --stdin --vars repo="my-app" --vars title="Add auth"

  # Use pack
  playbook run deep_audit --pack security-audits \
    --vars project="MyProject" \
    --input contract.sol

  # Copy to clipboard
  playbook run ship_blog \
    --vars topic="Web3 Security" \
    --vars audience="Developers" \
    --copy
```

### playbook list

List available playbooks.

```bash
playbook list [--pack <name>]

Options:
  --pack <name>        List playbooks in specific pack

Examples:
  # List core playbooks
  playbook list

  # List pack playbooks
  playbook list --pack security-audits
```

### playbook init

Initialize new playbook or pack.

```bash
playbook init <path> [--with-pack <name>]

Options:
  --with-pack <name>   Create pack structure instead of single playbook

Examples:
  # Create new playbook
  playbook init playbooks/my_playbook.md

  # Create new pack
  playbook init my-custom-pack --with-pack my-custom-pack
```

---

## Available Core Playbooks

### 🔐 Smart Contract Security

**`audit_contract`** - Comprehensive security audit

```bash
playbook run audit_contract \
  --vars project="DeFi Protocol" \
  --vars chain="Base" \
  --vars scope="Staking contract changes" \
  --vars threat_model="Economic attacks, reentrancy" \
  --vars risk="High - mainnet launch" \
  --input contracts/Staking.sol
```

**Output includes:**
- Assumptions (privileged roles, upgradeability patterns, oracles, trust model)
- Executive risk summary
- Findings by severity (Critical/High/Medium/Low)
- Security checklist with Pass/Fail/Unknown ratings
- Go/No-Go recommendation

---

### 💻 Development Workflows

**`review_pr`** - Pull request code review

```bash
playbook run review_pr \
  --vars repo="my-webapp" \
  --vars title="Add payment processing" \
  --vars risk="medium" \
  --input changes.diff
```

**Output includes:**
- High/Medium/Low risk issues with fixes
- Test plan (unit, integration, edge cases)
- Suggested follow-ups

**`release_notes`** - Generate changelog

```bash
playbook run release_notes \
  --vars product="MyApp" \
  --vars version="2.0.0" \
  --input git-log.txt
```

**Output includes:**
- Changelog (Added/Improved/Fixed/Deprecated/Breaking)
- Upgrade notes
- Test checklist
- Announcement copy (short/medium/dev-focused)

---

### 🚀 Web3 Operations

**`token_launch_checklist`** - End-to-end launch planning

```bash
playbook run token_launch_checklist \
  --vars project="MyToken" \
  --vars token="MTK" \
  --vars chain="Ethereum" \
  --vars launch_date="2026-02-01" \
  --vars distribution="80% liquidity, 20% team vesting" \
  --vars constraints="24h launch window"
```

**Output includes:**
- Timeline (T-21 to T+7)
- Checklists (contracts, security, liquidity, exchanges, comms, analytics, monitoring)
- Top 10 failure modes with mitigation strategies

**`panel_questions_web3`** - Panel discussion questions

```bash
playbook run panel_questions_web3 \
  --vars event="EthDenver" \
  --vars session="DeFi Security" \
  --vars audience="Builders" \
  --vars panelists="Alice (Auditor), Bob (Protocol Dev)" \
  --vars goal="Actionable security practices" \
  --vars avoid="Marketing fluff"
```

---

### ✍️ Content Creation

**`ship_blog`** - Technical blog post

```bash
playbook run ship_blog \
  --vars topic="Smart Contract Optimization" \
  --vars audience="Solidity developers" \
  --vars angle="Gas optimization patterns" \
  --vars constraints="800-1200 words" \
  --input notes.txt
```

**Output includes:**
- 5 title options
- One-line hook
- Outline (H2/H3 structure)
- Full draft
- TLDR bullets
- X/Twitter thread (7 tweets)
- CTA variants

---

## How It Works

```
┌─────────────┐
│ You Run     │
│ playbook    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ 1. Pre-hook     │ ← hooks/pre.sh (validation, data fetch)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Load         │ ← playbooks/your_template.md (or pack)
│    Template     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Substitute   │ ← {{variables}} replaced with your values
│    Variables    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Save Output  │ ← out/YYYYMMDD_HHMMSS_playbook.prompt.txt
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Post-hook    │ ← hooks/post.sh (copy to clipboard, notify)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. Print        │ ← Prompt displayed in terminal
└─────────────────┘
```

### Built-in Variables

- `{{date}}` — Current date (YYYY-MM-DD UTC)
- `{{time_utc}}` — Current time (HH:MM:SS UTC)
- `{{input}}` — Content from `--input` file or `--stdin`

### Custom Variables

Pass any variable with `--vars`:

```bash
--vars project="My DApp"
--vars chain="Polygon"
--vars risk="Medium"
```

Use in templates:
```markdown
Project: {{project}}
Blockchain: {{chain}}
Risk Level: {{risk}}
```

---

## Creating Your Own Playbooks

Create a new file: `playbooks/my_playbook.md`

```markdown
SYSTEM
You are a [role]. You think in [style].

CONTEXT
Project: {{project}}
Goal: {{goal}}
Date: {{date}} (UTC {{time_utc}})

INPUT
{{input}}

TASK
[Describe what Claude should do]

RULES
- If information is missing or unknown, state "Unknown" explicitly
- State all assumptions clearly in the Assumptions section
- Do not fabricate or hallucinate facts
- Be deterministic: same input should produce consistent output structure
- Focus on [specific aspect]
- Output must include [requirement]

OUTPUT SCHEMA
1) Clarifying questions (only if needed)
   - Q1:
   - Q2:

2) Assumptions

3) Analysis

4) Recommendations
```

Then use it:

```bash
playbook run my_playbook \
  --vars project="..." \
  --vars goal="..." \
  --input data.txt
```

---

## Hooks: Automate Your Workflow

Hooks are shell scripts that run before/after prompt generation.

### Pre-hook Example: Validate Environment

Edit `hooks/pre.sh`:

```bash
#!/usr/bin/env bash
set -e
echo "[pre] running for $PLAYBOOK_NAME"

# Example: ensure git repo is clean before audit
if [ "$PLAYBOOK_NAME" = "audit_contract" ]; then
  git diff --quiet || {
    echo "Error: uncommitted changes detected"
    exit 1
  }
fi
```

### Post-hook Example: Copy to Clipboard

Edit `hooks/post.sh`:

```bash
#!/usr/bin/env bash
set -e
echo "[post] saved prompt to $OUT_FILE"

# Copy to clipboard (macOS)
cat "$OUT_FILE" | pbcopy
echo "[post] ✓ copied to clipboard"

# Or send to Claude API
# curl -X POST https://api.anthropic.com/v1/messages ...
```

### Available Hook Variables

- `$PLAYBOOK_NAME` — Name of playbook being run
- `$PB_PACK` — Pack name (if using --pack)
- `$OUT_FILE` — Path to generated prompt (post-hook only)
- `$PB_<VAR>` — All custom vars (e.g., `$PB_PROJECT`, `$PB_CHAIN`)

---

## Advanced Usage

### Chain Multiple Playbooks

Use hooks to generate follow-up prompts:

```bash
# In post.sh
if [ "$PLAYBOOK_NAME" = "audit_contract" ]; then
  # Generate remediation tasks from audit output
  playbook run create_tasks --input "$OUT_FILE"
fi
```

### Load Variables from Config

```bash
# config.env
export PROJECT="MyDApp"
export CHAIN="Ethereum"
export RISK_LEVEL="High"

# Load and use
source config.env
playbook run audit_contract \
  --vars project="$PROJECT" \
  --vars chain="$CHAIN" \
  --vars risk="$RISK_LEVEL"
```

### CI/CD Integration

```yaml
# .github/workflows/audit.yml
name: Generate Audit Prompt

on:
  pull_request:
    paths:
      - 'contracts/**'

jobs:
  audit-prompt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup playbooks
        run: |
          git clone https://github.com/andreolf/claude-playbooks.git
          cd claude-playbooks && ./install.sh

      - name: Generate audit prompt
        run: |
          git diff origin/main...HEAD -- contracts/ > changes.diff
          playbook run audit_contract \
            --vars project="${{ github.repository }}" \
            --vars scope="PR #${{ github.event.pull_request.number }}" \
            --input changes.diff

      - uses: actions/upload-artifact@v3
        with:
          name: audit-prompt
          path: claude-playbooks/out/*.prompt.txt
```

---

## Migration from v1.x

v2.0 introduces subcommands. Legacy syntax still works with deprecation warning.

**Old syntax (v1.x):**

```bash
./playbook.py audit_contract --vars project="X"
```

**New syntax (v2.0+):**

```bash
playbook run audit_contract --vars project="X"
```

**What changed:**
- ✅ Added `run` subcommand (required in v3.0+)
- ✅ Added `list` and `init` subcommands
- ✅ Added `--stdin` and `--copy` flags
- ✅ Added pack support with `--pack` flag
- ✅ Installed to `~/.local/bin/playbook` (no .py extension needed)
- ✅ Better error messages and help text

**Compatibility:**
- v2.0: Legacy syntax works with warning
- v3.0: Legacy syntax removed, must use subcommands

---

## Examples

See `examples/` directory for working examples:

- [PR Review](./examples/pr-review/) - Review code changes
- [Contract Audit](./examples/contract-audit/) - Security audit workflow
- [Blog Generation](./examples/blog-generation/) - Content creation

Each example includes sample input and a `command.sh` to run.

---

## Testing

Run the test suite:

```bash
python3 test_playbook.py
```

Tests cover:
- Variable substitution
- Pack loading and validation
- License checking
- Argument parsing

---

## Project Structure

```
claude-playbooks/
├── playbook.py              # Main CLI (520 lines, zero dependencies)
├── install.sh               # Installation script
├── README.md                # This file
├── LICENSE                  # MIT License
├── CHANGELOG.md             # Version history
├── playbooks/               # Core playbook templates
│   ├── audit_contract.md
│   ├── review_pr.md
│   ├── release_notes.md
│   ├── ship_blog.md
│   ├── token_launch_checklist.md
│   └── panel_questions_web3.md
├── packs/                   # Optional playbook packs
│   └── examples/            # Sample pack
├── hooks/                   # Lifecycle hooks
│   ├── pre.sh              # Runs before template render
│   └── post.sh             # Runs after save
├── out/                     # Generated prompts (gitignored)
├── examples/                # Working examples
│   ├── pr-review/
│   ├── contract-audit/
│   └── blog-generation/
└── test_playbook.py         # Test suite
```

---

## Tips & Best Practices

- ✅ **Version control playbooks** — Track improvements over time
- ✅ **One playbook per task type** — Keep prompts focused
- ✅ **Document required variables** — Add comments in templates
- ✅ **Use hooks for automation** — Integrate with your tools
- ✅ **Iterate based on results** — Refine templates from Claude's output
- ✅ **Share with your team** — Standardize prompts across projects

---

## Troubleshooting

**Playbook not found**
```
FileNotFoundError: Playbook not found: playbooks/my_playbook.md
```
→ Check filename in `playbooks/`. Use name without `.md` extension.
→ For packs: `playbook list --pack <name>` to see available playbooks.

**Hook not executing**
```
Permission denied: hooks/pre.sh
```
→ Make hooks executable: `chmod +x hooks/*.sh`

**Variables not substituting**
```
Output shows: {{my_var}} instead of actual value
```
→ Check spelling in `--vars` matches template exactly (case-sensitive).
→ Unknown variables are left unchanged intentionally.

**Pack license error**
```
Error: Pack 'security-audits' requires a license.
```
→ Set environment variable: `export SECURITY_PACK_LICENSE="your-key"`
→ Check manifest for correct `license_env` name.

---

## Contributing

Have a useful playbook? PRs welcome!

1. Create playbook in `playbooks/` or new pack in `packs/`
2. Add robustness rules (see existing playbooks)
3. Document required variables
4. Add example to `examples/`
5. Test with `python3 test_playbook.py`
6. Submit PR

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## License

MIT © Francesco Andreoli

---

## Acknowledgments

Inspired by [claude-hud](https://github.com/jarrodwatts/claude-hud) for clear, visual documentation.

Built with ❤️ for the Claude community.
