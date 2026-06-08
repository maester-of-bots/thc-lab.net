from flask import render_template, request
import phonenumbers
from phonenumbers import geocoder, carrier

from app.phonenumbers import blueprint


@blueprint.route('/phone.html', methods=('GET', 'POST'))
def phone():
    result = None
    error = None

    if request.method == 'POST':
        raw = request.form.get('number', '').strip()
        try:
            number = phonenumbers.parse(raw)
            if phonenumbers.is_valid_number(number):
                result = {
                    'number': raw,
                    'region': geocoder.description_for_number(number, 'en'),
                    'carrier': carrier.name_for_number(number, 'en'),
                    'formatted': phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                }
            else:
                error = "Invalid phone number."
        except phonenumbers.NumberParseException as e:
            error = str(e)

    return render_template('phonenumbers/phone.html', result=result, error=error)
