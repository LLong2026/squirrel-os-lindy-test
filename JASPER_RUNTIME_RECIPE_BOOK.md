THE JASPER RUNTIME RECIPE BOOK
Deterministic Runtime Recipe Book — A Formal Engineering Specification for Deterministic System Construction

Author: Leon Calvin Long II — SQUIRL OS Technologies
Document Identifier: DRRB-SPEC-1-0-0 | Version 1.0.0 | Status: Released — Final
Public Release: September 12, 2026 — published as prior art and open study material.
JASPER — Judgment And Supervision of Probabilistic Execution Runtimes.
Formal state machine: JRS = (CurrentState, PendingOp, EntropyPool, ExecutionTrace, PolicyContext).

================================================================================

Engineering Specification
Deterministic Runtime
Recipe Book
A Formal Engineering Specification for
Deterministic System Construction
Document Version: 1.0.0
 Publication Date: September 2026
 Document Status: Released — Final
 Document Identifier: DRRB-SPEC-1-0-0
Intended Audience: Senior Engineers · System Architects · Technical Product Owners
INTERNAL TECHNICAL STANDARD  |  JASPER RUNTIME PROGRAM  |  © 2026  |  ALL RIGHTS RESERVED
Deterministic Runtime Recipe Book  |  Table of Contents  |  v1.0.0
Table of Contents
PART I — INVARIANT BOUNDARY PRIMER
1.1   What Is an Invariant Boundary?3

1.2   The Boundary Math4
1.3   Composing Boundaries5
1.4   Boundary Enforcement Mechanisms6
PART II — JASPER RUNTIME KERNEL SPECIFICATION
2.1   Kernel Philosophy8
2.2   Core Kernel Components9
2.3   The Truth Chain10
2.4   Commitment Structure11
2.5   Kernel Extension Points12
PART III — NO-CODE BLUEPRINT ENGINE
3.1   Engine Purpose and Scope13
3.2   Blueprint Schema14
3.3   The Predicate Expression DSL15
3.4   Blueprint Validation Pipeline16
3.5   Engine Runtime Binding17
PART IV — BUILDER BRIEF TEMPLATE
4.1   Purpose of the Builder Brief18
4.2   Builder Brief Template19
4.3   Builder Brief to Blueprint Mapping22
APPENDICES
Appendix A   Glossary23
Appendix B   Quick Reference Card25
Part I
Invariant Boundary Primer
Deterministic Runtime Recipe Book  |  Part I: Invariant Boundary Primer  |  v1.0.0

1.1   What Is an Invariant Boundary?
An invariant boundary is the formal contract between a runtime system and its  
external environment. It is not a suggestion, a soft constraint, or a best-effort target. 
It is an absolute specification of what must always be true — before any computation 
begins, during every intermediate step of that computation, and after every  
computation concludes — regardless of inputs, scale, elapsed time, or any other  
operational variable. The invariant boundary is the load-bearing wall of a  
deterministic system. Remove it, and the structure collapses.
Definition — Invariant Boundary
An invariant boundary is a formally specified set of boolean predicates over the 
state space of a runtime system, every one of which must evaluate to
true
for every reachable system state, under all possible input sequences and all 
possible execution orderings, without exception.
It is essential to distinguish the invariant boundary from related but weaker constructs 
that are frequently conflated with it in practice:
Construct Scope Temporal Extent Violation 
Consequence
Precondition Single operation Before execution Caller error; 
operation may 
refuse
Postcondition Single operation After execution Implementation 
error; result is 
invalid
Assertion Single code point At a specific line Runtime abort at 

Construct Scope Temporal Extent Violation 
Consequence
that point
Invariant 
Boundary
Entire system All reachable 
states — always
Hard runtime 
fault; structured 
fault record raised
Preconditions and postconditions are local agreements between a caller and a callee. 
They say nothing about the global system state. Assertions are diagnostic tools: they 
detect problems at specific code points but do not constitute a system-level contract. 
The invariant boundary operates at an entirely different level of abstraction — it  
defines the set of legal states the system is permitted to inhabit, and its violation is a 
system-level event, not a local one.
Axiom I-1 — Boundary Primacy
The invariant boundary supersedes all other correctness conditions. A system that 
satisfies all of its preconditions and postconditions but violates its invariant boundary 
is, by this specification, a
broken system
. No appeal to local correctness is sufficient to override a global invariant violation.
Invariant boundaries are most naturally specified as formal logical predicates over the 
system's state variables. They may be simple (a counter must never be negative) or 
compound (the sum of all account balances must equal the ledger total). They may be 
structural (a linked list must have no cycles) or temporal (a transaction must not be  
committed after its timeout has elapsed). The common thread is absoluteness: there 
is no valid execution path through a well-formed system that passes through a state 
that violates the boundary.
1.2   The Boundary Math

The following formal model provides the mathematical substrate on which all  
subsequent specifications in this document are built. Practitioners implementing the 
JASPER Runtime Kernel or authoring blueprints for the No-Code Blueprint Engine  
must understand this model in full. All higher-level constructs are direct expressions 
of it.
State Space
S
= { s₀, s₁, s₂, …, s  }ₙ
— a finite or countably infinite set of system states
s₀
 S∈
— the designated
genesis state
; the unique initial state of the system
Σ
— the input alphabet; the complete set of valid external stimuli
Transition Function
δ : S × Σ → S
The transition function maps a current state and an input symbol to a successor 
state. δ must be total and deterministic: for every (s, σ) pair, exactly one successor 
state exists.

Reachable States
Reach(s₀, δ)
= the smallest set R  S such that:⊆
(i)
s₀  R∈
(ii)
 s  R,  σ  Σ : δ(s, σ)  R∀ ∈ ∀ ∈ ∈
Invariant Predicate
I : S → {true, false}
A boolean predicate over the state space. I(s) = true means state s is a
safe state
.
Safety Property
 s  Reach(s₀, δ) → I(s) = true∀ ∈
Every reachable state must satisfy the invariant predicate. This is the central safety 
obligation of the system.

