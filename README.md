# Steam Scraper API

A FastAPI-based REST API for scraping game data from Steam.

## Features

- Get detailed game information using Steam App ID
- Search for games using keywords
- Retrieve game prices, descriptions, tags, ratings, and release dates

## Local Development

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the development server:
```bash
python -m uvicorn main:app --reload
```

## Production Deployment on Windows Desktop

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a .env file in the project root directory and add:
```
PORT=8000
HOST=0.0.0.0
```

3. Run with Waitress (Production Server):
```bash
python run_server.py
```

## Making the API Public

### Option 1: Using ngrok (Temporary Solution)
1. Download and install ngrok from: https://ngrok.com/download
2. Extract the ngrok.exe to a convenient location
3. Open command prompt and navigate to ngrok location
4. Start ngrok tunnel:
```bash
ngrok http 8000
```
5. Use the provided ngrok URL to access your API

### Option 2: Using a Domain (Permanent Solution)
1. Get a domain name
2. Set up port forwarding on your router to forward port 80/443 to your desktop's port 8000
3. Configure your domain's DNS to point to your public IP
4. (Recommended) Set up SSL using Let's Encrypt or Cloudflare
5. Make sure Windows Firewall allows incoming connections on port 8000

## Security Considerations

1. In production, update CORS settings in main.py to only allow your specific domains:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourwebsite.com"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

2. Consider adding rate limiting
3. Monitor server logs for abuse
4. Keep dependencies updated
5. Configure Windows Firewall appropriately

## API Endpoints

### GET /
- Welcome message
- Returns: `{"message": "Welcome to Steam Scraper API"}`

### GET /game/{app_id}
- Get detailed information about a specific game
- Parameters:
  - `app_id`: Steam App ID of the game
- Returns: Game details including title, price, description, tags, rating, and release date

### GET /search/{query}
- Search for games on Steam
- Parameters:
  - `query`: Search term
  - `limit`: Maximum number of results (default: 10)
- Returns: List of matching games with basic information

## Example Usage

```javascript
// Example of calling the API from your website
async function getGameDetails(appId) {
    const response = await fetch(`https://your-api-domain.com/game/${appId}`);
    const data = await response.json();
    return data;
}
```

## Troubleshooting Windows Issues

1. If you get permission errors:
   - Run the command prompt as administrator
   - Check Windows Defender settings

2. If the server isn't accessible:
   - Check Windows Firewall settings
   - Verify the port isn't being used by another application
   - Use `netstat -ano` to check port usage

3. If ngrok fails:
   - Make sure no other ngrok instances are running
   - Check if port 8000 is available
   - Run Command Prompt as administrator

## Note
- Please be mindful of Steam's rate limiting and terms of service when using this API
- Consider implementing caching for frequently requested data
- Monitor your system resources when running in production
