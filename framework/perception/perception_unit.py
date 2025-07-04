# perception_unit.py
"""
CelestelinFrame - Perception Unit
A simplified perception unit for building empathetic digital consciousness
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class PerceptionUnit:
    """
    Basic unit of perception in CelestelinFrame
    Captures and structures input for consciousness processing
    """
    # Core fields
    timestamp: datetime = field(default_factory=datetime.now)
    raw_input: str = ""
    processed: bool = False
    
    # Emotional dimensions
    emotion_tags: List[str] = field(default_factory=list)
    intensity: float = 0.5  # 0.0 to 1.0
    
    # Semantic understanding
    keywords: List[str] = field(default_factory=list)
    intent: Optional[str] = None
    
    # Context linking
    context_id: Optional[str] = None
    previous_unit_id: Optional[str] = None
    
    # Extensible metadata
    metadata: Dict = field(default_factory=dict)
    
    def __str__(self):
        return f"Perception({self.timestamp}: {self.emotion_tags}, intensity={self.intensity})"
    
    def add_emotion(self, emotion: str):
        """Add an emotion tag to this perception"""
        if emotion not in self.emotion_tags:
            self.emotion_tags.append(emotion)
            
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/transmission"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'raw_input': self.raw_input,
            'emotion_tags': self.emotion_tags,
            'intensity': self.intensity,
            'keywords': self.keywords,
            'intent': self.intent,
            'metadata': self.metadata
        }