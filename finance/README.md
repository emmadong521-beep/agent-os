# Finance Domain Layer

`finance/` is the finance domain layer for Agent Finance.

It sits on top of the shared Agent Runtime and contains finance-specific agent definitions, scopes, templates, examples, and common conventions. The design is one shared runtime plus multiple specialized finance agents.

## Architecture

- **Shared runtime:** task execution, workflows, memory, reflection, executor adapters, and contracts
- **Finance domain layer:** finance business context, report templates, common definitions, and sample datasets
- **Specialized finance agents:** focused agents for specific finance workflows

## Planned Agents

- `budget_variance`: Budget Variance & Business Insight Agent
- `compliance_review`: finance compliance and policy review assistant
- `ar_risk`: accounts receivable risk analysis agent
- `reconciliation`: reconciliation support agent
- `controlled_qa`: controlled finance knowledge Q&A agent

## Current MVP

The first MVP agent is `budget_variance`, focused on budget vs actual comparison, variance attribution, abnormal item detection, and management report generation.
