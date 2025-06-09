import uuid
from datetime import datetime
from game_models import GameState, Drink, ConversationResult
from game_generators import ScientistGenerator, PasswordGenerator, GPT_MODEL
import math
import random
import json

class GameEngine:
    def __init__(self, openai_client):
        self.client = openai_client
        self.scientist_generator = ScientistGenerator(openai_client)
        self.maximum_drink_taste_values = Drink(
            vol=100,
            sweetness=5,
            sourness=5,
            fruitness=5,
            herbalness=5,
            sparkling=1,
            ice=1,
            shaken=1
        )
    
    def create_game(self, num_scientists: int = 3) -> GameState:
        game_id = "0"
        password_parts = PasswordGenerator.generate_parts(num_scientists)
        
        scientists = []
        for i in range(num_scientists):
            scientist_id = str(i)
            scientist = self.scientist_generator.generate_scientist(scientist_id, password_parts[i])
            scientists.append(scientist)
        
        return GameState(
            id=game_id,
            day=1,
            scientists=scientists,
            collected_passwords=[],
            maximum_drink_taste_values=self.maximum_drink_taste_values,
            game_over=False,
        )
    
    def generate_drink_preference(self) -> dict:
        """Generate a new drink preference using the ScientistGenerator"""
        return self.scientist_generator.generate_preference()

    def generate_random_drink(self) -> Drink:
        return Drink(
            vol=random.randint(0, self.maximum_drink_taste_values.vol),
            sweetness=random.randint(0, self.maximum_drink_taste_values.sweetness),
            sourness=random.randint(0, self.maximum_drink_taste_values.sourness),
            fruitness=random.randint(0, self.maximum_drink_taste_values.fruitness),
            herbalness=random.randint(0, self.maximum_drink_taste_values.herbalness),
            sparkling=random.randint(0, self.maximum_drink_taste_values.sparkling),
            ice=random.randint(0, self.maximum_drink_taste_values.ice),
            shaken=random.randint(0, self.maximum_drink_taste_values.shaken)
        )

    def compare_drink_taste(self, served_drink: str, expected_drink: Drink):
        """
        Compare two drinks by computing normalized squared difference in taste parameters.
        """
        # Parse the served drink JSON
        served_drink_dict = json.loads(served_drink)
        served_drink = Drink(**served_drink_dict)
        
        total_diff = 0
        params = ['vol', 'sweetness', 'sourness', 'fruitness', 'herbalness', 'sparkling', 'ice', 'shaken']
        
        for param in params:
            max_value = getattr(self.maximum_drink_taste_values, param)
            served_value = getattr(served_drink, param)
            expected_value = getattr(expected_drink, param)
            
            # Normalize values
            norm_served = served_value / max_value
            norm_expected = expected_value / max_value
            
            # Add squared difference
            total_diff += (norm_served - norm_expected) ** 2
        
        # Average the difference
        average_diff = total_diff / len(params)
        
        # Calculate attempts amount (Maximum 4 attempts)
        return math.ceil(average_diff * 4)
    
    def get_scientist_response(self, game_state: GameState, scientist_id: str, user_message: str) -> ConversationResult:
        scientist = next((s for s in game_state.scientists if s.id == scientist_id), None)
        if not scientist:
            raise ValueError(f"Scientist {scientist_id} not found")
        
        # Get response from GPT
        ai_response = self.scientist_generator.generate_response(scientist, user_message, game_state)
        
        # Update scientist's memory
        scientist.conversation_history.append({
            "user": user_message,
            "assistant": ai_response,
            "day": game_state.day,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update suspicion level if security-related words are used
        if any(word in user_message.lower() for word in ["password", "code", "key", "security", "access", "control"]):
            scientist.suspicion_level = min(100, scientist.suspicion_level + 15)
        
        # Check if password was extracted
        password_extracted = scientist.password_part.lower() in ai_response.lower()
        password_part = None
        
        if password_extracted and scientist.password_part not in game_state.collected_passwords:
            game_state.collected_passwords.append(scientist.password_part)
            password_part = scientist.password_part
        
        # Check win condition
        game_won = len(game_state.collected_passwords) == len(game_state.scientists)
        if game_won:
            game_state.game_over = True
        
        return ConversationResult(
            response=ai_response,
            password_extracted=password_extracted,
            password_part=password_part,
            trust_level=scientist.trust_level,
            suspicion_level=scientist.suspicion_level,
            game_won=game_won
        )
    