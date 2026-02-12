from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
UNDATASIO_API_KEY = os.getenv('UNDATASIO_API_KEY')
LLAMAPARSE_API_KEY = os.getenv('LLAMAPARSE_API_KEY')

# Service API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')