import logging
import re
import time
from typing import Dict, List, Tuple, Any

logger = logging.getLogger("ner-a-mcp")

class DialectEngine:
    """
    A sophisticated normalization engine for Arabic dialects.
    Implements prioritized phrase matching, idiomatic lookup, 
    and word-level fallback with confidence scoring.
    """
    
    def __init__(self):
        # 1. Idiomatic full-phrase mappings (High confidence)
        self.idiomatic_mappings = {
            r"عامل ايه يا صاحبي": ("كيف حالك يا صديقي", 1.0),
            r"ايه الدنيا عاملة ايه": ("كيف حال الدنيا", 1.0),
            r"إيه الاخبار": ("ما الأخبار", 1.0),
            r"إيه الأخبار": ("ما الأخبار", 1.0),
            r"ازيك": ("كيف حالك", 0.95),
            r"كيفك": ("كيف حالك", 0.95),
            r"شلونك": ("كيف حالك", 0.95),
            r"ازي الحال": ("كيف حال الأمور", 0.95),
        }
        
        # 2. Sub-phrase mappings (Medium confidence)
        self.phrase_mappings = {
            "عامل ايه": ("كيف حالك", 0.90),
            "ايه الدنيا": ("كيف حال الدنيا", 0.85),
            "الاخبار ايه": ("ما الأخبار", 0.85),
            "على طول": ("مباشرة", 0.90),
        }
        
        # 3. Word-level mappings (Lower confidence for independent words)
        self.word_mappings = {
            "عايز": "أرغب",
            "أقدّم": "التقدم",
            "ايه": "ماذا",
            "عامل": "كيف حال",
            "صاحبي": "صديقي",
            "بؤلّك": "أقول لك",
            "ده": "هذا",
            "دي": "هذه",
            "كويس": "جيد",
            "برضه": "أيضاً",
            "شنو": "ماذا",
            "وايد": "كثيراً",
            "إيش": "ماذا",
            "حق": "لأجل",
            "ماكو": "لا يوجد",
            "بدي": "أريد",
            "هون": "هنا",
            "وين": "أين",
            "مشان": "لأجل",
            "هيك": "هكذا",
            "شلون": "كيف",
            "ماشي": "حسناً",
        }

    def normalize(self, text: str, target: str = "MSA") -> Dict[str, Any]:
        """
        Normalizes dialect text into the target (usually MSA) with confidence scoring.
        """
        start_time = time.time()
        input_text = text.strip()
        normalized_text = input_text
        confidence = 0.5  # Base confidence
        method = "fallback"

        # 1. Check Idiomatic Full Phrases (Regex-based for flexibility)
        for pattern, (replacement, conf) in self.idiomatic_mappings.items():
            if re.search(pattern, input_text):
                normalized_text = re.sub(pattern, replacement, input_text)
                confidence = conf
                method = "idiomatic_phrase"
                break
        
        # 2. If not found, check sub-phrases
        if method == "fallback":
            for phrase, (replacement, conf) in self.phrase_mappings.items():
                if phrase in normalized_text:
                    normalized_text = normalized_text.replace(phrase, replacement)
                    confidence = max(confidence, conf)
                    method = "sub_phrase"

        # 3. Word-level Fallback
        if method == "fallback" or method == "sub_phrase":
            words = normalized_text.split()
            final_words = []
            replaced_count = 0
            
            for word in words:
                cleaned_word = word.strip("؟!.,")
                if cleaned_word in self.word_mappings:
                    replacement = self.word_mappings[cleaned_word]
                    replaced_count += 1
                    # Restore punctuation
                    if cleaned_word != word:
                        replacement = word.replace(cleaned_word, replacement)
                    final_words.append(replacement)
                else:
                    final_words.append(word)
            
            if replaced_count > 0:
                normalized_text = " ".join(final_words)
                # Confidence adjusts based on how many words were actually mapped
                if method == "fallback":
                    confidence = min(0.8, 0.4 + (replaced_count / len(words)) * 0.4)
                    method = "lexical_mapping"
            else:
                method = "no_mapping_found"
                confidence = 0.1

        processing_time_ms = int((time.time() - start_time) * 1000)

        return {
            "original_text": input_text,
            "normalized_text": normalized_text,
            "target_dialect": target,
            "confidence": round(confidence, 2),
            "method_used": method,
            "processing_time_ms": max(1, processing_time_ms)
        }

dialect_engine = DialectEngine()
