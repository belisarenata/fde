#just in case I shouldn't crate an API :)
from decimal import Decimal
from enums import Stacks


def local_sort(width, height, length, mass): 
    try:
        width = Decimal(width)
        height = Decimal(height)
        length = Decimal(length)
        mass = Decimal(mass)
    except: 
        return "Invalid input"
    
    if not all((v is not None and v > 0) 
               for v in [width, height, length, mass]):
        return "Invalid input"

    if any(v > 150 for v in [width, height, length, mass]) \
        or width * height * length > 1000000:
        return Stacks.SPECIAL.value
    elif mass > 20:
        return Stacks.SPECIAL.value
    else:
        return Stacks.STANDARD.value