from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class TriageResult:
    """
    Output of the triage engine.

    decision:
        - AUTO_RESOLVE: safe to persist without human review
        - HUMAN_REVIEW: send to review queue
        - ESCALATE: conflicting or high-risk case requiring attention

    priority_score:
        Higher = reviewed sooner
    """
    decision: str
    priority_score: float
    reason_codes: List[str]


class IdentityReviewTriage:
    """
    MA-048: Identity Review Triage & Escalation Rules Engine

    Converts enriched identity + confidence output into:
    - decision routing (auto / review / escalate)
    - priority ranking for human review queue
    - structured reason codes for explainability
    """

    AUTO_RESOLVE_THRESHOLD = 0.90
    REVIEW_THRESHOLD = 0.75

    CONFLICT_PENALTY = 0.20
    MISSING_EVIDENCE_PENALTY = 0.15

    def __init__(self):
        pass

    # -------------------------
    # Public API
    # -------------------------
    def triage(self, identity_payload: Dict[str, Any]) -> TriageResult:
        """
        Expected input shape (flexible):
        {
            "confidence": float,
            "provider_scores": {"discogs": float, "musicbrainz": float, ...},
            "evidence": {
                "official_url": bool,
                "spotify_match": bool,
                "social_links": bool
            }
        }
        """

        confidence = float(identity_payload.get("confidence", 0.0))
        provider_scores = identity_payload.get("provider_scores", {}) or {}
        evidence = identity_payload.get("evidence", {}) or {}

        reason_codes: List[str] = []

        adjusted_confidence = self._adjust_confidence(
            confidence,
            provider_scores,
            evidence,
            reason_codes,
        )

        decision = self._decide(adjusted_confidence, provider_scores, reason_codes)
        priority_score = self._compute_priority(adjusted_confidence, reason_codes)

        return TriageResult(
            decision=decision,
            priority_score=priority_score,
            reason_codes=reason_codes,
        )

    # -------------------------
    # Decision Logic
    # -------------------------
    def _adjust_confidence(
        self,
        base: float,
        provider_scores: Dict[str, float],
        evidence: Dict[str, Any],
        reason_codes: List[str],
    ) -> float:

        adjusted = base

        # Conflict detection across providers
        if len(provider_scores) >= 2:
            scores = list(provider_scores.values())
            spread = max(scores) - min(scores)

            if spread > 0.25:
                adjusted -= self.CONFLICT_PENALTY
                reason_codes.append("provider_conflict")
            elif spread > 0.15:
                adjusted -= self.CONFLICT_PENALTY / 2
                reason_codes.append("provider_moderate_disagreement")

        # Evidence completeness
        evidence_flags = [
            evidence.get("official_url"),
            evidence.get("spotify_match"),
            evidence.get("social_links"),
        ]

        missing = sum(1 for v in evidence_flags if not v)

        if missing >= 2:
            adjusted -= self.MISSING_EVIDENCE_PENALTY
            reason_codes.append("low_evidence_support")
        elif missing == 1:
            adjusted -= self.MISSING_EVIDENCE_PENALTY / 2
            reason_codes.append("partial_evidence")

        # Clamp
        return max(0.0, min(1.0, adjusted))

    def _decide(
        self,
        confidence: float,
        provider_scores: Dict[str, float],
        reason_codes: List[str],
    ) -> str:

        # Hard conflict override
        if "provider_conflict" in reason_codes and confidence < 0.85:
            return "ESCALATE"

        if confidence >= self.AUTO_RESOLVE_THRESHOLD:
            return "AUTO_RESOLVE"

        if confidence >= self.REVIEW_THRESHOLD:
            return "HUMAN_REVIEW"

        return "ESCALATE"

    def _compute_priority(self, confidence: float, reason_codes: List[str]) -> float:
        """
        Higher score = higher priority in review queue.
        """
        base = 1.0 - confidence

        # escalate urgency
        if "provider_conflict" in reason_codes:
            base += 0.25
        if "low_evidence_support" in reason_codes:
            base += 0.15
        if "partial_evidence" in reason_codes:
            base += 0.05

        return round(min(1.0, max(0.0, base)), 4)