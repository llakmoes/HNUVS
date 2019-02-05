from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, UniqueConstraint
import datetime


Base = declarative_base()


class User(Base):
    user_chat_id = Column(Integer, primary_key=True)
    user_name = Column(String(20), primary_key=True)

    def __repr__(self):
        return "<User(Name='%s', Chat_id='%s')>" % (
            self.user_name, self.user_chat_id)

    def __init__(self, user_chat_id, user_name):
        self.user_chat_id = user_chat_id
        self.user_name = user_name


class Subscriber(Base):
    user_id = Column(Integer, ForeignKey('user.user_chat_id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.group_id'), primary_key=True)
    date = Column(DATETIME, default=datetime.datetime.utcnow, primary_key=True)

    def __repr__(self):
        return "<User(user_id='%s', group_id='%s')>" % (
            self.user_id, self.group_id)

    def __init__(self, user_id, group):
        self.user_id = user_id
        self.group_id = group.group_id


class Teacher(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    middle_name = Column(String(20))
    last_name = Column(String(20))
    __table_args__ = (UniqueConstraint('first_name', 'middle_name', 'last_name'),)

    def __repr__(self):
        return "<Teacher(first_name='%s', middle_name='%s', last_name='%s')>" % (
            self.first_name, self.middle_name, self.last_name)

    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name


class Lesson(Base):
    id = Column(Integer, primary_key=True)
    lesson_type = Column(Integer, ForeignKey('lesson_type.id'))
    lesson_name = Column(Integer, ForeignKey('lesson_name.id'))
    lesson_teacher = Column(Integer, ForeignKey('teacher.id'))
    lesson_room = Column(Integer, ForeignKey('lesson_room.id'))
    __table_args__ = (UniqueConstraint('lesson_type', 'lesson_name', 'lesson_teacher'),)

    def __repr__(self):
        return "<Lesson(lesson_type='%s', lesson_name='%s', lesson_teacher='%s')>" % (
            self.lesson_type, self.lesson_name, self.lesson_teacher)

    def __init__(self, lesson_type, lesson_name, lesson_teacher, lesson_room):
        self.lesson_type = lesson_type
        self.lesson_teacher = lesson_teacher.id
        self.lesson_name = lesson_name
        self.lesson_room = lesson_room


class Group(Base):
    group_id = Column(Integer, primary_key=True)
    group = Column(String(20), primary_key=True)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id'), primary_key=True)
    course = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Group(group='%s', faculty_id='%s', course='%s')>" % (
            self.group, self.faculty_id, self.course)

    def __init__(self, group_id, group, faculty_id, course):
        self.course = course
        self.faculty_id = faculty_id.faculty_id
        self.group = group
        self.group_id = group_id


class Faculty(Base):
    faculty_id = Column(Integer, primary_key=True)
    fullname = Column(String(200), primary_key=True)

    def __repr__(self):
        return "<Faculty(fullname='%s', faculty_id='%s')>" % (
            self.fullname, self.faculty_id)

    def __init__(self, faculty_id, fullname):
        self.faculty_id = faculty_id
        self.fullname = fullname


class Schedule(Base):
    id = Column(Integer, primary_key=True)
    date = Column(DATETIME)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))
    number = Column(Integer)
    group = Column(Integer, ForeignKey('group.group_id'))
    start_time = Column(String(20))
    finish_time = Column(String(20))
    __table_args__ = (UniqueConstraint('date', 'lesson_id', 'number', 'group', 'start', 'finish'),)

    def __repr__(self):
        return "<Schedule(date='%s', number='%s', group='%s', start='%s', finish='%s')>" % (
            self.date, self.number, self.group, self.start_time, self.finish_time)

    def __init__(self, lesson_id, number, group, start, finish):
        self.group = group.group_id
        self.number = number
        self.lesson_id = lesson_id.id
        self.finish_time = finish
        self.start_time = start


class LessonType(Base):
    id = Column(Integer, primary_key=True)
    type = Column(String(20), unique=True)

    def __repr__(self):
        return "<LessonType(typename='%s')>" % self.type

    def __init__(self, lesson_type):
        self.type = lesson_type


class LessonName(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)

    def __repr__(self):
        return "<LessonName(Lesson name='%s')>" % self.name

    def __init__(self, lesson_name):
        self.name = lesson_name


class LessonRoom(Base):
    id = Column(Integer, primary_key=True)
    room = Column(String(20), unique=True)

    def __repr__(self):
        return "<LessonRoom(Lesson name='%s')>" % self.room

    def __init__(self, lesson_room):
        self.room = lesson_room
