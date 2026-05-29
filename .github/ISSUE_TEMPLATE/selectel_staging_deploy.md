---
name: Selectel Staging Deploy
about: Track KURGIN Formula API staging deployment
title: "Selectel staging deploy"
labels: deployment, staging
assignees: ""
---

## Server

- [ ] Selectel server created
- [ ] Ubuntu installed
- [ ] SSH access confirmed
- [ ] Docker installed
- [ ] Firewall configured

## App

- [ ] Repository cloned
- [ ] `.env.staging` created
- [ ] API secret generated
- [ ] Container built
- [ ] Container started

## Checks

- [ ] `/v1/health`
- [ ] `/v1/ready`
- [ ] `/v1/analyze/stone`
- [ ] `/v1/platform/stone-card`
- [ ] `/v1/export/stone/pdf`
- [ ] batch JSON
- [ ] unauthorized request fails

## Notes

