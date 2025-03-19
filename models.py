from decimal import Decimal
from pydantic import BaseModel, field_validator

class Package(BaseModel):
    width: Decimal
    height: Decimal
    length: Decimal
    mass: Decimal

    @field_validator('width', 'height', 'length', 'mass')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("All measurements must be positive numbers")
        return v
