# Provenance Artifact — Capsule / Trust-Substrate Design Conversation (Dec 5, 2025)

**Date of conversation:** December 5, 2025 (per the timestamps embedded in the KYC VC and session-record examples below).
**Rediscovered and preserved:** October 4, 2026.
**Source:** early AI design chat (exact assistant to be confirmed by the author — Gemini/Copilot lineage note pending).
**Status:** verbatim excerpt of the earliest known appearance of the capsule/envelope + trust-substrate design, ten months before the 2026 patent filings.

## Why this artifact matters (lineage note, added Oct 4, 2026)

- **Verdict-gated settlement.** "Your payment engine in Base44 gates settlement on `verdict.compliant === true`" is the deterministic-gate primitive in embryo: probabilistic flows propose, a deterministic verdict gates execution. This is the seed of the bifurcated governance pattern behind the 2026 patent filings (64/145,825, 64/119,191 lineage).
- **Redaction at anchoring.** "Never store raw IP on Arweave; store hashes and tags" is the hash-only-evidence doctrine a year before it became formal policy (redaction at ingestion).
- **Envelope lineage.** The 4-capsule structure (signed identity, credentials, evidence spine, unified audit) → the Capsule entity (signed manifests) in the Dec 2025-era orchestration app → the chamber-relay kit pattern in the current platform. The capsule here is already doing envelope-work: sealed, signed, hash-anchored containers.
- **Positioning continuity.** "A trust substrate: one plugin for onboarding, payments, and regulatory comfort" is the trust-layer thesis of Sept 2026 almost verbatim, ten months earlier — the positioning was not a pivot; it was the original idea returning.

---

## Verbatim conversation excerpt (Dec 5, 2025)

### 1. What "all-in-one" means here

Scope of the platform:

- DID & identity: User- and service-level DIDs, DID docs, key rotation, and service endpoints.
- KYC & reusable identity: Verifiable Credentials for KYC that users can reuse across apps, not re-onboard every time.
- IP tracking & session intelligence: Capture IP, device, geo, and risk signals per session and payment.
- Arweave permanence: Immutable storage for receipts, policies, key rotations, and KYC proof hashes.
- Unified audit: Single endpoint returns identity, KYC status, IP/session metadata, and Arweave proofs.

This is a trust substrate: one plugin for onboarding, payments, and regulatory comfort.

### 2. Enhanced capsule layout (with KYC + IP)

We keep the 4-capsule structure and enrich it:

**Identity capsule (unchanged core, new hooks)**
- DID lifecycle: create, resolve, rotate, list services.
- New: IP-aware DID context
- Attach recent session fingerprints to the DID (IP ranges, device IDs, risk scores) as metadata (not on-chain).
- Expose /did/{did}/sessions for internal use.

**Credentials capsule (KYC brain)**
- VC types:
  - KYCVerified (reg-level KYC done)
  - KYCBasic / KYCHighRisk (tiers)
  - BusinessVerified for entity onboarding
- Issuance flow:
  - Integrates with KYC provider(s) off-chain.
  - On success, issues VC and:
    - Stores no raw PII in Arweave.
    - Anchors hash of KYC payload, timestamp, provider ID, and policy version.

**Arweave capsule (evidence spine)**

Stores:
- KYC proof receipts (hash + metadata)
- Policy versions and changelogs
- Key rotation receipts
- Payment audit records (with IP and risk hashes)

**Audit capsule (now with IP & KYC)**

/audit/verify:
- Checks DID → DID doc
- Verifies KYC VC(s)
- Pulls latest session/IP footprint from internal store
- Verifies Arweave receipts for KYC and policy
- Returns a unified risk and compliance verdict.

### 3. KYC model: how it actually works

You want reusable, decentralized KYC, not "upload your passport again" hell.

Concept:

A trusted KYC provider or your own internal KYC node verifies identity once and issues a Verifiable Credential that lives in the user's wallet or your custody flow.

Your platform checks proofs, not documents, for every subsequent onboarding.

