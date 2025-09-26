from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import class_mapper
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, Float, Text, ForeignKey, JSON, Numeric, Date, \
    TIMESTAMP, UUID, LargeBinary, text, Interval
from sqlalchemy.types import Enum
from sqlalchemy.ext.declarative import declarative_base


@as_declarative()
class Base:
    id: int
    __name__: str

    # Auto-generate table name if not provided
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # Generic to_dict() method
    def to_dict(self):
        """
        Converts the SQLAlchemy model instance to a dictionary, ensuring UUID fields are converted to strings.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            value = getattr(self, column.key)
                # Handle UUID fields
            if isinstance(value, uuid.UUID):
                value = str(value)
            # Handle datetime fields
            elif isinstance(value, datetime):
                value = value.isoformat()  # Convert to ISO 8601 string
            # Handle Decimal fields
            elif isinstance(value, Decimal):
                value = float(value)

            result[column.key] = value
        return result




class LoanApplications(Base):
    __tablename__ = 'loan_applications'
    id = Column(Integer, primary_key=True, autoincrement=True )
    user_id = Column(Integer, primary_key=False )
    loan_amount = Column(String, primary_key=False, autoincrement=True )
    loan_purpose = Column(String, primary_key=False, autoincrement=True )
    term_months = Column(String, primary_key=False, autoincrement=True )
    employment_status = Column(String, primary_key=False, autoincrement=True )
    monthly_income = Column(String, primary_key=False, autoincrement=True )
    address = Column(String, primary_key=False, autoincrement=True )
    city = Column(String, primary_key=False, autoincrement=True )
    state = Column(String, primary_key=False, autoincrement=True )
    postal_code = Column(String, primary_key=False, autoincrement=True )
    country = Column(String, primary_key=False, autoincrement=True )
    status = Column(String, primary_key=False, autoincrement=True )


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True )
    name = Column(String, primary_key=False, autoincrement=True )
    email = Column(String, primary_key=False, autoincrement=True )
    password = Column(String, primary_key=False, autoincrement=True )


