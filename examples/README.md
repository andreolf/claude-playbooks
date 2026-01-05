# Claude Playbooks Examples

This directory contains working examples demonstrating claude-playbooks features.

## Quick Links

- [PR Review Example](./pr-review/) - Review code changes from a diff
- [Contract Audit Example](./contract-audit/) - Security audit workflow
- [Blog Generation Example](./blog-generation/) - Content creation from notes

## Running Examples

Each example directory contains:
- Sample input file(s)
- `command.sh` - The exact command to run
- `expected-output.txt` - Sample of what the generated prompt looks like

To try an example:
```bash
cd examples/pr-review
bash command.sh
```

## Creating Your Own

Use these examples as templates:
1. Copy the structure you need
2. Modify variables and input files
3. Run and iterate on the template

## Tips

- Use `--print-only` to test without saving files
- Use `--stdin` to pipe content directly: `git diff | playbook run review_pr --stdin`
- Use `--copy` to copy output to clipboard for immediate use
