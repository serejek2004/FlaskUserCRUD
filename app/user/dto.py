from dataclasses import dataclass


@dataclass
class UserDTO:
    username: str
    email: str

    @classmethod
    def from_request(cls, data):
        return cls(
            username=data['username'],
            email=data['email'],
        )
