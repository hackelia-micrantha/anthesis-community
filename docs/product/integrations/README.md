# Integration Modes

Anthesis integration strength depends on whether the agent can perform externally observable effects without crossing Anthesis.

## Enforcement Strength

- **Advisory:** Anthesis recommends or records decisions, but raw effect paths remain available.
- **Moderate:** agents are configured to use Anthesis paths, but bypass is possible without additional controls.
- **Strong:** registries, credentials, network paths, or downstream validators prevent most bypasses.
- **Runtime-enforced:** the runtime prevents direct external effects except through Anthesis-controlled paths.

## Modes To Evaluate

| Mode | Core bypass question | Typical strength |
|---|---|---|
| Tool wrapper / `invoke` | Does the agent tool registry contain only Anthesis-controlled tools? | Moderate to strong |
| MCP mediation | Does the MCP registry expose only Anthesis? | Moderate to strong |
| Gateway / sidecar | Can network and process access force effects through Anthesis? | Strong |
| Capability tokens | Do downstream tools reject calls without Anthesis-issued grants? | Strong |
| SDK wrapper | Can code still import direct clients or use raw credentials? | Advisory to moderate |
| Sandboxed runtime | Does the runtime make bypass impossible for governed effects? | Runtime-enforced |

Prompts and conventions are not guarantees. Guarantees come from runtime control surfaces: registry restriction, network isolation, capability validation, gateway enforcement, credential isolation, and sandboxing.
