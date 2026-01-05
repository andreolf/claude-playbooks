#!/usr/bin/env bash
# Example: Generate a blog post using the ship_blog playbook

playbook run ship_blog \
  --vars topic="Smart Contract Security Best Practices" \
  --vars audience="Solidity developers" \
  --vars angle="Practical, actionable security patterns" \
  --vars constraints="800-1200 words, include code examples" \
  --input notes.txt
