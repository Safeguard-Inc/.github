<div align="center">

# Safeguard Pay

**Non-custodial, policy-guarded payment gateway and deterministic compliance engine for Soroban on Stellar.**

Safeguard provides an on-chain firewall for Web3 payments, payroll disbursals, and merchant settlements in SEP-41 SAC tokens (USDC, EURC, XLM). Every transaction is evaluated deterministically against policy rules before tokens move.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel_Console-brightgreen.svg)](https://safeguard-dashboard-mocha.vercel.app)
[![Stellar](https://img.shields.io/badge/Stellar-Testnet-blue.svg)](https://stellar.org)
[![Soroban](https://img.shields.io/badge/Soroban-Protocol%2022%2B-purple.svg)](https://stellar.org/soroban)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

</div>

---

## 🏛️ The 3-Tier Architecture

Safeguard is structured across three dedicated, production-ready repositories covering smart contracts, backend integration, and the frontend operator interface:

```mermaid
graph TD
    UI[safeguard-dashboard\nNext.js + Tailwind + Freighter] -->|Simulates & Submits| API[safeguard-backend\nREST API + TypeScript SDK]
    API -->|Interacts via RPC| Contract[safeguard-contracts\nSoroban Rust Gateway]
    Contract -->|Approve| Pay[Direct SAC Settlement]
    Contract -->|Flag| Escrow[On-Chain Escrow Vault]
    Contract -->|Block| Revert[Fail-Closed Revert #11/#12]
```

| Repository | Role | Stack | Link |
| :--- | :--- | :--- | :--- |
| **`safeguard-contracts`** | **Smart Contracts** | Rust, Soroban SDK | [Repo Link](https://github.com/Safeguard-Inc/safeguard-contracts) |
| **`safeguard-backend`** | **Integration & SDK** | TypeScript, Node.js, Stellar SDK | [Repo Link](https://github.com/Safeguard-Inc/safeguard-backend) |
| **`safeguard-dashboard`** | **Frontend Console** | Next.js 14, Tailwind, Freighter | [Repo Link](https://github.com/Safeguard-Inc/safeguard-dashboard) |

---

## 🌐 Live Deployments

* **Live Web Console & Checkout Demo:** [https://safeguard-dashboard-mocha.vercel.app](https://safeguard-dashboard-mocha.vercel.app)
* **Safeguard Payments Contract (Testnet):** `CBLQLJAG72M4XQRJMQHSKYIFVHQD7LNTNOQH2GRMCMBWMSLBSLTGTJC7`
* **Safeguard Policy Engine (Testnet):** `CDVME6OPYZO6RAIWRFKLI3ACZHPNZK7GDBIX7YSIER3QLA2SO47QX5IB`

---

## 🌊 Contributing & Stellar Drips Wave Sprints

Safeguard participates in the **Stellar Drips Wave** contributor sprints organized by the Drips Network in partnership with the Stellar Development Foundation (SDF).

We have 25+ scoped, contributor-ready backlog issues across our repositories:
* **[Smart Contract Issues](https://github.com/Safeguard-Inc/safeguard-contracts/issues)** (Rust / Soroban)
* **[Backend & SDK Issues](https://github.com/Safeguard-Inc/safeguard-backend/issues)** (TypeScript / Node.js)
* **[Frontend Issues](https://github.com/Safeguard-Inc/safeguard-dashboard/issues)** (React / Next.js)

All Wave issues carry complexity tags (`complexity: trivial`, `complexity: small`, `complexity: medium`, `complexity: large`) and explicit acceptance test criteria. Point rewards are paid out in USDC on Stellar at the conclusion of each sprint.

---

## 📜 License

All repositories are open source under the [Apache-2.0 License](LICENSE).
