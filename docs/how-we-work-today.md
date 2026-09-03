# How the {{TRACK_UPPER}} work gets done today

Written by whoever was asked to write it, at some point, and not revised since. It is the only
description of the process that exists.

> **A note for the reader.** This is not a specification. Parts of it are optimistic, parts are
> contradicted by the tracker and by the write-ups in `docs/incidents/`, and the parts that
> describe judgment calls do not say who makes them.

## The rough shape

1. Something arrives. It might be a request, a report, a question, or a decision somebody needs.
2. Whoever picks it up works out what it involves, mostly by asking someone who was there last
   time.
3. They do the work.
4. Someone else looks at it, when there is time.
5. It ships, or it is handed on, or it stalls and nobody notices for a while.
6. If it goes wrong, that surfaces later, usually from outside.

## Where it is written down

| Thing | Where it lives | Kept current? |
| :- | :- | :- |
| What is in flight | the tracker | Partly. Statuses are not consistent and some are stale. |
| What was decided | Mostly nowhere. Some in the tracker's notes column. | No |
| Why it was decided | In the heads of the people involved | No |
| What was checked before it shipped | Whatever the pull request or handoff note happens to say | No |
| What went wrong afterwards | `docs/incidents/`, written after the fact | Only for incidents big enough to write up |

## The judgment calls nobody wrote down

These get made every week. The process does not say who makes them, on what evidence, or what
happens when the answer is unclear.

- Whether a thing is small enough to do without asking anyone.
- Whether a source is current enough to rely on.
- Whether something needs review, and who is qualified to give it.
- When to stop trying and escalate.
- What counts as done.

## What people say about it

Kept verbatim, because the wording matters.

> "It works fine until the person who knows leaves." Support engineer, retrospective note.

> "I can find out what we did. I cannot find out why." Analytics lead, on the tracker.

> "Nobody skipped the check. There was no check." Head of Engineering, on `INC-02`.

## The two incidents

Both came out of the Assist pilot. Both are written up in `docs/incidents/`. Neither had a
control that would have caught it, which is the point of writing them up here.

| Incident | What happened |
| :- | :- |
| `INC-01` | A superseded refund window reached a customer. |
| `INC-02` | Advice to disable a webhook retry stopped an account's inbound feed. |

## If this document is wrong

It probably is, in places. The tracker and the incident write-ups are the record of what
happened; this is one person's account of how it is supposed to happen. Where they disagree,
the record wins.
