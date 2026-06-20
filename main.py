import os

from dotenv import load_dotenv

from analyze import main_analyze

load_dotenv()

api_key = os.getenv("API_KEY")

if __name__ == "__main__":
    main_analyze(api_key)
