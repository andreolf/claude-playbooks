# Contributing to Claude Playbooks

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/claude-playbooks.git
cd claude-playbooks
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

#### Adding a New Playbook

1. Create a new file in `playbooks/your_playbook.md`
2. Use the standard structure:
   - SYSTEM: Define the role and thinking style
   - CONTEXT: List required variables
   - INPUT: Where file input goes
   - TASK: Clear task description
   - RULES: Constraints and guidelines
   - OUTPUT SCHEMA: Structured format

3. Test your playbook:
```bash
./playbook.py your_playbook \
  --vars key1="value1" \
  --vars key2="value2" \
  --input sample.txt
```

4. Document it in the README.md under "Available Playbooks"

#### Improving Existing Playbooks

- Keep the existing structure
- Ensure backward compatibility with existing variables
- Test with actual use cases
- Document any breaking changes

#### Enhancing the Core Script

- Keep changes focused and small
- Maintain Python 3 compatibility
- Avoid adding external dependencies if possible
- Add comments for complex logic

### 4. Test Your Changes

```bash
# Test with different playbooks
./playbook.py audit_contract --vars project="Test" --print-only
./playbook.py review_pr --print-only

# Test error cases
./playbook.py nonexistent_playbook  # Should fail gracefully
./playbook.py audit_contract --vars invalid_format  # Should show error
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add: Brief description of your change

- Detailed point 1
- Detailed point 2"
```

### 6. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a pull request on GitHub with:
- Clear description of what you changed and why
- Examples of usage if adding a new playbook
- Any breaking changes highlighted

## Code Style

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings for functions
- Keep functions focused and small

### Markdown/Templates
- Use consistent heading levels
- Keep lines under 100 characters where practical
- Use bullet points for lists
- Include examples where helpful

## What Makes a Good Playbook?

✅ **Clear role definition**: "You are a [specific role]"
✅ **Explicit output schema**: Structured format that's easy to parse
✅ **Practical rules**: Constraints that improve output quality
✅ **Variable-driven**: Flexible through substitution, not hardcoded
✅ **Real-world tested**: Actually useful in production workflows

❌ **Avoid**:
- Vague instructions like "do your best"
- Too many variables (keep it under 10)
- Hardcoded project-specific details
- Overly complex nested structures

## Examples of Good Contributions

### Adding a Playbook
```markdown
Title: Add Solidity gas optimization playbook

Added a new playbook for analyzing Solidity contracts for gas optimization opportunities.

Variables:
- project: Project name
- contract: Contract name
- target_network: Deployment network

Tested with 3 real contracts, found useful optimizations in each case.
```

### Improving Documentation
```markdown
Title: Add CI/CD integration examples

Added examples for:
- GitHub Actions workflow
- GitLab CI configuration
- Jenkins pipeline

Each example tested and working.
```

## Need Help?

- Open an issue for questions
- Check existing issues and PRs first
- Be respectful and follow the Code of Conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
