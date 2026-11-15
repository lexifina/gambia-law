# The Gambia: law history in git


The law of The Gambia as a git history: one file per section, one commit per version on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every line; `git log` lists every change to a section; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is The Gambia's national law, which global-law reads at `gambia/national/acts/`.

**What is in it now:** one text, the Constitution of the Republic of The Gambia, 1997, as the National Assembly's 2002 reprint prints it (with Act No. 6 of 2001): the preamble, 222 section files and the two Schedules, in one version, which is not today's text (see below). [`constitution/README.md`](constitution/README.md) lists every provision; [`data/versions.json`](data/versions.json) gives the version and its PDF's sha256.

The Constitution is in `constitution/`, one file per section: `constitution/sec-025.md` is section 25 (freedom of speech, conscience, assembly, association and movement) and `sec-012-a.md` is section 12A; sections 51 to 57, deleted in 2001, share `sec-051.md`.

The text is in English, the official language, as the reprint prints it, typing errors included.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to section 25 of the Constitution | `git log -p --word-diff -- constitution/sec-025.md` |
| Who is credited with each line of section 25? | `git blame constitution/sec-025.md` |
| Every version of the Constitution, with the day each is dated | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- constitution ':!*/README.md'` |
| Section 25 as the record holds it on 1 January 2020 | `python tools/on.py 2020-01-01 constitution 25` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Gambian law](https://global-law.lexifina.com/v1/try_claude?country=gambia)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=gambia)**: the same question in ChatGPT.
- **[Search Gambian law on our site](https://lexifina.com/law?country=gambia&q=freedom+of+speech)**: a search for "freedom of speech", with each provision's text and its versions, no account needed.
- **[Developer REST API](https://global-law.lexifina.com/v1/search_law?query=freedom+of+speech&jurisdiction=gambia)**: the same search as JSON, with no key. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add gambia/national/acts
python3 tools/law.py show 2026-01-01 gambia/national/acts/constitution/sec-025.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, Africa/Banjul, on the day its version took effect, and carries that day in its `In-force:` trailer:

- an Act with no day of its own comes into operation on its publication in the Gazette (Constitution, section 100(7)); no Gazette dates are online, so no amending Act can be dated and none is applied;
- the one version is dated 3 April 2006, the creation date of the reprint's PDF; the reprint itself is dated only "2002". It is not the day the text took effect.

That version is credited to the publisher, `National Assembly of The Gambia (assembly.gm)`, as the oldest version available, not to a law: no earlier version is available as text.

## How it is checked

- `tools/build.py` writes the history from one corpus file in one pass, and the same corpus always gives the same commit hashes; its sha256 is in [`data/corpus.sha256`](data/corpus.sha256).
- `tools/check_repo.py` reads every version back from git on the day it took effect, compares it file by file with the corpus, and checks every commit's trailers and that `main` has no merge commits and no dates going backwards or in the future.
- [`REPRODUCE.md`](REPRODUCE.md) records that these checks have not yet been run for this build and that no second build has been compared.

## What it does not show

- **Today's Constitution.** The amendments of 2004, 2006, 2007, 2015 and 2017 are online only as scans with no text layer, and no OCR was used, so none is applied; the 2009 amending Act could not be downloaded.
- **Section 1 as the courts read it.** The reprint prints "Sovereign Secular Republic", which the Ministry of Justice reports the Supreme Court held unconstitutional.
- **The Constitution as enacted in 1997.** The reprint already holds Act No. 6 of 2001 and does not give the text it deleted.
- **Some section boundaries.** Sections 154, 179, 181, 193, 195 and 226 have no readable number in the printed margin, so their text runs on at the end of the preceding section's file; marginal notes, chapter headings and page numbers are not kept.
- **Any other Gambian law.** No other Act, no subsidiary legislation and no case law; the National Assembly's site listed 537 entries under Acts in October 2026, but none can be dated reliably yet.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [National Assembly of The Gambia](https://assembly.gm/constitution) | The Constitution, 2002 reprint, as a PDF with a text layer | no, one reprint | The text of the one version; retrieved 30 October 2026 |
| [Ministry of Justice](https://www.moj.gm) | The same reprint; the Constitutional Review Commission's Explanatory Memorandum (2020) | no | The memorandum reports the Supreme Court's ruling on section 1 |

## Licence

See [`LICENSE`](LICENSE). The National Assembly states no licence and no restriction on reuse; whether the Copyright Act 2004 excludes official texts has not been verified. Lexifina's own contributions (the arrangement of the history, the commit messages and the tools) are CC0 1.0.

No model wrote, translated or corrected legal text, and no model runs at build time; the scripts were written by an AI model (see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
