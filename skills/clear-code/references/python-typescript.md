# Python, TypeScript, and staged migrations

Use installed versions and existing project commands. Inspect their configuration
before suggesting flags or editing CI. These are tool options, not a mandatory
dependency bundle. Do not replace a working checker just to match this list.

## Python

- Use the current formatter/linter; Ruff can check branching with `C901` when
  enabled. Set a measured threshold deliberately rather than assuming its default
  matches the project's policy.
- Use the existing Pyright or mypy setup. Check includes, excludes, overrides,
  and whether newly added packages are actually checked. Tighten selected public
  boundaries before promising an immediate whole-repository strict conversion.
- Add Import Linter only if named package boundaries need automated enforcement.
  For example, domain decisions can accept values while an application operation
  coordinates storage and external calls; the domain package should not import
  its concrete HTTP or storage adapter. Avoid late imports that only hide cycles.
- Use existing tests for state transitions, invalid values, denied operations,
  and relevant retry/conflict behavior. Hypothesis stateful testing is useful
  when sequences of actions expose failures; it is not required for simple CRUD.
- Validate external data at entry points using the project's established schema
  mechanism. Keep a durable rule near its domain operation even when a transport
  schema also rejects malformed input.
- Represent state-dependent fields with explicit variants. If Pydantic is already
  used at the boundary, discriminated unions can validate the selected variant's
  required data. Plain Python annotations alone do not enforce these constraints
  at runtime; retain the project's validation and type-checking mechanisms.

For docstrings, follow the project's established style and PEP 257's public
contract guidance. Add structured argument/result/error sections when they carry
useful information; do not duplicate type annotations just to fill a template.
Selected stable Ruff docstring rules can check consistency if Ruff is adopted.
Consider pydoclint only when mismatches between structured docstrings and code
justify it: absent and prose-only docstrings are skipped by default, so inspect
coverage before claiming protection. Check overlap and stability before enabling
Ruff's pydoclint-derived rules; some require preview mode. Python's built-in
`doctest` can verify runnable usage examples when such examples are useful.

## TypeScript and Svelte

- Prefer TypeScript `strict` for new checked packages. Incremental adoption may
  need explicit boundaries around legacy code. Confirm that framework files,
  workspace packages, and generated clients are included in the relevant checks.
- Use discriminated unions for meaningful state variants and exhaustive handling
  where appropriate, so adding a state exposes callers that need updating. Keep
  runtime validation at external boundaries; a type assertion cannot supply it.
- Use existing ESLint support for `complexity` and nesting when appropriate.
  Type assertions, `any`, ignored errors, and broad exclusions must not replace
  boundary validation or bypass a newly adopted rule.
- Use dependency-cruiser or a comparable existing tool for dependency boundaries
  and cycles when those rules warrant a graph check. Configure module aliases
  and file extensions so the checked graph matches the actual application.
- Group related components, state, API access, and tests by feature when useful.
  Keep server-owned decisions out of UI event handlers and client state stores.
  Local form validation may improve feedback; the authoritative operation still
  validates what it accepts.
- For Svelte, run the project's framework-aware check as well as relevant tests;
  ordinary TypeScript checks may not cover component templates. In server-rendered
  apps, do not keep per-user state in shared server module variables.
- Test a changed user flow and its relevant loading, empty, error, or conflict
  states. Do not require a full browser suite for an isolated documentation change.
- Consider Knip when unused files, exports, or dependencies make migration cleanup
  difficult. Start with reporting only and verify entry points, dynamic consumers,
  generated inputs, and framework configuration before deleting anything. Svelte
  support has analysis limits; inspect its compiler configuration. Add enforcement
  only after useful coverage is established. Do not add it when existing tooling
  already covers the same need adequately.

Use TSDoc-compatible `/** ... */` comments for public interfaces when documenting
behavior that types do not express. Keep implementation reasoning in local
comments. If documentation syntax needs enforcement, `eslint-plugin-tsdoc` can
check it within the existing ESLint setup; it does not verify behavioral claims.
Do not install a documentation generator or linter solely because this guide
mentions it. Verify meaningful examples with the existing test tools where useful.

## Migrate one working slice

1. Write the behavior contract and identify the current authority before moving
   code. Include identifiers, versions, persisted data, errors, and permission or
   side-effect semantics where these are part of the operation.
2. Choose the slice's public boundary and a cutover point. A Python backend can
   serve a TypeScript frontend through a typed API. Moving server authority to
   TypeScript is a separate decision, not an automatic consequence of a frontend
   migration. Record which deployed runtime currently performs each operation.
3. Reuse one wire contract. Test both runtimes against representative valid,
   rejected, and compatibility cases during coexistence. Include dates, null versus
   absent fields, serialization, and old records when those distinctions matter.
   Static type generation does not prove runtime or behavioral parity.
4. Keep one write authority per operation. If parallel writes are unavoidable,
   require a designed reconciliation, failure, and retry strategy before enabling
   them. Prefer comparison on saved fixtures or isolated test data; shadow calls
   must not trigger real side effects.
5. Verify the slice, switch its consumer, and retain a credible rollback path.
   Account for schema compatibility: returning to old code may be unsafe after
   destructive data changes. Retire old code and temporary parity machinery only
   after callers have moved and the agreed compatibility window ends.

Do not delete a proven domain core or introduce a new service solely to achieve
a uniform language. Choose based on ownership, deployment needs, and maintenance
cost. A single-runtime design can also use this workflow.

## Tool references

Consult documentation for the repository's installed versions before changing
configuration:

- [Ruff complexity rule](https://docs.astral.sh/ruff/rules/complex-structure/)
- [PEP 257 docstring conventions](https://peps.python.org/pep-0257/)
- [Ruff docstring rules](https://docs.astral.sh/ruff/rules/#pydocstyle-d)
- [pydoclint coverage and configuration](https://jsh9.github.io/pydoclint/)
- [Python doctest](https://docs.python.org/3/library/doctest.html)
- [TSDoc ESLint plugin](https://tsdoc.org/pages/packages/eslint-plugin-tsdoc/)
- [ESLint complexity rule](https://eslint.org/docs/latest/rules/complexity)
- [Import Linter](https://github.com/seddonym/import-linter)
- [dependency-cruiser](https://github.com/sverweij/dependency-cruiser)
- [TypeScript strict](https://www.typescriptlang.org/tsconfig/strict.html)
- [TypeScript discriminated unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
- [Pydantic discriminated unions](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions)
- [Svelte checking](https://svelte.dev/docs/cli/sv-check)
- [SvelteKit state management](https://svelte.dev/docs/kit/state-management)
- [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- [How Knip works](https://knip.dev/explanations/how-knip-works)
- [Knip compiler coverage and limitations](https://knip.dev/features/compilers)
