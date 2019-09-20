from dotenv import load_dotenv
load_dotenv(dotenv_path='config/.env')

from api import app

if __name__ == "__main__":
    app.run()