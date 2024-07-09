import uuid

from fastapi import HTTPException, APIRouter, Request, BackgroundTasks
from starlette import status

import dao
from api_router.schemas_users import RegisterUserRequest, BaseUserInfo
from background_tasks.confirm_registration import confirm_registration

api_router_users = APIRouter(
    prefix='/api/users',
    tags=['API', 'Users']
)


@api_router_users.post('/create/', status_code=status.HTTP_201_CREATED)
def create_user(
        request: Request,
        new_user: RegisterUserRequest,
        background_tasks: BackgroundTasks,
) -> BaseUserInfo:
    maybe_user = dao.get_user_by_email(new_user.email)
    if maybe_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email {new_user.email} already exists'
        )

    created_user = dao.create_user(**new_user.model_dump())
    background_tasks.add_task(confirm_registration, created_user, request.base_url)
    return created_user


@api_router_users.get('/verify/{user_uuid}')
def verify_user_account(user_uuid: uuid.UUID):
    maybe_user = dao.get_user_by_uuid(user_uuid)
    if not maybe_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Wrong data'
        )
    dao.activate_user_account(maybe_user)
    return {'verified': True, 'user_email': maybe_user.email}