KYC VC JSON-LD (extended)

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "type": ["VerifiableCredential", "KYCVerified"],
  "issuer": "did:web:your-fintech.com",
  "credentialSubject": {
    "id": "did:key:SUBJECT_DID",
    "kycTier": "standard",
    "jurisdiction": "US",
    "kycProvider": "TRUSTED_PROVIDER_CODE",
    "verifiedAt": "2025-12-05T01:23:45Z"
  },
  "evidence": [{
    "type": "KYCProofReceipt",
    "arweaveTxid": "ARWEAVE_TXID",
    "payloadHash": "SHA256_OF_KYC_DATA",
    "policyVersion": "kyc-policies@1.2.0"
  }],
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2025-12-05T01:23:45Z",
    "verificationMethod": "did:web:your-fintech.com#keys-1",
    "jws": "..."
  }
}
```

User control vs custody: Credential can live:
- In a user wallet (pure SSI model), or
- In your controlled identity vault with user consent (faster for mass fintech use).

### 4. IP tracking and session intelligence

This is where you differentiate hard: identity + location + behavior.

**What you capture per session**

Raw inputs (kept off-chain, in secure DB/logs):
- IP address
- Geo lookup result (country, region, risk)
- Device fingerprint (user agent, OS, browser hints; maybe fingerprinting library)
- Login method (wallet, email, SSO, etc.)
- Velocity metrics (how many logins/payments per window)

Derived fields (used in audit / risk):
- ipRiskLevel (low / medium / high)
- geoRiskLevel (sanctions, high-fraud country)
- deviceTrustLevel (seen before, suspicious, etc.)
- sessionScore (0-100 risk-based)

You never store full raw IP on Arweave; you store hashes and tags for audit-proof correlation, not deanonymization.

**Session record structure (internal DB)**

```json
{
  "sessionId": "UUID",
  "did": "did:key:SUBJECT_DID",
  "ip": "203.0.113.42",
  "ipHash": "SHA256(IP+SALT)",
  "geoCountry": "US",
  "deviceFingerprint": "DEVICE_HASH",
  "loginAt": "2025-12-05T01:23:45Z",
  "risk": {
    "ipRiskLevel": "low",
    "geoRiskLevel": "low",
    "deviceTrustLevel": "medium",
    "sessionScore": 18
  }
}
```

**Arweave "session receipt" (optional)**

When needed (e.g., high-value payment, regulatory events), you create a session proof:

```json
{
  "type": "SessionEvidence",
  "sessionId": "UUID",
  "did": "did:key:SUBJECT_DID",
  "ipHash": "SHA256(IP+SALT)",
  "geoCountry": "US",
  "deviceHash": "DEVICE_HASH",
  "riskSnapshot": {
    "sessionScore": 18,
    "ipRiskLevel": "low",
    "geoRiskLevel": "low"
  },
  "linkedPaymentId": "PAYMENT_ID",
  "timestamp": "2025-12-05T01:30:00Z"
}
```

You upload that to Arweave and tag it (see tagging rules below). IP stays hashed; regulators can still prove consistency and non-tampering.

### 5. Unified audit endpoint (KYC + IP + permanence)

This is your "XRP++ compliance superpower".

Endpoint: POST /audit/verify

Input (simplified):

```json
{
  "did": "did:key:SUBJECT_DID",
  "paymentId": "PAYMENT_ID",
  "requiredChecks": ["did", "kyc", "session", "arweave"]
}
```

Output (example):

```json
{
  "did": {
    "id": "did:key:SUBJECT_DID",
    "document": {"...": "..."},
    "status": "active",
    "keyRotationHistory": [
      {"arweaveTxid": "TX_KEY_ROT_1", "rotatedAt": "..."}
    ]
  },
  "kyc": {
    "required": true,
    "status": "valid",
    "tier": "standard",
    "jurisdiction": "US",
    "provider": "TRUSTED_PROVIDER_CODE",
    "credentialId": "VC_ID",
    "revoked": false,
    "evidence": {
      "arweaveTxid": "TX_KYC_PROOF_1",
      "hashMatch": true,
      "policyVersion": "kyc-policies@1.2.0"
    }
  },
  "session": {
    "sessionId": "UUID",
    "ipHash": "SHA256(IP+SALT)",
    "geoCountry": "US",
    "deviceHash": "DEVICE_HASH",
    "risk": {
      "sessionScore": 18,
      "ipRiskLevel": "low",
      "geoRiskLevel": "low",
      "deviceTrustLevel": "medium"
    },
    "arweaveEvidence": {
      "txid": "TX_SESSION_1",
      "hashMatch": true
    }
  },
  "payment": {
    "paymentId": "PAYMENT_ID",
    "amount": "100.00",
    "currency": "USD",
    "linkedDID": "did:key:SUBJECT_DID",
    "linkedKycCredentialId": "VC_ID",
    "arweaveEvidence": "TX_PAYMENT_PROOF_1"
  },
  "verdict": {
    "compliant": true,
    "riskScore": 22,
    "flags": [],
    "policyVersion": "audit-rules@1.0.0",
    "timestamp": "2025-12-05T01:31:00Z"
  }
}
```

Your payment engine in Base44 gates settlement on verdict.compliant === true.

### 6. Arweave tagging (updated for KYC + IP)

For KYC, IP/session, and payments, use consistent tags:

**KYC receipts:**
- Service: credentials
- Purpose: kyc-receipt
- VCID: VC_ID
- DID: SUBJECT_DID
- PolicyVersion: kyc-policies@1.2.0
- Hash: SHA256_OF_KYC_PAYLOAD
- Capsule: credentials-engine
- Env: prod

**Session/IP evidence:**
- Service: audit
- Purpose: session-evidence
- SessionId: UUID
- DID: SUBJECT_DID
- Hash: SHA256(IP+SALT)
- Capsule: audit-layer
- Env: prod

**Payment proofs:**
- Service: audit
- Purpose: payment-proof
- PaymentId: PAYMENT_ID
- DID: SUBJECT_DID
- VCID: VC_ID
- Capsule: audit-layer
- Env: prod

---

*End of verbatim excerpt. Preserved forward-only per the append-only doctrine. The original conversation contained illustrative placeholders, not production data. This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*

---

# Continuation of the Same Conversation — Base44-Ready DID + Arweave Platform (Drag-and-Drop Capsule)

*Additive preservation, Oct 4, 2026 (same Dec 5, 2025 conversation, second half). Original excerpt above unaltered. This half contains the Base44-ready 4-capsule system with implementation manifests.*

## 1. Capsule Layout (4-Capsule System)

**Capsule 1 — Identity Core** — DID creation, resolution, key rotation, service endpoints.
Exports: `/did`, `/did/{did}`, `/did/{did}/rotate`, `/did/{did}/services`
Internal services: DID registry, DID document generator, Key rotation engine, Signature suite (Ed25519 / Secp256k1)

**Capsule 2 — Credentials Engine** — Issue, verify, revoke Verifiable Credentials.
Exports: `/vc/issue`, `/vc/verify`, `/vc/revoke`, `/vc/status/{vcId}`
Internal services: VC issuer, VC verifier, Revocation list manager, Schema registry

**Capsule 3 — Arweave Pipeline** — Permanent storage for proofs, receipts, manifests, policy versions.
Exports: `/arweave/upload`, `/arweave/{txid}`, `/arweave/bundle`
Internal services: Bundler, Deduplication layer, Compression layer, Tagging policy engine, Gateway proxy

**Capsule 4 — Unified Audit Layer** — One-call verification.
Exports: `/audit/verify`, `/audit/events`, `/audit/payment/{paymentId}`
Internal services: DID resolver, VC verifier, Arweave integrity checker, Payment metadata inspector, Compliance rules engine

## 2. Demo Flow

1. User onboards → DID created instantly → DID doc stored in Identity capsule → DID metadata anchored to Arweave (hash only).
2. KYC completed → VC issued (KYCVerified) → VC receipt + policy version anchored to Arweave → VC ID returned to client.
3. Payment metadata includes: DID, VC ID, Arweave TXIDs for evidence.
4. Counterparty or regulator calls `/audit/verify` → response includes DID document, VC validity + revocation status, Arweave artifacts + hash integrity, policy version lineage, key rotation history.

> Instant, portable, immutable compliance.

## 3. Base44 Capsule Manifests

**Identity Capsule Manifest**

```yaml
capsule:
  name: identity-core
  version: 1.0.0