Boundary Violation
A
boundary violation
occurs when a transition δ(s, σ) = s' produces a successor state s' such that:
I(s') = false
This constitutes a
hard runtime fault
. The system must not continue execution from s'.
Warning — Boundary Violations Are Not Recoverable by Default
A boundary violation does not indicate a transient error that a retry may resolve. It 
indicates that the system has reached a state it was never permitted to reach. 
Execution must halt for the affected computation lane. The fault must be recorded in 
full. Recovery, if it occurs, must happen via the Recovery Enforcement tier (see 
Section 1.4), not via silent retry.
Boundary Tightness
The choice of invariant predicate I is not arbitrary. Boundary tightness describes how 
precisely the safe region is specified relative to the true space of operationally valid  
states:
● Overly loose invariant: I(s) = true for states that are, in fact, unsafe. The 
system may enter dangerous territory without triggering a fault. The 
boundary provides a false sense of safety.

● Overly tight invariant: I(s) = false for states that are operationally valid. 
The system raises spurious faults, degrading availability and causing 
excessive fault ejection.
● Optimal invariant: The tightest predicate that excludes all unsafe states 
without excluding any state required for correct operation. Formally: I(s) = 
false if and only if s is unsafe.
Axiom I-2 — Optimal Tightness Principle
The invariant predicate must be calibrated to the tightest bound that (a) excludes all 
states whose reachability constitutes a safety failure, and (b) includes all states 
required for the system to perform its intended function. Any invariant that satisfies 
(a) but not (b) is operationally defective. Any invariant that satisfies (b) but not (a) is 
a safety defect.
1.3   Composing Boundaries
Production systems are almost never monolithic. They are composed of subsystems, 
each with its own state space, transition function, and invariant predicate.  
Understanding how invariant boundaries compose across subsystem boundaries is  
foundational to building safe layered architectures.
Hierarchical Invariant Stacking
Let subsystem A operate under invariant I_A, and subsystem B operate under  
invariant I_B. When A and B are composed into a unified system AB, the composed  
invariant I_AB is defined as their logical conjunction:
I_AB(s_AB) = I_A(s_A)  I_B(s_B)∧

where s_AB = (s_A, s_B) is the joint state of the composed system.
I_AB(s_AB) = true if and only if both I_A(s_A) = true
and
I_B(s_B) = true.
This conjunction means that composed invariants are strictly more constraining than 
either constituent in isolation. A violation in any one subsystem is a violation of the  
composed system. There is no mechanism by which a valid state in B can compensate 
for an invalid state in A.
Conflict Detection in Composed Invariants
Composed invariants may conflict. A conflict occurs when I_A and I_B are mutually 
exclusive over the shared state variables — that is, when no state s exists such that 
both I_A(s) = true and I_B(s) = true simultaneously. Such a conflict renders the  
composed system permanently faulted from genesis state s₀ and constitutes a design 
error, not a runtime error.
Warning — Conflict in Composed Invariants
If I_A  I_B is unsatisfiable, the composed system has no valid states. Blueprint ∧
validation (see Section 3.4) must reject this configuration at parse time. Deployment 
of a composed invariant set that is unsatisfiable is a critical design defect and must 
never reach a production JASPER Runtime Kernel instance.
Conflict Resolution Rules
When partial conflicts exist (invariants share state variables with overlapping but not 
fully exclusive ranges), the following resolution rules apply in priority order:

1. Strictest-wins rule: For any shared state variable, the most restrictive 
constraint across all composed invariants governs. No subsystem may relax a 
constraint imposed by another subsystem in the composition.
2. Explicit override declaration: If a subsystem must legitimately relax a 
constraint established by a higher layer, it must declare an explicit invariant 
override at the composition boundary, subject to formal review and sign-off.
3. Isolation partitioning: If conflict cannot be resolved by the above rules, the 
conflicting subsystems must be isolated into separate computation lanes with 
non-overlapping state spaces. Shared state is prohibited between conflicting 
invariant domains.
1.4   Boundary Enforcement Mechanisms
Specifying an invariant boundary is necessary but not sufficient. The boundary must 
be enforced. This specification defines three enforcement tiers, which are ordered by 
the cost of failure detection. Earlier tiers are preferred. A boundary violation detected 
at Tier 3 represents a more serious system condition than one caught at Tier 1.
Tier 1 — Static Enforcement
Static enforcement occurs before the system executes. It is the highest-value  
enforcement tier because it eliminates entire classes of invariant violations from the 
deployed artifact. Static enforcement tools include:
● Compile-time type systems: Dependent types, refinement types, and 
linear types can encode many invariant predicates directly into the type 
algebra. A well-typed program is guaranteed not to construct values that 
violate encoded invariants.
● Formal verification: Model checkers (e.g., TLA+, Alloy, SPIN) exhaustively 
verify that the invariant predicate holds for all reachable states of the formal 
model. Formal verification is mandatory for all kernel-layer components.

● SMT solvers: Satisfiability Modulo Theory solvers (e.g., Z3, CVC5) can 
discharge invariant proof obligations arising from program analysis, verifying 
that no execution path leads to an invariant-violating state.
Tier 2 — Dynamic Enforcement
Dynamic enforcement occurs during execution. It is the second line of defense,  
catching violations that static tools cannot prove absent — typically because they  
depend on runtime values or external inputs that cannot be fully enumerated  
statically.
● Runtime invariant guards: Before each state transition is committed, the 
proposed successor state is evaluated against all registered invariant 
predicates. Any predicate returning false triggers the Fault Ejector (see 
Section 2.2).
● Watchdog timers: Temporal invariants (e.g., "this computation must 
complete within T milliseconds") are enforced by watchdog mechanisms that 
halt the computation lane if the time bound is exceeded.
● Circuit breakers: When a subsystem's fault rate exceeds a configurable 
threshold within a sliding window, the circuit breaker trips, isolating the 
subsystem from the rest of the system to prevent cascading violations.
Tier 3 — Recovery Enforcement
Recovery enforcement activates after a violation has been detected and the affected 
computation lane has been halted. Its purpose is to restore the system to a known-
good state while preserving auditability.
● Rollback to last-good-state: The State Ledger (see Section 2.2) is 
consulted to identify the most recent committed state sₖ for which I(sₖ) = 
true. The system rolls back to sₖ and the fault record is appended to the Truth 
Chain.
● Checkpoint restoration: For systems with explicit checkpoint intervals, 
restoration rewinds to the most recent verified checkpoint rather than the 
last committed state.

● Poison message quarantine: If the violation was triggered by a specific 
input σ, that input is quarantined in an isolated fault buffer. The system 
resumes processing subsequent inputs from the last-good-state, and the 
quarantined input is preserved for forensic analysis.
Tier When Mechanism Detection 
Cost
Preferred For
1 — Static Before 
execution
Type systems, 
model 
checkers, SMT 
solvers
Zero runtime 
cost
Structural, 
type-level 
invariants
2 — Dynamic During 
execution
Runtime 
guards, 
watchdogs, 
circuit 
breakers
Per-transition 
overhead
Value-
dependent, 
input-
triggered 
invariants
3 — Recovery After violation Rollback, 
checkpoint 
restore, 
quarantine
High — 
violation 
already 
occurred
Residual 
cases not 
caught by 
Tiers 1–2
Axiom I-3 — Defense in Depth
All three enforcement tiers must be present in any JASPER-compliant system. 
Reliance on a single tier — even Tier 1 — is insufficient. Tier 1 failures surface as 
deployment defects; Tier 2 failures surface as runtime faults; Tier 3 failures surface 
as recovery events. A system with only Tier 1 enforcement has no protection 
against input-triggered violations. A system with only Tier 2 or 3 enforcement has no 
protection against structural design defects.
Part II

JASPER Runtime Kernel Specification
Deterministic Runtime Recipe Book  |  Part II: JASPER Runtime Kernel Specification  |  v1.0.0
2.1   Kernel Philosophy
The JASPER Runtime Kernel is the minimal, deterministic execution core from which 
all higher-level system behaviors are derived. It is not a general-purpose operating  
environment. It is a mathematically disciplined execution substrate designed for one 
purpose: to guarantee that every computation it hosts is fully reproducible, fully  
auditable, and fully verifiable against its invariant boundary.
Axiom II-1 — The Determinism Guarantee
Given identical inputs and identical genesis state s₀, the JASPER Runtime Kernel 
must always produce identical outputs and an identical final state s  — without ₙ
exception, without qualification, and without dependence on any property of the 
execution environment that was not explicitly provided as an input.
This guarantee is absolute. It is not a probabilistic claim ("usually produces the same 
result"). It is not a best-effort claim ("produces the same result under normal  
conditions"). It is a hard invariant of the kernel itself, enforceable by formal  
verification and auditable via the Truth Chain (see Section 2.3).
To sustain this guarantee, the kernel operates under the following categorical  
prohibitions:

● No ambient randomness: The kernel contains no entropy source. Any 
computation requiring randomness must receive a deterministic seed as an 
explicit input through the Input Canonicalizer.
● No uncontrolled side effects: All side effects (I/O, network access, disk 
writes, external service calls) are deferred to the Effect Queue and executed 
outside the deterministic boundary. The kernel's state transitions are pure.
● No external time dependency: The kernel does not read the system clock. 
All temporal values are injected as explicit inputs through the Clock Oracle. 
The kernel's behavior is therefore independent of wall-clock time.
● No implicit global state: All state accessible to kernel computations is 
owned by the State Ledger and is fully versioned and auditable.
These prohibitions are not architectural preferences. They are necessary and  
sufficient conditions for the Determinism Guarantee to hold. Any kernel extension  
that violates any of these prohibitions invalidates the guarantee for every  
computation hosted by that kernel instance.
2.2   Core Kernel Components
The JASPER Runtime Kernel is composed of six core components. Each component  
has a precisely defined interface, a precisely defined responsibility, and precisely  
defined interaction rules with the other components. No component may be replaced, 
bypassed, or extended except through the sanctioned extension points defined in  
Section 2.5.
Execution Scheduler
The Execution Scheduler is a pure priority-queue dispatch engine. Pending  
computations are enqueued with explicit priority values. The scheduler selects the  
highest-priority ready computation and dispatches it. There is no preemption without 
an explicit yield from the running computation. This ensures that the scheduling order 
is a deterministic function of the queue's state and the declared priorities — it is never 
perturbed by external interrupt signals, timer expirations, or other non-deterministic 
signals.

State Ledger
The State Ledger is the authoritative record of all system state. It is append-only: no 
entry may be modified or removed after it has been committed. Every state transition 
produces a new ledger entry containing the successor state, the input that triggered 
the transition, a content hash, and a reference to the predecessor entry. The State  
Ledger is the ground truth from which the Truth Chain (see Section 2.3) is derived.
Input Canonicalizer
All external inputs — regardless of source, format, or transport mechanism — must  
pass through the Input Canonicalizer before they touch any kernel computation. The 
Canonicalizer normalizes inputs into a canonical deterministic form: byte sequences 
are normalized to a defined encoding, numeric types are cast to defined widths,  
timestamps are converted to the kernel's logical time representation, and any  
ambiguous or polymorphic input format is reduced to its canonical representation.  
Inputs that cannot be canonicalized are rejected before entering the kernel boundary.
Clock Oracle
The Clock Oracle is the sole mechanism by which temporal values enter the kernel.  
The kernel does not, under any circumstances, call a system-time API directly.  
Instead, the Clock Oracle receives time values as explicit external inputs, validates  
them for monotonicity and format, and injects them into the computation as a named, 
versioned input token. Consumers of time values inside the kernel reference the Clock 
Oracle's most recently injected value — not wall-clock time.
Effect Isolator
The Effect Isolator intercepts all operations that would produce externally visible side 
effects: writes to disk, network calls, messages to external queues, UI updates, and all 
other forms of output. Instead of executing these effects immediately, the Isolator  
defers them to an Effect Queue. The Effect Queue is flushed after the current state  
transition has been committed to the State Ledger. This separation ensures that the 
kernel's state transitions are pure and that side effects are executed at most once, in 
a defined order, after the state that authorized them has been durably recorded.

Fault Ejector
The Fault Ejector is activated whenever an invariant guard returns false during the  
Validate phase of the Commitment Structure (see Section 2.4). Upon activation, the  
Fault Ejector immediately halts the affected computation lane, discards the staging  
buffer, constructs a structured fault record containing the violating state, the  
triggering input, the failing invariant predicate, and the current Truth Chain position, 
and appends the fault record to the Truth Chain. The Fault Ejector never silently  
swallows a violation.
Component Primary Responsibility Key Invariant
Execution Scheduler Priority-queue dispatch; 
explicit yield only
Scheduling order is a 
pure function of queue 
state
State Ledger Append-only, content-
addressed state record
No entry is ever modified 
or deleted after 
commitment
Input Canonicalizer Normalize all external 
inputs to canonical form
No non-canonical input 
ever reaches a kernel 
computation
Clock Oracle Inject temporal values as 
explicit named inputs
No kernel computation 
reads wall-clock time 
directly
Effect Isolator Defer all side effects to 
post-commit Effect 
Queue
No side effect executes 
before its authorizing 
state is committed
Fault Ejector Halt lane and record 
structured fault on 
invariant violation
No invariant violation is 
silently swallowed or 
retried
2.3   The Truth Chain
The Truth Chain is the immutable, linearly ordered log of all state transitions from the 
genesis state s₀ to the current state sₙ. It is the auditable record of everything the  
kernel has ever done and the mechanism by which deterministic replay, time-travel  
debugging, and compliance auditing are made possible.

Definition — Truth Chain
The Truth Chain is a Merkle-chained sequence of transition records T = (e₀, e₁, e₂, 
…, e ) where each entry e  encodes the k-th state transition. Each e  contains: the ₙ ₖ ₖ
predecessor hash H(e ₁), the input σ , the resulting state s , the content hash ₖ₋ ₖ ₖ
H(s ), a timestamp from the Clock Oracle, and a cryptographic signature over the ₖ
full entry.
Core Properties
The Truth Chain must satisfy all four of the following properties to be considered valid:
4. Append-only: No entry may be modified or deleted after it has been 
committed. Any attempt to alter a historical entry is detectable as a hash 
mismatch from that entry forward through the chain.
5. Content-addressed: Each entry's hash includes the hash of its predecessor. 
This Merkle-chain structure means that any tampering with any historical 
entry invalidates all subsequent entries. The chain is self-verifying.
6. Causally ordered: Entry eₙ is written only after eₙ₋₁ has been committed, 
verified, and its hash is known. There is no concurrent or out-of-order writing 
to the Truth Chain. Causal order is guaranteed by the single-writer constraint 
on the Commit phase.
7. Auditable: Any external party who possesses the genesis hash H(e₀) and the 
full chain T can independently recompute every state transition and verify the 
full chain without privileged access to the kernel internals.
Operational Applications of the Truth Chain
● Time-travel debugging: An operator may reconstruct the kernel's state at 
any historical moment by replaying the Truth Chain from e₀ to the entry 
immediately preceding the point of interest. This reconstruction is 

deterministic and produces exactly the same intermediate states as the 
original execution.
● Deterministic replay: The complete input sequence encoded in the Truth 
Chain can be extracted and re-applied to a fresh kernel instance initialized 
with the same genesis state. The replay must produce an identical final state 
sₙ. Any divergence is evidence of a non-determinism defect in the kernel.
● Compliance auditing: Regulators, auditors, and system operators can 
independently verify that every state transition was authorized by a valid 
input, satisfied all invariant predicates at the time of commitment, and was 
recorded faithfully. The cryptographic chain ensures that the audit log cannot 
be retroactively falsified.
Axiom II-2 — Chain Integrity
Any JASPER-compliant system that cannot present a valid, unbroken Truth Chain 
from s₀ to its current state is in an undefined operational condition. It must be 
treated as potentially compromised and must not be permitted to commit new state 
transitions until chain integrity is restored from a verified checkpoint.
2.4   Commitment Structure
All state transitions in the JASPER Runtime Kernel are governed by the three-phase  
Commitment Structure. No state transition may be recorded in the State Ledger or the 
Truth Chain without successfully completing all three phases in order. This protocol is 
the primary dynamic enforcement mechanism (Tier 2) for invariant boundaries.
Phase 1 — Propose
The Execution Scheduler dispatches a computation. The computation runs against  
the current committed state and produces a candidate successor state s'. This  
candidate is placed in the Staging Buffer — a temporary, uncommitted holding area. 

The staging buffer is isolated from the State Ledger; its contents are not yet part of  
any committed state and are not visible to other computations. The invariant guards 
are invoked at the end of this phase to prepare for validation.
Phase 2 — Validate
All registered invariant guards evaluate the proposed state s' held in the Staging  
Buffer. Each guard is a pure boolean predicate. They are evaluated in declared order. 
If all guards return true, the proposal advances to Phase 3. If any guard returns false, 
the Staging Buffer is immediately discarded, the Fault Ejector is activated, and no  
state transition is committed. The failure is a permanent record — it is not subject to 
retry at this phase.
Phase 3 — Commit
The validated state s' is written atomically to the State Ledger. A new Truth Chain  
entry is constructed, hashed, signed, and appended to the Truth Chain. The Staging  
Buffer is cleared. The Effect Isolator's queued effects are flushed in declared order.  
The Execution Scheduler is notified that the transition is complete and may dispatch 
the next computation.
Phase Action Success Path Failure Path
1 — Propose Compute s'; write 
to Staging Buffer
Advance to Phase 
2
Computation error 
→ lane halted; no 
state change
2 — Validate Evaluate all 
invariant guards 
against s'
All guards return 
true → advance to 
Phase 3
Any guard returns 
false → Staging 
Buffer discarded; 
Fault Ejector 
activated; fault 
record written to 
Truth Chain
3 — Commit Write s' to State 
Ledger; append 
Truth Chain entry; 
flush Effect Queue
Transition 
committed; 
Scheduler 
notified; s' 
becomes current 
state
Ledger write 
failure → system 
halted; integrity 
alarm raised; 
manual recovery 
required

Important — Atomicity of Phase 3
The State Ledger write, the Truth Chain append, and the Effect Queue flush in 
Phase 3 must be treated as an atomic unit. If any of these three operations fails 
after another has succeeded, the system is in an inconsistent state. This condition 
must trigger an integrity alarm and halt new commitments until a recovery procedure 
has re-established consistency.
2.5   Kernel Extension Points
The JASPER Runtime Kernel is intentionally minimal. Augmentation is supported  
exclusively through four sanctioned extension points. Any modification to the kernel 
that does not go through these extension points is a violation of the kernel  
specification and voids the Determinism Guarantee for that instance.
Extension Point Interface to 
Implement
Determinism 
Constraint
Side Effects 
Permitted?
Input Adapters Input 
Canonicalizer 
interface
Must produce 
identical canonical 
output for 
identical raw input
No
Effect Handlers Effect Queue 
interface
Handlers operate 
outside the 
deterministic 
boundary; 
ordering is 
guaranteed by 
queue position
Yes — by design
Invariant 
Plugins
Invariant 
Predicate 
interface
Must be pure 
boolean 
predicates; no 
side effects; no 
external calls; no 
mutable state
No
Telemetry Taps Read-only State 
Observer interface
Read-only access 
to committed 
No (observing 
only)

Extension Point Interface to 
Implement
Determinism 
Constraint
Side Effects 
Permitted?
state only; must 
not mutate any 
kernel structure
Warning — Extension Point Discipline
Invariant Plugins must be pure with absolute strictness. An invariant plugin that 
reads from a network endpoint, accesses the filesystem, generates a random 
number, or modifies any shared structure introduces non-determinism into the 
Validate phase. Such a plugin invalidates the Determinism Guarantee and must be 
rejected at blueprint validation time (see Section 3.4).
Part III
No-Code Blueprint Engine
Deterministic Runtime Recipe Book  |  Part III: No-Code Blueprint Engine  |  v1.0.0
3.1   Engine Purpose and Scope
The No-Code Blueprint Engine is the authoring layer that exposes the full operational 
power of the JASPER Runtime Kernel through a structured declarative interface. Its  
purpose is to allow non-engineers — domain experts, technical product owners, and  
system architects — to define, compose, and deploy deterministic runtime  
configurations without writing kernel-level code.

The engine does not relax any of the kernel's guarantees. It does not introduce a  
lower tier of determinism for non-engineers. Every blueprint deployed through the  
engine is subject to the full Determinism Guarantee, the full invariant boundary  
framework, and the full Commitment Structure of the JASPER Runtime Kernel. The  
engine changes the authoring modality; it does not change the execution semantics.
Definition — Blueprint
A Blueprint is a formally structured declarative document — authored in YAML or 
JSON — that completely describes a deterministic runtime configuration for a 
JASPER Runtime Kernel instance. A blueprint specifies the genesis state, all invariant 
predicates, all transition definitions, all declared effects, and all telemetry hooks. A 
sealed blueprint is cryptographically signed and is the sole authoritative source of 
configuration for its bound kernel instance.
Scope Boundaries
The following capabilities are within scope of the Blueprint Engine:
● Authoring and validating blueprints through the declarative schema
● Composing blueprints from reusable invariant and transition libraries
● Deploying sealed blueprints to kernel instances
● Versioning and auditing deployed blueprints
The following capabilities are explicitly outside scope and must be implemented at  
the kernel extension layer:
● Defining new kernel components
● Implementing custom canonicalizers or effect handlers
● Modifying the Commitment Structure or the Truth Chain format
● Direct access to State Ledger storage

3.2   Blueprint Schema
A blueprint is a YAML or JSON document conforming to the JASPER Blueprint Schema 
v1.0. The top-level structure contains the following required and optional fields:
Field Type Required Description
blueprint_id UUID v4 string Yes Globally unique 
identifier for this 
blueprint. 
Immutable after 
sealing.
version SemVer string Yes Blueprint version 
following semantic 
versioning (e.g., 
1.0.0).
genesis_state Object Yes The initial state 
object s₀. Must be 
a valid instance of 
the state schema.
invariants Array of 
InvariantDef
Yes Named invariant 
definitions. Each 
must specify: 
name, description, 
predicate (DSL 
expression), and 
enforcement_tier.
transitions Array of 
TransitionDef
Yes Named transition 
definitions. Each 
must specify: 
name, trigger, 
precondition, 
action, and 
postcondition.
effects Array of EffectDef No Declared side 
effects. Each must 
specify: name, 
handler, 
trigger_transitio
n, and reversible.
telemetry Array of 
TelemetryDef
No Declared metrics 
and event hooks. 
Each must 
specify: name, type 

Field Type Required Description
(metric | event), 
and expression.
Annotated Blueprint Snippet
# JASPER Blueprint Schema v1.0 — Annotated Sample blueprint_id: "f47ac10b-
58cc-4372-a567-0e02b2c3d479"   # UUID v4 — globally unique, immutable 
version: "1.0.0"                                         # SemVer — increment 
on any schema change  genesis_state: 
# Initial state s₀ for this kernel instance   account_balance: 0   
transaction_count: 0   status: "ACTIVE"  invariants:   - name: 
"balance_non_negative"     description: "Account balance must never fall 
below zero."     predicate: "state.account_balance >= 0"              # DSL 
predicate — pure boolean expression     enforcement_tier: "dynamic"    - 
name: "active_status_required"     description: "Transactions may only be 
processed in ACTIVE status."     predicate: "state.status == 'ACTIVE'"     
enforcement_tier: "dynamic"  transitions:   - name: "credit"     trigger: 
"CreditEvent"                               # Input event type from 
canonicalized input     precondition: "input.amount > 0"                     
# Must be true before action executes     action: "state.account_balance += 
input.amount;              state.transaction_count += 1"               # 
State mutation (pure; no side effects here)     postcondition: 
"state.account_balance > prev.account_balance"  # Must be true after action  
effects:   - name: "send_credit_notification"     handler: 
"NotificationEffectHandler"     trigger_transition: "credit"     reversible: 
false  telemetry:   - name: "balance_gauge"     type: "metric"     
expression: "state.account_balance"                  # Read-only; does not 
mutate state
3.3   The Predicate Expression DSL
The Predicate Expression DSL is the language in which invariant predicates,  
preconditions, and postconditions are authored within a blueprint. It is designed to be 
expressive enough to specify meaningful runtime constraints while being restrictive  
enough to guarantee termination, determinism, and sandboxing.
Definition — Predicate Expression DSL
The Predicate Expression DSL is a statically typed, purely functional, sandboxed 
expression language whose evaluation always terminates, whose result is always a 
boolean or a typed value, and which can access no external resources — no 

filesystem, no network, no system APIs, no mutable state.
Core Language Properties
● Pure functional: Expressions contain no assignment statements, no loops, 
no mutation operators, and no sequencing of imperative actions. Every 
expression is a referentially transparent computation over its inputs.
● Statically typed: All values have inferred types. Numeric types, string 
types, boolean types, and enumeration types are supported. Type errors are 
caught at blueprint parse time, before the blueprint can advance to the 
validation pipeline.
● Bounded evaluation: All expressions must terminate. Recursion is 
prohibited. Iteration over collections uses bounded map and filter operators 
with statically known bounds. No expression may have unbounded runtime.
● Sandboxed: The DSL runtime has no access to the filesystem, network, 
system clock (except through the Clock Oracle input token), or any external 
API. It can only read from the current state object and the current input 
token.
Built-in Operators and Functions
Operator / 
Function
Category Description Example
==, !=, <, <=, >, 
>=
Comparison Standard 
relational 
operators over 
numeric and 
string types
state.balance >= 
0
&&, ||, ! Boolean logic Short-circuit AND, 
OR, and NOT
state.active && 
input.amount > 0
+, -, *, / Arithmetic Standard 
arithmetic; 
division by zero 
produces a DSL 
state.balance + 
input.amount

Operator / 
Function
Category Description Example
fault, not a kernel 
fault
in(value, set) Membership Returns true if 
value is a member 
of the specified 
literal set
in(state.status, 
["ACTIVE", 
"SUSPENDED"])
len(collection) Collection Returns the count 
of elements in a 
collection
len(state.items) 
< 100
all(collection, 
pred)
Collection Returns true if the 
predicate holds 
for every element
all(state.orders, 
o: o.amount > 0)
any(collection, 
pred)
Collection Returns true if the 
predicate holds 
for at least one 
element
any(state.flags, 
f: f == "ALERT")
matches(str, 
pattern)
String Returns true if 
string matches 
the specified 
literal regular 
expression
matches(input.id, 
"^[A-Z]{3}-[0-9]
{4}$")
if(cond, then, 
else)
Conditional Ternary 
conditional 
expression; both 
branches must be 
type-compatible
if(state.active, 
state.balance, 0)
prev.field State reference Accesses the 
value of a state 
field before the 
current transition
state.balance > 
prev.balance
3.4   Blueprint Validation Pipeline
Before a blueprint can be deployed to a JASPER Runtime Kernel instance, it must pass through 
the five-stage Blueprint Validation Pipeline in sequence. A failure at any stage halts  
the pipeline and returns a structured validation error report. Stages are not skipped. A 
blueprint that has not been sealed by Stage 5 cannot be bound to a kernel instance.

Stage 1 — Schema Validation
The blueprint document is parsed and validated against the Genesis Blueprint  
Schema. Every required field must be present and correctly typed. All UUID fields  
must conform to UUID v4 format. All version strings must conform to SemVer. All  
arrays must conform to their respective element schemas. Schema validation is a  
purely structural check — it does not evaluate any DSL expressions.
Stage 2 — Semantic Validation
The validated structure is checked for semantic integrity. This stage verifies that all  
cross-references within the blueprint are internally consistent:
● All trigger_transition references in effect definitions must correspond to 
named transitions that exist in the transitions array.
● No two transitions may share the same name.
● No two invariants may share the same name.
● Every transition defined must be reachable from genesis state s₀ via at least 
one valid input sequence. Unreachable transitions are flagged as warnings 
but do not halt the pipeline.
● All state fields referenced in DSL expressions must exist in the genesis_state 
object.
Stage 3 — Invariant Consistency Check
All invariant predicates are submitted to an SMT solver (Z3 or equivalent) for  
satisfiability analysis. This stage answers two questions:
8. Are all invariants individually satisfiable? If any single invariant 
predicate I is unsatisfiable (i.e., I(s) = false for all possible states s), the 
blueprint is immediately rejected. The genesis state would violate it from the 
start.
9. Are all invariants jointly satisfiable? The conjunction I₁ ∧ I₂ ∧ … ∧ Iₙ is 
checked for satisfiability. If the conjunction is unsatisfiable, the blueprint 
defines a system with no valid states and is rejected.

Stage 4 — Simulation Dry-Run
The blueprint is executed against a synthetic event trace generated by the validation 
engine. The trace exercises every declared transition at least once, including edge-
case inputs at the boundary of declared preconditions. The simulation runs inside a  
sandboxed, in-memory kernel instance and verifies that the blueprint behaves  
deterministically — that is, replaying the same trace from genesis state s₀ always  
produces the same final state. Any non-deterministic behavior detected in the  
simulation is a critical validation failure.
Stage 5 — Sign and Seal
A blueprint that has passed Stages 1–4 is cryptographically sealed. The sealing  
operation computes a SHA-256 hash over the canonical serialization of the blueprint 
document, signs the hash with the deployment authority's private key, and records  
the sealed blueprint hash in the deployment registry and in the kernel's Truth Chain  
prior to binding. A sealed blueprint is immutable. Any modification to a sealed  
blueprint produces a new blueprint with a new version and requires the full pipeline to 
be re-executed from Stage 1.
Stage Name Primary Check Failure Action
1 Schema Validation Structure and field 
types
Halt pipeline; 
return schema 
error report
2 Semantic 
Validation
Referential 
integrity, 
duplicates, 
unreachable 
transitions
Halt pipeline; 
return semantic 
error report
3 Invariant 
Consistency
Satisfiability of 
individual and 
joint invariants 
(SMT)
Halt pipeline; 
return 
unsatisfiability 
proof
4 Simulation Dry-
Run
Deterministic 
behavior over 
synthetic event 
trace
Halt pipeline; 
return divergence 
report with trace
5 Sign and Seal Cryptographic 
signing; 
deployment 
registry recording
Halt pipeline; 
investigate 
signing 
infrastructure

3.5   Engine Runtime Binding
A sealed blueprint is a static document until it is bound to a running JASPER Runtime Kernel  
instance. Binding is the process by which the blueprint's declarative specifications are 
translated into the kernel's native operational structures. Binding is a one-time  
operation performed at kernel instance initialization.
Binding Sequence
10.Blueprint parse and verify: The engine parses the sealed blueprint, 
verifies its cryptographic signature against the deployment authority's public 
key, and verifies that its hash matches the hash recorded in the deployment 
registry. A mismatch at this stage prevents binding.
11.Genesis state installation: The genesis_state object from the blueprint 
becomes the state s₀ of the kernel instance. It is written to the State Ledger 
as the first entry and becomes the anchor of the Truth Chain.
12.Invariant compilation: Each invariant predicate is compiled from its DSL 
expression into a native Invariant Plugin that implements the Invariant 
Predicate interface. The compiled plugins are registered with the kernel's 
Validate phase engine.
13.Transition registration: Each transition definition is compiled into a kernel-
native transition record and registered with the Execution Scheduler. Triggers 
are mapped to input event types recognized by the Input Canonicalizer.
14.Effect registration: Each declared effect is instantiated with its designated 
handler and registered with the Effect Isolator's Effect Queue. The trigger-to-
effect mapping is established from the transition definitions.
15.Telemetry attachment: Each telemetry definition is compiled into a read-
only Telemetry Tap and attached to the State Observer interface. Taps begin 
observing after the first successful commitment.

Note — Binding Idempotency
Binding a sealed blueprint to a kernel instance that has already been initialized with 
the same blueprint version is a no-operation. The engine detects the existing 
binding by comparing the blueprint hash to the genesis Truth Chain entry and skips 
re-binding. This ensures that restart and recovery operations do not re-initialize a 
running kernel's genesis state.
Part IV
Builder Brief Template
Deterministic Runtime Recipe Book  |  Part IV: Builder Brief Template  |  v1.0.0
4.1   Purpose of the Builder Brief
The Builder Brief is the human-authored requirements document that precedes all  
blueprint authoring. It is the design contract between the problem owner — the  
person or team with domain knowledge of the problem to be solved — and the system 
builder — the person or team responsible for translating that problem into a Genesis 
Runtime Blueprint.
The  Builder  Brief  captures  the  problem  domain,  success  criteria,  invariant 
requirements, scope boundaries, input contracts, effect declarations, and risk  
inventory in structured plain language. It does not contain DSL expressions or  
technical schema definitions. Its language is precise and unambiguous, but it is  
accessible to domain experts who are not system engineers.

Axiom IV-1 — Brief Before Blueprint
No blueprint authoring may begin before a Builder Brief has been completed, 
reviewed, and signed off by both the Problem Owner and the System Builder. A 
blueprint authored without a signed Builder Brief is not JASPER-compliant and must 
not be submitted to the Validation Pipeline.
The Builder Brief serves three distinct functions:
16.Alignment: It creates a shared, signed record of what the system is required 
to do and what it must never do. Misalignment between problem owner 
expectations and system builder interpretation is the most common source of 
invariant specification errors.
17.Traceability: Each field of the Builder Brief maps directly to one or more 
fields of the Blueprint Schema (see Section 4.3). This mapping ensures full 
requirements traceability from problem domain to deployed runtime.
18.Audit trail: The signed Builder Brief, paired with the sealed Blueprint and 
the Truth Chain, constitutes the complete engineering record of the system's 
intent, specification, and execution history. This record is the foundation of 
compliance auditing.
4.2   Builder Brief Template
The following template defines all required fields of a Genesis Builder Brief. Every field 
is mandatory unless marked [Optional]. Instructions for each field are shown in italics. 
Example values are shown in the shaded example boxes.

HEADER
BRIEF ID
Auto-generated UUID v4. Do not modify after creation.
e.g., a3f8d2c1-7e4b-4a9f-b3d1-0c2e5f8a1234
Brief Date
Date this brief was authored. ISO 8601 format (YYYY-MM-DD).
e.g., 2026-09-08
Brief Author(s)
Full names and roles of all parties who authored this brief.
e.g., Leon Hargrove (Technical Product Owner), Priya Nair (System Architect)
System Name
The canonical name of the system being specified. Must match the blueprint's system 
identifier.
e.g., Settlement Ledger Gateway v2
Version
SemVer version of this Builder Brief. Increment the minor version for substantive content 
changes.

e.g., 1.0.0
PROBLEM STATEMENT
What problem does this system solve?
State the problem in two to four sentences. Focus on the observable symptom and the 
business or operational consequence. Do not describe the solution here.
e.g., Financial settlement instructions are currently processed by an agent 
that reads system time directly, causing non-deterministic ordering of same-
timestamp instructions. This has resulted in three reconciliation failures in 
Q3 2026, each requiring 4–8 hours of manual recovery.
Who are the affected stakeholders?
List every party whose operations, decisions, or obligations are affected by this system's 
behavior or failure.
e.g., Treasury Operations (primary), Compliance and Audit (regulatory 
reporting), Counterparty institutions (downstream settlement recipients), 
Reconciliation Engineering (failure recovery).
What is the cost of failure?
Quantify the cost of system failure if possible. Include financial impact, regulatory exposure, 
and operational cost. This drives the enforcement tier selection in the Invariant Requirements 
section.
e.g., Each reconciliation failure costs approximately $240,000 in operational 
recovery and carries a potential regulatory fine of up to $2M under MiFID II. 

A systemic failure during peak settlement could affect $4.2B of in-flight 
instructions.
SUCCESS CRITERIA
What observable outcomes indicate success?
List concrete, externally observable outcomes that a non-engineer could verify. Avoid internal 
technical states.
e.g., Settlement instructions with identical logical timestamps are processed 
in a stable, reproducible order on every run. Reconciliation failures drop to 
zero within 90 days of deployment.
How is success measured?
Provide quantitative metrics where possible. Specify measurement method, sampling 
frequency, and responsible party.
e.g., Determinism: 100% replay fidelity across 10,000 randomized test traces 
(measured by the Validation Pipeline Dry-Run). Reconciliation: zero failures 
in first 90 days post-deployment (measured by Treasury Operations daily 
report).
What is the minimum viable success threshold?
Define the lowest level of performance that would still represent an acceptable deployment. 
This is the floor, not the target.
e.g., Replay fidelity ≥ 99.99% across test traces, with zero reconciliation 
failures attributable to ordering non-determinism in the first 30 days.

INVARIANT REQUIREMENTS
List each invariant the system must uphold. For each, state the safety implication of 
violation and the enforcement tier. Use one entry per invariant.
# Invariant (Plain 
Language)
Safety Implication 
of Violation
Enforcement Tier
INV-01 No settlement 
instruction may be 
committed with a 
net amount of 
zero or less.
Zero-value 
settlements are 
regulatory noise 
that trigger audit 
flags and 
consume 
reconciliation 
capacity.
Dynamic
INV-02 The sum of all 
committed debits 
must equal the 
sum of all 
committed credits 
at every 
settlement cycle 
boundary.
An imbalance 
indicates a lost or 
duplicated 
instruction, 
resulting in a 
reconciliation 
break with 
counterparty 
exposure.
Dynamic + 
Recovery
INV-03 No instruction 
may reference a 
counterparty 
identifier not 
present in the 
active 
counterparty 
registry at the 
time of 
processing.
Processing an 
instruction for an 
unknown 
counterparty 
creates an 
unresolvable 
settlement 
obligation.
Static + Dynamic
[Add rows as 
needed]

SCOPE BOUNDARY
What is explicitly in scope?
List every function, behavior, or data domain that this system is responsible for. Be specific 
enough that a builder could construct a complete transition set from this list.
e.g., Receiving and canonicalizing inbound settlement instructions; enforcing 
settlement invariants; committing valid instructions to the ledger; emitting 
post-commitment notification effects; maintaining the Truth Chain for this 
system's lifecycle.
What is explicitly out of scope?
List everything this system must not do, even if technically feasible. This prevents scope 
creep and constrains blueprint authoring.
e.g., Counterparty credit risk assessment; foreign exchange conversion; 
instruction routing to downstream settlement networks; user authentication and 
authorization.
What are the known unknowns?
List aspects of the problem domain that are not yet fully understood and may affect blueprint 
authoring. Each known unknown must be resolved before the blueprint is signed and sealed.
e.g., The precise format of the counterparty registry API response is not yet 
finalized (pending Counterparty Services team confirmation). The handling of 
partial settlement (instructions submitted with insufficient funds) has not 
been specified by Treasury Operations.

INPUT CONTRACT
What inputs does this system accept?
List every input event type the system must handle. For each, name the event, its source, 
and its triggering condition.
e.g., SettlementInstruction (inbound from Order Management System); 
CycleCloseCommand (inbound from Settlement Controller); 
CounterpartyRegistryUpdate (inbound from Registry Service).
What are the valid input ranges and formats?
Specify the permissible value ranges, data types, and format constraints for each input. This 
directly informs the Input Canonicalizer configuration.
e.g., SettlementInstruction.amount: decimal, precision 2, range [0.01, 
999,999,999.99]. SettlementInstruction.currency: ISO 4217 3-character code. 
SettlementInstruction.timestamp: ISO 8601 UTC, no future dates.
What inputs must be rejected?
List explicitly any input that must cause a rejection before it reaches the kernel. This 
becomes the Input Canonicalizer's reject list.
e.g., Any instruction with amount ≤ 0; any instruction with a counterparty ID 
not present in the registry; any instruction with a timestamp more than 5 
minutes in the future relative to the injected Clock Oracle value.
EFFECT DECLARATION

What side effects will this system produce?
List every externally visible action this system will take as a result of state transitions. All 
effects must be declared here before they can appear in the Blueprint Schema.
e.g., POST to NotificationService API upon successful instruction commitment; 
write settlement record to AuditLedger upon cycle close; emit 
SettlementCompletedEvent to the downstream message bus.
What external systems will be written to?
List every external system that this system will write to or call in a state-modifying way. 
These become the Effect Handler targets.
e.g., NotificationService (REST API, write); AuditLedger (PostgreSQL database, 
write); SettlementMessageBus (Apache Kafka, produce).
What reversibility guarantees apply?
For each declared effect, state whether it is reversible (can be compensated by a 
corresponding undo effect) or irreversible. Irreversible effects require heightened invariant 
enforcement before commitment.
e.g., NotificationService POST: irreversible (notification already sent). 
AuditLedger write: irreversible (regulatory record). SettlementMessageBus 
produce: irreversible (message consumed by counterparty).
RISK AND OPEN ITEMS
Known risks and mitigations
List each known risk with its likelihood, impact, and the mitigation strategy to be embedded 

in the blueprint design.
e.g., Risk: Counterparty Registry is temporarily unavailable during 
instruction processing. Impact: HIGH (instruction cannot be validated). 
Mitigation: Local cache of registry with TTL; instructions received during 
cache miss are quarantined as poison messages pending registry recovery.
Open decisions blocking blueprint authoring
List every design decision that has not yet been made and that blocks the completion of a 
specific blueprint section. For each, state the blocking section.
e.g., OPEN-01: Partial settlement handling policy (blocks Transitions section 
of Blueprint). OPEN-02: Counterparty registry API response format (blocks 
Input Contract and Input Canonicalizer configuration).
Parties responsible for resolving open items
For each open item, assign a named individual and a target resolution date.
e.g., OPEN-01: Treasury Operations Lead (target: 2026-09-15). OPEN-02: 
Counterparty Services Architect (target: 2026-09-12).
SIGN-OFF
Both sign-offs must be obtained before blueprint authoring may commence.  
Electronic signatures with timestamp are acceptable.
Role Name Signature Date
Problem Owner
System Builder

Effective Date
The date on which this brief becomes the binding design contract. Must be on or after the 
later of the two sign-off dates.
e.g., 2026-09-08
4.3   Builder Brief to Blueprint Mapping
The following traceability table maps each Builder Brief section to the corresponding 
Blueprint Schema field. This mapping ensures that no requirement captured in the  
Builder Brief is orphaned — every stated requirement has a corresponding  
specification artifact in the deployed blueprint.
Builder Brief Section Blueprint Schema 
Field(s)
Notes
HEADER — System Name blueprint_id, version Brief system name 
becomes the blueprint's 
human-readable label; ID 
and version are 
independently assigned
PROBLEM STATEMENT — 
What problem?
Blueprint header 
description field
Summarized in the 
blueprint's 
documentation block; not 
a schema-enforced field 
but required by 
convention
SUCCESS CRITERIA — 
Observable outcomes
invariants[].descriptio
n, telemetry name and 
expression
Each success criterion 
should be traceable to at 
least one invariant or one 
telemetry metric
SUCCESS CRITERIA — 
Quantitative measures
telemetry[] Quantitative success 
metrics become 
telemetry tap definitions 
measuring state fields or 
transition rates

Builder Brief Section Blueprint Schema 
Field(s)
Notes
INVARIANT 
REQUIREMENTS — Each 
invariant
invariants[].name, 
invariants[].predicate, 
invariants[].enforcemen
t_tier
One-to-one mapping. 
Plain-language invariants 
must be translated into 
DSL predicate 
expressions
SCOPE BOUNDARY — In 
scope functions
transitions[] Each in-scope function 
maps to one or more 
named transition 
definitions
SCOPE BOUNDARY — Out 
of scope
No direct mapping — 
documented as blueprint 
exclusions
Out-of-scope items are 
documented in the 
blueprint's exclusions 
block to prevent future 
scope drift
SCOPE BOUNDARY — 
Known unknowns
Open items in blueprint 
version notes
Must be resolved before 
blueprint can be 
submitted to Validation 
Pipeline Stage 3
INPUT CONTRACT — 
Accepted inputs
transitions[].trigger Each accepted input type 
maps to one or more 
transition triggers
INPUT CONTRACT — 
Valid ranges and formats
Input Canonicalizer 
configuration (separate 
from blueprint body)
Input format rules 
configure the Input 
Adapter extension point; 
referenced by 
transitions[].precondit
ion
INPUT CONTRACT — 
Rejected inputs
transitions[].precondit
ion
Rejection conditions are 
encoded as negated 
preconditions; inputs that 
fail preconditions are 
quarantined
EFFECT DECLARATION — 
Side effects
effects[].name, 
effects[].trigger_trans
ition
One-to-one mapping of 
declared effects to effect 
definitions in the 
blueprint
EFFECT DECLARATION — 
External systems
effects[].handler Each external system 
maps to a named Effect 
Handler implementation 
registered at the 
extension point
EFFECT DECLARATION — 
Reversibility
effects[].reversible Boolean field in each 
effect definition; 

Builder Brief Section Blueprint Schema 
Field(s)
Notes
irreversible effects 
trigger heightened pre-
commit invariant 
evaluation
RISK AND OPEN ITEMS — 
Risk mitigations
invariants[], 
transitions[].precondit
ion
Each risk mitigation 
strategy should have a 
corresponding invariant 
or precondition that 
enforces it
SIGN-OFF — Effective 
Date
Blueprint effective_date 
metadata field
The Brief's effective date 
becomes the blueprint's 
minimum valid 
deployment date
Deterministic Runtime Recipe Book  |  Appendix A: Glossary  |  v1.0.0
Appendix A — Glossary
The following definitions apply throughout this specification. Where a term is used  
outside the context of this document, these definitions take precedence over  
common-usage interpretations.
Invariant Boundary
The formal contract between a runtime system and its external environment, specifying 
a set of boolean predicates that must evaluate to true for every reachable state of the 
system, under all possible input sequences, without exception. See Section 1.1.
Genesis State (s₀)
The designated initial state of a JASPER Runtime Kernel instance. Every execution trace begins 
from s₀. The genesis state is declared in the blueprint's genesis_state field and installed 

as the first entry in the State Ledger at binding time. It is the anchor of the Truth Chain. 
See Sections 1.2 and 3.5.
Truth Chain
The immutable, Merkle-chained, linearly ordered log of all state transitions from genesis 
state s₀ to the current state sₙ. Each entry is content-addressed (its hash includes the 
predecessor hash), causally ordered, cryptographically signed, and append-only. The 
Truth Chain enables time-travel debugging, deterministic replay, and compliance 
auditing. See Section 2.3.
Commitment Structure
The three-phase protocol governing all state transitions in the JASPER Runtime Kernel. 
Phase 1 (Propose) computes a candidate successor state and places it in the Staging 
Buffer. Phase 2 (Validate) evaluates all invariant guards against the candidate state. 
Phase 3 (Commit) writes the validated state to the State Ledger and appends a new 
entry to the Truth Chain. See Section 2.4.
Blueprint
A formally structured declarative document (YAML or JSON) conforming to the Genesis 
Blueprint Schema, which completely describes a deterministic runtime configuration for 
a JASPER Runtime Kernel instance. A blueprint specifies the genesis state, all invariants, all 
transitions, all declared effects, and all telemetry hooks. A blueprint is sealed by 
cryptographic signature before deployment. See Part III.
Predicate DSL
The Predicate Expression Domain-Specific Language — a statically typed, purely 
functional, sandboxed expression language used to author invariant predicates, 
transition preconditions, and postconditions within a blueprint. All expressions are 
guaranteed to terminate, produce no side effects, and access no external resources. 
See Section 3.3.

Effect Queue
The ordered buffer maintained by the Effect Isolator into which all side-effecting 
operations (I/O, network calls, disk writes, external messages) are deferred during 
kernel execution. The Effect Queue is flushed after the state transition that authorized 
the effects has been committed to the State Ledger. Effects are executed in declaration 
order. See Section 2.2.
Input Canonicalizer
The kernel component responsible for normalizing all external inputs into a canonical 
deterministic form before they reach any kernel computation. Inputs that cannot be 
canonicalized are rejected at the system boundary. The Canonicalizer is extensible via 
the Input Adapter extension point. See Section 2.2.
Fault Ejector
The kernel component activated upon invariant violation during Phase 2 (Validate) of 
the Commitment Structure. The Fault Ejector halts the affected computation lane, 
discards the Staging Buffer, constructs a structured fault record containing the violating 
state, the triggering input, the failing invariant predicate, and the current Truth Chain 
position, and appends the fault record to the Truth Chain. The Fault Ejector never 
silently swallows a violation. See Section 2.2.
Kernel Extension Point
One of four sanctioned mechanisms by which the JASPER Runtime Kernel may be 
augmented without breaking the Determinism Guarantee: Input Adapters, Effect 
Handlers, Invariant Plugins, and Telemetry Taps. Any modification to the kernel that 
does not go through a sanctioned extension point voids the Determinism Guarantee. 
See Section 2.5.

Deterministic Replay
The operation of re-applying the complete input sequence encoded in the Truth Chain to 
a fresh kernel instance initialized with the same genesis state s₀. Deterministic replay 
must produce an identical final state sₙ and an identical sequence of intermediate 
states. Any divergence between an original execution and its deterministic replay is 
evidence of a non-determinism defect in the kernel. See Section 2.3.
Boundary Tightness
The degree of precision with which an invariant predicate delineates the safe state 
space from the unsafe state space. An optimal invariant is the tightest predicate that 
excludes all unsafe states without excluding any state required for correct operation. 
Overly loose invariants permit unsafe states; overly tight invariants cause excessive 
fault ejection. See Section 1.2.
Deterministic Runtime Recipe Book  |  Appendix B: Quick Reference Card  |  v1.0.0
Appendix B — Quick Reference Card
This appendix provides a compact reference for the four primary technical areas of  
this specification. It is intended for use by practitioners actively working with the  
JASPER Runtime system who require a fast reminder of core definitions without  
navigating the full document.
1. Boundary Math — Core Formulas
Symbol / Formula
Meaning
S = {s₀, s₁, …, s }ₙ

System state space with designated genesis state s₀
Σ
Input alphabet — the complete set of valid external stimuli
δ : S × Σ → S
Transition function — total and deterministic
Reach(s₀, δ)
The set of all states reachable from s₀ under δ
I : S → {true, false}
Invariant predicate over the state space
 s  Reach(s₀, δ) → I(s) = true∀ ∈
The Safety Property — the core obligation
I(δ(s, σ)) = false
Boundary violation — hard runtime fault
I_AB = I_A  I_B∧
Composed invariant — conjunction of subsystem invariants
2. Kernel Components — At a Glance
Component
One-Line Function
Execution Scheduler
Priority-queue dispatch; no preemption without explicit yield

State Ledger
Append-only, content-addressed record of all committed states
Input Canonicalizer
Normalizes all external inputs to canonical form before kernel entry
Clock Oracle
Injects time as an explicit named input; no direct system clock reads
Effect Isolator
Defers all side effects to an Effect Queue; flushed post-commit
Fault Ejector
Halts lane and writes structured fault record on invariant violation
3. Blueprint Schema — Top-Level Fields
Field
Type
Purpose
blueprint_id
UUID v4
Globally unique, immutable blueprint identifier
version
SemVer
Blueprint version; incremented on any content change

genesis_state
Object
Initial state s₀ for the bound kernel instance
invariants
Array
Named invariant definitions with DSL predicate expressions
transitions
Array
Named transition definitions with trigger, precondition, action, postcondition
effects
Array
Declared side effects with handler and reversibility flag
telemetry
Array
Read-only metrics and event hooks (do not mutate state)
4. Commitment Protocol — Phase Summary
Phase
Action
On Success
On Failure

Phase 1
Propose
Compute s'; place in Staging Buffer
→ Phase 2
Lane halted; no state change
Phase 2
Validate
Evaluate all invariant guards against s'
→ Phase 3
Staging Buffer discarded; Fault Ejector activated; fault appended to Truth Chain
Phase 3
Commit
Write s' to State Ledger; append Truth Chain entry; flush Effect Queue
Transition complete; Scheduler notified
Integrity alarm; new commitments halted; manual recovery required
Reference — Enforcement Tiers
Tier 1 — Static:
Type systems, model checkers, SMT solvers (pre-execution)
|
Tier 2 — Dynamic:

Runtime guards, watchdogs, circuit breakers (during execution)
|
Tier 3 — Recovery:
Rollback, checkpoint restore, poison message quarantine (post-violation)
Deterministic Runtime Recipe Book  |  Document Version 1.0.0  |  September 2026  |  DRRB-SPEC-1-0-0
 A Formal Engineering Specification for Deterministic System Construction  |  All Rights Reserved

================================================================================

## Intellectual Property

This specification is authored by Leon Calvin Long II / SQUIRL OS Technologies. The methods and apparatus described herein are claimed in US patent applications — 7 patents pending + 5 SBIR tracks (including 64/114,746 Universal Adaptive Intelligence Orchestration and 64/119,191 Deterministically Governed Probabilistic Neural Computation). Patent ownership remains with Leon Calvin Long II / SquirlOS Technologies; this publication grants study and research USE only, and serves as prior art. Research publications: doi.org/10.5281/zenodo.21613628 | ORCID: orcid.org/0009-0002-1140-9568 | github.com/LLong2026

## Disclaimer

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

Leon Calvin Long II — SQUIRL OS, Self-Healing AI Infrastructure
September 2026
