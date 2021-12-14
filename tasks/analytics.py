from sqlalchemy import inspect

from models.customer import Customer
from models.zipcoderank import Zipcoderank


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def rank_zip_codes(db):
    Zipcoderank.query.delete()
    db.session.commit()
    customers_list = Customer.query.all()
    for customer in customers_list:
        existing_zipcoderank = Zipcoderank.query.filter_by(zip_code=customer.zip_code).first()
        if existing_zipcoderank:
            existing_zipcoderank.mode += 1
            db.session.commit()
        else:
            zipcoderank = Zipcoderank({'zip_code': customer.zip_code, 'county': customer.county, 'mode': 1})
            db.session.add(zipcoderank)
            db.session.commit()

    return [object_as_dict(zipcoderank) for zipcoderank in Zipcoderank.query.order_by(Zipcoderank.mode.desc()).all()]
