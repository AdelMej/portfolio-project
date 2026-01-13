from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def get():
    return JSONResponse(
        status_code=200,
        content={"ayo": "hello world !"}
    )
