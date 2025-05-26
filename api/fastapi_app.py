from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import openai
from game_engine import GameEngine
from game_models import GameState
from pydantic import BaseModel


class CreateGameRequest(BaseModel):
    num_scientists: int = 3

class CreateGameResponse(BaseModel):
    game_id: str
    day: int
    scientists: List[Dict[str, Any]]
    ingredients: List[str]
    collected_passwords: int
    total_passwords: int

class MakeDrinkRequest(BaseModel):
    ingredients: List[str]

class TalkToScientistRequest(BaseModel):
    scientist_id: str
    message: str
    drink_quality: int

class GameStatusResponse(BaseModel):
    game_id: str
    day: int
    collected_passwords: int
    total_passwords: int
    game_over: bool
    available_scientists: List[Dict[str, Any]]

def get_game(game_id: str) -> GameState:
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    return games_db[game_id]

games_db: Dict[str, GameState] = {}

app = FastAPI(title="Spaceship Bar Infiltration API", version="1.0.0")

# Initialize game engine
try:
    openai_client = openai.OpenAI()
    game_engine = GameEngine(openai_client)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    print("Please set your OPENAI_API_KEY environment variable")

@app.post("/games", response_model=CreateGameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new game"""
    game_state = game_engine.create_game(request.num_scientists)
    games_db[game_state.id] = game_state
    
    scientists_info = []
    for scientist in game_state.scientists:
        scientists_info.append({
            "id": scientist.id,
            "name": scientist.name,
            "personality": scientist.personality,
            "backstory": scientist.backstory,
            "field": scientist.field,
            "trust_level": scientist.trust_level,
            "suspicion_level": scientist.suspicion_level
        })
    
    return CreateGameResponse(
        game_id=game_state.id,
        day=game_state.day,
        scientists=scientists_info,
        ingredients=game_state.ingredients,
        collected_passwords=len(game_state.collected_passwords),
        total_passwords=len(game_state.scientists)
    )

@app.get("/games/{game_id}/status", response_model=GameStatusResponse)
async def get_game_status(game_id: str):
    """Get current game status"""
    game_state = get_game(game_id)
    available_scientists = game_engine.get_available_scientists(game_state)
    
    scientists_info = []
    for scientist in available_scientists:
        scientists_info.append({
            "id": scientist.id,
            "name": scientist.name,
            "personality": scientist.personality,
            "trust_level": scientist.trust_level,
            "suspicion_level": scientist.suspicion_level
        })
    
    return GameStatusResponse(
        game_id=game_state.id,
        day=game_state.day,
        collected_passwords=len(game_state.collected_passwords),
        total_passwords=len(game_state.scientists),
        game_over=game_state.game_over,
        available_scientists=scientists_info
    )

@app.post("/games/{game_id}/drink")
async def make_drink(game_id: str, request: MakeDrinkRequest):
    """Make a drink"""
    game_state = get_game(game_id)
    result = game_engine.make_drink(request.ingredients)
    
    return {
        "quality": result.quality,
        "description": result.description,
        "ingredients": result.ingredients
    }

@app.post("/games/{game_id}/talk")
async def talk_to_scientist(game_id: str, request: TalkToScientistRequest):
    """Talk to a scientist"""
    game_state = get_game(game_id)
    
    try:
        result = game_engine.get_scientist_response(
            game_state, request.scientist_id, request.message, request.drink_quality
        )
        
        return {
            "response": result.response,
            "password_extracted": result.password_extracted,
            "password_part": result.password_part,
            "trust_level": result.trust_level,
            "suspicion_level": result.suspicion_level,
            "game_won": result.game_won
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/games/{game_id}/advance-day")
async def advance_day(game_id: str):
    """Advance to next day"""
    game_state = get_game(game_id)
    game_engine.advance_day(game_state)
    
    return {"message": f"Advanced to day {game_state.day}"}

@app.delete("/games/{game_id}")
async def delete_game(game_id: str):
    """Delete a game"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    del games_db[game_id]
    return {"message": "Game deleted"}