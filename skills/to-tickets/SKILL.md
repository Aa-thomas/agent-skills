---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Check existing implementation and contracts

Inspect the relevant existing implementation before naming components, modules, interfaces, or invariants to reuse. Reuse previously verified context when still current. If access is unavailable, explicitly record what remains unverified; do not invent existing modules. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### Required content in every ticket

Every ticket, including local files, tracker issues, and rewrites of existing tickets, must include:

1. **Expected behaviour and explicit acceptance criteria.** Describe the learner/user or system outcome and observable pass/fail criteria. Include a concrete demonstration when useful.
2. **Relevant existing components or modules to reuse.** Name verified reuse candidates and their responsibility. Distinguish existing code from work supplied by a dependency and genuinely new work. If none exist, say so; if not inspected, say unverified.
3. **Interfaces and rules that must remain true.** State the relevant data/API contracts, identity, compatibility, authorization, lifecycle, and other invariants. Include only those material to the slice.
4. **Important failure cases and how to verify them.** Pair concrete failures with an observable recovery or rejection outcome and the appropriate test or manual verification seam. Avoid tests that merely mirror implementation.
5. **Dependencies and decisions still unresolved.** List real blocking tickets and external gates separately from open implementation decisions. State whether a decision blocks implementation, who/what must resolve it when known, and "None known" only when supported.

Do not fill gaps with invented decisions. Preserve scope, acceptance criteria, dependency edges, and approval gates when rewriting existing tickets unless the user authorizes a change. A rewrite or design reference does not approve a gated proposal. Do not label a ticket ready to implement while an unresolved required product decision still blocks it.

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown. Reuse approval already given in the conversation; an authorized rewrite of an approved breakdown does not require another quiz unless scope or blocking edges materially change.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. Apply the `ready-for-agent` triage label only when the required decisions and gates permit it; retain explicit blocked/proposed status otherwise.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**Status:** ready-for-agent | blocked | proposed (choose based on actual gates)

## Expected behaviour

The end-to-end outcome from the user's perspective. Include a concrete demonstration where useful.

## Acceptance criteria

- [ ] Observable criterion 1
- [ ] Observable criterion 2

## Existing components and modules to reuse

- Verified component/module and responsibility; distinguish dependency-delivered and new work.

## Interfaces and invariants

- Contract or rule that must remain true.

## Failure cases and verification

- Failure scenario → expected recovery/rejection → verification method.

## Blocked by

- Blocking ticket references and external gates, or "None (can start immediately)".

## Unresolved decisions

- Decision, whether it blocks implementation, and resolution needed; or "None known".

</local-ticket-template>

<issue-template>

## Parent

Reference to the source issue, if applicable.

## Expected behaviour

The end-to-end outcome from the user's perspective. Include a concrete demonstration where useful.

## Acceptance criteria

- [ ] Observable criterion 1
- [ ] Observable criterion 2

## Existing components and modules to reuse

- Verified component/module and responsibility; distinguish dependency-delivered and new work.

## Interfaces and invariants

- Contract or rule that must remain true.

## Failure cases and verification

- Failure scenario → expected recovery/rejection → verification method.

## Blocked by

- Blocking ticket references and external gates, or "None (can start immediately)".

## Unresolved decisions

- Decision, whether it blocks implementation, and resolution needed; or "None known".

</issue-template>

Prefer stable component/module names and verified source links for reuse and contracts; do not prescribe speculative file paths or a layer-by-layer implementation plan. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.


## Attribution

Adapted from [Matt Pocock's to-tickets](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md), upstream file revision `e868c831fcfb1e124e010bcdf84a429ec879160f`, under the accompanying MIT license. This personal adaptation requires the five ticket sections above. Explicit invocation is retained through `agents/openai.yaml`.
