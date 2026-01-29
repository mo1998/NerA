import re

class ShariaEngine:
    """
    A rule-based engine to check Sharia compliance in contracts.
    """
    
    NON_COMPLIANT_KEYWORDS = [
        r"\bربا\b",         # Riba (Interest)
        r"\bفائدة\b",       # Interest
        r"\bفوائد\b",       # Interests
        r"\bميسر\b",        # Maisir (Gambling/Speculation)
        r"\bغرر\b",         # Gharar (Excessive uncertainty)
        r"\bقمار\b",        # Gambling
        r"\bنسبة مئوية سنوية\b", # APR
    ]

    COMPLIANT_KEYWORDS = [
        r"\bمرابحة\b",      # Murabaha
        r"\bمشاركة\b",      # Musharaka
        r"\bصكوك\b",        # Sukuk
        r"\bزكاة\b",        # Zakat
        r"\bإسلامي\b",       # Islamic
        r"\bشرعي\b",        # Sharia-compliant
    ]

    def check(self, text: str, school: str = "Hanafi") -> dict:
        issues = []
        for pattern in self.NON_COMPLIANT_KEYWORDS:
            if re.search(pattern, text):
                term = pattern.replace(r"\b", "")
                issues.append(f"Potential non-compliant term detected: {term}")
        
        status = "compliant" if not issues else "non-compliant"
        
        return {
            "status": status,
            "reasons": issues,
            "school_applied": school,
            "references": ["AAOIFI-Standard-21"] if issues else []
        }

sharia_engine = ShariaEngine()
