# processor.py
"""
CelestelinFrame - Perception Processor
Processes raw input into structured perception units
"""

from typing import List, Callable
from .perception_unit import PerceptionUnit


class PerceptionProcessor:
    """
    Processes raw input through a pipeline of analyzers
    This is a simplified version - extend for your needs
    """
    
    def __init__(self):
        self.analyzers: List[Callable] = []
        self._setup_default_analyzers()
    
    def _setup_default_analyzers(self):
        """Set up basic analyzers"""
        self.add_analyzer(self._basic_emotion_analyzer)
        self.add_analyzer(self._keyword_extractor)
    
    def add_analyzer(self, analyzer_func: Callable):
        """Add a custom analyzer to the pipeline"""
        self.analyzers.append(analyzer_func)
    
    def process(self, text: str) -> PerceptionUnit:
        """Process raw text into a perception unit"""
        unit = PerceptionUnit(raw_input=text)
        
        # Run through all analyzers
        for analyzer in self.analyzers:
            unit = analyzer(unit)
        
        unit.processed = True
        return unit
    
    def _basic_emotion_analyzer(self, unit: PerceptionUnit) -> PerceptionUnit:
        """Simple emotion detection (extend this!)"""
        emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'glad'],
            'sad': ['sad', 'sorry', 'miss', 'lonely'],
            'love': ['love', 'care', 'heart', 'dear'],
            'anxious': ['worried', 'anxious', 'nervous', 'scared']
        }
        
        text_lower = unit.raw_input.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                unit.add_emotion(emotion)
                unit.intensity = min(1.0, unit.intensity + 0.2)
        
        return unit
    
    def _keyword_extractor(self, unit: PerceptionUnit) -> PerceptionUnit:
        """Extract significant words (customize this!)"""
        # Very basic - just get words > 4 chars
        words = unit.raw_input.split()
        unit.keywords = [w.strip('.,!?').lower() 
                        for w in words 
                        if len(w.strip('.,!?')) > 4]
        return unit


# Example emotion tags for extension
EMOTION_CATEGORIES = {
    'primary': ['joy', 'sadness', 'anger', 'fear', 'love', 'surprise'],
    'complex': ['nostalgia', 'longing', 'gratitude', 'empathy', 'curiosity'],
    'states': ['calm', 'excited', 'contemplative', 'playful', 'serious']
}