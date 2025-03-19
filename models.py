from pydantic import BaseModel, field_validator

class Package(BaseModel):
    width: float
    height: float
    length: float
    mass: float

    '''@field_validator('width', 'height', 'length', 'mass')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("All measurements must be positive numbers")
        return v'''

class SortResponse(BaseModel):
    stack: str