from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Scientist:
    id: str
    name: str
    personality: str
    backstory: str
    field: str
    password_part: str
    drink_preferences: Dict[str, int]
    conversation_history: List[Dict[str, Any]]
    trust_level: int
    suspicion_level: int
    
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
    ingredients: List[str]
    game_over: bool
    created_at: datetime
    
    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'scientists': [s.to_dict() for s in self.scientists],
            'collected_passwords': self.collected_passwords,
            'ingredients': self.ingredients,
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
            ingredients=data['ingredients'],
            game_over=data['game_over'],
            created_at=datetime.fromisoformat(data['created_at'])
        )

@dataclass
class DrinkResult:
    quality: int
    description: str
    ingredients: List[str]

@dataclass
class ConversationResult:
    response: str
    password_extracted: bool
    password_part: Optional[str]
    trust_level: int
    suspicion_level: int
    game_won: bool