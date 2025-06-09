import random
from typing import List
from game_models import Scientist, Drink

class ScientistGenerator:
    def __init__(self, openai_client):
        self.client = openai_client
        self.personalities = [
            "paranoid and secretive", "friendly but naive", "arrogant and condescending",
            "depressed and lonely", "ambitious and competitive", "anxious and nervous",
            "tough and no-nonsense", "intellectual and philosophical", "cheerful but ditzy",
            "grumpy and cynical", "romantic and dreamy", "perfectionist and detail-oriented"
        ]
        
        self.names = [
            "Dr. Elena Vasquez", "Dr. Marcus Chen", "Dr. Sarah Thompson", "Dr. Viktor Petrov",
            "Dr. Amara Singh", "Dr. James Wilson", "Dr. Luna Rodriguez", "Dr. Alex Kim",
            "Dr. Rachel Green", "Dr. David Brown", "Dr. Maya Patel", "Dr. Lucas Anderson"
        ]
        
        self.fields = [
            "quantum physics", "xenobiology", "astroengineering", "neural networks",
            "dark matter research", "terraforming", "spacecraft propulsion", "cosmic radiation",
            "alien linguistics", "space medicine", "gravitational studies", "AI ethics"
        ]
    
    def generate_backstory(self, name: str, personality: str, field: str) -> str:
        global NO_OPENAI
        if NO_OPENAI:
            return("Dr. Elena Vasquez, once a brilliant but mistrusted\
                    quantum physicist ostracized for her radical theories,\
                    now carries the heavy burden of safeguarding a fragment\
                    of a critical security password aboard the research spaceship.\
                    Haunted by past betrayals and shadowy conspiracies within her own\
                    scientific community, her paranoia fuels her secretive nature,\
                    driving her to protect the mission at all costs. This mission \
                   is her chance to redeem herself and prove that her groundbreaking work can alter the fate of humanity.")
        else:
            """Generate AI backstory for a scientist"""
            prompt = f"""Generate a detailed backstory for a scientist character with these traits:
            Name: {name}
            Personality: {personality}
            Field of study: {field}
            
            The scientist works on a research spaceship and has been entrusted with part of a critical security password.
            Create a compelling backstory (2-3 sentences) that explains their background, motivation, and why they're on this mission.
            Make it engaging and unique. Return only the backstory, no additional text."""
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.8
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error generating backstory: {e}")
                return f"Dr. {name.split()[-1]} is a dedicated {field} researcher with a {personality} disposition."
    
    def generate_scientist(self, scientist_id: str, password_part: str) -> Scientist:
        """Generate a complete scientist character"""
        personality = random.choice(self.personalities)
        name = random.choice(self.names)
        field = random.choice(self.fields)
        self.names.remove(name)
        
        backstory = self.generate_backstory(name, personality, field)
        
        return Scientist(
            id=scientist_id,
            name=name,
            personality=personality,
            backstory=backstory,
            field=field,
            password_part=password_part,
            expected_drink_taste=Drink(),
            conversation_history=[],
            trust_level=random.randint(30, 70),
            suspicion_level=random.randint(0, 20)
        )

class PasswordGenerator:
    def generate_parts(num_parts: int) -> List[str]:
        parts = []
        for _ in range(num_parts):
            part = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
            parts.append(part)
        return parts