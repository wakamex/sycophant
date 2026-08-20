# Publication boundary

This focused repository contains the evidence needed to inspect the public pilot without publishing the entire source research workspace.

## Included

- frozen conditions, routes, estimand, shuffle seed, and outreach heuristic
- exact prompt template with placeholders
- derived scores for all 15 matched route-item comparisons
- route summaries and the one available same-position ranking check
- run, scorer, and execution provenance
- dependency-free analysis and figure-generation scripts

## Not included

### Restricted LMCA records

No requested or restricted LMCA record is present. If access is granted later, its policy prohibits public sharing and requires care around model providers and training retention. Those records should remain in a private, access-controlled workspace.

### Third-party papers and datasets

The source workspace contains downloaded PDFs, extracted paper text, website snapshots, and dataset archives from several projects. Their public availability does not create one uniform right to redistribute them. This repository links to the LMCA paper and identifies its public table entries instead.

The research note for Pang et al. (2025) records citation metadata, links, license, and a short relevance summary. It does not redistribute the article text.

### Raw agent traces

The source workspace records full agent requests, events, results, provider metadata, system instructions, run identifiers, and local execution paths. Those files are useful for private auditing but disclose much more operational information than is needed to evaluate this result. They also mix material governed by different provider terms.

### Unrelated and exploratory work

The source workspace includes abandoned diagnostics, incomplete attempts, benchmark surveys, CEO-framing experiments, scraped public-source research, and unreviewed local changes. Publishing them together would obscure which decisions were frozen before this pilot and increase the chance of accidental disclosure.

### Full model responses

This report uses one short qualitative comparison and publishes the numeric outcomes. Full responses remain in the private archive because they sit inside the raw provider traces and are not required to reproduce the headline estimand. They can be reviewed or released separately after a provider-terms and privacy check.

## Private archive

The private source run is identified in [data/provenance.json](data/provenance.json). Its checksum manifest passed verification before this public package was prepared.
