# Import for environment variables
import os

import logging


class Config:

    # Get logging config
    log_file = os.environ.get('LOG_FILE', 'covid-tracker.log')
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
