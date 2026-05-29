# Selectel Staging Security Checklist

## Must be true before external testing

- [ ] `KURGIN_API_SECRET` is set.
- [ ] Unauthorized calls fail.
- [ ] API key is stored only on server/backend, not browser.
- [ ] Formula API is not embedded in frontend.
- [ ] CORS is limited to staging platform domain if exposed.
- [ ] Supplier files are not committed.
- [ ] Logs do not print API secret.
- [ ] SSH access is limited.
- [ ] Firewall exposes only required ports.
- [ ] Production secrets are not used in staging.

## Recommended

- Use HTTPS via reverse proxy.
- Keep Formula API behind Platform backend where possible.
- Use Selectel/private network if both services are hosted there.
- Rotate staging API key after testing.
