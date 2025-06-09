from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Drink:
    def __init__(self, taste: dict | None = None):
        default_taste = {
            "vol": 0,
            "sweetness": 0,
            "sourness": 0,
            "fruitness": 0,
            "herbalness": 0,
            "sparkling": 0,
            "ice": 0,
            "shaken": 0
        }
        self.taste: dict = taste if taste is not None else default_taste.copy()

@dataclass
class Scientist:
    id: str
    name: str
    personality: str
    backstory: str
    field: str
    password_part: str
    expected_drink_taste: Drink
    conversation_history: List[Dict[str, Any]]
    trust_level: int
    suspicion_level: int
    attempts_left: int = 0  # Default to 0 attempts
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

@dataclass
class GameState:
    id: str
    day: int
    scientists: List[Scientist]
    collected_passwords: List[str]
    maximum_drink_taste_values: List[str]
    game_over: bool
    
    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'scientists': [s.to_dict() for s in self.scientists],
            'collected_passwords': self.collected_passwords,
            'maximum_drink_taste_values': self.maximum_drink_taste_values,
            'game_over': self.game_over,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        scientists = [Scientist.from_dict(s) for s in data['scientists']]
        return cls(
            id=data['id'],
            day=data['day'],
            scientists=scientists,
            collected_passwords=data['collected_passwords'],
            maximum_drink_taste_values=data['maximum_drink_taste_values'],
            game_over=data['game_over'],
            created_at=datetime.fromisoformat(data['created_at'])
        )

@dataclass
class ConversationResult:
    response: str
    password_extracted: bool
    password_part: Optional[str]
    trust_level: int
    suspicion_level: int
    game_won: bool