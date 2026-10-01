---
layout: default
title: Tor Nelson - Resume
name: Tor Nelson
location: Seattle, Washington
phone: (425) 686-8842
email: tor.nelson@gmail.com
links:
  - text: linkedin.com/in/tornelson
    url: https://linkedin.com/in/tornelson
  - text: github.com/TSNelson
    url: https://github.com/TSNelson
  - text: onmission.systems
    url: https://onmission.systems
stack: TypeScript / JavaScript · React · Node/Express · PostgreSQL · REST APIs · Vitest · Git · PowerShell · Python
pdf: Tor-Nelson-Resume.pdf
---

**Systems engineer who builds the machinery that makes automation and AI reliable in production.** For seven years I've done this in customer environments I didn't design, where the work usually starts from a symptom rather than a specification: monitoring that catches failures before users report them, closed-loop remediation, and version-controlled operations across roughly ten client businesses. Since 2025 I've applied the same discipline to AI-driven software development. I architected and built Copybook, a production SaaS, and the specification-first, review-gated development harness that produced it: agents implement, generated tests hold the code to its specification, and human judgment moves up the stack to architecture, design, and review.

## Experience

### Founder / Systems & Product Engineer — OnMission Systems

**Seattle, WA · 2025 – Present** *(concurrent with Prairie IT Services)*

Designed and built **Copybook** ([URL: Copybook link]), a production SaaS for developing AI literacy by designing intentional AI interactions, and the AI development harness that produced it.

- **Architected the product and built it to production standard.** TypeScript end to end: React 18 and Vite, Express, Drizzle ORM on Neon serverless PostgreSQL, Zod, Zustand, and TanStack Query, with Stripe payments, Passport (local and Google OAuth), Helmet, CSRF protection, rate limiting, and Winston logging. Set the architecture and design patterns, and directed the refactors that held the codebase to them.
- **Designed and operated the development harness.** Staged planning carries each change from product design through system-change planning to phased implementation, with a review gate at every stage boundary and decision records and validation reports keeping the work auditable. Review began as line-by-line reading of generated code and relaxed as the harness proved reliable, with automation increasing to match.
- **Built explicit controls around AI-generated implementation.** Specification precedes implementation, and generated unit and integration tests, weighted toward integration for reliability, hold the code to the specification through a tiered automated release gate. A written testing philosophy governs what the agents generate, so a suite of more than 1,000 tests stays consistent and every test earns its place.
- **Treated documentation as code to keep the codebase agent-legible.** Guard tests enforce the claims the documentation makes, so it can't drift into misleading context for the agents that read it.
- **Designed Copybook's instruction catalogue and the taxonomy behind it.** Techniques are classified by the model behavior they're meant to produce, and the product shows why each works and when to use it, so users build judgment rather than follow recipes.
- **Generalized the harness into a method for AI-collaborative workflows.** Staged and artifact-centered, with explicit authorities, interaction contracts, escalation rules, and gates. The software workflow is the first complete instance; its principles are being carried into other knowledge-work domains and into agent-skill development.

### IT Consultant & Automation Engineer — Prairie IT Services *(independent contractor)*

**Seattle, WA · May 2019 – Present**

Owned automation, monitoring, and remediation for roughly ten small-business clients and several hundred endpoints in a two-person managed-services practice. Self-initiated the function and carried it from scripts through monitoring to closed-loop remediation, alongside daily operations and end-user support. Every system below is still in production.

- **Built the detection layer and integrated it with operations.** Monitoring opens tickets on early-warning conditions with relevant diagnostic logs already attached, so work begins with evidence rather than a user's description of the symptom. Scheduled work generates its own work orders, shifting the queue from user-reported breakage toward detected conditions.
- **Built closed-loop remediation.** Automated detection and repair of system-file corruption, a recurring incident class now resolved without a technician touching the machine.
- **Built backup reliability automation.** Failure detection, restore validation, and automated recovery workflows, replacing after-the-fact discovery of failed backups.
- **Replaced manual administration with version-controlled operations.** A composable PowerShell function library for Microsoft 365 and Exchange Online administration, standardized across every client tenant, so operations are repeatable and reviewable rather than point-and-click.
- **Established a recurring security review process** across the client base, including the procedure, its execution, and supporting documentation.
- **Run the operational surface underneath it all.** Windows desktop and server administration, endpoint support and triage, RMM administration, patching, identity and license lifecycle, and the ticket queue. With no escalation tier, diagnosis and resolution are one person's job.

## Technical

**AI & software systems** — development harness design, specification-driven implementation, review-gate architecture, generated test suites as behavioral contracts, guard-enforced invariants, agent workflow design, instruction and interaction design

**Software engineering** — software architecture and design patterns, TypeScript, JavaScript, React, Node/Express, PostgreSQL, REST APIs, Git, automated testing (Vitest, Testing Library, Supertest), spec-first and test-driven development, Python

**Automation & reliability** — PowerShell, Bash, composable function libraries, version-controlled operational tooling, scheduled and event-triggered automation, monitoring and detection, diagnostic capture, closed-loop remediation, backup verification and recovery, failure-mode analysis

**Infrastructure & operations** — Windows desktop and server administration, Microsoft 365 and Exchange Online, identity and license lifecycle, endpoint management and remediation, RMM (N-able N-central), ticketing workflow design, runbook and procedure documentation, security review

## Education

**B.S., The Evergreen State College** — Molecular Biology and Biochemistry
