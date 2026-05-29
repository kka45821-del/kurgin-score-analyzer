# Selectel Staging Deployment Checklist

## Before deploy

- [ ] Set `KURGIN_API_SECRET`
- [ ] Set `KURGIN_API_ENV=staging`
- [ ] Set allowed origins
- [ ] Confirm Docker build
- [ ] Run API contract test locally
- [ ] Confirm `/v1/health`
- [ ] Confirm `/v1/ready`

## After deploy

- [ ] Test one-stone analysis
- [ ] Test batch JSON
- [ ] Test batch Excel upload
- [ ] Test PDF export
- [ ] Test Excel export
- [ ] Test ZIP package export
- [ ] Test unauthorized request fails
- [ ] Check logs
- [ ] Check memory during PDF package generation

## Do not expose

- Formula code in frontend
- API secret in browser
- supplier files
- raw internal formula coefficients
