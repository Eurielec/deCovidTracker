from sql import schemas


class Normalizer:

    def __init__(self):
        """
        Create Normalizer instance
        """
        return

    def normalize_event(self, event: schemas.EventCreate):
        """
        Returns a normalized event.

        Arguments:
            event (schemas.EventCreate): not normalized event
        """
        event.email = event.email.lower()
        event.nif_nie = event.nif_nie.upper()
        event.type = event.type.lower()

        return event
