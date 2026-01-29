import re

class NewsTrustEngine:
    """
    Scores Arabic news credibility based on linguistic markers and sources.
    """
    
    FAKE_NEWS_MARKERS = [
        r"عاجل جدا",        # Very Urgent
        r"صدمة",            # Shocking
        r"شاهد قبل الحذف",   # Watch before delete
        r"لن تصدق",         # You won't believe
        r"فضيحة",           # Scandal
        r"مصادر سرية",       # Secret sources
    ]
    
    TRUSTED_SOURCES = [
        "واس",              # SPA (Saudi Press Agency)
        "كونا",             # KUNA
        "وام",              # WAM
        "الشرق الأوسط",
        "الجزيرة",
        "العربية"
    ]

    def analyze(self, text: str) -> dict:
        score = 1.0
        details = []
        
        for marker in self.FAKE_NEWS_MARKERS:
            if re.search(marker, text):
                score -= 0.15
                details.append(f"Clickbait/Sensationalist marker detected: {marker}")
        
        # Check for source mentions
        source_found = False
        for source in self.TRUSTED_SOURCES:
            if source in text:
                score += 0.1
                details.append(f"Mention of reputable source: {source}")
                source_found = True
        
        score = max(0.0, min(1.0, score))
        
        return {
            "trust_score": round(score, 2),
            "indicators": details,
            "verdict": "high" if score > 0.8 else "medium" if score > 0.5 else "low"
        }

news_trust_engine = NewsTrustEngine()
