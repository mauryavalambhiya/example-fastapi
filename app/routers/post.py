from typing import Optional, List
from sqlalchemy import func
from .. import oauth2
from .. import models, schemas
from fastapi import Depends, FastAPI, Response , status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine,get_db
from .. import models,schemas,utils
import time

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user), limit : int= 10,skip :int = 0,search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM  public.posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(post)
    # result  = db.query(models.Post)
    # print(result)
    # return post

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return {"status" : post}


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post : schemas.PostCreate,db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) values({post.title},{post.content},{post.published}) RETURNING * """)
    # above will work but it will be vernalable to SQL injection
    # cursor.execute("""INSERT INTO posts (title,content,published) values (%s,%s,%s) RETURNING * """,
    # (post.title,post.content,post.published)) 
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post.dict()) unpaking the post and asaing to corasponding filds
    # print(post)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    return new_post

#    if you put request no 1 above request no 2 than it will
#interprit  "/letest" as id perameter and
#it will give an error so order maters a lote

# request no = 2
# @router.get("/posts/letest")
# def get_letest():
#     post = my_posts[len(my_posts)-1]
#     return post

# request no = 1
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int,db : Session = Depends(get_db), current_user  : int = Depends(oauth2.get_current_user)):   # velidation of perameter
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # if somehow you put into some wiard issu the jus put coma after str(id) like this :- cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id),)
    # post = cursor.fetchall()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found")
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id : int,db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # delete post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)),)
    # post = cursor.fetchone()
    # conn.commit()    
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    print("Working......")
    
    # my_posts.pop(post)
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post : schemas.PostCreate,db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title= %s,content = %s, published = %s WHERE id = %s  RETURNING *""", (post.title, post.content, str(post.published) ,str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post  = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()