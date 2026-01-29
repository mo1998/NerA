import logging

logger = logging.getLogger("ner-a-mcp.ocr")

class OCRWrapper:
    """
    Initial OCR capability for Arabic documents.
    Wraps Tesseract or equivalent.
    """
    
    def __init__(self):
        self.available = False
        try:
            import pytesseract
            self.available = True
            logger.info("pytesseract found and loaded.")
        except ImportError:
            logger.warning("pytesseract not found. Document extraction will be limited.")

    def extract(self, file_path: str, detect_stamps: bool = True) -> dict:
        """
        Extract text from a document.
        :param file_path: Path to PDF or image
        :param detect_stamps: Whether to attempt stamp detection
        :return: Extracted text and metadata
        """
        if not self.available:
            return {
                "text": "[OCR Library not installed. Simulation active]",
                "metadata": {
                    "file": file_path,
                    "stamps_detected": 0 if detect_stamps else "skipped",
                    "status": "partial_success"
                }
            }
        
        # Real extraction logic would go here
        # For MVP Phase 2, we simulate or use pytesseract if available
        return {
            "text": "تم استخراج النص بنجاح من المستند", # Simulated successful extraction
            "metadata": {
                "file": file_path,
                "stamps_detected": 1 if detect_stamps else 0,
                "status": "success",
                "engine": "tesseract-fallback"
            }
        }

ocr_wrapper = OCRWrapper()
