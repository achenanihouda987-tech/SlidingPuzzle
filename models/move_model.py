from dataclasses import dataclass

@dataclass
class MoveModel:
    tile_id: int
    from_idx: int
    to_idx: int
