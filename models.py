from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Request:
    prompt: str
    workspace: Path
    allow_run: bool = False

@dataclass
class Plan:
    summary: str
    architecture: str
    uiux: str
    files: list[dict]
    verification: list[str]

@dataclass
class Result:
    files: list[str] = field(default_factory=list)
    review_status: str = "unknown"
    repaired: bool = False
