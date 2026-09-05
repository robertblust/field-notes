# Field notes

Problems that took real work to understand, written down while the reasoning was still
fresh. One file per problem.

These are not tutorials and not postmortems. Nothing here broke in production; mostly
something looked or sounded wrong, resisted the obvious explanation, and turned out to be
something else. The notes exist because the next person to meet the same symptom — often
me — will arrive holding the same wrong hypothesis I did.

## The shape of an entry

Every note carries the same five parts, and the second is the one that makes it worth
publishing:

| | |
|---|---|
| **Symptom** | in the words someone would actually search for, not the words of the diagnosis |
| **What it wasn't** | each wrong explanation, with the evidence that killed it |
| **Root cause** | what was actually happening |
| **Fix** | at the level the cause lives at, which is not always the level the symptom appears at |
| **How it was verified** | the measurement, and what would have falsified it |

Most write-ups keep only the third and fourth. That loses the expensive part. A wrong
diagnosis that survived a real measurement is worth more than the answer, because the
answer is obvious once you have it and the wrong turn is not.

## Notes

- [An ElevenLabs clip that clicks at the end](notes/elevenlabs-clip-ends-on-a-click.md) —
  two unrelated defects wearing one symptom, and only one of them is damage to the file.

## Checking

`python3 verify.py` resolves every relative link in every note. External URLs are
deliberately not fetched — a checker that hits the network fails on someone else's outage,
and a suite that cries wolf is one people stop reading. CI runs the same command. The
`conventions` job, called from robertblust/conventions at the pinned tag, holds the vendored
copy to its release and every Markdown file here to `conventions/WRITING.md`.

## License

[CC BY 4.0](LICENSE). Use it, quote it, build on it; credit it. The prose is the artifact
here, which is why this is a content license rather than the Apache 2.0 the code
repositories carry.
