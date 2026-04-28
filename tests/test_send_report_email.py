from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


emailer = load_module("send_report_email", ROOT / "scripts" / "send_report_email.py")


class SendReportEmailTests(unittest.TestCase):
    def test_resolve_config_prefers_complete_smtp_settings(self) -> None:
        env = {
            "SMTP_HOST": "smtp.example.com",
            "SMTP_PORT": "465",
            "SMTP_USER": "sender@example.com",
            "SMTP_PASS": "secret",
            "SMTP_FROM": "Reports <sender@example.com>",
            "SENDGRID_API_KEY": "ignored",
        }

        config = emailer.resolve_delivery_config(env, provider="auto")

        self.assertEqual(config.provider, "smtp")
        self.assertEqual(config.smtp_host, "smtp.example.com")
        self.assertEqual(config.smtp_port, 465)
        self.assertEqual(config.smtp_user, "sender@example.com")
        self.assertEqual(config.from_email, "Reports <sender@example.com>")

    def test_resolve_config_reports_missing_smtp_values(self) -> None:
        env = {"SMTP_HOST": "smtp.example.com"}

        with self.assertRaises(emailer.MissingEmailConfig) as context:
            emailer.resolve_delivery_config(env, provider="smtp")

        message = str(context.exception)
        self.assertIn("SMTP_USER", message)
        self.assertIn("SMTP_PASS", message)
        self.assertIn("SMTP_FROM", message)

    def test_resolve_config_supports_sendgrid_and_mailgun(self) -> None:
        sendgrid = emailer.resolve_delivery_config(
            {"SENDGRID_API_KEY": "sg-key", "SENDGRID_FROM": "news@example.com"},
            provider="sendgrid",
        )
        mailgun = emailer.resolve_delivery_config(
            {
                "MAILGUN_API_KEY": "mg-key",
                "MAILGUN_DOMAIN": "mg.example.com",
                "MAILGUN_FROM": "news@example.com",
            },
            provider="mailgun",
        )

        self.assertEqual(sendgrid.provider, "sendgrid")
        self.assertEqual(sendgrid.api_key, "sg-key")
        self.assertEqual(mailgun.provider, "mailgun")
        self.assertEqual(mailgun.mailgun_domain, "mg.example.com")

    def test_build_message_contains_plain_text_and_html_parts(self) -> None:
        message = emailer.build_smtp_message(
            from_email="Reports <sender@example.com>",
            to_emails=["founder@example.com"],
            subject="Weekly insight",
            html="<h1>Hello</h1>",
            text="Hello",
        )

        self.assertEqual(message["Subject"], "Weekly insight")
        self.assertEqual(message["To"], "founder@example.com")
        self.assertTrue(message.is_multipart())
        self.assertIn("text/plain", message.as_string())
        self.assertIn("text/html", message.as_string())

    def test_main_rejects_conflicting_html_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            html_file = Path(tmpdir) / "body.html"
            html_file.write_text("<p>from-file</p>", encoding="utf-8")
            argv = [
                "--to",
                "founder@example.com",
                "--subject",
                "hello",
                "--html-file",
                str(html_file),
                "--html",
                "<p>from-arg</p>",
            ]
            code = emailer.main(argv)
        self.assertEqual(code, 2)

    def test_main_rejects_conflicting_text_inputs(self) -> None:
        argv = [
            "--to",
            "founder@example.com",
            "--subject",
            "hello",
            "--html",
            "<p>from-arg</p>",
            "--text-file",
            "private/sample.txt",
            "--text",
            "from-arg",
        ]
        code = emailer.main(argv)
        self.assertEqual(code, 2)

    def test_main_accepts_inline_html_with_dry_run(self) -> None:
        env = {
            "SMTP_HOST": "smtp.example.com",
            "SMTP_USER": "sender@example.com",
            "SMTP_PASS": "secret",
            "SMTP_FROM": "sender@example.com",
        }
        argv = [
            "--to",
            "founder@example.com",
            "--subject",
            "hello",
            "--html",
            "<p>Hello</p>",
            "--dry-run",
        ]

        with patch.dict(emailer.os.environ, env, clear=True):
            code = emailer.main(argv)

        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
