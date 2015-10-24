# -*- coding: utf-8 -*-


# import logging


class Logger:

    def trace(self, msg):
        print(msg)

    def error(self, url=None, msg=None, data=None):
        print('URL:' + url + '\n' + msg)
        if data:
            print(data)
        # TODO: send email and Slack message
