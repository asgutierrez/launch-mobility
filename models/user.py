from database import db
from pydantic import BaseModel, validator


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, validated_data):
        self.email = validated_data.email
        self.password = validated_data.password


class UserValidator(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_must_contain_at_symbol(cls, v):
        if '@' not in v:
            raise ValueError('must contain at (@) symbol')
        return v

    class Config:
        extra = 'forbid'
