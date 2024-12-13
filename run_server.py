from waitress import serve
from main import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting server on http://{host}:{port}")
    serve(app, host=host, port=port, threads=4)
