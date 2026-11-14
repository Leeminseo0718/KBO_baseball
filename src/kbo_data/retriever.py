from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_KNOWLEDGE = Path(__file__).resolve().parents[2] / "knowledge" / "metrics.jsonl"


@dataclass(frozen=True)
class Hit:
    doc: dict[str, Any]
    score: float
    matched_alias: str | None


def _grams(text: str) -> Counter[str]:
    compact = re.sub(r"\s+", "", text.lower())
    grams = [compact[i : i + 2] for i in range(len(compact) - 1)]
    return Counter(grams or [compact])


class MetricRetriever:
    """Finds the metric definitions that a question refers to.

    Scoring is lexical so it runs offline and is reproducible: a character-bigram
    TF-IDF cosine, plus a fixed bonus when one of the metric's aliases appears
    in the question. Only definitions stored in knowledge/metrics.jsonl can be
    returned, which is what lets the planner refuse metrics it has no definition for.
    """

    ALIAS_BONUS = 1.0

    def __init__(self, path: Path | None = None) -> None:
        source = path or DEFAULT_KNOWLEDGE
        self.docs = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
        texts = [" ".join([doc["name"], *doc["aliases"], doc["definition"]]) for doc in self.docs]
        self._vectors = [_grams(text) for text in texts]
        document_frequency: Counter[str] = Counter()
        for vector in self._vectors:
            document_frequency.update(vector.keys())
        self._idf = {gram: math.log((1 + len(self.docs)) / (1 + count)) + 1 for gram, count in document_frequency.items()}

    def _cosine(self, query: Counter[str], doc: Counter[str]) -> float:
        dot = sum(query[g] * doc[g] * self._idf.get(g, 0.0) ** 2 for g in query if g in doc)
        norm_q = math.sqrt(sum((v * self._idf.get(g, 1.0)) ** 2 for g, v in query.items()))
        norm_d = math.sqrt(sum((v * self._idf.get(g, 1.0)) ** 2 for g, v in doc.items()))
        return dot / (norm_q * norm_d) if norm_q and norm_d else 0.0

    def search(self, question: str, k: int = 3, min_score: float = 1.0) -> list[Hit]:
        lowered = question.lower()
        query = _grams(question)
        hits = []
        for doc, vector in zip(self.docs, self._vectors):
            aliases = sorted(doc["aliases"], key=len, reverse=True)
            matched = next((alias for alias in aliases if alias.lower() in lowered), None)
            score = self._cosine(query, vector) + (self.ALIAS_BONUS if matched else 0.0)
            if score >= min_score:
                hits.append(Hit(doc, round(score, 4), matched))
        hits.sort(key=lambda hit: (-hit.score, -len(hit.matched_alias or "")))
        # "탈삼진" also contains "삼진"; keep the longest alias when one hit's alias sits inside another's.
        kept: list[Hit] = []
        for hit in hits:
            if any(hit.matched_alias and other.matched_alias and hit.matched_alias != other.matched_alias
                   and hit.matched_alias in other.matched_alias for other in hits):
                continue
            kept.append(hit)
        return kept[:k]
