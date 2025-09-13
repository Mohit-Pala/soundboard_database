import dataclasses

@dataclasses.dataclass
class AuthModel:
    Id: int
    FirebaseId: str
    Email: str
    Username: str