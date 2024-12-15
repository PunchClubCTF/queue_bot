from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from app import create_app
from app.telegram_bot import run_bot
import threading
import signal
import sys

app = create_app()

def signal_handler(sig, frame):
    print('Stopping application...')
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    try:
        app.run(host='0.0.0.0', debug=False, use_reloader=False)
    except Exception as e:
        print(f"Flask app error: {e}")
        sys.exit(1)
    finally:
        # Ensure bot thread is stopped if it's still running
        if bot_thread.is_alive():
            bot_thread.join(timeout=5)