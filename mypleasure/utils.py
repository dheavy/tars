# -*- coding: utf-8 -*-


# import logging


class Logger:

    def trace(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)
        # TODO: send email, show stack in Slack message
