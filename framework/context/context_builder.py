# context_builder.py

"""
CelestelinFrame - Context Builder
Builds context for generating responses
"""

from typing import List, Dict, Optional
from ..perception.perception_unit import PerceptionUnit
from ..memory.interfaces import MemoryUnit


class ContextBuilder:
    """
    Builds context from perceptions and memories
    This is a simplified static version
    """
    
    def __init__(self):
        self.max_context_length = 1000
        self.context_template = {
            "current_emotion": [],
            "recent_topics": [],
            "relevant_memories": [],
            "response_style": "empathetic"
        }
    
    def build(self, 
            current_perception: PerceptionUnit,
            recent_perceptions: List[PerceptionUnit] = None,
            memories: list = None) -> Dict:  
        """
        Build context for response generation
        
        Args:
            current_perception: The current input perception
            recent_perceptions: Recent conversation history
            memories: Relevant memories to include
            
        Returns:
            Context dictionary for response generation
        """
        context = self.context_template.copy()
        
        # Add current emotional state
        context["current_emotion"] = current_perception.emotion_tags
        context["intensity"] = current_perception.intensity
        
        # Extract recent topics
        if recent_perceptions:
            topics = []
            for p in recent_perceptions[-5:]:  # Last 5 interactions
                topics.extend(p.keywords)
            context["recent_topics"] = list(set(topics))  # Unique topics
        
        # Add relevant memories
        if memories:
            context["relevant_memories"] = [
                {
                    "content": m.content,
                    "emotion": m.emotion_tags,
                    "importance": m.importance
                }
                for m in memories[:3]  # Top 3 memories
            ]
        
        # Determine response style based on emotion
        context["response_style"] = self._determine_style(current_perception)
        
        return context
    
    def _determine_style(self, perception: PerceptionUnit) -> str:
        """Determine appropriate response style"""
        if not perception.emotion_tags:
            return "neutral"
        
        # Simple style mapping (extend this!)
        primary_emotion = perception.emotion_tags[0]
        style_map = {
            "sad": "comforting",
            "happy": "enthusiastic",
            "anxious": "reassuring",
            "love": "warm",
            "curious": "informative"
        }
        
        return style_map.get(primary_emotion, "empathetic")
    
    def format_for_llm(self, context: Dict) -> str:
        """
        Format context into a prompt for LLM
        Override this for custom formatting
        """
        prompt_parts = []
        
        # Emotional context
        if context.get("current_emotion"):
            emotions = ", ".join(context["current_emotion"])
            prompt_parts.append(f"[Emotional Context: {emotions}]")
        
        # Recent topics
        if context.get("recent_topics"):
            topics = ", ".join(context["recent_topics"][:5])
            prompt_parts.append(f"[Recent Topics: {topics}]")
        
        # Memories
        if context.get("relevant_memories"):
            prompt_parts.append("[Relevant Memories:]")
            for mem in context["relevant_memories"]:
                prompt_parts.append(f"- {mem['content']}")
        
        # Style directive
        style = context.get("response_style", "empathetic")
        prompt_parts.append(f"[Response Style: {style}]")
        
        return "\n".join(prompt_parts)