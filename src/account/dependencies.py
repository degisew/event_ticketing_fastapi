from typing import Annotated
from fastapi import Depends
from src.account.schemas import UserResponseSchema
from src.account.services import UserService


CurrentUser = Annotated[UserResponseSchema,
                         Depends(UserService.get_current_user)]
