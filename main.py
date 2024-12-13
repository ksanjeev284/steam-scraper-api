from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
from typing import Optional, List, Dict
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Steam Scraper API",
    description="API for scraping Steam game data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your website domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameDetails(BaseModel):
    title: str
    price: Optional[str]
    description: Optional[str]
    tags: List[str]
    rating: Optional[str]
    release_date: Optional[str]

def get_game_details(app_id: str) -> GameDetails:
    url = f"https://store.steampowered.com/app/{app_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('div', class_='apphub_AppName').text.strip() if soup.find('div', class_='apphub_AppName') else "N/A"
        price_element = soup.find('div', class_='game_purchase_price price') or soup.find('div', class_='discount_final_price')
        price = price_element.text.strip() if price_element else "N/A"
        
        description = soup.find('div', class_='game_description_snippet')
        description = description.text.strip() if description else "N/A"
        
        tags = [tag.text.strip() for tag in soup.find_all('a', class_='app_tag')]
        
        rating_element = soup.find('div', class_='game_review_summary')
        rating = rating_element.text.strip() if rating_element else "N/A"
        
        release_date = soup.find('div', class_='release_date')
        release_date = release_date.find('div', class_='date').text.strip() if release_date else "N/A"
        
        return GameDetails(
            title=title,
            price=price,
            description=description,
            tags=tags,
            rating=rating,
            release_date=release_date
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching game details: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to Steam Scraper API"}

@app.get("/game/{app_id}", response_model=GameDetails)
def get_game(app_id: str):
    """
    Get detailed information about a Steam game using its App ID
    """
    return get_game_details(app_id)

@app.get("/search/{query}")
def search_games(query: str, limit: int = 10):
    """
    Search for games on Steam using a query string
    """
    url = f"https://store.steampowered.com/search/suggest"
    params = {
        "term": query,
        "f": "games",
        "cc": "US",
        "lang": "english"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for game in soup.find_all('a', limit=limit):
            game_id = game.get('data-ds-appid', '')
            title = game.find('div', class_='match_name').text.strip() if game.find('div', class_='match_name') else "N/A"
            price_element = game.find('div', class_='match_price')
            price = price_element.text.strip() if price_element else "N/A"
            
            results.append({
                "app_id": game_id,
                "title": title,
                "price": price
            })
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching games: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
