from logger import logger
from vectorstore.faq_ingestor import ingest_pdf_to_chroma

def update_faq_for_bank(pdf_path: str):
    ingest_pdf_to_chroma(pdf_path)
    print("FAQ ingested successfully.")


#  python3 -c "from backend.vectorstore.update_faq import update_faq_for_bank; update_faq_for_bank('/Users/satvik/Desktop/Thrivv/Onboarding agent/backend/vectorstore/faqdocs/SBI_Savings_Account_FAQ.pdf')"