services:
  - did-registry
  - did-resolver
  - key-rotation
ingress:
  - /did
  - /did/{did}
  - /did/{did}/rotate
outputs:
  - didDocument
  - rotationReceipt
events:
  - did.created
  - did.rotated
```

**Credentials Capsule Manifest**

```yaml
capsule:
  name: credentials-engine
  version: 1.0.0
services:
  - vc-issuer
  - vc-verifier
  - vc-revocation
  - schema-registry
ingress:
  - /vc/issue
  - /vc/verify
  - /vc/revoke
  - /vc/status/{vcId}
events:
  - vc.issued
  - vc.revoked
```

**Arweave Capsule Manifest**

```yaml
capsule:
  name: arweave-pipeline
  version: 1.0.0
services:
  - bundler
  - uploader
  - gateway
  - dedup
  - compressor
ingress:
  - /arweave/upload
  - /arweave/{txid}
  - /arweave/bundle
outputs:
  - arweaveTxid
events:
  - arweave.uploaded
```

**Audit Capsule Manifest**

```yaml
capsule:
  name: audit-layer
  version: 1.0.0
services:
  - integrity-checker
  - unified-verifier
  - compliance-engine
ingress:
  - /audit/verify
  - /audit/events
  - /audit/payment/{paymentId}
events:
  - audit.verified
  - audit.failed
