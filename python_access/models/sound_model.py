import dataclasses

@dataclasses.dataclass
class SoundModel:
    Id: int
    UserId: int
    SoundName: str
    Description: str
    SoundPath: str
    Time: int