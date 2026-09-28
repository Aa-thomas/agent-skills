---
name: to-tickets
description: Turn an approved plan, specification, issue, or conversation into grounded implementation tickets with explicit outcomes, contracts, failure checks, dependencies, and open decisions. Use when the user explicitly invokes $to-tickets to draft or publish a ticket breakdown. Draft first; publish only when the destination and breakdown are authorized.
---

# To Tickets

Turn a defined change into narrow, reviewable tickets that another agent can
implement without inventing product rules or rediscovering the repository.

## Establish scope and destination

Read the supplied plan, specification, issue, and relevant conversation context.
When a referenced issue or document is authoritative, read its full current body
and relevant comments before drafting.

Resolve the ticket destination from project instructions, an existing tracker, or
the user's request. If no destination is configured, draft the breakdown in the
response and identify the missing destination; do not depend on an unavailable
setup command or create a substitute tracker.

Drafting does not authorize publication. Reuse approval already given for the
same breakdown and destination, but obtain the user's decision before publishing
when either is not authorized. Do not close or modify a parent issue.

## Ground the tickets in the repository

Inspect the relevant implementation, tests, domain terms, ADRs, and existing
interfaces before naming reuse candidates or invariants. Distinguish:

- verified existing code and its responsibility;
- work that an earlier dependency ticket will introduce;
- genuinely new components; and
- anything that remains unverified because source access is unavailable.

Do not invent filenames, components, product decisions, guarantees, or evidence.
Preserve the source plan's scope, acceptance criteria, approval gates, and
blocking decisions unless the user authorizes a change.

## Build implementable slices

Prefer tracer-bullet tickets: each delivers a narrow, complete, demonstrable path
through the layers it actually needs. Size a ticket for one fresh implementation
context and give it only dependencies that truly prevent it from starting.

Use a separate prefactor ticket only when it makes a later behavior change safer
or materially simpler. For a wide mechanical migration that cannot land green as
vertical slices, use expand–migrate–contract: introduce the compatible form,
migrate callers in independently verifiable batches, then remove the old form
after every caller moves.

Every ticket must contain:

1. **Expected behavior and acceptance criteria.** State an observable result and
   pass/fail conditions, with a concrete demonstration when useful.
2. **Existing components or modules to reuse.** Name inspected owners and their
   responsibilities; label dependency-delivered, new, and unverified work.
3. **Interfaces and invariants.** Include only material data, API, identity,
   authorization, compatibility, lifecycle, and ownership rules.
4. **Failure cases and verification.** Pair important failures with observable
   rejection or recovery and a meaningful test or manual seam.
5. **Dependencies and unresolved decisions.** Separate ticket blockers, external
   gates, and open decisions. State whether each decision blocks implementation.

Use `ready-for-agent` only when required decisions and gates are resolved.
Otherwise retain `blocked` or `proposed`; do not turn uncertainty into readiness.

## Review the breakdown

Before publication, return a numbered proposal. For each ticket show:

- title;
- blockers or “None”;
- the end-to-end result it delivers; and
- status when a gate or unresolved decision affects readiness.

Ask for changes only when the breakdown, dependencies, or unresolved authority
needs the user's judgment. Reuse prior approval when a rewrite leaves those
material properties unchanged.

## Publish safely

When publication is authorized, read
[ticket formats and publication rules](references/ticket-formats.md). Publish
blockers first so later tickets can use real identifiers. Use native dependency
relationships where supported and explicit text links otherwise.

Before creating tickets, search the destination for the approved titles or a
stable source reference to avoid duplicates. If a write times out or returns an
uncertain result, read back the destination before retrying. Stop when the exact
publication state cannot be established.

Finish with created identifiers and links, dependency edges, status labels, and
anything left as a draft or blocked decision. Do not claim publication from local
files, a preview, or an unconfirmed response.

## Attribution

Adapted from [Matt Pocock's to-tickets](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md),
upstream file revision `e868c831fcfb1e124e010bcdf84a429ec879160f`,
under the accompanying MIT license. This adaptation retains explicit invocation
and requires the five ticket content areas above.
