# Fixtures

The PDLC track's seed material. Everything here is fictional and describes Portwell
Software, a fictional B2B vendor preparing an AI-assisted customer-support product.

Two properties matter:

1. **Identifiers are shared.** Accounts, policies, people, and product areas match the other
   three tracks. Tests and cross-track references key on those strings.
2. **The material is not clean.** Duplication, missing sources, superseded versions, and
   contradictions are seeded on purpose. Finding them is the work; tidying them away removes
   the exercise.

<!-- TRACK SEED: describe this track's fixture files, what each is for, and which seeded
     problems are deliberate. -->

## Seeded problems

Each track's fixtures carry at least one instance of each family below, visible and available
to work on. Module 4 adds held-out instances the track has not seen.

| Family | Looks like |
| :- | :- |
| Stale context | A superseded artifact that is still reachable and still cited |
| Missing provenance | A claim, field, or answer with no source |
| Specification gaming | A threshold, test, or classification changed to make a miss pass |
| Weak routing | A consequential change treated as a routine one |
| Recovery failure | A retry loop with no escalation, or state corrupted rather than reset |
