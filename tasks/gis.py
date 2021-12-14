import requests
from sqlalchemy import inspect

from models.zipcoderank import Zipcoderank


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_distance_between_zip_codes(zip_code):
    repeated_zipcode = Zipcoderank.query.order_by(Zipcoderank.mode.desc()).first()

    response = requests.get(
        url=f"https://www.zipcodeapi.com/rest/DemoOnly000rEHtaqLsbe1YgtXEDp9eTTizuRd2XohTa0uOmTJOZO2KJvrsXy0ZO/distance.json/{zip_code}/{repeated_zipcode.zip_code}/km")
    data = response.json()

    return data
