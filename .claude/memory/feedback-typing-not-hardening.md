---
name: feedback-typing-not-hardening
description: When asked to improve typing, add annotations only — no runtime guards or behavior changes unless explicitly requested
metadata:
  type: feedback
---

When the user asks to "type" or "harden" a function in the typing sense, they mean better type hints — not new runtime validation, raises, or error-message changes.

**Why:** During the `Indicator.__call__` typing work (Aug 2026), "harden?" on `_get_series` was taken as license to add column-existence checks and a ValueError for `item=` on non-DataFrame input; the user rejected it: "no revert. i just meant better typing hints."

**How to apply:** Keep typing work annotation-only. If a runtime guard seems genuinely worthwhile, propose it separately and let the user opt in before writing it.
