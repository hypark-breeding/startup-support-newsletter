# Attachment Analysis

Government startup support announcements often include the real details in attached
documents rather than in the web page body. Agents should inspect attachments when the
user asks whether a program is worth applying to, when eligibility is unclear, or when
the page summary is too thin.

## Document Processor Reuse

Prefer specialized document-processing skills, MCP tools, or local parsers for attachment reading. This project should orchestrate source selection and fit analysis, not reimplement every PDF/HWPX/Word parser. See `docs/document-processing-integrations.md`.

## File Type Priority

Use this priority when multiple equivalent announcement files are available:

1. `pdf`
2. `hwpx`
3. `doc` / `docx`

If only `hwp`, image, or zip files are available, process them as fallback formats.

## Download Policy

- Download only from official or verified source pages.
- Save local working copies under `downloads/`.
- Do not commit downloaded announcement files.
- Keep user business plans under `private/` or another user-approved local path.
- Do not commit business plans, application drafts, financials, or private company data.

## Extraction Targets

Extract these fields from announcement attachments:

- program title
- organization
- application period
- eligibility
- exclusion criteria
- support amount and support type
- required documents
- evaluation criteria
- selection process and schedule
- obligations after selection
- contact
- official source URL
- attachment URL and file type

## Attachment Selection

When a page has multiple files:

1. Prefer files whose title includes `공고`, `공고문`, `모집공고`, or `announcement`.
2. Apply file type priority: `pdf > hwpx > word`.
3. Use application forms only after the announcement document.
4. If a zip contains a PDF or HWPX announcement, extract and analyze that first.

## Output

Return a short attachment summary plus normalized JSON-compatible fields. Preserve
important constraints exactly when possible, especially dates, founder age, company age,
location, industry restrictions, and required relocation.
