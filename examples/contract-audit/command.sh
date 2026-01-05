#!/usr/bin/env bash
# Example: Audit a smart contract using the audit_contract playbook

playbook run audit_contract \
  --vars project="SimpleVault" \
  --vars chain="Ethereum" \
  --vars scope="Complete contract - deposit, withdraw, admin functions" \
  --vars threat_model="Reentrancy, access control, arithmetic issues" \
  --vars risk="High - will hold user funds" \
  --input Sample.sol
