# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| main (latest) | ✅ |

## Reporting a Vulnerability

Please report security issues privately to **giorgikapanadze222@gmail.com**. Provide detailed reproduction steps and any relevant logs. We aim to acknowledge reports within 48 hours and provide a remediation plan within 7 days.

## Best Practices

- Do not commit real secrets. Use `.env` files and secret managers (Render/Vercel).
- Rotate credentials regularly, especially Django `SECRET_KEY` and database passwords.
- Enable HTTPS in production and configure CORS/CSRF following Django recommendations.
- Monitor dependency advisories (Dependabot/GitHub alerts).

Thank you for helping keep RevalytIQ secure.
