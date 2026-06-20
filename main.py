from dotenv import load_dotenv
import os
from analyze import main_analyze

load_dotenv()

api_key = os.getenv("API_KEY")

if __name__ == "__main__":
    main_analyze(api_key)
