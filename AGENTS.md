<!-- conventions · v1.6.0 -->
Shared conventions of the robertblust, guestgraph and companygraph organizations live in
`conventions/`, vendored from robertblust/conventions at the release `conventions.json`
names. Read them before writing or committing anything here.

- `conventions/WRITING.md` — how we write: one voice, three registers, English and German.
- `conventions/WORKING.md` — how we work with git and GitHub.
- `conventions/REPOSITORIES.md` — the family: what each repository is and what pins what.
- `conventions/WRITER.md`, `conventions/TRANSLATOR.md`, `conventions/GLOSSARY.md` — the two roles that
  make a text, and the terms they keep.

Everything below this block is this repository's own. `sh conventions/conventions-sync check`
says whether the copy matches the release, `sync` brings it to the release the pin names, and
`sh conventions/conventions-check` holds this repository's own Markdown to `WRITING.md`. Edit
a shared file in robertblust/conventions, never here.
<!-- end conventions -->

# robertblust/field-notes — working conventions

Problems that took real work to understand, one file per problem, in the five-part shape the
README gives: symptom, what it was not, root cause, fix, how it was verified. The README is
the manual for writing one; this file is only what an agent needs before touching anything
here.

## Checks

Two jobs, both required by the ruleset on `main`: `verify`, which runs `python3 verify.py` and
resolves every relative link in every note, and `conventions`, called from
robertblust/conventions at the pinned tag and shown by GitHub as `conventions / conventions`.
External URLs are not fetched on purpose; the README says why. Everything about how to write
and how to work with git is in `conventions/`.

