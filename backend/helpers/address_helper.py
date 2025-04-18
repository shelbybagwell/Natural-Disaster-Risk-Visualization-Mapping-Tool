import re

class AddressHelper:

    def is_valid_street(street):
        return len(street) <= 100

    def is_valid_city(city):
        return re.match(r"^[a-zA-Z\s\-\']{1,50}$", city)

    def is_valid_state(state):
        return re.match(r"^[A-Z]{2}$", state)

    def is_valid_zip_code(postal_code):
        return re.match(r"^\d{5}(-\d{4})?$", postal_code)

    def is_valid_country(country):
        return re.match(r"^[a-zA-Z\s\-\']{2,50}$", country)
    
    def is_valid_address_name(username):
        return re.match(r"^[a-zA-Z\d\s\-\&\'\"\.]{1,50}$", username)
    
    def is_valid_lat_long(latitude, longitude):

        """
        Validates latitude and longitude values.

        Args:
            lat (float or str): Latitude to validate (-90 to 90).
            lon (float or str): Longitude to validate (-180 to 180).

        Returns:
            bool: True if both values are valid, False otherwise.
        """
        try:
            lat = float(latitude)
            long = float(longitude)
        except (ValueError, TypeError):
            return False

        return (-90 <= lat <= 90) and (-180 <= long <= 180)
