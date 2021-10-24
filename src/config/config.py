# Import for environment variables
import os

import logging
import json


class Config:

    # Get logging config
    log_file = os.environ.get('LOG_FILE', 'covid-tracker.log')
    config_file = os.environ.get('CONFIG_FILE', 'config.json')
    log_level = os.environ.get('LOG_LEVEL', 'INFO')

    def logging(self):
        '''
        Configure logging.
        '''
        assert self.log_file is not None
        assert self.log_level is not None

        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            format='%(asctime)s %(levelname)s:%(name)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=self.log_level
        )
        return self.log_level

    def get_associations_configs(self):
        with open(self.config_file, "r") as c:
            config = json.load(c)
        return config

    def get_association_config(self, association: str):
        config = self.get_associations_configs()
        try:
            association_config = config[association]
        except Exception:
            return None
        return association_config
