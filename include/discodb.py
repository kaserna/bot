#  Класс для работы с базой данных

import sqlite3
import datetime


class DiscoDB:
    con = None
    cur = None

    def __init__(self):
        self.con = sqlite3.connect('Discord.db')
        self.cur = self.con.cursor()

    def getcommandhelp(self, command):
        sel = self.cur.execute("SELECT * from Commands WHERE comm = '" + command + "'").fetchone()
        return sel

    def logcommand(self, user, command):
        self.cur.execute("INSERT INTO logtable(user, command, timestamp) values (?,?,?)", (str(user), str(command),
                                                                                           datetime.datetime.today()))
        self.con.commit()

    def getlast10commands(self):
        sel = self.cur.execute("select user, command from logtable order by timestamp desc limit 10").fetchall()
        return sel
