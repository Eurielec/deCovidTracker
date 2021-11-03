"""
Module to define jobs to be executed as tasks on schedule.
"""
from datetime import datetime, timedelta

from config import config
from utilities import mail, helpers
from sql.crud import get_events_by_day, create_event


class Job:

    def __init__(self):
        """
        Create an instance of class Job.
        """
        c = config.Config()
        self.associations_configs = c.get_associations_configs()
        self.e = mail.Email()

        return

    def mail(self, db):
        """
        Send mail with association's events. Should run every month.
        """
        print("Running monthly mail")
        for association, a_config in self.associations_configs.items():
            data = get_events_by_day(
                db,
                association,
                limit=0,
                _from=datetime.today().date() - timedelta(days=31),
                _to=datetime.today().date() + timedelta(days=1))
            csv = helpers.json_to_csv(data)
            self.e.send_email(a_config['to_email'], association, csv)

    def close_association_events(self, db, association):
        data = get_events_by_day(
            db,
            association,
            limit=0,
            _from=datetime.today().date() - timedelta(days=31),
            _to=datetime.today().date() + timedelta(days=1))
        events_by_email = {}
        for event in data:
            try:
                previous = events_by_email[event.email]
            except Exception:
                previous = []
            previous.append(event)
            previous.sort(key=lambda x: x.time)
            events_by_email[event.email] = previous
        print(events_by_email)
        for email, events in events_by_email.items():
            if events[-1].type == "access":
                new_event = {
                    "type": "exit",
                    "time": datetime.now(),
                    "email": email,
                    "nif_nie": events[-1].nif_nie,
                    "association": association
                }
                create_event(db, new_event)

    def close_open_events(self, db):
        """
        Close open events. Should be called at the end of the day.
        """
        for association, a_config in self.associations_configs.items():
            self.close_association_events(db, association)
