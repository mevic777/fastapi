from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, database, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


# We are using router in order to make code lighter and to structure our code
# -> we use prefix in order to make our decorators less writable
router = APIRouter(prefix='/posts', tags=["Posts"])


# Because of the router object and prefix parameter, we don't have to write
# everytime '/posts'
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    '''
        limit -> query parameter that tells our API how to filter the information
        in the URL it looks like this: http://127.0.0.1:8000/posts?limit=$limit
        if we have more than one query parameter we add the & sign
        http://127.0.0.1:8000/posts?limit=$limit&skip=$skip
        http://127.0.0.1:8000/posts?search=great%20beaches -> %20 in the URL means a space in a string
    '''
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    votes_query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return votes_query


'''
    Depends() -> helps us a lot to create depencies for our route / URLs
    for example:
        1. I need to create a post, but for that i need to have access to the database
            db: Session = Depends(database.get_db) -> helps me to create a session towards my database through the ORM
        2. I need to be logged in:
            user_id: int = Depends(oauth2.get_current_user) -> helps me to create a dependency for user to see if he has a token
            and it is not expired, so only in that case i would be able to create a post
'''


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is not such post {id}")

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed")

    post_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is not such post {id}")

    if update_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed")

    post_query.update(post.dict())
    db.commit()

    return update_post
