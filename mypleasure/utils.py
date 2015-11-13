# -*- coding: utf-8 -*-
# import logging
import smtplib
from datetime import datetime
from mypleasure import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


class Logger:

    def __init__(self, verbosity=1, reporting=1):
        print(settings)
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

        self.email_server = smtplib.SMTP(
            settings.EMAIL_SMTP_SERVER, settings.EMAIL_SMTP_PORT
        )

    def trace(self, msg):
        if self.verbosity > 0:
            print(msg)

    def error(self, url='', msg='', data=None):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report = {}
        report['timestamp'] = now
        report['url'] = url
        report['message'] = '----\n+ ERROR ({0}) +\n'.format(now)
        report['message'] += '\n> Job URL: ' + url + '\n'
        report['message'] += '\n> Message:\n' + msg
        if data:
            report['message'] += '\n\n> Data:\n' + str(data)

        # Print to console if set to `verbose`.
        if self.verbosity > 0:
            print(report['message'])

        # Log to file if specified.
        if self.reporting == 1:
            self.__logfile(report)

        # Send Slack message to dedicated channel
        # (and log to file) if specified.
        if self.reporting == 2:
            self.__slack(report)

        # Send email report (and log to file) if specified.
        if self.reporting == 3:
            self.__email(report)

    def __logfile(self, report):
        pass

    def __email(self, report):
        self.__logfile(report)

        msg = MIMEMultipart()
        msg['Subject'] = '[ERROR] ' + report['url'] + ' @ '
        msg['Subject'] += report['timestamp']
        msg['From'] = formataddr((str(
            Header('TARS from Mypleasu.re', 'utf-8')),
            'tars.error@mypleasu.re'
        ))
        msg['To'] = settings.EMAIL_SMTP_RECIPIENT

        body = report['message']
        msg.attach(MIMEText(body, 'plain'))

        try:
            self.email_server.starttls()
            self.email_server.login(
                settings.EMAIL_SMTP_USER, settings.EMAIL_SMTP_PWD
            )
            self.email_server.sendmail(
                settings.EMAIL_SMTP_RECIPIENT,
                settings.EMAIL_SMTP_RECIPIENT,
                msg.as_string()
            )
            self.email_server.quit()
        except:
            pass

    def __slack(self, msg):
        self.__logfile(msg)
        pass
