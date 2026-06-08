import phonenumbers
from phonenumbers import geocoder, carrier


def phone_number_lookup(phone_number):
    number = phonenumbers.parse(phone_number)

    if phonenumbers.is_valid_number(number):
        region = geocoder.description_for_number(number, "en")
        service_provider = carrier.name_for_number(number, "en")
        return f"Phone Number: {phone_number}\nRegion: {region}\nService Provider: {service_provider}"
    else:
        return "Invalid phone number."


phone_number = "+1234567890"
result = phone_number_lookup(phone_number)
print(result)
