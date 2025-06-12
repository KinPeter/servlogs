from fastapi import APIRouter, Depends, Request

from app.utils.auth import auth_user
from app.utils.types import PkBaseModel


router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    dependencies=[Depends(auth_user)],
)


class DockerContainer(PkBaseModel):
    """Model for Docker container information."""

    id: str
    name: str
    status: str


@router.get("/", summary="List all Docker containers")
async def list_containers(request: Request) -> list[DockerContainer]:
    """List all Docker containers."""
    containers = request.app.state.docker.containers.list(all=True)
    return [
        DockerContainer(
            id=container.id,
            name=container.name,
            status=container.status,
        )
        for container in containers
    ]
