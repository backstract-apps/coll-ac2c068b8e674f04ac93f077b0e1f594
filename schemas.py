from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class LoanApplications(BaseModel):
    user_id: Optional[int]=None
    loan_amount: Optional[str]=None
    loan_purpose: Optional[str]=None
    term_months: Optional[str]=None
    employment_status: Optional[str]=None
    monthly_income: Optional[str]=None
    address: Optional[str]=None
    city: Optional[str]=None
    state: Optional[str]=None
    postal_code: Optional[str]=None
    country: Optional[str]=None
    status: Optional[str]=None


class ReadLoanApplications(BaseModel):
    user_id: Optional[int]=None
    loan_amount: Optional[str]=None
    loan_purpose: Optional[str]=None
    term_months: Optional[str]=None
    employment_status: Optional[str]=None
    monthly_income: Optional[str]=None
    address: Optional[str]=None
    city: Optional[str]=None
    state: Optional[str]=None
    postal_code: Optional[str]=None
    country: Optional[str]=None
    status: Optional[str]=None
    class Config:
        from_attributes = True


class Users(BaseModel):
    name: Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None


class ReadUsers(BaseModel):
    name: Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None
    class Config:
        from_attributes = True




class PostUserLogin(BaseModel):
    email: str = Field(..., max_length=100)

    @field_validator('email')
    def validate_email(cls, value: Optional[str]):
        if value is None:
            if False:
                return value
            else:
                raise ValueError("Field 'email' cannot be None")
        # Ensure re is imported in the generated file
        pattern = r'''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'''
        if isinstance(value, str) and not re.match(pattern, value):
            # Use repr() for the regex pattern in the error for clarity
            raise ValueError(f"Field 'email' does not match regex pattern")
        return value
    password: str = Field(..., max_length=100)

    @field_validator('password')
    def validate_password(cls, value: Optional[str]):
        if value is None:
            if False:
                return value
            else:
                raise ValueError("Field 'password' cannot be None")
        # Ensure re is imported in the generated file
        pattern = r'''^[a-zA-Z0-9!@#$%^&*()_+={\}\[\]|;:'",.<>/?~\\-]{8,64}$'''
        if isinstance(value, str) and not re.match(pattern, value):
            # Use repr() for the regex pattern in the error for clarity
            raise ValueError(f"Field 'password' does not match regex pattern")
        return value

    class Config:
        from_attributes = True



class PutUsersId(BaseModel):
    id: Optional[int]=None
    name: Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    name: Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None

    class Config:
        from_attributes = True



class PostLoanApplications(BaseModel):
    user_id: Optional[int]=None
    loan_amount: Optional[str]=None
    loan_purpose: Optional[str]=None
    term_months: Optional[str]=None
    employment_status: Optional[str]=None
    monthly_income: Optional[str]=None
    address: Optional[str]=None
    city: Optional[str]=None
    state: Optional[str]=None
    postal_code: Optional[str]=None
    country: Optional[str]=None
    status: Optional[str]=None
    token: str = Field(..., max_length=500)

    class Config:
        from_attributes = True



class PutLoanApplicationsId(BaseModel):
    id: Optional[int]=None
    user_id: Optional[int]=None
    loan_amount: Optional[str]=None
    loan_purpose: Optional[str]=None
    term_months: Optional[str]=None
    employment_status: Optional[str]=None
    monthly_income: Optional[str]=None
    address: Optional[str]=None
    city: Optional[str]=None
    state: Optional[str]=None
    postal_code: Optional[str]=None
    country: Optional[str]=None
    status: Optional[str]=None
    token: str = Field(..., max_length=500)

    class Config:
        from_attributes = True

