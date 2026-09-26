# Principles and their limits

Use these sources to explain a design choice or resolve a tradeoff. They inform
the skill's existing rules; they are not separate frameworks to install or extra
checklists to apply to every change.

- **John Ousterhout: deep modules and information hiding.** Prefer a small,
  useful public interface that hides substantial implementation knowledge.
  Single-use modules can earn their place this way. Review interface complexity
  alongside line counts; neither large modules nor many tiny helpers are goals.
  [Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign)
- **Scott Wlaschin: model valid states explicitly.** When fields are related,
  represent the permitted combinations as distinct variants with required data.
  Keep runtime validation for external input and test the enforcing behavior;
  adding a type name alone does not guarantee correctness.
  [Designing with types](https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/)
- **Kent Beck and Martin Fowler: separate refactoring from changing behavior.**
  Restructure in small steps with passing behavioral checks, then introduce the
  intended behavior change. Separate steps need not mean separate PRs when one
  coherent change remains easy to review.
  [Preparatory refactoring and the two hats](https://martinfowler.com/articles/preparatory-refactoring-example.html)
- **Dan North: CUPID.** Familiar language and local conventions reduce the work
  needed to understand code. Prefer predictable, composable, domain-oriented
  operations; justify departures from established patterns. Transfer the intent
  across languages rather than imposing the same class or directory structure.
  [CUPID](https://dannorth.net/blog/cupid-for-joyful-coding/)
- **OpenAI: actionable enforcement.** Explain the permitted fix in a failing
  check's diagnostics. Use a real recurring failure to justify a custom rule;
  reuse existing tooling and keep the project's own architecture authoritative.
  The article's particular layer structure is not a universal requirement.
  [Harness engineering](https://openai.com/index/harness-engineering/)
- **Jon Gjengset: selective reliability practices.** Preserve decision rationale
  and acknowledged limitations. Scale verification to the consequence of failure:
  generated test cases or representative load measurements can help where ordinary
  examples miss important behavior. Use native tooling and stable evidence; do not
  import Rust-specific tools or impose every technique on routine changes.
  [Towards Impeccable Rust: author's slides](https://jon.thesquareplanet.com/slides/towards-impeccable-rust/export.pdf)

Stronger testing needs a concrete target: the invariant, failure mode, or measured
budget it protects. Start with the relevant failure case and existing test tools.
Expand only when an identified risk or missing evidence warrants the added cost.