```

## 4. JSON-LD Credential Template (KYC Verified VC)

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "type": ["VerifiableCredential", "KYCVerified"],
  "issuer": "did:web:yourdomain",
  "credentialSubject": {
    "id": "did:key:xyz",
    "kycLevel": "standard"
  },
  "evidence": [{
    "type": "ArweaveReceipt",
    "txid": "ARWEAVE_TXID",
    "hash": "SHA256_HASH"
  }],
  "proof": {"...": "..."}
}
```

## 5. Arweave Tagging Standard

Every artifact uploaded must include: Service (identity / credentials / policy / audit), Purpose (did-doc / vc-receipt / key-rotation / payment-proof), Version (semver), DID (subject DID), VCID (credential ID), Hash (sha256), Capsule (base44-service-name), Env (dev / staging / prod) — ensuring discoverability, auditability, and lineage.

## 6. Lineage note for this half (added Oct 4, 2026)

- The capsule manifests (services / ingress / outputs / events) are the direct ancestor of the platform's adapter-contract and capsule-deployment patterns: self-contained, versioned modules with declared ingress and emitted events.
- "One-call verification" (/audit/verify) prefigures the unified compliance-verdict endpoint that settlement gating depends on.
- The XRP-comparison framing ("the identity + permanence layer XRP wishes it had") marks the earliest appearance of the XRP++ positioning later used in the ISO 20022 bridge program.

*End of continuation. Prototype disclaimer applies: this software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments.*

---

## Source Confirmation (added Oct 4, 2026)

The author confirmed on Oct 4, 2026 that the assistant on this conversation was **GitHub Copilot**. This adds a third lineage data point to the provenance map: the geometric manifold thread originated with Copilot (RDC-1 Phase 1 discovery sessions), the Genesis Equation / reconstruction thread originated with Gemini, and the capsule/envelope trust-substrate thread recorded here also originated with Copilot. Original excerpts above unaltered per the forward-only doctrine.
