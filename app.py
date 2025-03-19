from decimal import Decimal
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from models import Package
from enums import Stacks

app = FastAPI(
    title="Package Sorting API",
    description="API for sorting packages based on their dimensions and mass", 
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return '''
            <html> 
            Hello :wave: <br>

             Start app by running "fastapi dev main.py" on terminal. <br>

             To open the terminal, press ⇧⌘c or click on the little sandwich icon next to Run And Debug -> View -> Terminal <br>
             
             You can use the /docs to try out the sorting function <br>

             Run "python -m pytest test_api.py -v" for tests <br>
             </html>
             '''

def is_bulky(package: Package) -> bool:
    """
    Determine if a package is bulky based on volume or dimensions
    """
    volume = package.width * package.height * package.length
    max_dimension = max(package.width, package.height, package.length)
    return volume > 1_000_000 or max_dimension >= 150

def is_heavy(package: Package) -> bool:
    """
    Determine if a package is heavy based on mass
    """
    return package.mass >= 20


def determine_stack(package: Package) -> str:
    """
    Determine the appropriate stack for a package based on its properties
    """
    bulky = is_bulky(package)
    heavy = is_heavy(package)

    if bulky and heavy:
        return Stacks.REJECTED.value
    elif bulky or heavy:
        return Stacks.SPECIAL.value
    else:
        return Stacks.STANDARD.value

@app.post("/sort", response_class=PlainTextResponse)
async def sort_package(
    package: Package
):
    """
    Sort a package based on its dimensions and mass
    Handles both form submissions and JSON API requests
    """

    if not all((v is not None and v > 0) for v in package.__dict__.values()):
        raise HTTPException(status_code=422, detail=str("Invalid input"))

    result = determine_stack(package)
    return result
    


    