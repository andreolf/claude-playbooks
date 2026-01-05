# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please do NOT open a public issue.

Instead, please send a report to: **francesco.andreoli89@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You should receive a response within 48 hours. We'll keep you updated on the progress toward a fix and disclosure.

## Security Considerations

### Input Validation

- The playbook system accepts file paths via `--input`
- Always validate input file paths in your hooks
- Be cautious with user-provided variables that may be executed

### Hook Execution

- Pre and post hooks execute arbitrary shell commands
- Review hooks before running playbooks from untrusted sources
- Hooks run with the same permissions as the user

### Generated Prompts

- Prompts may contain sensitive information from input files
- Output directory (`out/`) should be included in `.gitignore`
- Consider encrypting stored prompts if they contain secrets

### Best Practices

1. **Never commit sensitive data**: Use `.gitignore` for output directories
2. **Review hooks**: Always inspect `hooks/*.sh` before running
3. **Validate inputs**: Check file paths and variables in hooks
4. **Limit permissions**: Run with minimal required privileges
5. **Keep dependencies updated**: Although this project has zero dependencies, keep Python updated

## Known Limitations

- No input sanitization for hook environment variables
- Hooks execute with full shell access
- No encryption for stored prompts

## Disclosure Policy

- Security issues will be disclosed after a fix is available
- We aim to release fixes within 7 days for critical issues
- Public disclosure will credit the reporter (unless anonymity requested)
