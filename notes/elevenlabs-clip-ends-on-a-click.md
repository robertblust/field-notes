# An ElevenLabs clip that clicks at the end

*August 2026. Text-to-speech narration for a slide deck, `eleven_v3`, MP3 out of the API
written straight to disk.*

## Symptom

Some narration clips ended on an audible click. Not all of them, with no obvious pattern —
"sometimes", which is the word that makes a bug expensive. It sounded unprofessional in a
way that was immediately obvious to a listener and completely invisible in the code, which
did nothing to the audio: it wrote the API's bytes to a file.

## What it wasn't

### Not a decoder artifact

The first thing to rule out, because it costs nothing. Decoding with `afconvert` and again
with `lame --decode` gave the same result, and — the actual control — **7 of 22 clips
decoded cleanly through the same decoder**. A decoder that manufactured clicks would have
manufactured them everywhere.

### Not (only) truncation

The clip ended mid-waveform. Sample-level, at the point of the cut:

```
sample 1408246   -3449
sample 1408247   -2119
sample 1408248     -42     ← full amplitude to digital silence in 2 samples (~45 µs)
```

A textbook truncation click: −18 dBFS one moment, nothing the next. A 5 ms raised-cosine
fade brought that step from −18.2 dBFS to −44.8 dBFS, a 26 dB improvement, and the
discontinuity was gone by every measurement.

**The click was still there.** That was the turning point, and it arrived only because
someone listened to the fixed file instead of trusting the number.

### Not something regeneration would fix

Regenerating the same text at the same settings produced a clip that ended in a clean
natural taper — `1697 → 1253 → 741 → 405 → 271` — with no truncation at all.

**It still clicked.** Two fixes had now each removed the truncation, by different means, and
neither had removed the click. Truncation was real, measurable, worth fixing, and not the
answer.

### Not the loud burst at 28.7 s

A discontinuity scan flagged a "burst of near-full-scale noise erupting out of silence"
mid-clip, at 267× the local median. It looked damning.

It was ordinary speech. The scan compared each point against its *local* neighbourhood, and
a consonant after a pause always wins that comparison. Measured against the **whole file**,
where speech routinely peaked at 20000–29000, the burst was unremarkable. A ratio needs a
denominator you chose on purpose.

### Not 22 of 22 clips

An early audit reported every clip as defective. It was an artifact of the detector: it
found the last sample above a threshold `T`, then reported the amplitude there — so a clip
with no truncation still reported a value just above `T`. **The metric was floored at its
own threshold and I read the floor as data.** Lowering `T` separated the population and the
real count was about half.

## Root cause

**Two unrelated defects wearing one symptom.**

**1. Truncation.** The rendered audio sometimes stops mid-waveform instead of decaying. It
is a per-generation lottery: the clip that started this measured a step of 2077,
regenerating it gave a clean taper, and regenerating the whole deck moved the defect onto
three *different* clips. Nothing in the request predicts it.

**2. A detached final consonant.** At `style: 0.45` the model over-articulates a word-final
plosive into a release that separates from the word — a 20 ms stop closure, then a **120 ms
burst of noise**. The ear hears that as a click rather than as a consonant.

The second one is **speech, not damage**. This is the whole finding. It survives any amount
of fading because there is nothing malformed to repair, and it reproduces on regeneration
because the model is doing what it was asked to do.

The clinching experiment was destructive: cut the burst out entirely. The click vanished —
and so did the /t/. The word `ausgeschaltet` became `ausgeschalte`, and a listener
immediately called it unnatural. That is what proved the burst *was* the click, rather than
merely accompanying it.

## Fix

Each cause at its own level, because they are not the same kind of thing.

**Truncation → repair the file.** Decode, apply a 5 ms raised-cosine fade at the cut,
append 150 ms of silence, re-encode. Deterministic, and applies to already-generated audio
with no API cost.

**Detached release → change the request, then treat the remainder.** `style: 0.45 → 0.0`
shortens the release from 120 ms to 20–70 ms at the source. What is left gets an
exponential decay that **keeps the attack and collapses the tail** — 35 ms time constant,
6 dB trim. Keeping the attack is what preserves the consonant; that was learned from the
failed experiment above.

Two guards keep the treatment off real speech, and both are needed. A final word after a
rhetorical pause has the *same shape* as a detached release and differs only in scale:

| | duration | level vs clip peak |
|---|---|---|
| consonant release | under 200 ms | at least 8 dB down |
| final word after a pause | 320–430 ms | within 5 dB |

Treating one of those as a consonant would chew the last word of the slide. Either test
alone lets one through.

Only clips that actually have a defect are re-encoded; the rest are written exactly as the
API sent them, which keeps a second lossy generation off audio that does not need one.

## How it was verified

Across three repositories, 86 clips:

| | before | after |
|---|---|---|
| truncated | 20 (worst step **8215**) | **0** |
| detached burst | 17 (up to 195 ms) | 9, all under 80 ms and attenuated 6–9 dB |

Every clip was measured under **two independent decoders**, which matters more than it
sounds: `lame` honours the MP3 gapless tag and `afconvert` does not, so they disagreed
about where a file ends. On two clips that disagreement was the difference between
"defective" and "fine" — an early count of 3 affected files was really 5. A single-decoder
result was decoder-dependent and I had stated it as fact.

And then a person listened to all of it, in both languages, start to finish.

## What generalises

**The ear is the oracle; the meter is an instrument.** Three times a measurement said the
problem was solved and a listener said otherwise. Every one of those was a real
improvement to a real defect that simply was not the defect being complained about.

**A ratio is only as good as its denominator.** "267× the local median" and "unremarkable
against the whole file" described the same 60 ms of audio.

**A thresholded detector reports its threshold as data.** If every clean case comes back
just above `T`, the population has not been separated — the floor has been measured. Vary
the threshold and watch whether the ranking survives.

**One symptom can be two defects,** and fixing either one completely will look like failure
right up until you fix the other.

**Some defects are not damage.** When the artifact reproduces on regeneration and resists
every repair, stop repairing the output and change the request. The fix belongs at the
level the cause lives at, which is not always the level the symptom appears at.

**Decoders disagree about the ends of files.** Gapless metadata is optional and honoured
inconsistently. Verify under more than one.
