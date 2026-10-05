# Anthesis community visual experiment

Status: **bounded browser-side experiment contract**

Experiment: `phyllotaxis-utility-v1`

## Purpose

Compare the existing Anthesis community presentation with the Phyllotaxis Utility profile while keeping page content, routes, claims, and primary actions the same.

This is intended to answer whether the denser Utility presentation makes the project easier to understand and navigate. It is not a general personalization or tracking system.

## Variants

- `current` — the pre-Utility Anthesis presentation preserved in `web/site-theme-current.css`.
- `utility` — the Phyllotaxis Utility presentation in `web/site-theme.css`.

Explicit review URLs use:

- `?variant=current`
- `?variant=utility`

An explicit variant overrides and updates the sticky assignment.

## Assignment

`web/experiment.js` resolves the variant in this order:

1. valid `variant` query parameter;
2. existing first-party `anthesis_variant` cookie;
3. 50/50 random assignment.

The assignment cookie stores only `current` or `utility`, uses `SameSite=Lax`, and expires after 30 days. There is no experiment user identifier and no fingerprinting.

With JavaScript disabled, the Utility stylesheet remains the deterministic fallback.

## Event contract

Meaningful navigation actions emit a browser `CustomEvent` named:

`anthesis:experiment`

The event detail contains only:

- experiment name;
- variant;
- event name;
- same-origin page path.

Current event names:

- `try_anthesis`
- `trial_docs`
- `community_github`
- `project_brief`
- `contributing`
- `trial_contact`

No event is transmitted off-device by this implementation. A collector, if added, must consume this contract rather than add independent user identity or fingerprinting.

## Metrics

The primary signals are intentionally task-oriented:

| Event | Interpretation |
| --- | --- |
| `try_anthesis` | visitor found the runnable path |
| `trial_docs` | visitor sought the detailed evaluator workflow |
| `community_github` | visitor inspected the community/source |
| `project_brief` | visitor sought deeper project explanation |
| `contributing` | visitor sought contribution guidance |
| `trial_contact` | visitor showed design-partner/trial intent |

Do not treat raw click-through differences as statistically meaningful without sufficient traffic. For low-volume traffic, combine event counts with structured reviewer/test-user feedback and accessibility/performance checks.

## Collector boundary

Centralized collection is deliberately outside the first browser-side slice.

A future first-party collector should:

- aggregate by experiment, variant, event, and coarse surface only;
- avoid persistent visitor IDs and fingerprinting;
- document retention and access;
- support opt-out where required by the broader observability policy;
- avoid introducing a third-party analytics dependency merely for this experiment;
- preserve the same event schema so the browser implementation stays stable.

Deployment ownership/freshness must be understood before adding an edge collector to the Cloudflare path.

## Review / stopping criteria

Retire the experiment when one of these becomes true:

- the Utility profile is accepted as the default based on qualitative and quantitative evidence;
- the current presentation is retained;
- traffic is too low to support a useful public A/B result and the test is converted to explicit reviewer/user testing;
- maintaining two visual variants begins to create content or accessibility drift.

The experiment should not become permanent theme infrastructure without a separate product requirement.
