__author__ = 'mithrawnuruodo'


import sqlite3
import Control.MessageHandler as handler
import Control.Messages as messages
import datetime
import pytz
from time import strftime

#berlin = pytz.timezone('Europe/Berlin')
gmt = pytz.timezone('GMT')

from ServiceFunctions import now_unix
import pickle

class PrintingTaskData(object):

    def __init__(self):
        self.slices = None
        self.stl_file =""
        self.illumination_time = 0
        self.illumination_intensity = 0

        self.step_width = 0
        self.slice_number = 0
        self.file_name = ""
        self.id = -1
        self.insert_time = 0

    @property
    def time(self):
        print("time in time")
        t = datetime.datetime.utcfromtimestamp(int(self.insert_time))
        t = pytz.utc.localize(t)
        t = t.strftime('%Y-%m-%d %H:%M:%S')
        return t


class DataBaseController(handler.Observable):


    def __init__(self, in_memory_mode=True, bus=handler.MessageBus(), connect_on_init=True):

        handler.Observable.__init__(self, bus=bus)
        self.__in_memory_mode = in_memory_mode
        self.__database = None


        if connect_on_init:
            self.start_db()


    def start_db(self):


        if self.__in_memory_mode:
            #print('file:server_database?mode=memory&cache=shared')
            #self.__database = sqlite3.connect('file:server_database?mode=memory&cache=shared')
            self.__database = sqlite3.connect(":memory:", check_same_thread=False)
        else:
            self.__database = sqlite3.connect("server.db",  check_same_thread=False)
            #print("server.db")


        self.make_init_tables()




    def make_init_tables(self):

            #print("make tables")
            c = self.__database.cursor()

            r = c.execute("SELECT * FROM sqlite_master WHERE name ='jobs' and type='table'")
            if r.fetchone() is None:

                c.execute('''CREATE TABLE jobs
                    (jid integer primary key autoincrement, step_width real,
                        illumination_intensity real, file_name text, stl_file text, slices text, insertion_time date)
                ''')


            r = c.execute("SELECT * FROM sqlite_master WHERE name ='slices' and type='table'")
            if r.fetchone() is None:

                c.execute('''CREATE TABLE slices
                    (sid integer primary key autoincrement, job int, illumination_time real, )
                ''')


            r = c.execute("SELECT * FROM sqlite_master WHERE name ='points' and type='table'")
            if r.fetchone() is None:

                c.execute('''CREATE TABLE points
                    (pid integer primary key autoincrement, x real, y real, sid integer)
                ''')

            r = c.execute("SELECT * FROM sqlite_master WHERE name ='lines' and type='table'")
            if r.fetchone() is None:

                c.execute('''CREATE TABLE lines
                    (lid integer primary key autoincrement, sid integer,p_start integer, p_end integer)
                ''')

            self.__database.commit()



    def save_printing_task(self, task):


        msg = messages.NewPrintingTaskMsg(DataBaseController(),"new printing task found", task)



        #print(msg)
        #print(pickle.dumps(msg))

        self.put_message(msg)
        c = self.__database.cursor()


        # insert job row
        c.execute(
                  'INSERT INTO jobs' +
                  '  (step_width, illumination_time, illumination_intensity, file_name, stl_file, slices, insertion_time)' +
                    ' VALUES ' +
                    '(' + str(task.step_width) + ', ' + str(task.illumination_time) + ', ' + str(task.illumination_intensity) + ', "'  +
                    str(task.file_name) + '", "' +  str(task.stl_file) + '", "' + str(task.slice_number) + '", "'+ str(now_unix()) + '")'
                )

        jid = c.lastrowid
        #print("inserted :" + str(jid))

        slices = task.slices

        for slice in slices:

            illumination_time = slice[0]

            # insert slice row
            c.execute('INSERT INTO slices' +
                '  (job, illumination_time) ' +
                ' VALUES ' +
                '(' + str(jid) + ')'
            )

            #print(jid)
            sid = c.lastrowid
            #print("sid="+str(sid))

            #print("slice: " + str(slice ))

            for line in slice[1]:
                # insert point row

                pid0 = -1
                pid1 = -1
                i = 0
                for p in line:

                    #print("p in line : " + str(p))

                    #c.execute('SELECT pid from points WHERE sid=' + str(sid) + ' AND x = ' + str(p[0]) + ' AND y = ' + str(p[1]) + '')
                    #print('insert into points ... (' + str(p[0]) + ', ' + str(p[1]) + ',' + str(sid) + ')')
                    c.execute(
                    'INSERT INTO points' +
                    '  (x,y, sid)' +
                        ' VALUES ' +
                        '(' + str(p[0]) + ', ' + str(p[1]) + ',' + str(sid) + ')'
                    )

                    if i == 0:
                        pid0 = c.lastrowid
                        i = i+1
                    else:
                        pid1 = c.lastrowid

                c.execute(
                    'INSERT INTO lines' +
                    ' (p_start, p_end)' +
                    ' VALUES ' +
                    '(' + str(pid0) + ', ' + str(pid1) + ')'
                )

        self.__database.commit()

        return jid


    def last_insert_id(self):
        c = self.__database.cursor()
        return c.lastrowid


    def release(self):
        self.__database.close()


    def get_all_slices(self):

        c = self.__database.cursor()


        # get sli job row
        c.execute('''
                    SELECT * FROM slices
                ''')

        result = c.fetchone()
        return result


    def printing_tasks(self):
        # get sli job row
        c = self.__database.cursor()
        ret = []
        for row in c.execute('SELECT jid, file_name, stl_file, insertion_time FROM jobs'):

            #print("res : " + str(row))
            task = PrintingTaskData()
            task.id = int(row[0])
            task.file_name = row[1]
            task.stl_file = row[2]
            task.insert_time = row[3]
            print("tid : " +str(task.id) + " | " + str(int(row[0])))
            print("task " + str(task))
            ret.append(task)


        return ret


    def active_job(self):

        return 0

    def get_by_id(self, jid):

        c = self.__database.cursor()
        for row in c.execute('SELECT file_name, stl_file, insertion_time FROM jobs WHERE jid=' + str(int(jid)) + ''):

            task = PrintingTaskData()
            task.id = int(jid)
            task.file_name = row[0]
            task.stl_file = row[1]
            task.insert_time = row[2]
            return task







    #def save(self, printing_task):

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def draw_printing_tasks(n=100):

    import numpy as np
    from math import ceil

    np.random.seed(42)
    tasks = []

    for i in range(0,n):

        t = PrintingTaskData()
        t.stl_file = id_generator(size=1000)

        slices_num = np.random.rand()*n

        slices_num = int(ceil(slices_num))
        slices = []
        for s in range(0,slices_num):
            slice = []
            points =int(ceil(np.random.rand()*n))

            for p in range(0,points):
                x0 = np.random.rand()
                y0 = np.random.rand()
                x1 = np.random.rand()
                y1 = np.random.rand()
                slice.append([[x0,y0],[x1,y1]])

            slices.append(slice)

        t.slices = slices
        t.illumination_time = np.random.rand()
        t.illumination_intensity = np.random.rand()
        t.step_width = np.random.rand()
        t.slice_number = len(slices)
        t.file_name = "drawn_file" + str(i)

        tasks.append(t)


    return tasks


def task_inserter(n = 100):

    tasks = draw_printing_tasks(n)
    db_controller = DataBaseController(in_memory_mode=False)

    i = 0
    for t in tasks:
        print('#######TASK[' + str(i) + ']############')
        db_controller.save_printing_task(t)
        print(t.stl_file)
        i=i+1

    db_controller.release()


def task_worker(n = 100):

    db_controller = DataBaseController(in_memory_mode=False)

    while True:
        #if id is not None:
        #    print("last_insert_id: " + str(id))

        slices = db_controller.get_all_slices()
        if slices is not None:
            print("printing slices: ")
            print(slices)
            print("")
            print("")


    db_controller.release()

import multiprocessing as m

if __name__=="__main__":

    make = True

    #tasks = draw_printing_tasks(10)

    print("creating new db controller")
    db_controller = DataBaseController(in_memory_mode=False)

    if make:
        db_controller.make_init_tables()

    db_controller.release()

    # prepare for parallel working on db
    n = 20
    inserter = lambda: task_inserter(n)
    #worker = lambda: task_worker(n)

    #worker_process = m.Process(target=worker)
    inserter_process = m.Process(target=inserter)

    #worker_process.start()
    inserter_process.start()

