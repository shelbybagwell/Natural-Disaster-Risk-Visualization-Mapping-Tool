import re

class AddressHelper:

    def is_valid_street(street):
        return len(street) <= 100

    def is_valid_city(city):
        return re.match(r"^[a-zA-Z\s\-\']{1,50}$", city)

    def is_valid_state(state):
        return re.match(r"^[A-Z]{2}$", state)

    def is_valid_postal_code(postal_code):
        return re.match(r"^\d{5}(-\d{4})?$", postal_code)

    def is_valid_country(country):
        return re.match(r"^[a-zA-Z\s\-\']{2,50}$", country)
