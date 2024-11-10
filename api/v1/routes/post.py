from fastapi import APIRouter, Depends, status, WebSocket, WebSocketDisconnect, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from api.v1.models.user import User
from api.v1.responses.success_response import success_response
from api.v1.schemas.post import CreatePostSchema, UpdatePostSchema, RepostCreate, RepostResponse
from api.v1.utils.dependencies import get_db
from api.v1.utils.websocket import manager
from api.v1.services.user import user_service
from api.v1.services.post import post_service



posts = APIRouter(prefix="/posts", tags=["post"])


@posts.get("", response_model=List[RepostResponse])
async def get_feeds(
        db: Session = Depends(get_db),
        user: User = Depends(user_service.get_current_user),):

    feeds = post_service.get_feeds(db=db, user=user)

    return success_response(
            status_code=status.HTTP_200_OK,
            message="Feeds returned successfully",
            data=feeds)


@posts.post("")
async def create_post(
    post: CreatePostSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):
    new_post = post_service.create(db=db, user=user, schema=post)

    manager.broadcast(new_post)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Post created successfully",
        data=new_post,
    )


@posts.delete(
    "/{id}",
    summary="Delete a post",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    id: str,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):
    post_service.delete(db=db, user=user, post_id=id)

    return success_response(
        status_code=status.HTTP_204_NO_CONTENT, message="Post deleted successfully"
    )


@posts.patch("/{id}", summary="Update a post", status_code=status.HTTP_200_OK)
async def update_post(
    id: str,
    schema: UpdatePostSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):
    updated_post = post_service.update(db=db, user=user, post_id=id, schema=schema)

    manager.broadcast(updated_post)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Post updated successfully",
        data=updated_post,
    )


@posts.websocket("/ws")
async def websocket_post_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.send_text("connected")
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@posts.patch("/{id}/like", status_code=status.HTTP_200_OK)
async def like_post(
    id: str,
    background_task: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    liked_post = post_service.like_post(db=db, user=user, post_id=id, background_task=background_task)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Post liked successfully",
    )

  
@posts.get("/{id}/like", status_code=status.HTTP_200_OK)
async def get_likes(
    id: str,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    likes = post_service.get_likes(db=db, post_id=id, user=user)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="Likes returned successfully",
        data=likes,
    )
  
  
@posts.post("/{id}/repost", status_code=status.HTTP_201_CREATED)
async def repost(
    id: str,
    schema: RepostCreate,
    background_task: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    repost = post_service.repost(db=db, post_id=id, schema=schema, user=user, background_task=background_task)

    manager.broadcast(repost)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Reposted successfully",
        data=repost,
    )
