from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from game_engine import GameEngine
from game_models import GameState, Drink
from openai import OpenAI
import os



# Globals
app = FastAPI(title="AI Game API")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
game_engine = GameEngine(openai_client)
active_game: Optional[GameState] = None

class MessageRequest(BaseModel):
    message: str

class ScientistResponse(BaseModel):
    response: str
    isOver: bool
    game_won: bool

class DrinkTasteRequest(BaseModel):
    vol: int = 0
    sweetness: int = 0
    sourness: int = 0
    fruitness: int = 0
    herbalness: int = 0
    sparkling: int = 0
    ice: int = 0
    shaken: int = 0

# Endpoints
@app.post("/game/start")
async def start_game():
    global active_game
    if active_game is not None:
        raise HTTPException(status_code=400, detail="A game is already in progress")
    
    active_game = game_engine.create_game(num_scientists=3)
    return {
        "game_id": active_game.id,
        "scientist_ids": [s.id for s in active_game.scientists]
    }

@app.get("/scientist/{scientist_id}")
async def get_scientist(scientist_id: str):
    if active_game is None:
        raise HTTPException(status_code=400, detail="No active game")
    
    scientist = next((s for s in active_game.scientists if s.id == scientist_id), None)
    if scientist:
        scientist.expected_drink_taste = game_engine.generate_random_drink()
        return scientist.to_dict()
    raise HTTPException(status_code=404, detail="Scientist not found")

@app.post("/scientist/{scientist_id}/serve-drink")
async def serve_drink(scientist_id: str, drink: DrinkTasteRequest):
    print(drink, "test")
    if active_game is None:
        raise HTTPException(status_code=400, detail="No active game")
    
    scientist = next((s for s in active_game.scientists if s.id == scientist_id), None)
    print(scientist, "test")
    if scientist:
        scientist.attempts_left = game_engine.compare_drink_taste(drink.json(), scientist.expected_drink_taste)
        
        # Generate new drink preference
        new_preference = game_engine.generate_drink_preference()
        scientist.expected_drink_taste = Drink(**new_preference['expected_drink_taste'])
        scientist.drink_hint = new_preference['hint']
        
        return {
            "scientist_id": scientist_id,
            "attempts_granted": scientist.attempts_left,
            "message": f"I'm {'very interested' if scientist.attempts_left > 2 else 'interested' if scientist.attempts_left > 0 else 'uninterested'} in your drink..."
        }
    raise HTTPException(status_code=404, detail="Scientist not found")

@app.post("/scientist/{scientist_id}/conversation")
async def get_scientist_response(scientist_id: str, request: MessageRequest):
    if active_game is None:
        raise HTTPException(status_code=400, detail="No active game")
    
    scientist = next((s for s in active_game.scientists if s.id == scientist_id), None)
    if scientist:
        result = game_engine.get_scientist_response(
            game_state=active_game,
            scientist_id=scientist_id,
            user_message=request.message,
        )
        
        return ScientistResponse(
            response=result.response,
            isOver=scientist.attempts_left <= 0,
            game_won=result.game_won
        )
    raise HTTPException(status_code=404, detail="Scientist not found")
