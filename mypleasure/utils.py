# -*- coding: utf-8 -*-
import logging
import logging.handlers
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from pyslack import SlackClient
from mypleasure import settings


class Logger:

    def __init__(self, verbosity=1, reporting=1):
        '''
        Logger util for relevant data and errors.

        Args:
            verbosity: 0 silences logger in console, 1 prints output.
                Logging to file is active at any level.
            reporting: 0 silences reporting, 1 logs into logfile,
                2 sends Slack message only,
                3 sends email only,
                4 sends both Slack and email messages.
                Both 2, 3 and 4 also print to logfile.
        '''
        self.verbosity = verbosity
        self.reporting = reporting

        self.email = smtplib.SMTP(
            settings.EMAIL_SMTP_SERVER, settings.EMAIL_SMTP_PORT
        )

        self.slack = SlackClient(settings.SLACK_API_KEY)

        # Set up logging to files.
        self.file = logging.getLogger(__name__)
        debug_handler = logging.handlers.RotatingFileHandler(
            settings.DEBUG_LOG_FILE,
            mode=settings.LOG_FILE_WRITE_MODE,
            maxBytes=settings.LOG_FILE_BACKUP_COUNT,
            backupCount=settings.LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )
        error_handler = logging.handlers.RotatingFileHandler(
            settings.ERROR_LOG_FILE,
            mode=settings.LOG_FILE_WRITE_MODE,
            maxBytes=settings.LOG_FILE_BACKUP_COUNT,
            backupCount=settings.LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )
        logformatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s'
        )
        debug_handler.setFormatter(logformatter)
        error_handler.setFormatter(logformatter)
        self.file.addHandler(debug_handler)
        self.file.addHandler(error_handler)
        self.file.setLevel(logging.ERROR)

    def trace(self, msg):
        if self.verbosity > 0:
            print(msg)
        self.__debug_to_file(msg)

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
            self.__error_to_file(report)

        # Send Slack message to dedicated channel
        # (and log to file) if specified.
        if self.reporting == 2 or self.reporting == 4:
            self.__slack(report)

        # Send email report (and log to file) if specified.
        if self.reporting == 3 or self.reporting == 4:
            self.__email(report)

    def __debug_to_file(self, msg):
        self.file.debug(msg)

    def __error_to_file(self, report):
        self.file.error(report)

    def __email(self, report):
        self.__error_to_file(report)

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
            self.email.starttls()
            self.email.login(
                settings.EMAIL_SMTP_USER, settings.EMAIL_SMTP_PWD
            )
            self.email.sendmail(
                settings.EMAIL_SMTP_RECIPIENT,
                settings.EMAIL_SMTP_RECIPIENT,
                msg.as_string()
            )
            self.email.quit()
        except:
            # TODO - log email error to file
            pass

    def __slack(self, report):
        self.__error_to_file(report)
        try:
            self.slack.chat_post_message(
                settings.SLACK_CHAT_ROOM, report['message'], username='TARS'
            )
        except:
            # TODO - log Slack error to file
            pass
