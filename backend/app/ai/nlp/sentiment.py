import logging
import re
from typing import NamedTuple, Optional

logger = logging.getLogger(__name__)


class SentimentResult(NamedTuple):
    sentiment_score: float  # -1.0 (severe distress/negative) to +1.0 (positive/safe)
    confidence: float       # 0.0 to 1.0
    model_name: str


class SentimentAnalyzer:
    """Multilingual sentiment and distress signal extraction engine.

    NOTE: For local development and lightweight prototyping, this engine utilizes
    a calibrated multilingual lexicon and distress keyword parser for Hindi, Hinglish,
    and English. In production, this can be swapped with fine-tuned IndicBERT / MuRIL
    transformers via configuration without altering the interface.
    """

    # Distress / negative keywords (English, Hindi Devanagari, and Romanized Hinglish)
    SEVERE_DISTRESS_KEYWORDS = {
        # English
        "kill", "die", "suicide", "threat", "attack", "destroy", "violence", "burn",
        "murder", "assault", "terrified", "panic", "hopeless", "ruined",
        # Hindi Devanagari
        "मार", "मरना", "धमकी", "हमला", "डर", "खतरा", "बर्बाद", "हिंसा", "दहशत",
        # Hinglish
        "dhamki", "marne", "darr", "khatra", "hamla", "barbaad", "jaan", "marenge",
    }

    NEGATIVE_KEYWORDS = {
        # English
        "afraid", "anxious", "scared", "fear", "worried", "sad", "uneasy", "crying",
        "alone", "stress", "trouble", "unsafe", "pain", "harass", "pressure", "insult",
        # Hindi Devanagari
        "चिंता", "परेशान", "घबराहट", "अकेला", "रो", "दुख", "अपमान", "दबाव", "असुरक्षित",
        # Hinglish
        "chinta", "pareshan", "ghabrahat", "akela", "dukhi", "rone", "apman", "dabav", "unsafe",
    }

    POSITIVE_KEYWORDS = {
        # English
        "safe", "good", "fine", "better", "relieved", "okay", "peace", "calm", "happy",
        "protected", "support", "help", "grateful",
        # Hindi Devanagari
        "सुरक्षित", "अच्छा", "ठीक", "राहत", "शांत", "मदद", "खुश",
        # Hinglish
        "surakshit", "accha", "theek", "rahat", "shant", "madad", "khush", "thik",
    }

    NEGATION_WORDS = {"not", "no", "never", "nahin", "nahi", "nhi", "नहीं", "मत"}

    def __init__(self, model_name: str = "lightweight-multilingual-indic"):
        self.model_name = model_name
        logger.info(
            f"[NLP Engine] Initialized sentiment analyzer using '{self.model_name}' "
            "(Lightweight development engine calibrated for PoA Act distress signals)"
        )

    def analyze(self, text: Optional[str]) -> SentimentResult:
        """Analyze text response and extract continuous distress/sentiment score and confidence."""
        if not text or not text.strip():
            # Neutral fallback for empty / unprovided text
            return SentimentResult(
                sentiment_score=0.0,
                confidence=0.5,
                model_name=self.model_name,
            )

        cleaned = text.strip().lower()
        words = re.findall(r"[\w\u0900-\u097F]+", cleaned)

        if not words:
            return SentimentResult(
                sentiment_score=0.0,
                confidence=0.5,
                model_name=self.model_name,
            )

        severe_neg_count = 0
        neg_count = 0
        pos_count = 0

        # Scan words with negation awareness
        for i, word in enumerate(words):
            is_negated = (i > 0 and words[i - 1] in self.NEGATION_WORDS) or (
                i > 1 and words[i - 2] in self.NEGATION_WORDS
            )

            if word in self.SEVERE_DISTRESS_KEYWORDS:
                if is_negated:
                    pos_count += 0.5
                else:
                    severe_neg_count += 1
            elif word in self.NEGATIVE_KEYWORDS:
                if is_negated:
                    pos_count += 0.5
                else:
                    neg_count += 1
            elif word in self.POSITIVE_KEYWORDS:
                if is_negated:
                    neg_count += 1
                else:
                    pos_count += 1

        # Calculate sentiment score (-1.0 to +1.0)
        # Weight severe distress heavily
        neg_weight = (severe_neg_count * 2.0) + (neg_count * 1.0)
        pos_weight = pos_count * 1.0
        total_signals = neg_weight + pos_weight

        if total_signals == 0:
            # No strong explicit sentiment markers found -> mildly neutral
            sentiment_score = 0.0
            confidence = 0.6
        else:
            raw_score = (pos_weight - neg_weight) / (total_signals + 0.5)
            # Clamp between -1.0 and 1.0
            sentiment_score = max(-1.0, min(1.0, round(raw_score, 3)))
            # Confidence scales with volume of identified signals and length
            confidence = min(0.95, round(0.65 + (0.05 * total_signals), 2))

        return SentimentResult(
            sentiment_score=sentiment_score,
            confidence=confidence,
            model_name=self.model_name,
        )


# Global singleton instance
sentiment_analyzer = SentimentAnalyzer()
