from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    """
    Simple hello for the server's root.
    """
    return {"Hello": "Eurielec"}
