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

## Pruned to four skills

`gt-site` is a Liquid brand site, so only the skills that bear on one were
kept:

| skill | what it does here |
|---|---|
| `shopify-liquid` | Liquid syntax and theme-architecture validation |
| `shopify-dev` | shopify.dev documentation search |
| `shopify-admin` | Admin API schema access |
| `shopify-use-shopify-cli` | store and theme management via the CLI |

The other seventeen — Hydrogen, POS UI, the four Polaris extension surfaces,
Functions, payments apps, partner, app-store review, onboarding, ShopifyQL,
storefront GraphQL, custom data, customer, ucp — were removed. They were
mostly TypeScript definitions for surfaces this repo does not touch: **85 MB
and 13,245 files became 6.5 MB and 66.**

Nothing dangles: no manifest in this plugin enumerates skill directories, they
are discovered from `skills/`. To restore one, copy it back from upstream at
the pinned commit.

## Updating

Re-copy from upstream at a new commit and update the table above. Nothing in
this directory is edited locally; local changes would be lost on the next copy.
