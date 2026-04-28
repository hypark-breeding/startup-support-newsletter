# Procurement Opportunities

Use this workflow when the user asks for public procurement, contracts, bids, RFPs,
ordering plans, public purchase opportunities, or municipal tender notices.

## Sources

- Prefer the official Data.go.kr KONEPS bid notice API for structured search.
- Use KONEPS (`g2b.go.kr`) as the official portal and final source of truth.
- Use municipal contract portals such as Seoul Contract Market for local ordering plans,
  bid notices, public quote requests, opening results, and public purchase information.

## Required Configuration

For live KONEPS API calls, ask for `DATA_GO_KR_SERVICE_KEY` if it is missing. Do not
commit the key. Use browser or Crawl4AI extraction for public pages when API access is not
configured, and label results as page-extracted.

## Classification

Normalize procurement items as `procurement_opportunities` and keep them separate from
startup grants.

Recommended fields:

- title
- buyer
- procurement_channel: `g2b|data_go_kr_api|municipal_contract_portal|other`
- procurement_type: `service|goods|construction|software|research|other`
- bid_notice_no
- budget
- bid_deadline
- contract_method
- eligibility
- source_url
- detail_url
- confidence

## Ranking

Prioritize:

- Open bid deadline.
- Strong fit to the founder's product, geography, references, certifications, and team size.
- Clear RFP or specification attachment.
- Lower barrier opportunities such as small service bids, PoC, software, research, or public purchase.

## Safety

Do not guarantee bid eligibility or award likelihood. Separate confirmed disqualifiers from
fixable preparation gaps, and tell the user when a procurement specialist or legal review is needed.
