#!/usr/bin/env python3
"""
offer-letter-generator — role + compensation details → professional offer letter
Includes all legal clauses, equity details, benefits summary, contingency conditions,
at-will language, confidentiality reminders, legally sound for multiple jurisdictions
"""
import anthropic, json, re, sys
from datetime import datetime, timezone

SYSTEM = """You are a senior HR attorney and compensation specialist.
Generate a professional, legally-sound employment offer letter.

Requirements:
- Include all standard legal protections for the employer
- Be warm and welcoming in tone despite the legal precision
- Adapt jurisdiction-specific language based on the location provided
- Include placeholder brackets [LIKE THIS] for anything you don't have data for
- Never invent compensation numbers not provided

Return ONLY valid JSON — no markdown, no explanation.

{
  "letter_text": "full formatted offer letter text with proper line breaks",
  "key_terms_summary": {
    "role": "string",
    "start_date": "string",
    "base_salary": "string",
    "bonus_target": "string or null",
    "equity": "string or null",
    "pto_days": "string or null",
    "benefits_highlights": ["list"],
    "contingencies": ["background check","reference check","right to work verification","..."]
  },
  "clauses_included": ["at-will","confidentiality","ip_assignment","arbitration","non-disparagement","..."],
  "jurisdiction_notes": "any jurisdiction-specific adaptations made",
  "missing_information": ["fields you need before sending — bracketed in the letter"],
  "recommended_expiry": "typically 5-7 business days from send date",
  "legal_disclaimer": "This is a template — have your legal counsel review before sending"
}"""

def generate(
    candidate_name: str,
    role: str,
    department: str = "",
    start_date: str = "",
    base_salary: str = "",
    salary_currency: str = "USD",
    bonus_target_pct: int = 0,
    equity: str = "",
    pto_days: int = 0,
    benefits: list = None,
    reporting_to: str = "",
    location: str = "",
    jurisdiction: str = "US",
    company_name: str = "",
    company_signatory: str = "",
    extra_notes: str = ""
) -> dict:
    client = anthropic.Anthropic()
    context_parts = [
        f"Candidate: {candidate_name}",
        f"Role: {role}",
        f"Department: {department}" if department else "",
        f"Start date: {start_date}" if start_date else "",
        f"Base salary: {salary_currency}{base_salary}" if base_salary else "",
        f"Bonus target: {bonus_target_pct}% of base" if bonus_target_pct else "",
        f"Equity: {equity}" if equity else "",
        f"PTO: {pto_days} days" if pto_days else "",
        f"Benefits: {', '.join(benefits)}" if benefits else "",
        f"Reports to: {reporting_to}" if reporting_to else "",
        f"Location: {location}" if location else "",
        f"Jurisdiction: {jurisdiction}",
        f"Company: {company_name}" if company_name else "",
        f"Signed by: {company_signatory}" if company_signatory else "",
        f"Additional notes: {extra_notes}" if extra_notes else "",
        f"Date: {datetime.now(timezone.utc).strftime('%B %d, %Y')}"
    ]
    context = "\n".join(p for p in context_parts if p)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":f"Generate an offer letter:\n\n{context}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def save_letter(result: dict, output_path: str):
    from pathlib import Path
    Path(output_path).write_text(result.get("letter_text",""), encoding="utf-8")
    print(f"Offer letter saved to {output_path}")

def print_result(r: dict):
    terms = r.get("key_terms_summary",{})
    print(f"\n{'═'*60}")
    print(f"  OFFER LETTER GENERATED — {terms.get('role','?')}")
    print(f"{'═'*60}")
    print(f"\n  Key terms:")
    if terms.get("base_salary"): print(f"  Salary:    {terms['base_salary']}")
    if terms.get("bonus_target"): print(f"  Bonus:     {terms['bonus_target']}")
    if terms.get("equity"): print(f"  Equity:    {terms['equity']}")
    if terms.get("pto_days"): print(f"  PTO:       {terms['pto_days']}")
    benefits = terms.get("benefits_highlights",[])
    if benefits: print(f"  Benefits:  {', '.join(benefits[:4])}")
    contingencies = terms.get("contingencies",[])
    if contingencies: print(f"  Contingent on: {', '.join(contingencies)}")
    clauses = r.get("clauses_included",[])
    if clauses: print(f"\n  Clauses: {', '.join(clauses)}")
    missing = r.get("missing_information",[])
    if missing:
        print(f"\n  ⚠ Fill in before sending:")
        for m in missing: print(f"  [ ] {m}")
    print(f"\n  Expiry recommendation: {r.get('recommended_expiry','5 business days')}")
    print(f"  Jurisdiction notes: {r.get('jurisdiction_notes','')}")
    print(f"\n  ⚠ {r.get('legal_disclaimer','')}")
    print(f"{'═'*60}\n")
    print("  ─── LETTER PREVIEW (first 500 chars) ───")
    print(f"\n  {r.get('letter_text','')[:500]}...")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate professional employment offer letter")
    p.add_argument("candidate", help="Candidate full name")
    p.add_argument("role", help="Job title")
    p.add_argument("--company","-c",default="[COMPANY NAME]")
    p.add_argument("--salary","-s",default="")
    p.add_argument("--currency",default="USD")
    p.add_argument("--start",default="")
    p.add_argument("--bonus",type=int,default=0,help="Bonus target %")
    p.add_argument("--equity",default="")
    p.add_argument("--pto",type=int,default=0)
    p.add_argument("--location",default="")
    p.add_argument("--jurisdiction",default="US")
    p.add_argument("--department",default="")
    p.add_argument("--manager",default="")
    p.add_argument("--signatory",default="")
    p.add_argument("--output","-o",help="Save letter to file")
    p.add_argument("--json",action="store_true")
    a = p.parse_args()
    r = generate(a.candidate, a.role, a.department, a.start, a.salary, a.currency,
                 a.bonus, a.equity, a.pto, [], a.manager, a.location, a.jurisdiction,
                 a.company, a.signatory)
    if a.output: save_letter(r, a.output)
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_result(r)
