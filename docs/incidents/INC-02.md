# INC-02: retry advice stopped an inbound feed

**Written:** 2026-07-29, by the solution consultant who took the escalation.
**Severity:** an account's inbound EDI feed stopped for most of a working day.

## What happened

An Assist proposal answered an integrations question by advising the customer to disable a
webhook retry. The customer did. Their inbound feed depended on that retry to survive a
transient failure at their end, so the next transient failure dropped the messages instead of
retrying them.

The proposal was sent without a human reading it.

## What was checked before it went out

The proposal's confidence was high, and the answer was consistent with the knowledge article it
came from. The article was current and correctly sourced. The article was not wrong.

## What nobody checked

Whether the answer was safe for this account, as opposed to correct in general. The account is
Enterprise, and the account's own commitments list integrations as an area a human reviews.
That was recorded. Nothing read it.

## What was done afterwards

The retry was re-enabled and the backlog reprocessed. The customer was credited for the day.

The Head of Engineering's comment in the review, kept verbatim because the wording is the point:

> "Nobody skipped the check. There was no check."

## What would have caught it

Treating integrations as consequential, the way billing already is. The distinction between the
two areas is not written anywhere except in the per-account commitments, and nothing reads
those at the point the routing decision is made.

## Open

The question of which areas are consequential, and where that list should live so that a routing
decision can read it, is unresolved.
