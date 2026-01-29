import logging
import asyncio
from mcp.server.fastmcp import FastMCP
from datetime import datetime
from hijridate import Hijri, Gregorian
from ner_a_mcp.logic.sharia import sharia_engine
from ner_a_mcp.logic.trust import news_trust_engine
from ner_a_mcp.logic.ocr import ocr_wrapper
from ner_a_mcp.logic.dialects import dialect_engine

import sys

# Configure logging to be more descriptive and visible
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("ner-a-mcp")

# Initialize FastMCP server
mcp = FastMCP("NerA-MCP")

@mcp.tool()
async def convert_hijri_date(date_str: str, calendar: str = "Hijri") -> str:
    """
    Convert between Hijri and Gregorian calendars.
    
    :param date_str: Date string in format 'YYYY-MM-DD'
    :param calendar: Source calendar ('Hijri' or 'Gregorian')
    :return: Formatted converted date string
    """
    logger.info(f"Converting date: {date_str} from {calendar}")
    try:
        parts = [int(p) for p in date_str.split("-")]
        if len(parts) != 3:
            logger.error(f"Invalid date format: {date_str}")
            return "Error: Date must be in YYYY-MM-DD format"
        
        y, m, d = parts
        
        if calendar.lower() == "hijri":
            g = Hijri(y, m, d).to_gregorian()
            res = f"Gregorian: {g.year}-{g.month:02d}-{g.day:02d}"
        else:
            h = Gregorian(y, m, d).to_hijri()
            res = f"Hijri: {h.year}-{h.month:02d}-{h.day:02d}"
        
        logger.info(f"Conversion result: {res}")
        return res
    except Exception as e:
        logger.exception(f"Date conversion failed for {date_str}")
        return f"Error: {str(e)}"

@mcp.tool()
async def analyze_arabic_name(name: str) -> dict:
    """
    Analyze an Arabic name to extract root, lineage, and variants.
    
    :param name: Full Arabic name
    :return: Dictionary with name analysis
    """
    logger.info(f"Analyzing name: {name}")
    # Phase 1+ Refined logic
    prefixes = ["بن", "ابن", "بنت", "أب", "أم", "أبو"]
    parts = name.strip().split()
    
    if not parts:
        logger.warning(f"Empty name provided for analysis")
        return {"root_name": "", "lineage": [], "variants": [], "confidence": 0}

    root_name = parts[0]
    lineage = []
    
    i = 1
    while i < len(parts):
        if parts[i] in prefixes and i + 1 < len(parts):
            # Handle compounds like 'bin Abd Allah'
            if parts[i+1] == "عبد" and i + 2 < len(parts):
                lineage.append(f"{parts[i]} {parts[i+1]} {parts[i+2]}")
                i += 3
            else:
                lineage.append(f"{parts[i]} {parts[i+1]}")
                i += 2
        elif parts[i] == "عبد" and i + 1 < len(parts):
            lineage.append(f"{parts[i]} {parts[i+1]}")
            i += 2
        else:
            lineage.append(parts[i])
            i += 1
            
    variants = [name, root_name]
    if lineage:
        variants.append(f"{root_name} {lineage[0]}")
    
    res = {
        "root_name": root_name,
        "lineage": lineage,
        "variants": list(set(variants)),
        "confidence": 0.90
    }
    logger.info(f"Analysis result for {name}: {res}")
    return res

@mcp.tool()
async def normalize_arabic_dialect(text: str, target: str = "MSA") -> dict:
    """
    Normalize Arabic dialect to Modern Standard Arabic (MSA) with confidence scoring.
    
    :param text: Input Arabic text (e.g., Egyptian, Gulf)
    :param target: Target dialect (default: MSA)
    :return: Dictionary containing normalized_text, confidence, and metadata
    """
    logger.info(f"Normalizing text: {text} to {target}")
    res = dialect_engine.normalize(text, target)
    logger.info(f"Normalization result: {res['normalized_text']} (Confidence: {res['confidence']})")
    return res

@mcp.tool()
async def check_sharia_compliance(contract_text: str, school: str = "Hanafi") -> dict:
    """
    Check if a contract text is Sharia-compliant.
    
    :param contract_text: The text of the contract to analyze
    :param school: The Islamic school of jurisprudence (default: Hanafi)
    :return: Compliance status and findings
    """
    logger.info(f"Checking Sharia compliance for text length: {len(contract_text)}")
    res = sharia_engine.check(contract_text, school)
    logger.info(f"Compliance result: {res['status']}")
    return res

@mcp.tool()
async def arabic_news_credibility(article_text: str) -> dict:
    """
    Score the credibility of an Arabic news article.
    
    :param article_text: The text of the news article
    :return: Trust score and indicators
    """
    logger.info(f"Analyzing news credibility for text length: {len(article_text)}")
    res = news_trust_engine.analyze(article_text)
    logger.info(f"Trust score: {res['trust_score']}")
    return res

@mcp.tool()
async def extract_arabic_document(file_path: str, detect_stamps: bool = True) -> dict:
    """
    Extract text and metadata from Arabic document (PDF/Image).
    
    :param file_path: Path to the document file
    :param detect_stamps: Whether to detect stamps/seals (default: True)
    :return: Extracted text and document metadata
    """
    logger.info(f"Extracting document: {file_path}")
    res = ocr_wrapper.extract(file_path, detect_stamps)
    logger.info(f"Extraction result: {res['metadata']['status']}")
    return res

if __name__ == "__main__":
    mcp.run()
