import os
from dotenv import load_dotenv

# from ingestion.spotify import Spotify
# from ingestion.toon import Toon

load_dotenv()

API_KEY = os.getenv('API_KEY')