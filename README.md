# offer-letter-generator

> **Role + compensation details → professional offer letter.** All legal clauses included, warm tone, equity and benefits sections, jurisdiction-adapted (US, UK, EU). Exports to text file.

[![PyPI](https://img.shields.io/pypi/v/offer-letter-generator?style=flat)](https://pypi.org/project/offer-letter-generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install offer-letter-generator

python -m offer_letter_generator "Ahmed Hassan" "Senior Engineer" \
  --company "Acme Corp" \
  --salary "120000" --currency USD \
  --bonus 15 --equity "0.1% over 4-year vest" \
  --pto 25 --start "2025-07-01" \
  --location "Cairo, Egypt" --jurisdiction EG \
  --output offer_ahmed.txt
```

## Clauses automatically included

At-will employment · Confidentiality · IP assignment · Arbitration ·
Non-disparagement · Contingency conditions (background check, right to work) ·
Benefits summary · Equity vesting schedule

## Jurisdiction support

Adapts language for: US (state-level variations), UK, Egypt, UAE, EU countries.
Flags any fields that need local legal review.

⚠️ Have legal counsel review before sending.

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
