import asyncio
from ner_a_mcp.server import (
    convert_hijri_date, 
    analyze_arabic_name, 
    normalize_arabic_dialect,
    check_sharia_compliance,
    arabic_news_credibility,
    extract_arabic_document
)

async def test_tools():
    print("--- Testing hijri_conversion ---")
    h_to_g = await convert_hijri_date("1446-09-01", "Hijri")
    print(f"Hijri 1446-09-01 -> {h_to_g}")
    
    g_to_h = await convert_hijri_date("2025-01-29", "Gregorian")
    print(f"Gregorian 2025-01-29 -> {g_to_h}")
    
    print("\n--- Testing analyze_arabic_name ---")
    name_info = await analyze_arabic_name("محمد بن عبد الله")
    print(f"Analysis: {name_info}")
    
    print("\n--- Testing normalize_arabic_dialect ---")
    dialect_text = "عايز أقدّم على قرض"
    normalized = await normalize_arabic_dialect(dialect_text)
    print(f"Dialect: {dialect_text}")
    print(f"Normalized: {normalized}")

    print("\n--- Testing check_sharia_compliance ---")
    compliance_text = "هذا العقد يتضمن نسبة ربا ثابتة"
    compliance = await check_sharia_compliance(compliance_text)
    print(f"Text: {compliance_text}")
    print(f"Result: {compliance}")

    print("\n--- Testing arabic_news_credibility ---")
    news_text = "عاجل جدا: صدمة كبيرة في الأوساط الرياضية"
    trust = await arabic_news_credibility(news_text)
    print(f"News: {news_text}")
    print(f"Result: {trust}")

    print("\n--- Testing extract_arabic_document ---")
    ocr_res = await extract_arabic_document("sample_iqama.jpg")
    print(f"OCR Result: {ocr_res}")

if __name__ == "__main__":
    asyncio.run(test_tools())
