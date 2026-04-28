# Email Delivery

Use this workflow when the user asks to send a designed startup-support or insight
report by email.

## Delivery Policy

- Generate or preview the report before sending.
- Use real delivery only when the recipient, subject, and sender identity are clear.
- Never commit SMTP passwords, API keys, OAuth tokens, or `.env` files.
- If required settings are missing, ask the user for the missing values and tell them
  they can provide values as environment variables or a local `.env` file.
- Keep private business plans, lead lists, and recipient lists local.

## Supported Providers

The default script is `scripts/send_report_email.py`.

### SMTP

Required:

- `SMTP_HOST`
- `SMTP_USER`
- `SMTP_PASS`
- `SMTP_FROM`

Optional:

- `SMTP_PORT`, default `587`
- `SMTP_TLS`, default `true`
- `SMTP_SSL`, default `true` when port is `465`, otherwise `false`

### SendGrid

Required:

- `SENDGRID_API_KEY`
- `SENDGRID_FROM` or `EMAIL_FROM`

### Mailgun

Required:

- `MAILGUN_API_KEY`
- `MAILGUN_DOMAIN`
- `MAILGUN_FROM` or `EMAIL_FROM`

Optional:

- `MAILGUN_API_BASE`, default `https://api.mailgun.net/v3`

## Missing Configuration Prompt

When configuration is missing, ask only for the missing values. Keep the prompt short:

```text
?? ?? ??? ?? ????. ?? ??? ?? ?? ?? ?????.

- SMTP_HOST
- SMTP_USER
- SMTP_PASS
- SMTP_FROM

SendGrid? Mailgun? ?? ??? ? provider ??? API key ?? ?????.
???? Git? ???? ?? ?? env ?? .env?? ?????.
```

## Preview First

Render the report HTML:

```bash
python3 scripts/render_insight_report.py \
  --input private/insight-report.json \
  --output private/insight-report.html
```

Then dry-run delivery:

```bash
python3 scripts/send_report_email.py \
  --to founder@example.com \
  --subject "?? ???? ???? ???" \
  --html-file private/insight-report.html \
  --dry-run
```

## Actual Send

After preview approval and configuration are present:

```bash
python3 scripts/send_report_email.py \
  --to founder@example.com \
  --subject "?? ???? ???? ???" \
  --html-file private/insight-report.html
```

For a specific provider:

```bash
python3 scripts/send_report_email.py \
  --provider sendgrid \
  --to founder@example.com \
  --subject "?? ???? ???? ???" \
  --html-file private/insight-report.html
```

## Quality Checks

- Confirm the email has at least one official source URL for current opportunities.
- Label recurring or predicted opportunities separately from open applications.
- Confirm recipient addresses before actual send.
- Run dry-run first when working in a new environment.
- If the provider returns an error, report the status code and provider response without
  exposing secrets.
