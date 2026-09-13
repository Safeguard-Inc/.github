<div align="center">

# Safeguard

**Compliance infrastructure for [Stellar Confidential Tokens](https://stellar.org/blog/developers/developer-preview-confidential-tokens-on-stellar).**

Confidential tokens hide amounts and balances. They do not hide *accounts* —
and that is where compliance lives.

[Website & live demo](https://safeguard-docs.vercel.app) ·
[Documentation](https://safeguard-docs.vercel.app/docs/architecture) ·
[Pitch video](https://safeguard-docs.vercel.app/assets/video/safeguard-pitch.mp4) ·
[Live contracts](#live-on-stellar-testnet) ·
[Contributing](#where-to-start)

</div>

---

## Watch the pitch

[![Five-minute Safeguard pitch: the problem, the architecture, the live decision engine and the contracts running on Testnet](https://safeguard-docs.vercel.app/assets/video/safeguard-pitch-poster.jpg)](https://safeguard-docs.vercel.app/assets/video/safeguard-pitch.mp4)

Five minutes, end to end: why confidential transfers need a decision rather
than a report, how the three layers divide that work, the policy engine driven
live in the browser, and the contracts this organisation has deployed to
Stellar Testnet — with the real contract ids, the read-only deployment
verification and the measured cost of an operation.

The video is **built from the documentation repository rather than edited by
hand** — slides, live captures, voice-over and edit are all produced by
[`video/`](https://github.com/Safeguard-Inc/safeguard-docs/tree/main/video), so
it cannot drift away from what the project does. Captions are published as a
WebVTT track and the claims on screen are each backed by a command recorded in
[`video/README.md`](https://github.com/Safeguard-Inc/safeguard-docs/blob/main/video/README.md#where-the-numbers-in-scene-9-come-from).

## The problem

Stellar's Confidential Token design keeps transaction amounts and balances
private while preserving the compliance surface area: addresses stay visible,
and the protocol preview already exposes policy contracts, allow/block-list
identity registries, account freezing, SAC passthrough and auditor
functionality.

What is missing is the layer between those primitives and a real deployment.
Every issuer that needs allowlists, sanctions screening and jurisdiction rules
ends up writing the same rule engine, the same versioning scheme and the same
decision semantics — usually with nobody able to show that two implementations
agree on a contested case.

## The solution

Safeguard is that layer, split across repositories with a strict separation of
duties and a one-way, versioned dependency chain:

```
             SAFEGUARD
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    POLICY      HOOKS     AUDIT
    DEFINE     ENFORCE    VERIFY
       │           │         │
  "what are    "run them   "what
   the rules"  on-chain"   happened"
       │           │         │
       └───────────┴─────────┘
                   │
                   ▼
                 DOCS
          explain · demonstrate · verify
```

| Repository | Layer | What it does |
| ---------- | ----- | ------------ |
| [`safeguard-policy`](https://github.com/Safeguard-Inc/safeguard-policy) | **Define** | Versioned policy model, rule primitives, on-chain registries, and a deterministic `APPROVE` / `BLOCK` / `FLAG` engine with a documented precedence order. |
| [`safeguard-hooks`](https://github.com/Safeguard-Inc/safeguard-hooks) | **Enforce** | A fail-closed Soroban compliance-hooks contract gating all six confidential-token operations, with admin-gated freeze administration and optional SAC passthrough. |
| [`safeguard-audit`](https://github.com/Safeguard-Inc/safeguard-audit) | **Verify** | Append-only audit records with chained integrity digests, authorization, investigation, evidence packages and reproducible reports. |
| [`safeguard-docs`](https://github.com/Safeguard-Inc/safeguard-docs) | **Explain** | The documentation hub and a live, verifiable policy decision demo. |
| [`.github`](https://github.com/Safeguard-Inc/.github) | — | Organization profile and shared community health files. |

## Design principles

These are enforced by tests, not by convention.

- **Fail closed.** Missing information never silently approves. An unknown
  account status flags. An unknown jurisdiction takes the rule's action. An
  unreachable policy contract denies. An unbound token denies.
- **Determinism.** The decision engine is a pure function of a fully
  materialized request: no randomness, no wall clock, no hidden state, no
  network. Identical input always produces an identical decision.
- **Precedence that cannot be argued with.** Account status → allowlist →
  denylist → sanctions → jurisdiction. The first decisive outcome wins, and
  the order is pinned by property tests so two implementations cannot disagree
  about a contested case.
- **Codes are assign-only.** Reason codes and contract error codes are quoted
  in stored records, reverted transactions and incident reports, so they are
  never renumbered and never reused. Removed variants keep their number.
- **Cost is published, not guessed.** Every public contract function is
  measured in stroops and documented. Enforcement gates short-circuit, so a
  denial is cheaper than an approval.
- **Privacy is a rule, not an aspiration.** Error messages and audit records
  may carry identifiers, which are public transaction metadata, but never
  balances, ciphertexts, view keys or credentials.

## Live on Stellar Testnet

Real deployed contracts, verified end-to-end. Full record:
[`docs/contracts.html`](https://safeguard-docs.vercel.app/docs/contracts).

| Layer | Contract |
| ----- | -------- |
| Policy (DEFINE) | [`CDVME6OPYZO6RAIWRFKLI3ACZHPNZK7GDBIX7YSIER3QLA2SO47QX5IB`](https://stellar.expert/explorer/testnet/contract/CDVME6OPYZO6RAIWRFKLI3ACZHPNZK7GDBIX7YSIER3QLA2SO47QX5IB) |
| Hooks (ENFORCE) | [`CC7UKMCY3J7LB2WGU6D3MPRSSK3RKEC6MEXJJKOXRPTZAPRNXKPVPKPN`](https://stellar.expert/explorer/testnet/contract/CC7UKMCY3J7LB2WGU6D3MPRSSK3RKEC6MEXJJKOXRPTZAPRNXKPVPKPN) |

Network `Test SDF Network ; September 2015` · RPC
`https://soroban-testnet.stellar.org`

Verified on these deployments: `schema_version` returns 1; `admin` returns the
configured admin; `is_authorized` answers `false` (fail-closed) for a token not
bound to an active policy; `register_version`, `activate_version` and
`bind_token` each succeeded and emitted their events; the hooks contract was
initialized, configured against the policy contract, and had its token bound;
and freeze/unfreeze were exercised for real against the ledger.

The admin secret key is never stored in a repository — it is read from the
`SAFEGUARD_ADMIN_SK` environment variable. Confidential Tokens on Stellar are
a developer preview, so treat these deployments as a rehearsal, not production.

## Where to start

| I want to… | Go to |
| ---------- | ----- |
| See the decision engine work without cloning anything | [the live demo](https://safeguard-docs.vercel.app/demo) |
| Understand how the three layers fit together | [`docs/architecture.html`](https://safeguard-docs.vercel.app/docs/architecture) |
| Look up an error or reason code | [`docs/error-codes.md`](https://github.com/Safeguard-Inc/safeguard-docs/blob/main/docs/error-codes.md) |
| Read the design in depth | [`safeguard-policy/docs`](https://github.com/Safeguard-Inc/safeguard-policy/tree/main/docs) · [`safeguard-hooks/docs`](https://github.com/Safeguard-Inc/safeguard-hooks/tree/main/docs) · [`safeguard-audit/docs`](https://github.com/Safeguard-Inc/safeguard-audit/tree/main/docs) |
| Contribute | the open issues below, and each repository's `CONTRIBUTING.md` |

Every repository is a plain Rust or Node workspace with no exotic toolchain:

```bash
git clone https://github.com/Safeguard-Inc/safeguard-policy
cd safeguard-policy && cargo test --workspace
```

```bash
git clone https://github.com/Safeguard-Inc/safeguard-docs
cd safeguard-docs && npm test
```

## Contributing

Contributions are welcome across all layers — policy rules and adapters,
enforcement gates and hardening suites, audit ingestion and reporting, SDKs,
documentation and tooling.

Good first steps are the issues tagged
[`good first issue`](https://github.com/search?q=org%3ASafeguard-Inc+label%3A%22good+first+issue%22+state%3Aopen&type=issues)
across the organization. Every repository carries a `CONTRIBUTING.md`, a
`CODE_OF_CONDUCT.md` and a `SECURITY.md`.

A contribution is expected to arrive with the tests that prove it, and any
documentation claim it invalidates should be updated in the same change.

## Security

Please do not open a public issue for a security report. See
[`SECURITY.md`](https://github.com/Safeguard-Inc/safeguard-policy/blob/main/SECURITY.md)
for the disclosure process.

## License

Apache-2.0 across the organization.
