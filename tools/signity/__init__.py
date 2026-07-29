"""Signity Ledger の参照実装。

外部依存は YAML 読み込み時の PyYAML のみ。JSON のみを扱う場合は不要。

正本は docs/architecture/ 以下の設計文書と
schemas/decision-event.schema.v0.3.json であり、本パッケージはその実装である。
食い違った場合は正本を正とする。
"""

from .canonical import CANONICALIZATION, canonicalize, content_hash
from .ledger import compute_chain, load, verify_chain
from .projection import project

__all__ = [
    "CANONICALIZATION",
    "canonicalize",
    "content_hash",
    "compute_chain",
    "load",
    "verify_chain",
    "project",
]
