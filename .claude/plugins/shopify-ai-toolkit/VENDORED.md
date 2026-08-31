# Vendored: Shopify AI Toolkit

Copied into this repo at Tom's request so the toolkit travels with `gt-site`
rather than depending on each machine having the plugin installed.

| | |
|---|---|
| Upstream | https://github.com/Shopify/Shopify-AI-Toolkit |
| Commit | `51a7d6cbed88fec14658f4e2d243dcdab128cf77` |
| Version | 1.7.0 |
| Licence | MIT — Copyright 2025-present, Shopify Inc. (see `LICENSE`) |
| Vendored | 2026-08-31 |

The commit is the one the `claude-plugins-official` marketplace pins for
`shopify-ai-toolkit@claude-plugins-official`, not the repository's HEAD, so this
copy matches what `claude plugin install` would have fetched.

## Telemetry — on by default

From the toolkit's own `plugin.json`:

> Skill scripts send usage telemetry (queries, code, model/client identifiers)
> to shopify.dev by default; set `OPT_OUT_INSTRUMENTATION=true` to disable.

That includes code. Set `OPT_OUT_INSTRUMENTATION=true` in the environment if
GT's theme source should not leave the machine.

## What is actually relevant here

`gt-site` is a Liquid brand site. Of the 21 skills, the ones that bear on it
are `shopify-liquid` (Liquid validation), `shopify-dev` (docs search),
`shopify-admin` (Admin API schema) and `shopify-use-shopify-cli`. The rest
cover Hydrogen, POS UI, Polaris extensions, Functions and payments apps — about
66 MB of the 85 MB here is TypeScript type definitions for those surfaces.

## Updating

Re-copy from upstream at a new commit and update the table above. Nothing in
this directory is edited locally; local changes would be lost on the next copy.
