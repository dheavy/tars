# -*- coding: utf-8 -*-
# import logging
from datetime import datetime


class Logger:

    def trace(self, msg):
        print(msg)

    def error(self, url='', msg='', data=None):
        report = '----\n+ ERROR ({0}) +\n'.format(datetime.now())
        report += 'Job URL: ' + url + '\n' + msg
        if data:
            report += str(data)
        print(report)
        # TODO: send email and Slack message
