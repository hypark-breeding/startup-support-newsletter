#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import smtplib
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage
from pathlib import Path
from typing import Mapping, NamedTuple


TRUE_VALUES = {"1", "true", "yes", "on"}


class MissingEmailConfig(RuntimeError):
    pass


class DeliveryConfig(NamedTuple):
    provider: str
    from_email: str
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_pass: str | None = None
    smtp_tls: bool = True
    smtp_ssl: bool = False
    api_key: str | None = None
    mailgun_domain: str | None = None
    mailgun_api_base: str = "https://api.mailgun.net/v3"


def first_env(env: Mapping[str, str], *names: str) -> str | None:
    for name in names:
        value = env.get(name)
        if value:
            return value
    return None


def env_bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    value = env.get(name)
    if value is None:
        return default
    return value.strip().lower() in TRUE_VALUES


def missing_message(provider: str, names: list[str]) -> str:
    joined = ", ".join(names)
    return (
        f"Missing email configuration for {provider}: {joined}. "
        "Provide the values as environment variables or in a local .env file. "
        "Do not commit secrets."
    )


def resolve_delivery_config(env: Mapping[str, str], provider: str = "auto") -> DeliveryConfig:
    provider = provider.lower()
    if provider not in {"auto", "smtp", "sendgrid", "mailgun"}:
        raise ValueError("provider must be auto, smtp, sendgrid, or mailgun")

    if provider == "auto":
        if env.get("SMTP_HOST"):
            provider = "smtp"
        elif env.get("SENDGRID_API_KEY"):
            provider = "sendgrid"
        elif env.get("MAILGUN_API_KEY"):
            provider = "mailgun"
        else:
            raise MissingEmailConfig(
                "Missing email configuration. Configure SMTP_HOST/SMTP_USER/SMTP_PASS/SMTP_FROM, "
                "or SENDGRID_API_KEY with SENDGRID_FROM, or MAILGUN_API_KEY/MAILGUN_DOMAIN/MAILGUN_FROM."
            )

    if provider == "smtp":
        required = {
            "SMTP_HOST": env.get("SMTP_HOST"),
            "SMTP_USER": env.get("SMTP_USER"),
            "SMTP_PASS": env.get("SMTP_PASS"),
            "SMTP_FROM": first_env(env, "SMTP_FROM", "EMAIL_FROM"),
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise MissingEmailConfig(missing_message("SMTP", missing))
        port = int(env.get("SMTP_PORT") or "587")
        smtp_ssl = env_bool(env, "SMTP_SSL", port == 465)
        smtp_tls = env_bool(env, "SMTP_TLS", not smtp_ssl)
        return DeliveryConfig(
            provider="smtp",
            from_email=required["SMTP_FROM"] or "",
            smtp_host=required["SMTP_HOST"],
            smtp_port=port,
            smtp_user=required["SMTP_USER"],
            smtp_pass=required["SMTP_PASS"],
            smtp_tls=smtp_tls,
            smtp_ssl=smtp_ssl,
        )

    if provider == "sendgrid":
        api_key = env.get("SENDGRID_API_KEY")
        from_email = first_env(env, "SENDGRID_FROM", "EMAIL_FROM")
        missing = []
        if not api_key:
            missing.append("SENDGRID_API_KEY")
        if not from_email:
            missing.append("SENDGRID_FROM or EMAIL_FROM")
        if missing:
            raise MissingEmailConfig(missing_message("SendGrid", missing))
        return DeliveryConfig(provider="sendgrid", from_email=from_email or "", api_key=api_key)

    api_key = env.get("MAILGUN_API_KEY")
    domain = env.get("MAILGUN_DOMAIN")
    from_email = first_env(env, "MAILGUN_FROM", "EMAIL_FROM")
    missing = []
    if not api_key:
        missing.append("MAILGUN_API_KEY")
    if not domain:
        missing.append("MAILGUN_DOMAIN")
    if not from_email:
        missing.append("MAILGUN_FROM or EMAIL_FROM")
    if missing:
        raise MissingEmailConfig(missing_message("Mailgun", missing))
    return DeliveryConfig(
        provider="mailgun",
        from_email=from_email or "",
        api_key=api_key,
        mailgun_domain=domain,
        mailgun_api_base=env.get("MAILGUN_API_BASE") or "https://api.mailgun.net/v3",
    )


def build_smtp_message(
    *,
    from_email: str,
    to_emails: list[str],
    subject: str,
    html: str,
    text: str,
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject
    message.set_content(text)
    message.add_alternative(html, subtype="html")
    return message


def send_smtp(config: DeliveryConfig, to_emails: list[str], subject: str, html: str, text: str) -> dict[str, str]:
    if not config.smtp_host or not config.smtp_port:
        raise MissingEmailConfig("SMTP host and port are required")
    message = build_smtp_message(
        from_email=config.from_email,
        to_emails=to_emails,
        subject=subject,
        html=html,
        text=text,
    )
    if config.smtp_ssl:
        with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, context=ssl.create_default_context()) as smtp:
            if config.smtp_user and config.smtp_pass:
                smtp.login(config.smtp_user, config.smtp_pass)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(config.smtp_host, config.smtp_port) as smtp:
            if config.smtp_tls:
                smtp.starttls(context=ssl.create_default_context())
            if config.smtp_user and config.smtp_pass:
                smtp.login(config.smtp_user, config.smtp_pass)
            smtp.send_message(message)
    return {"provider": "smtp", "status": "sent"}


def send_sendgrid(config: DeliveryConfig, to_emails: list[str], subject: str, html: str, text: str) -> dict[str, str]:
    if not config.api_key:
        raise MissingEmailConfig("SENDGRID_API_KEY is required")
    payload = {
        "personalizations": [{"to": [{"email": email} for email in to_emails]}],
        "from": {"email": config.from_email},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": text},
            {"type": "text/html", "value": html},
        ],
    }
    request = urllib.request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return {"provider": "sendgrid", "status": str(response.status)}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"SendGrid error {exc.code}: {body}") from exc


