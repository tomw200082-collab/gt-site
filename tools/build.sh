#!/usr/bin/env bash
# Rebuild src/index.html (Hebrew) from src/index.en.html + the i18n catalogue.
# Every step is idempotent: the English source is never modified.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/extract_strings.py
python3 tools/build_catalogue.py
python3 tools/apply_translation.py
python3 tools/patch_hebrew_build.py
python3 tools/patch_rtl_shell.py
python3 tools/patch_form_intake.py
node    tools/validate.js
