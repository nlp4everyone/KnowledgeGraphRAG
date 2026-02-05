# Typing
from typing import Any, Callable, Union
from pydantic import BaseModel, Field
# Chonkie Chunking
from chonkie import RecursiveRules
# Local imports
from src.schemas.chunking import ChunkingStrategy

class ChonkieChunkingConfig(BaseModel):
    """Configuration for text chunking using Chonkie's RecursiveChunker.

    Attributes:
        strategy: The chunking strategy to use (character or recursive)
        chunk_size: Maximum size of chunks to create (in tokens)
        min_characters_per_chunk: Minimum number of characters per chunk
        tokenizer: Tokenizer to use (can be 'character' or a callable)
        rules: RecursiveRules configuration for chunking
    """
    strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE
    chunk_size: int = 2560
    chunk_overlap: int = 256
    min_characters_per_chunk: int = 24
    min_sentences_per_chunk: int = 1
    min_characters_per_sentence: int = 12
    tokenizer: Union[str, Callable, Any] = "character"
    rules: RecursiveRules = Field(default_factory=RecursiveRules)
