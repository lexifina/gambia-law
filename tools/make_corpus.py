"""units.json (from parse.py) -> corpus.json for The Gambia. No network."""
import json, sys, hashlib
units = json.load(open(sys.argv[1], encoding='utf8'))
sha = hashlib.sha256(open(sys.argv[2], 'rb').read()).hexdigest()
URL = 'https://national-assembly.ams3.digitaloceanspaces.com/key-documents/VW6fALCcLURgQrtl18AAJfYSVcKpNbBycKo7IxOD.pdf'
C = {
 "country": {"code": "GM", "name": "The Gambia", "slug": "gambia", "lang": "en", "tz": "Africa/Banjul", "future_branch": "future",
  "publisher": {"name": "National Assembly of The Gambia (assembly.gm)", "email": "assembly@assembly-gm.invalid"},
  "default_in_force_rule": {"text": "Constitution s.100(7): an Act comes into operation on its publication in the Gazette. No Gazette dates are online, so no amending Act is applied.", "source": "https://assembly.gm/constitution"},
  "licence_note": "Text of the Constitution of The Gambia 1997, 'reprinted 2002', as published by the National Assembly of The Gambia (assembly.gm/constitution); the site states no reuse restriction."},
 "sources": [{"name": "Constitution of the Republic of The Gambia, 1997, 'Reprined 2002' (National Assembly)", "url": URL, "retrieved": "2026-10-30",
  "licence": "No licence or reuse restriction stated; assembly.gm robots.txt allows all agents. The same text is on moj.gm.",
  "notes": "PDF sha256 " + sha + "; 142 pages, text layer read with PyMuPDF."}],
 "laws": {"publisher-oldest": {"label": "National Assembly of The Gambia", "title": "Constitution of The Gambia, 1997 (reprint 2002), oldest version available", "kind": "publisher",
  "enacted": "2006-04-03", "published": "2006-04-03", "url": URL, "temporary_until": None, "restores": None, "note": None}},
 "applies": [],
 "decisions": [
  "One version only, credited to the publisher as 'oldest version available'. The PDF carries no day-level date: the reprint is dated '2002' and the file's own creation date is 3 April 2006, which is used as the version date. It is NOT the in-force date of the text.",
  "The reprint includes Act No. 6 of 2001 and not the later amendments (2004, 2006, 2007, 2015, 2017), which exist only as scans. It still prints 'Sovereign Secular Republic' in s.1, which the Supreme Court is reported to have held unconstitutional (MoJ, CRC Explanatory Memorandum 2020). It is therefore not today's text.",
  "One file per section, plus the preamble and the two schedules. Headings come from the printed Arrangement of Sections; marginal notes, chapter and part headings and page numbers are not kept. Text is as printed, including its typing errors; only spacing and quote/dash forms were normalised.",
  "Sections 51 to 57 are one file (the reprint prints them as deleted by No. 6 of 2001). Sections 154, 179, 181, 193, 195 and 226 have no readable number in the printed margin, so their text runs on at the end of the preceding section's file.",
  "Paragraph markers such as (a) and (1) are as printed; the reprint sometimes mislabels them (for example s.5), and that is kept."],
 "ai_use": ["none"],
 "acts": [{"slug": "constitution", "short": "Const.", "title": "Constitution of the Republic of The Gambia, 1997 (reprinted 2002)", "url": URL, "first_law": None, "earlier_laws": [],
  "versions": [{"from": "2006-04-03", "source_url": URL, "sha256": sha, "units": units, "credits": {k: ["publisher-oldest"] for k in units},
   "note": "Reprint of the 1997 Constitution including Act No. 6 of 2001, as published by the National Assembly. Dated by the PDF's creation date; later amendments are scans only and are not applied."}]}]
}
json.dump(C, open('corpus.json', 'w', encoding='utf8', newline='\n'), ensure_ascii=False, indent=1)
print(len(units))
