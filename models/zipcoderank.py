from database import db


class Zipcoderank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(5), nullable=False, unique=True)
    county = db.Column(db.String(250))
    mode = db.Column(db.Integer, nullable=False)

    def __init__(self, validated_data):
        self.zip_code = validated_data['zip_code']
        self.county = validated_data['county']
        self.mode = validated_data['mode']
