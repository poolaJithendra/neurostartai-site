import os
from dotenv import load_dotenv

load_dotenv()

AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "neurostart-21")

# Hugging Face (text generation/scoring)
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
HF_API_URL_TEXT = "https://api-inference.huggingface.co/models/google/flan-t5-base"

# Pinterest (optional)
PINTEREST_APP_ID = os.getenv("PINTEREST_APP_ID", "")
PINTEREST_APP_SECRET = os.getenv("PINTEREST_APP_SECRET", "")
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")
PINTEREST_BOARD_ID = os.getenv("PINTEREST_BOARD_ID", "")
