from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.post("/")
async def test():
    return {"test": "test"}
