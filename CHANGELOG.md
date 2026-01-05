# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
