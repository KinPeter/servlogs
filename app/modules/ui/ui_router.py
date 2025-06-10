from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["ui"],
)


@router.get("/", response_class=HTMLResponse, summary="Return the UI index.html")
async def read_root():
    with open("app/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
