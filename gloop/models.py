from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class SimilarityData:
    size: int
    file1: str
    file2: str
    result: Optional[Any] = None


@dataclass
class BestLoopInfo:
    start_file: str
    end_file: str
    start_index: int
    end_index: int
    score: float
