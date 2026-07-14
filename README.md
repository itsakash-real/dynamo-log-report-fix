# log-report — Fixed Terminal-Bench 2 (Harbor) Task

A Harbor task that parses an Apache-style access log and produces a small JSON
summary report. This repo contains the **fixed** version of a task that was
originally broken in several ways (see below).

## What it does

Given `access.log` in the working directory, the agent must write
`/app/report.json` containing:
- `total_requests` — count of non-empty log lines
- `unique_ips` — count of distinct client IPs
- `top_path` — most frequently requested URL path

## What was broken (and fixed)

| Area | Original problem | Fix |
|---|---|---|
| `task.toml` | `artifacts` was a string pointing to the wrong file (`/app/out.json`) | Now a top-level array pointing to the real output (`/app/report.json`) |
| `Dockerfile` | Base image was `python:latest` (unpinned); leaked `solution_hint.py` (a full reference solution) into the agent image | Pinned to `python:3.13-slim-bookworm@sha256:...`; leaked file removed |
| Verifier | Only checked the output file existed and was non-empty — a no-op agent could pass | Rewritten to parse the JSON and assert every value against the real log contents |
| `instruction.md` | Didn't state the output path/schema; missing required timeout line | Rewritten with exact schema and the mandatory "You have 120 seconds…" line |

## Verify it yourself

```bash
harbor run -p . --agent oracle   # reward 1.0
harbor run -p . --agent nop      # reward 0.0
```

Full defect list and calibration evidence are in the PR/submission notes.
