from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class MyException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(MyException)
async def my_exception_handler(request: Request, exc: MyException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc.name} cannot be found!!!!" })

@app.get("/")
def read_name():
    return "Hiiiiiiiiiiiiiiiiiiiiii"

@app.get("/{name}")
def read_name(name: str):
    if name == "something":
        raise MyException(name=name)
    return {"name": name}