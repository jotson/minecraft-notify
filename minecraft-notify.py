#!/usr/bin/python

import datetime
import smtplib
from email.mime.text import MIMEText

logfiles = ['/path/to/your/server.log']  # list of log files to scan
status = '/tmp/minecraft-server-last-scan'  # last scan date is stored here
email = ['user1@example.com', 'user2@example.com', '...']
ignore = ['username-to-ignore', 'username-to-ignore']
smtp_host = 'smtp host'
smtp_port = 587
smtp_user = 'smtp server login'
smtp_password = 'smtp server password'
smtp_from = 'from@example.com'


def handleEvent(description):
    # Skip users in ignore list
    for user in ignore:
        if description.find(user) != -1:
            return

    # Email notification
    description = description.rstrip('\n')
    msg = MIMEText(description)
    msg['Subject'] = "[MINECRAFT] " + description
    msg['From'] = smtp_from
    msg['To'] = ', '.join(email)
    s = smtplib.SMTP(smtp_host, smtp_port)
    s.starttls()
    s.login(smtp_user, smtp_password)
    s.sendmail(smtp_from, email, msg.as_string())
    s.quit()


if __name__ == '__main__':
    # Load lastScan datetime
    lastScan = None
    try:
        f = open(status, 'r')
        data = f.readlines()
        f.close()
        lastScan = datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
    except:
        pass
    if lastScan is None:
        lastScan = datetime.datetime.now()
    f = open(status, 'w')
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    f.close()

    for log in logfiles:
        f = open(log, 'r')
        data = f.readlines()
        f.close()

        ts = None
        for line in data:
            try:
                (event_date, event_time, event_level, event_description) = line.split(' ', 3)
                ts = datetime.datetime.strptime(event_date + ' ' + event_time, '%Y-%m-%d %H:%M:%S')
                if ts > lastScan:
                    if event_description.find("joined the game") != -1:
                        handleEvent(event_description)
                    if event_description.find("left the game") != -1:
                        handleEvent(event_description)
            except ValueError:
                pass
