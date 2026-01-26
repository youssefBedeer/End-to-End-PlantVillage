from dataclasses import dataclass 
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionSchema:
    root_dir: Path 
    source_url: str
    local_path: str