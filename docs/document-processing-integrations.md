# Document Processing Integrations

This project should not own every document parser. Agents should reuse available
document-processing skills, MCP tools, or local libraries whenever possible, then feed
the extracted text/tables back into the startup-support workflow.

## Integration Principle

- Use this repository for source selection, policy reasoning, normalization, calendar
  output, and business-plan fit analysis.
- Use specialized document tools for attachment parsing.
- Keep downloaded files and private business plans local.
- Do not commit extracted private text unless it is an intentionally redacted fixture.

## Preferred Attachment Pipeline

Follow the project file priority first:

1. `pdf`
2. `hwpx`
3. `doc` / `docx`

Then choose a processor by file type.

## Processor Matrix

| File type | Preferred processor | Notes |
| --- | --- | --- |
| `pdf` | PDF-capable document skill, MCP, or local text extraction/OCR tool | Prefer text-layer extraction first. Use OCR only for scanned PDFs. |
| `hwpx` | HWP/HWPX-capable Korean document skill or converter | Public Korean announcements often use HWPX. Preserve tables and numbered criteria. |
| `doc` / `docx` | Word/document skill or DOCX parser | Useful for business plans and application forms. |
| `hwp` | HWP-capable skill/converter fallback | Treat as fallback after PDF/HWPX when equivalent files exist. |
| `zip` | Archive extraction, then process contained files by priority | Pick announcement file before forms. |
| image | OCR-capable document tool | Use only when no machine-readable attachment is available. |

## Candidate External Capabilities

Agents may use any available equivalent tools. Good candidates include:

- A document skill for `.docx` or Word document reading.
- An HWP/HWPX skill for Korean public-sector documents.
- A PDF extraction or OCR MCP/tool.
- A browser or download tool for official attachment retrieval.
- A local conversion tool if installed in the user's environment.

When a tool is unavailable, state the limitation and fall back to the next available
processor instead of pretending the document was fully read.

## Extraction Contract

Regardless of processor, convert the attachment into this intermediate shape:

```json
{
  "file_path": "downloads/example.pdf",
  "file_type": "pdf",
  "source_url": "https://official.example/notice",
  "extraction_method": "pdf-text|ocr|hwpx-converter|docx-parser|manual",
  "text": "",
  "tables": [],
  "warnings": []
}
```

Then normalize into `schemas/announcement.schema.json` and, when comparing with a
business plan, `schemas/fit-analysis.schema.json`.

## Quality Checks

- Confirm that the processor read the actual announcement, not only an application form.
- Check whether tables were dropped or garbled.
- Preserve exact dates, amounts, eligibility limits, and exclusion clauses.
- If extraction quality is poor, include a warning in the final report.