def send_mailgun(config: DeliveryConfig, to_emails: list[str], subject: str, html: str, text: str) -> dict[str, str]:
    if not config.api_key or not config.mailgun_domain:
        raise MissingEmailConfig("MAILGUN_API_KEY and MAILGUN_DOMAIN are required")
    endpoint = f"{config.mailgun_api_base.rstrip('/')}/{config.mailgun_domain}/messages"
    data = urllib.parse.urlencode(
        {"from": config.from_email, "to": ",".join(to_emails), "subject": subject, "text": text, "html": html}
    ).encode("utf-8")
    auth = base64.b64encode(f"api:{config.api_key}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {"provider": "mailgun", "status": str(response.status), "response": body}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Mailgun error {exc.code}: {body}") from exc


def parse_recipients(values: list[str]) -> list[str]:
    recipients: list[str] = []
    for value in values:
        recipients.extend(part.strip() for part in value.split(",") if part.strip())
    if not recipients:
        raise ValueError("At least one --to recipient is required")
    return recipients


def html_to_text(html_body: str) -> str:
    text = re.sub(r"<style[\s\S]*?</style>", " ", html_body, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or "K-startup insight report attached in HTML body."


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def merged_env(dotenv_path: Path | None) -> dict[str, str]:
    env = dict(os.environ)
    if dotenv_path:
        for key, value in load_dotenv(dotenv_path).items():
            env.setdefault(key, value)
    return env


def send_report(config: DeliveryConfig, to_emails: list[str], subject: str, html: str, text: str) -> dict[str, str]:
    if config.provider == "smtp":
        return send_smtp(config, to_emails, subject, html, text)
    if config.provider == "sendgrid":
        return send_sendgrid(config, to_emails, subject, html, text)
    if config.provider == "mailgun":
        return send_mailgun(config, to_emails, subject, html, text)
    raise ValueError(f"Unsupported provider: {config.provider}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send a designed K-startup report by email.")
    parser.add_argument("--provider", choices=["auto", "smtp", "sendgrid", "mailgun"], default="auto")
    parser.add_argument("--to", action="append", required=True, help="Recipient email. Repeat or comma-separate.")
    parser.add_argument("--subject", required=True)
    html_group = parser.add_mutually_exclusive_group(required=True)
    html_group.add_argument("--html-file", help="Path to HTML body file.")
    html_group.add_argument("--html", help="Raw HTML body string.")
    text_group = parser.add_mutually_exclusive_group()
    text_group.add_argument("--text-file")
    text_group.add_argument("--text", help="Raw text body string.")
    parser.add_argument("--dotenv", default=".env", help="Local env file. Defaults to .env if present.")
    parser.add_argument("--dry-run", action="store_true", help="Resolve config and print a send preview without sending.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 1

    to_emails = parse_recipients(args.to)
    if args.html_file:
        html_body = Path(args.html_file).read_text(encoding="utf-8")
    else:
        html_body = args.html or ""

    if args.text_file:
        text_body = Path(args.text_file).read_text(encoding="utf-8")
    elif args.text:
        text_body = args.text
    else:
        text_body = html_to_text(html_body)

    try:
        config = resolve_delivery_config(merged_env(Path(args.dotenv)), provider=args.provider)
    except MissingEmailConfig as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.dry_run:
        print(
            json.dumps(
                {
                    "provider": config.provider,
                    "from": config.from_email,
                    "to": to_emails,
                    "subject": args.subject,
                    "html_bytes": len(html_body.encode("utf-8")),
                    "sent": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    result = send_report(config, to_emails, args.subject, html_body, text_body)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
