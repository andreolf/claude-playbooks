#!/usr/bin/env bash
# Example: Review a pull request using the review_pr playbook

playbook run review_pr \
  --vars repo="my-webapp" \
  --vars title="Add payment processing" \
  --vars risk="medium" \
  --input sample.diff
