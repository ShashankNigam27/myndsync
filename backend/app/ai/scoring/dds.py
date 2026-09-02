import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class DynamicDistressScorer:
    """Deterministic Dynamic Distress Score (DDS) Calculation Engine (Section 15).

    NOTE ON WEIGHTS:
    Per Section 15 of engineering-master-spec.md:
    Initial illustrative weights below are ASSUMPTIONS and require clinical validation
    before real-world deployment. The formula is strictly deterministic (not ML)
    to guarantee transparency, interpretability, and auditability.
    """

    # Illustrative component weights (ASSUMPTION — PENDING CLINICAL VALIDATION)
    WEIGHT_SENTIMENT: float = 0.30       # w1: NLP Sentiment component
    WEIGHT_EMOTION: float = 0.25         # w2: Emotion classification component
    WEIGHT_VOICE_STRESS: float = 0.20    # w3: Voice stress (redistributed proportionally when absent)
    WEIGHT_ENGAGEMENT: float = 0.15      # w4: Engagement dropoff / latency component
    WEIGHT_CONTEXTUAL: float = 0.10      # w5: Contextual risk factors (e.g., active threat, hearing date)

    # Risk Band Thresholds per Section 15
    # Low: 0-39 | Moderate: 40-59 | High: 60-79 | Critical: 80-100
    THRESHOLD_MODERATE: float = 40.0
    THRESHOLD_HIGH: float = 60.0
    THRESHOLD_CRITICAL: float = 80.0

    @classmethod
    def compute_score(
        cls,
        sentiment_score: float,
        was_skipped: bool = False,
        response_latency_sec: Optional[int] = None,
        emotion_label: Optional[str] = None,
        voice_stress_score: Optional[float] = None,
        contextual_risk_score: Optional[float] = None,
    ) -> float:
        """Compute instantaneous DDS score (0.0 - 100.0) via deterministic formula with proportional weight redistribution."""
        active_components: List[Tuple[float, float]] = []

        # 1. Sentiment component: [-1.0, 1.0] -> [0.0, 100.0] distress
        # Polarity -1.0 (severe distress) -> 100.0; +1.0 (peace/safe) -> 0.0
        sentiment_distress = ((1.0 - max(-1.0, min(1.0, sentiment_score))) / 2.0) * 100.0
        active_components.append((cls.WEIGHT_SENTIMENT, sentiment_distress))

        # 2. Emotion component (when available)
        if emotion_label:
            emotion_map = {
                "fear": 90.0,
                "hopelessness": 85.0,
                "anger": 70.0,
                "sadness": 60.0,
                "neutral": 20.0,
            }
            emotion_val = emotion_map.get(emotion_label.lower(), 50.0)
            active_components.append((cls.WEIGHT_EMOTION, emotion_val))

        # 3. Voice stress component: [0.0, 1.0] -> [0.0, 100.0] (when available)
        if voice_stress_score is not None:
            voice_distress = max(0.0, min(1.0, voice_stress_score)) * 100.0
            active_components.append((cls.WEIGHT_VOICE_STRESS, voice_distress))

        # 4. Engagement dropoff component: [0.0, 100.0]
        if was_skipped:
            engagement_distress = 80.0  # Skipped check-in indicates potential disengagement / risk
        elif response_latency_sec is not None:
            # Latency scaling: 0s-10s -> 15.0, 30s -> 45.0, 60s+ -> 90.0
            engagement_distress = min(100.0, max(15.0, float(response_latency_sec) * 1.5))
        else:
            engagement_distress = 20.0  # Default nominal engagement
        active_components.append((cls.WEIGHT_ENGAGEMENT, engagement_distress))

        # 5. Contextual risk component: [0.0, 100.0]
        if contextual_risk_score is not None:
            contextual_val = max(0.0, min(100.0, contextual_risk_score))
        else:
            contextual_val = 20.0  # Default nominal contextual risk
        active_components.append((cls.WEIGHT_CONTEXTUAL, contextual_val))

        # Proportional weight redistribution for active components
        total_weight = sum(w for w, _ in active_components)
        if total_weight <= 0:
            return 50.0

        raw_dds = sum((w / total_weight) * val for w, val in active_components)
        # Clamp to [0.0, 100.0]
        return max(0.0, min(100.0, round(raw_dds, 2)))

    @classmethod
    def determine_risk_band(
        cls, score: float, safety_keyword_flag: bool = False
    ) -> str:
        """Assign categorical risk band per Section 15 thresholds."""
        if safety_keyword_flag or score >= cls.THRESHOLD_CRITICAL:
            return "critical"
        elif score >= cls.THRESHOLD_HIGH:
            return "high"
        elif score >= cls.THRESHOLD_MODERATE:
            return "moderate"
        else:
            return "low"

    @staticmethod
    def calculate_trend_slope(
        past_scores: List[float], current_score: float, window_size: int = 5
    ) -> float:
        """Calculate linear trend slope over the most recent check-in scores.

        A positive slope indicates deteriorating condition (increasing distress).
        A negative slope indicates improving condition.
        """
        all_scores = past_scores + [current_score]
        recent = all_scores[-window_size:]
        n = len(recent)

        if n < 2:
            return 0.0

        x = list(range(n))
        y = recent
        mean_x = sum(x) / n
        mean_y = sum(y) / n

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        slope = numerator / denominator
        return round(slope, 2)


# Global singleton instance
distress_scorer = DynamicDistressScorer()
