# Anthesis Envelope

The Anthesis Envelope is an encapsulated lifecycle contract that carries intent, normalized input, plan, policy decision, capabilities, approvals, evidence, results, evaluation, and audit metadata through an agentic workflow.

```text
input
  -> normalize
  -> plan
  -> govern
  -> authorize capabilities
  -> execute
  -> collect evidence
  -> evaluate
  -> audit / learn
```

The envelope is the object a trial should inspect to prove what was requested, what was allowed or denied, who or what acted, what scope was granted, what happened, and what evidence remains.

For most local or single-organization trials, signed envelopes plus hash-chained append-only logs are likely enough. Ledger-style anchoring is a research option, not the default assumption.
