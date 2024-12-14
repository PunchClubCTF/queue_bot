from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from app import create_app
from app.telegram_bot import run_bot
import threading

app = create_app()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    app.run(host='0.0.0.0', debug=True)