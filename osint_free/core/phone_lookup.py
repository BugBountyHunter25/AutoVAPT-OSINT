import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def lookup_phone_info(phone):
    try:
        parsed = phonenumbers.parse(phone)
        info = {
            "valid": phonenumbers.is_valid_number(parsed),
            "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "country": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),
            "timezone": timezone.time_zones_for_number(parsed)
        }
        return info
    except Exception as e:
        return {"error": str(e)}
