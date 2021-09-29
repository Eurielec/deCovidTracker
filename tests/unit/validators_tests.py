from src.utilities import validators


def test_dni_validator():
    v = validators.Validator()
    # DNI
    assert v.validate_nif_nie("00000000A") is False
    assert v.validate_nif_nie("89729888B") is True

    # NIE
    assert v.validate_nif_nie("X1470310N") is True
    assert v.validate_nif_nie("X1234567N") is False


def test_email_validator():
    v = validators.Validator()
    assert v.validate_email("something@alumnos.upm.es") is True
    assert v.validate_email("something@upm.es") is True
    assert v.validate_email("something@gsi.upm.es") is True
    assert v.validate_email("something@gmail.com") is False
