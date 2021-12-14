from database import db
from typing import Optional
from pydantic import BaseModel, validator


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    middle_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(250))
    county = db.Column(db.String(250))
    state = db.Column(db.String(250))

    def __init__(self, validated_data):
        self.first_name = validated_data.first_name
        self.last_name = validated_data.last_name
        self.email = validated_data.email
        self.zip_code = validated_data.zip_code
        self.middle_name = validated_data.middle_name
        self.user_id = validated_data.user_id


class CustomerValidator(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: str
    zip_code: str
    user_id: Optional[int] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None

    @validator('email')
    def email_must_contain_at_symbol(cls, v):
        if '@' not in v:
            raise ValueError('must contain at (@) symbol')
        return v

    @validator('zip_code')
    def zip_code_length(cls, v):
        if not v.isnumeric() or len(v) != 5:
            raise ValueError('must be numeric and have 5 digits')
        return v

    class Config:
        extra = 'forbid'
