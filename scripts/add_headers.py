# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: CC0-1.0
"""Idempotently prepend the org header to first-party .py files (RR-B-03/04)."""
import pathlib

HEADER = ("# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.\n"
          "# SPDX-License-Identifier: CC0-1.0\n")

for path in [*pathlib.Path("src").rglob("*.py"), *pathlib.Path("tests").rglob("*.py"),
             *pathlib.Path("scripts").rglob("*.py")]:
    text = path.read_text(encoding="utf-8")
    if "SPDX-License-Identifier" in text[:200]:
        continue
    path.write_text(HEADER + text, encoding="utf-8")
    print(f"headered {path}")
