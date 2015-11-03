# -*- coding: utf-8 -*-


# import logging


class Logger:

    def trace(self, msg):
        print(msg)

    def error(self, url='', msg='', data=None):
        report = '----\nERROR :(\n' + 'Job URL: ' + url + '\n' + msg
        if data:
            report += str(data)
        print(report)
        # TODO: send email and Slack message
