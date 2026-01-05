# Claude Playbooks

Transform your Claude workflows with reusable, parameterized prompt templates. Write your prompt structure once, render it with context-specific variables for every use.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🎯 **Status**: Production-ready. Used for smart contract audits, PR reviews, token launches, and technical content creation.

## What You Get

| Feature | What It Does |
|---------|--------------|
| 📝 **Template System** | Write prompts once with `{{variables}}`, reuse across projects |
| 📂 **File Injection** | Pass entire files or diffs as input to your prompts |
| 🔄 **Lifecycle Hooks** | Run custom scripts before/after prompt generation |
| 💾 **Auto-archiving** | Every prompt saved with timestamp for future reference |
| ⚡ **Zero Dependencies** | Just Python 3 — no packages to install |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/claude-playbooks.git
cd claude-playbooks

# Make it executable
chmod +x playbook.py

# Generate your first prompt
./playbook.py audit_contract \
  --vars project="MyDeFi" \
  --vars chain="Ethereum" \
  --input contracts/Staking.sol
```

**Output**: A structured audit prompt with your contract code embedded, saved to `out/` and printed to your terminal.

---

## Available Playbooks

### 🔐 Smart Contract Security

**`audit_contract`** — Comprehensive security audit template
```bash
./playbook.py audit_contract \
  --vars project="DeFi Protocol" \
  --vars chain="Base" \
  --vars scope="Staking contract changes" \
  --vars threat_model="Economic attacks, reentrancy" \
  --vars risk="High - mainnet launch" \
  --input contracts/Staking.sol
```

**What you get**: Structured audit report with findings by severity (Critical/High/Medium/Low), security checklist, and go/no-go recommendation.

---

### 💻 Development Workflows

**`review_pr`** — Pull request review template
```bash
./playbook.py review_pr --input changes.diff
```
**What you get**: Code quality review focusing on security, best practices, and maintainability.

**`release_notes`** — Generate changelog from changes
```bash
./playbook.py release_notes \
  --vars version="2.0.0" \
  --input git-log.txt
```
**What you get**: Structured release notes with breaking changes, features, and fixes.

---

### 🚀 Web3 Operations

**`token_launch_checklist`** — End-to-end launch planning
```bash
./playbook.py token_launch_checklist \
  --vars project="MyToken" \
  --vars token="MTK" \
  --vars chain="Ethereum" \
  --vars launch_date="2026-02-01" \
  --vars distribution="80% liquidity, 20% team vesting"
```

**What you get**:
- Timeline (T-21 to T+7)
- Checklists for contracts, security, liquidity, exchanges, comms
- Top 10 failure modes with mitigation strategies
- Post-launch monitoring plan

**`panel_questions_web3`** — Panel discussion questions
```bash
./playbook.py panel_questions_web3 \
  --vars topic="DeFi Security" \
  --vars panelists="Alice (Auditor), Bob (Protocol Dev)"
```

---

### ✍️ Content Creation

**`ship_blog`** — Technical blog post structure
```bash
./playbook.py ship_blog \
  --vars topic="Smart Contract Optimization" \
  --vars audience="Solidity developers"
```

---

## How It Works

```
┌─────────────┐
│ You Run     │
│ ./playbook  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ 1. Pre-hook     │ ← hooks/pre.sh (validation, data fetch)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Load         │ ← playbooks/your_template.md
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
│ 4. Save Output  │ ← out/TIMESTAMP_playbook.prompt.txt
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
- `{{input}}` — Content from `--input` file

### Custom Variables
Any variable you pass with `--vars`:
```bash
--vars project="My DApp"
--vars chain="Polygon"
--vars risk="Medium"
```

Use in your templates:
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
- Be specific
- Focus on [aspect]
- Output must include [requirement]

OUTPUT SCHEMA
1) Section heading
   - Item
   - Item

2) Another section
   - Detail
```

Then use it:
```bash
./playbook.py my_playbook \
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
- `$OUT_FILE` — Path to generated prompt (post-hook only)
- `$PB_<VAR>` — All custom vars (e.g., `$PB_PROJECT`, `$PB_CHAIN`)

---

## Command Reference

```bash
./playbook.py <name> [options]

Options:
  --input <file>       Inject file content as {{input}}
  --vars key=value     Set template variable (repeatable)
  --print-only         Print only, don't save to out/

Examples:
  # Basic usage
  ./playbook.py review_pr --input changes.diff

  # Multiple variables
  ./playbook.py audit_contract \
    --vars project="DeFi" \
    --vars chain="Base" \
    --input contracts/

  # Print without saving
  ./playbook.py ship_blog \
    --vars topic="Web3 Security" \
    --print-only
```

---

## Project Structure

```
claude-playbooks/
├── playbook.py              # Main script
├── install.sh               # Installation helper
├── README.md                # Documentation
├── playbooks/               # Template directory
│   ├── audit_contract.md
│   ├── token_launch_checklist.md
│   ├── review_pr.md
│   ├── release_notes.md
│   ├── ship_blog.md
│   └── panel_questions_web3.md
├── hooks/                   # Lifecycle hooks
│   ├── pre.sh              # Runs before template render
│   └── post.sh             # Runs after save
└── out/                     # Generated prompts (gitignored)
    └── YYYYMMDD_HHMMSS_<playbook>.prompt.txt
```

---

## Advanced Usage

### Chain Multiple Playbooks
Use hooks to generate follow-up prompts:
```bash
# In post.sh
if [ "$PLAYBOOK_NAME" = "audit_contract" ]; then
  # Generate remediation tasks from audit output
  ./playbook.py create_tasks --input "$OUT_FILE"
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
./playbook.py audit_contract \
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
      - name: Generate audit prompt
        run: |
          git diff origin/main...HEAD -- contracts/ > changes.diff
          ./playbook.py audit_contract \
            --vars project="${{ github.repository }}" \
            --vars scope="PR #${{ github.event.pull_request.number }}" \
            --input changes.diff
      - uses: actions/upload-artifact@v3
        with:
          name: audit-prompt
          path: out/*.prompt.txt
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

**Hook not executing**
```
Permission denied: hooks/pre.sh
```
→ Make hooks executable: `chmod +x hooks/*.sh`

**Variables not substituting**
```
Output shows: {{my_var}} instead of actual value
```
→ Check spelling in `--vars` matches template exactly (case-sensitive)

---

## Contributing

Have a useful playbook? PRs welcome!

1. Create playbook in `playbooks/`
2. Document required variables
3. Add example to README
4. Test with sample data
5. Submit PR

---

## License

MIT © Francesco Andreoli

---

## Acknowledgments

Inspired by [claude-hud](https://github.com/jarrodwatts/claude-hud) for clear, visual documentation.
