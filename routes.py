from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile,Query, Form
from sqlalchemy.orm import Session
from typing import List,Annotated
import service, models, schemas
from fastapi import Query
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete('/loan_applications/id/')
async def delete_loan_applications_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_loan_applications_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/users/id/')
async def delete_users_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_users_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/user/login')
async def post_user_login(raw_data: schemas.PostUserLogin, db: Session = Depends(get_db)):
    try:
        return await service.post_user_login(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/users/id/')
async def put_users_id(raw_data: schemas.PutUsersId, headers: Request, db: Session = Depends(get_db)):
    try:
        return await service.put_users_id(db, raw_data, headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/users/')
async def post_users(raw_data: schemas.PostUsers, db: Session = Depends(get_db)):
    try:
        return await service.post_users(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/loan_applications/')
async def post_loan_applications(raw_data: schemas.PostLoanApplications, db: Session = Depends(get_db)):
    try:
        return await service.post_loan_applications(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/records')
async def get_users_records(token: Annotated[str, Query(max_length=500)], headers: Request, db: Session = Depends(get_db)):
    try:
        return await service.get_users_records(db, token, headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/loan_applications/id/')
async def put_loan_applications_id(raw_data: schemas.PutLoanApplicationsId, db: Session = Depends(get_db)):
    try:
        return await service.put_loan_applications_id(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/view/loan/application')
async def get_view_loan_application(user_id: int, token: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.get_view_loan_application(db, user_id, token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

