"""
Module to schedule and run jobs via tasks.
"""

import schedule
import time
from multiprocessing import Process

from config import config
from utilities import jobs


class Task:

    def __init__(self):
        c = config.Config()
        self.associations_configs = c.get_associations_configs()

        self.j = jobs.Job()
        self.setup()

    def setup(self):
        """
        Configure jobs to run.
        """
        # schedule.every().day.at("23:55").do(self.j.close_open_events)
        # schedule.every(4).monday.at("9:00").do(self.j.mail)
        schedule.every(30).seconds.do(self.j.close_open_events)
        schedule.every(45).seconds.do(self.j.mail)

    def run_pending(self):
        """
        Worker for another thread to run background tasks.
        """
        while True:
            schedule.run_pending()
            print("Running")
            time.sleep(1)

    def start(self):
        """
        Start tasks manager in background.
        """
        t = Process(target=self.run_pending)
        t.start()
