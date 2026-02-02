from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
UNDATASIO_API_KEY = os.getenv('UNDATASIO_API_KEY')
LLAMAPARSE_API_KEY = os.getenv('LLAMAPARSE_API_KEY')