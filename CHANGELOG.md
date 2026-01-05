# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-05

### Breaking Changes (with backward compatibility)

- **CLI now uses subcommands**: `playbook run <name>` instead of `playbook <name>`
  - Legacy syntax still works in v2.0 with deprecation warning to stderr
  - Will be removed in v3.0
- **Installation location changed**: Now installs to `~/.local/bin/playbook` (no .py extension)

### Added

#### Core Features
- **Playbook Packs**: Organize and distribute specialized playbook collections
  - Directory structure: `packs/<pack>/meta/manifest.json` and `packs/<pack>/playbooks/*.md`
  - Manifest-driven pack management with validation
  - License support via environment variables (`requires_license`, `license_env` fields)
  - `playbook list --pack <name>` to discover pack playbooks
  - `playbook run <name> --pack <name>` to execute from packs

- **New Subcommands**:
  - `playbook list` - List available playbooks (core or pack)
  - `playbook init <path>` - Create new playbook from template
  - `playbook init <path> --with-pack <name>` - Scaffold complete pack structure

#### Quality of Life
- **`--stdin` flag**: Read input from stdin instead of file
  - Example: `git diff | playbook run review_pr --stdin`
- **`--copy` flag**: Automatically copy output to clipboard
  - Works on macOS (pbcopy), Linux (xclip/xsel)
  - Graceful degradation with warning if unavailable
- **Better error messages**: Actionable errors with suggestions and available options
- **Help text improvements**: Clear descriptions for all commands and flags

### Enhanced

#### Playbook Robustness
All playbooks now include standardized robustness rules:
- "If information is missing or unknown, state 'Unknown' explicitly"
- "State all assumptions clearly in the Assumptions section"
- "Do not fabricate or hallucinate facts"
- "Be deterministic: same input should produce consistent output structure"

#### audit_contract.md Enhancements
- **Expanded Assumptions section**:
  - Privileged roles and admin key patterns
  - Upgradeability pattern detection (UUPS/Transparent/Beacon/None/Unknown)
  - External dependencies and oracle assumptions
  - Explicit trust model documentation
- **Enhanced Checklist format**: Pass/Fail/Unknown ratings with detailed criteria for each item
- **8 comprehensive security categories**: Access control, reentrancy, arithmetic, external calls, upgradability, oracles, MEV, ERC compliance

#### Installation Experience
- **Improved install.sh**:
  - Colored output for better UX (✓, ⚠ indicators)
  - Automatic PATH detection
  - Shell-specific instructions (bash, zsh, fish)
  - macOS/Linux .bashrc vs .bash_profile detection
  - Smoke test command suggestions
  - Clear next steps after installation

### Documentation

- **Comprehensive README rewrite**:
  - New value proposition: "Turn messy inputs into consistent, reusable prompts"
  - "Core vs Packs" section explaining both concepts
  - Complete command reference for all subcommands
  - Migration guide from v1.x with examples
  - Pack creation guide with monetization path
  - Updated all examples to new CLI syntax
  - CI/CD integration examples

- **Examples directory**:
  - `examples/pr-review/` - Pull request review workflow
  - `examples/contract-audit/` - Smart contract audit workflow
  - `examples/blog-generation/` - Content creation workflow
  - Each example includes: sample input, command.sh, and expected output format

- **Test suite**: `test_playbook.py` with comprehensive coverage
  - Variable substitution tests
  - Pack loading and validation tests
  - License checking tests
  - Argument parsing tests
  - 23 test cases covering core functionality

### Technical

- **Zero new dependencies**: Still pure Python 3 stdlib only
- **Single-file architecture maintained**: 524 lines (up from 96)
- **Clear code organization**: Section comments for maintainability
- **Pack manifest validation**: JSON schema validation with clear error messages
- **Environment-based licensing**: Simple, honor-system compatible with future enhancements

### Migration Guide

**v1.x → v2.0**:
```bash
# Old (still works with warning)
./playbook.py audit_contract --vars project="X"

# New
playbook run audit_contract --vars project="X"
```

**What to update**:
1. Change `./playbook.py <name>` → `playbook run <name>`
2. Use `playbook list` to discover available playbooks
3. Reinstall: `./install.sh` (new location: ~/.local/bin/playbook)

**Compatibility timeline**:
- v2.0: Legacy syntax works with deprecation warning
- v3.0: Legacy syntax removed (subcommands required)

### Deprecations

- Legacy CLI syntax (`./playbook.py <name>`) will be removed in v3.0
  - Currently shows deprecation warning to stderr
  - Update scripts to use `playbook run <name>` syntax

---

## [1.0.0] - 2026-01-05

### Added
- Initial release of Claude Playbooks system
- Core `playbook.py` script with template rendering engine
- Variable substitution system with `{{variable}}` syntax
- Built-in variables: `{{date}}` and `{{time_utc}}`
- File input injection via `--input` flag
- Lifecycle hooks system (pre/post)
- Timestamped output archiving in `out/` directory

### Playbooks Included
- `audit_contract` - Smart contract security audit template
- `token_launch_checklist` - Token launch planning and risk management
- `review_pr` - Pull request review template
- `release_notes` - Release notes generation
- `ship_blog` - Technical blog post creation
- `panel_questions_web3` - Web3 panel discussion questions

### Documentation
- Comprehensive README with examples and usage guide
- CODE_OF_CONDUCT for community guidelines
- CONTRIBUTING guide for contributors
- SECURITY policy for vulnerability reporting
- MIT LICENSE

### Infrastructure
- Git repository initialization
- GitHub repository setup
- `.gitignore` for output files and Python artifacts

[1.0.0]: https://github.com/andreolf/claude-playbooks/releases/tag/v1.0.0
