import random
from game_engine import GameEngine
from game_models import GameState
import openai
from dotenv import load_dotenv
import os

load_dotenv()

class TerminalInterface:
    def __init__(self):
        try:
            if not os.getenv('OPENAI_API_KEY'):
                raise ValueError("OPENAI_API_KEY not found in environment variables")
                
            self.client = openai.OpenAI()
            self.engine = GameEngine(self.client)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            print("Please set your OPENAI_API_KEY environment variable")
            exit(1)
    
    def display_intro(self):
        print("🚀 SPACESHIP BAR INFILTRATION GAME 🚀")
        print("=" * 50)
        print("You are an undercover agent working as a bartender on a research vessel.")
        print("Your mission: Extract password fragments from the scientists to take control of the ship.")
        print("Use your bartending skills and social engineering to gain their trust...")
        print()
    
    def display_scientists(self, game_state: GameState):
        print("SCIENTISTS ABOARD:")
        for i, scientist in enumerate(game_state.scientists, 1):
            print(f"{i}. {scientist.name}")
            print(f"   Personality: {scientist.personality}")
            print(f"   Background: {scientist.backstory}")
            print()
    
    def display_status(self, game_state: GameState):
        print(f"\n--- STATUS ---")
        print(f"Day: {game_state.day}")
        print(f"Password parts collected: {len(game_state.collected_passwords)}/{len(game_state.scientists)}")
        if game_state.collected_passwords:
            print(f"Collected parts: {', '.join(game_state.collected_passwords)}")
    
    def get_drink_ingredients(self, game_state: GameState) -> list:
        print(f"\nAvailable ingredients: {', '.join(game_state.ingredients)}")
        print("Enter ingredients separated by commas (e.g., vodka, lime, cola):")
        
        ingredient_input = input("Ingredients: ").strip()
        if ingredient_input.lower() in ['quit', 'exit']:
            return None
        
        return [ing.strip() for ing in ingredient_input.split(',') if ing.strip()]
    
    def interact_with_scientist(self, game_state: GameState, scientist, drink_quality: int):
        print(f"\n--- Conversation with {scientist.name} ---")
        print(f"Trust Level: {scientist.trust_level}/100 | Suspicion: {scientist.suspicion_level}/100")
        print(f"You have {drink_quality} attempts based on the drink quality.")
        print()
        
        attempts_used = 0
        
        while attempts_used < drink_quality and not game_state.game_over:
            print(f"\nAttempt {attempts_used + 1}/{drink_quality}")
            user_input = input("You say: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                return False
            
            attempts_used += 1
            
            # Get AI response
            result = self.engine.get_scientist_response(
                game_state, scientist.id, user_input, drink_quality - attempts_used
            )
            
            print(f"{scientist.name}: {result.response}")
            
            if result.password_extracted:
                print(f"\n🎉 SUCCESS! You extracted the password part: {result.password_part}")
                break
            
            if result.game_won:
                break
        
        print(f"\nConversation with {scientist.name} ended.")
        return True
    
    def play_day(self, game_state: GameState):
        print(f"\n{'='*20} DAY {game_state.day} {'='*20}")
        print("The evening shift begins. Scientists start arriving at your bar...")
        
        available_scientists = self.engine.get_available_scientists(game_state)
        random.shuffle(available_scientists)
        
        for scientist in available_scientists:
            if game_state.game_over:
                break
            
            print(f"\n{scientist.name} approaches the bar.")
            print(f'"{scientist.name}": "Good evening! Could I get a drink?"')
            
            # Drink making phase
            ingredients = self.get_drink_ingredients(game_state)
            if ingredients is None:
                return False
            
            drink_result = self.engine.make_drink(ingredients)
            print(f"\n{drink_result.description}")
            print(f"Drink quality: {drink_result.quality}/5")
            
            if not self.interact_with_scientist(game_state, scientist, drink_result.quality):
                return False
        
        self.engine.advance_day(game_state)
        return True
    
    def play(self):
        self.display_intro()
        
        game_state = self.engine.create_game()
        self.display_scientists(game_state)
        
        while not game_state.game_over:
            self.display_status(game_state)
            
            if len(game_state.collected_passwords) == len(game_state.scientists):
                complete_password = ''.join(game_state.collected_passwords)
                print(f"\n🎉 CONGRATULATIONS! 🎉")
                print(f"You successfully infiltrated the ship in {game_state.day - 1} days!")
                print(f"Complete access code: {complete_password}")
                print("The ship is now under your control!")
                break
            
            input("\nPress Enter to continue to the next day...")
            if not self.play_day(game_state):
                break
        
        print("\nGame Over!")