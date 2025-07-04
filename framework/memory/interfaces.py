# interfaces.py

"""
CelestelinFrame - Memory Interfaces
Define how memories are structured and accessed
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class MemoryUnit:
    """Basic memory unit structure"""
    
    def __init__(self, content: str, timestamp: datetime = None):
        self.id = self._generate_id()
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.emotion_tags: List[str] = []
        self.associations: List[str] = []  # IDs of related memories
        self.importance: float = 0.5
        self.access_count: int = 0
        self.metadata: Dict[str, Any] = {}
    
    def _generate_id(self) -> str:
        """Generate unique memory ID"""
        import uuid
        return f"mem_{uuid.uuid4().hex[:8]}"
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'emotion_tags': self.emotion_tags,
            'importance': self.importance,
            'access_count': self.access_count,
            'metadata': self.metadata
        }


class MemoryStore(ABC):
    """
    Abstract base class for memory storage
    Implement this to create your own memory system
    """
    
    @abstractmethod
    def store(self, memory: MemoryUnit) -> str:
        """Store a memory and return its ID"""
        pass
    
    @abstractmethod
    def retrieve(self, memory_id: str) -> Optional[MemoryUnit]:
        """Retrieve a specific memory by ID"""
        pass
    
    @abstractmethod
    def search(self, query: str, limit: int = 5) -> List[MemoryUnit]:
        """Search memories by content or metadata"""
        pass
    
    @abstractmethod
    def get_related(self, memory_id: str, limit: int = 3) -> List[MemoryUnit]:
        """Get memories related to a specific memory"""
        pass


class SimpleMemoryStore(MemoryStore):
    """
    A very basic in-memory store for demonstration
    Replace with your own persistent storage!
    """
    
    def __init__(self):
        self.memories: Dict[str, MemoryUnit] = {}
    
    def store(self, memory: MemoryUnit) -> str:
        self.memories[memory.id] = memory
        return memory.id
    
    def retrieve(self, memory_id: str) -> Optional[MemoryUnit]:
        memory = self.memories.get(memory_id)
        if memory:
            memory.access_count += 1
        return memory
    
    def search(self, query: str, limit: int = 5) -> List[MemoryUnit]:
        """Simple keyword search"""
        query_lower = query.lower()
        results = []
        
        for memory in self.memories.values():
            if query_lower in memory.content.lower():
                results.append(memory)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_related(self, memory_id: str, limit: int = 3) -> List[MemoryUnit]:
        """Get associated memories"""
        memory = self.retrieve(memory_id)
        if not memory:
            return []
        
        related = []
        for assoc_id in memory.associations[:limit]:
            if assoc_mem := self.retrieve(assoc_id):
                related.append(assoc_mem)
        
        return related
