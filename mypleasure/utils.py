# -*- coding: utf-8 -*-


# import logging


class Logger:

    def trace(self, msg):
        print(msg)

    def error(self, url=None, msg=None, data=None):
        report = '----\nERROR :(\n' + 'Job URL: ' + url + '\n' + msg
        if data:
            report += data
        print(report)
        # TODO: send email and Slack message
