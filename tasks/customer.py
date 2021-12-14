import requests
from csv import DictReader


def get_county_by_zip_code(zip_code):
    with open('extra/us_postal_codes.csv') as csvfile:
        reader = DictReader(csvfile)

        for row in reader:
            if int(row['Zip Code']) == int(zip_code):
                return row['County']

        return None


def get_city_state_and_county_by_zip_code_from_file(zip_code):
    with open('extra/us_postal_codes.csv') as csvfile:
        reader = DictReader(csvfile)

        for row in reader:
            if int(row['Zip Code']) == int(zip_code):
                return row['Place Name'], row['State'], row['County']

        return None, None, None


def get_city_state_and_county_by_zip_code(zip_code):
    try:
        response = requests.get(url=f"https://www.zipcodeapi.com/rest/DemoOnly000rEHtaqLsbe1YgtXEDp9eTTizuRd2XohTa0uOmTJOZO2KJvrsXy0ZO/info.json/{zip_code}/degrees")
        data = response.json()
        return data['city'], data['state'], get_county_by_zip_code(zip_code)
    except Exception as e:
        return get_city_state_and_county_by_zip_code_from_file(zip_code)


def update_customer_location_data(db, customer, zip_code):
    city, state, county = get_city_state_and_county_by_zip_code(zip_code)
    save_customer(db, customer, city, county, state)
    return city, state, county


def save_customer(db, customer, city, county, state):
    customer.county = county
    customer.city = city
    customer.state = state
    db.session.commit()