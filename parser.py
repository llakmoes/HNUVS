#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from requests import session
import datetime


class Parser:
    FIND_TOKEN = re.compile(r'3A%22[a-zA-Z0-9]*%22%3B')

    def __init__(self, User_Agent=None):
        if not User_Agent:
            self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (HTML, like Gecko)' \
                              ' Version/12.0 Safari/605.1.15'
        else:
            self.User_Agent = User_Agent
        self.HEADERS = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Host': 'rozklad.univd.edu.ua',
            'Accept-Language': 'ru',
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'http://rozklad.univd.edu.ua',
            'Referer': 'http://rozklad.univd.edu.ua/timeTable/group',
            'Content-Length': '530',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.User_Agent,
            'Connection': 'keep-alive',
        }
        self.class_session = session()
        response = self.class_session.get("http://rozklad.univd.edu.ua/timeTable/group")
        self.YII_CSRF_TOKEN = response.cookies.get('YII_CSRF_TOKEN')
        self.res = self.FIND_TOKEN.findall(self.YII_CSRF_TOKEN)

    def get_date(self, group, date):
        data = [
            ('YII_CSRF_TOKEN', self.res[0][5:-6]),
            ('TimeTableForm[group]', str(group)),
            ('TimeTableForm[date1]', f'{date.day}.{date.month}.{date.year}'),
            ('TimeTableForm[date2]',
             f'{date.day}.{date.month}.{date.year}'),
        ]
        response = self.class_session.post('http://rozklad.univd.edu.ua/timeTable/group', headers=self.HEADERS,
                                           data=data)
        schedules = []
        soup = BeautifulSoup(response.text, features="html.parser")
        scores = soup.find_all(text=date.strftime('%d.%m.%Y'))
        schedule = scores[-1].parent.parent.parent
        lessons = schedule.find_all("div", {"class": "cell mh-50"})
        timings = schedule.find_all("div", {"class": "mh-50 cell cell-vertical"})
        for i in range(0, len(lessons)):
            lesson = lessons[i]['data-content'].strip()
            thing = timings[i]
            if len(lesson) > 0:
                print(lesson)
                lesson_number = int(thing.find_all("span", {"class": "lesson"})[0].text[0])
                lesson_start = thing.find_all("span", {"class": "start"})[0].text
                lesson_finish = thing.find_all("span", {"class": "finish"})[0].text
                lesson_type = re.findall(r'\[\w+]<br>', str(lesson))[0][1:-5]
                lesson_name = re.findall(r'[\s*\w+]*\[\w+]<br>', lesson)[0][:-10]
                lesson_teacher = re.findall(r'\w+ \w+.\w+.<br>', lesson)[0][:-4].split(" ")
                lesson_room = re.findall(r'ауд\. \w*.*\w*<br>', lesson)[0][5:-4]
                schedule = {
                    "number": lesson_number,
                    "start": lesson_start,
                    "finish": lesson_finish,
                    "lesson": lesson_name,
                    "first_name": lesson_teacher[1][0:1],
                    "middle_name": lesson_teacher[1][2:3],
                    "last_name": lesson_teacher[0],
                    "lesson_type": lesson_type,
                    "lesson_room": lesson_room,
                    "group": group,
                    "date": date
                }
                schedules.append(schedule)
            else:
                schedules.append(None)
        return schedules
