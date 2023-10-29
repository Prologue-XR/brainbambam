from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends
from models import Language, UserIdentity
from repository.language.get_languages import get_languages

language_router = APIRouter()

@language_router.get(
    "/language/languages",
    dependencies=[Depends(AuthBearer())],
    tags=["Language"],
)
def get_user_languages_route(
    current_user: UserIdentity = Depends(get_current_user),
) -> list[Language]:
    """
    Get user languages.
    """
    return get_languages(current_user.id)
