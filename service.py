from sqlalchemy.orm import Session, aliased
from database import SessionLocal
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
import math
import random
import asyncio
from pathlib import Path


async def delete_loan_applications_id(db: Session, id: int):

    query = db.query(models.LoanApplications)
    query = query.filter(and_(models.LoanApplications.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        loan_applications_deleted = record_to_delete.to_dict()
    else:
        loan_applications_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"loan_applications_deleted": loan_applications_deleted},
    }
    return res


async def delete_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_deleted": users_deleted},
    }
    return res


async def post_user_login(db: Session, raw_data: schemas.PostUserLogin):
    email: str = raw_data.email
    password: str = raw_data.password

    query = db.query(models.Users)
    query = query.filter(
        and_(models.Users.email == email, models.Users.password == password)
    )

    login_record = query.first()

    login_record = (
        (
            login_record.to_dict()
            if hasattr(login_record, "to_dict")
            else vars(login_record)
        )
        if login_record
        else login_record
    )

    secret_key = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"""
    bs_jwt_payload = {
        "exp": int(
            (
                datetime.datetime.utcnow() + datetime.timedelta(seconds=100000)
            ).timestamp()
        ),
        "data": login_record,
    }

    jwt_secret_keys = jwt.encode(bs_jwt_payload, secret_key, algorithm="HS256")

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"login_record": login_record, "jwt_secret_keys": jwt_secret_keys},
    }
    return res


async def put_users_id(db: Session, raw_data: schemas.PutUsersId, request: Request):
    id: int = raw_data.id
    name: str = raw_data.name
    email: str = raw_data.email
    password: str = raw_data.password

    header_authorization: str = request.headers.get("header-authorization")

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "name": name,
            "email": email,
            "password": password,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )

    try:
        decode_jwt = jwt.decode(
            header_authorization,
            "BYFmQ3KGaRz_lJ5VW1C-yn8ZLPW6tCuRLWKxIC_z8U8=",
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"decode_jwt": decode_jwt, "users_edited_record": users_edited_record},
    }
    return res


async def post_users(db: Session, raw_data: schemas.PostUsers):
    name: str = raw_data.name
    email: str = raw_data.email
    password: str = raw_data.password

    record_to_be_added = {"name": name, "email": email, "password": password}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    secret_key = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"""
    bs_jwt_payload = {
        "exp": int(
            (
                datetime.datetime.utcnow() + datetime.timedelta(seconds=100000)
            ).timestamp()
        ),
        "data": users_inserted_record,
    }

    jwt_secret_keys = jwt.encode(bs_jwt_payload, secret_key, algorithm="HS256")

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {
            "jwt_secret_keys": jwt_secret_keys,
            "users_inserted_record": users_inserted_record,
        },
    }
    return res


async def post_loan_applications(db: Session, raw_data: schemas.PostLoanApplications):
    user_id: int = raw_data.user_id
    loan_amount: str = raw_data.loan_amount
    loan_purpose: str = raw_data.loan_purpose
    term_months: str = raw_data.term_months
    employment_status: str = raw_data.employment_status
    monthly_income: str = raw_data.monthly_income
    address: str = raw_data.address
    city: str = raw_data.city
    state: str = raw_data.state
    postal_code: str = raw_data.postal_code
    country: str = raw_data.country
    status: str = raw_data.status
    token: str = raw_data.token

    record_to_be_added = {
        "city": city,
        "state": state,
        "status": status,
        "address": address,
        "country": country,
        "user_id": user_id,
        "loan_amount": loan_amount,
        "postal_code": postal_code,
        "term_months": term_months,
        "loan_purpose": loan_purpose,
        "monthly_income": monthly_income,
        "employment_status": employment_status,
    }
    new_loan_applications = models.LoanApplications(**record_to_be_added)
    db.add(new_loan_applications)
    db.commit()
    db.refresh(new_loan_applications)
    loan_applications_inserted_record = new_loan_applications.to_dict()

    try:
        decode_jwt = jwt.decode(
            token,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {
            "decode_jwt": decode_jwt,
            "loan_applications_inserted_record": loan_applications_inserted_record,
        },
    }
    return res


async def get_users_records(db: Session, token: str, request: Request):
    header_authorization: str = request.headers.get("header-authorization")

    query = db.query(models.Users)

    allreccords = query.all()
    allreccords = (
        [new_data.to_dict() for new_data in allreccords] if allreccords else allreccords
    )

    try:
        decode_jwt = jwt.decode(
            token,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"decode_jwt": decode_jwt, "allreccords": allreccords},
    }
    return res


async def put_loan_applications_id(
    db: Session, raw_data: schemas.PutLoanApplicationsId
):
    id: int = raw_data.id
    user_id: int = raw_data.user_id
    loan_amount: str = raw_data.loan_amount
    loan_purpose: str = raw_data.loan_purpose
    term_months: str = raw_data.term_months
    employment_status: str = raw_data.employment_status
    monthly_income: str = raw_data.monthly_income
    address: str = raw_data.address
    city: str = raw_data.city
    state: str = raw_data.state
    postal_code: str = raw_data.postal_code
    country: str = raw_data.country
    status: str = raw_data.status
    token: str = raw_data.token

    query = db.query(models.LoanApplications)
    query = query.filter(and_(models.LoanApplications.id == id))
    loan_applications_edited_record = query.first()

    if loan_applications_edited_record:
        for key, value in {
            "id": id,
            "city": city,
            "state": state,
            "status": status,
            "address": address,
            "country": country,
            "user_id": user_id,
            "loan_amount": loan_amount,
            "postal_code": postal_code,
            "term_months": term_months,
            "loan_purpose": loan_purpose,
            "monthly_income": monthly_income,
            "employment_status": employment_status,
        }.items():
            setattr(loan_applications_edited_record, key, value)

        db.commit()
        db.refresh(loan_applications_edited_record)

        loan_applications_edited_record = (
            loan_applications_edited_record.to_dict()
            if hasattr(loan_applications_edited_record, "to_dict")
            else vars(loan_applications_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"loan_applications_edited_record": loan_applications_edited_record},
    }
    return res


async def get_view_loan_application(db: Session, user_id: int, token: str):

    query = db.query(models.LoanApplications)
    query = query.filter(and_(models.LoanApplications.user_id == user_id))

    get_loan_appications = query.all()
    get_loan_appications = (
        [new_data.to_dict() for new_data in get_loan_appications]
        if get_loan_appications
        else get_loan_appications
    )

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"token": token, "get_loan_applications": get_loan_appications},
    }
    return res
