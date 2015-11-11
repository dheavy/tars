# -*- coding: utf-8 -*-
# import logging
from datetime import datetime


class Logger:

    def __init__(self, verbosity=1, reporting=1):
        '''
        Logger util for relevant data and errors.

        Args:
            verbosity: 0 silences logger in console, 1 prints output.
            reporting: 0 silences reporting, 1 logs into logfile,
                2 sends Slack message only,
                3 sends email only,
                4 sends both Slack and email messages.
                Both 2, 3 and 4 also print to logfile.
        '''
        self.verbosity = verbosity
        self.reporting = reporting

    def trace(self, msg):
        if self.verbosity > 0:
            print(msg)

    def error(self, url='', msg='', data=None):
        report = '----\n+ ERROR ({0}) +\n'.format(datetime.now())
        report += 'Job URL: ' + url + '\n' + msg
        if data:
            report += str(data)
        if self.verbosity > 0:
            print(report)
        # TODO: send email and Slack message
