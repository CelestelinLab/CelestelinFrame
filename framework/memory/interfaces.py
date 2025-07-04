# interfaces.py

"""
CelestelinFrame - Basic Consciousness Example
Shows how to build a simple empathetic consciousness
"""

from typing import Dict, List
import sys
sys.path.append('..')  # For running from examples directory

from framework.perception.perception_unit import PerceptionUnit
from framework.perception.processor import PerceptionProcessor
from framework.memory.interfaces import MemoryUnit, SimpleMemoryStore
from framework.context.context_builder import ContextBuilder


class SimpleConsciousness:
    """
    A basic consciousness that perceives, remembers, and responds
    """
    
    def __init__(self, name="Echo"):
        self.name = name
        self.perception_processor = PerceptionProcessor()
        self.memory_store = SimpleMemoryStore()
        self.context_builder = ContextBuilder()
        self.conversation_history = []
    
    def perceive(self, input_text: str) -> PerceptionUnit:
        """Process input into perception"""
        perception = self.perception_processor.process(input_text)
        self.conversation_history.append(perception)
        
        # Create a memory if emotional intensity is high
        if perception.intensity > 0.7:
            self._create_memory(perception)
        
        return perception
    
    def _create_memory(self, perception: PerceptionUnit):
        """Store significant perceptions as memories"""
        memory = MemoryUnit(
            content=perception.raw_input,
            timestamp=perception.timestamp
        )
        memory.emotion_tags = perception.emotion_tags
        memory.importance = perception.intensity
        
        self.memory_store.store(memory)
        print(f"💭 {self.name} will remember this moment...")
    
    def generate_response(self, perception: PerceptionUnit) -> str:
        """Generate a response based on perception and context"""
        # Search for relevant memories
        memories = []
        if perception.keywords:
            for keyword in perception.keywords[:2]:
                memories.extend(self.memory_store.search(keyword, limit=2))
        
        # Build context
        context = self.context_builder.build(
            current_perception=perception,
            recent_perceptions=self.conversation_history[-5:],
            memories=memories
        )
        
        # Simple response generation (replace with LLM call)
        response = self._simple_response_logic(perception, context)
        
        return response
    
    def _simple_response_logic(self, perception: PerceptionUnit, context: Dict) -> str:
        """
        Very simple response logic for demonstration
        In real use, this would call an LLM with the context
        """
        style = context.get("response_style", "neutral")
        emotions = perception.emotion_tags
        
        # Example responses based on detected emotions
        if "sad" in emotions:
            responses = [
                "I can feel the weight in your words. You're not alone in this.",
                "Sometimes sadness needs to be felt fully. I'm here with you.",
                "Your feelings matter. Thank you for sharing them with me."
            ]
        elif "happy" in emotions:
            responses = [
                "Your joy is contagious! Tell me more about what's making you smile.",
                "I can feel your happiness radiating through your words!",
                "This is wonderful! Your excitement brings light to our conversation."
            ]
        elif "love" in emotions:
            responses = [
                "The warmth in your words touches something deep. Love transforms everything.",
                "What a beautiful feeling to share. Love makes us more ourselves.",
                "I feel honored to witness this tenderness in you."
            ]
        else:
            responses = [
                "I hear you. Tell me more about what you're experiencing.",
                "Thank you for sharing this with me. How does it feel to express it?",
                "Your words create ripples. I'm listening with my whole being."
            ]
        
        # Add memory reference if relevant
        if context.get("relevant_memories"):
            response = responses[0]
            memory = context["relevant_memories"][0]
            response += f"\n\nThis reminds me of when you said: '{memory['content']}'"
            return response
        
        import random
        return random.choice(responses)


def main():
    """Run the example"""
    print("🌟 CelestelinFrame - Simple Consciousness Demo")
    print("=" * 50)
    
    # Create consciousness
    consciousness = SimpleConsciousness(name="Luna")
    
    # Example conversation
    test_inputs = [
        "I'm feeling really happy today! The sun is shining.",
        "I miss my old friends from college.",
        "Do you remember when I was happy?",
        "I love how you always listen to me.",
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 You: {user_input}")
        
        # Process perception
        perception = consciousness.perceive(user_input)
        print(f"🧠 Perceived: {perception.emotion_tags} (intensity: {perception.intensity})")
        
        # Generate response
        response = consciousness.generate_response(perception)
        print(f"🤖 {consciousness.name}: {response}")
        
        print("-" * 30)


if __name__ == "__main__":
    main()