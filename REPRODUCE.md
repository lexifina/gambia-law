# How this repository was made (The Gambia)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Constitution of the Republic of The Gambia, 1997, 'Reprined 2002' (National Assembly) | <https://national-assembly.ams3.digitaloceanspaces.com/key-documents/VW6fALCcLURgQrtl18AAJfYSVcKpNbBycKo7IxOD.pdf> | 2026-10-30 | No licence or reuse restriction stated. The same text is on moj.gm. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the Republic of The Gambia, 1997 (reprinted 2002) | 1 | 2006-04-03 to 2006-04-03 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 1 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (Africa/Banjul) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constitution s.100(7): an Act comes into operation on its publication in the Gazette. No Gazette dates are online, so no amending Act is applied. https://assembly.gm/constitution

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `5e95291007ce1eec758b9d3451d1b42a3a4934426b114bcf1e29ac5eb89bd7fb` (284273 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- One version only, credited to the publisher as 'oldest version available'. The PDF carries no day-level date: the reprint is dated '2002' and the file's own creation date is 3 April 2006, which is used as the version date. It is NOT the in-force date of the text.
- The reprint includes Act No. 6 of 2001 and not the later amendments (2004, 2006, 2007, 2015, 2017), which exist only as scans. It still prints 'Sovereign Secular Republic' in s.1, which the Supreme Court is reported to have held unconstitutional (MoJ, CRC Explanatory Memorandum 2020). It is therefore not today's text.
- One file per section, plus the preamble and the two schedules. Headings come from the printed Arrangement of Sections; marginal notes, chapter and part headings and page numbers are not kept. Text is as printed, including its typing errors; only spacing and quote/dash forms were normalised.
- Sections 51 to 57 are one file (the reprint prints them as deleted by No. 6 of 2001). Sections 154, 179, 181, 193, 195 and 226 have no readable number in the printed margin, so their text runs on at the end of the preceding section's file.
- Paragraph markers such as (a) and (1) are as printed; the reprint sometimes mislabels them (for example s.5), and that is kept.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
