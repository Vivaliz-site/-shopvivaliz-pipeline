# Global task continuity
Policy: `GLOBAL_TASK_CONTINUITY_V8`.

This repository is governed by the canonical detached-recovery controller in
`Vivaliz-site/site-shopvivaliz`. The adapter at
`scripts/agent_task_state.py` pins `repository=Vivaliz-site/-shopvivaliz-pipeline` and fails closed
rather than creating an unmonitored local checkpoint.

Production recovery is watchdog -> dispatcher -> Gemini -> durable checkpoint.
A repository is certified only after a real `continuity_e2e_pass` for the
same repository identity. Codex is not used by background recovery and remains
the last explicit finite option.
