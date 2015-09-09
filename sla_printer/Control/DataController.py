__author__ = 'mithrawnuruodo'


import sqlite3
from MessageHandler import Observable, MessageBus, Message


class NewPrintingTaskMsg(Message):

    def __init__(self, sender, description, task):
        Message.__init__(self, sender=sender, description=description)
        self.task




class DataBaseController(Observable):


    def __init__(self, in_memory_mode=True, bus=None):

        Observable.__init__(self, bus=bus)
        self.__in_memory_mode = in_memory_mode
        self.__database = None

        self.start_db()


    def start_db(self):


        if self.__in_memory_mode:
            #print('file:server_database?mode=memory&cache=shared')
            #self.__database = sqlite3.connect('file:server_database?mode=memory&cache=shared')
            self.__database = sqlite3.connect(":memory:")
        else:
            self.__database = sqlite3.connect("server.db")
            #print("server.db")




    def make_init_tables(self):

            c = self.__database.cursor()

            c.execute('''CREATE TABLE jobs
                (jid integer primary key autoincrement, step_width real, illumination_time real,
                    illumination_intensity real, file_name text, stl_file text, slices text)
            ''')

            c.execute('''CREATE TABLE slices
                (sid integer primary key autoincrement, job int)
            ''')

            c.execute('''CREATE TABLE points
                (pid integer primary key autoincrement, x real, y real, sid integer)
            ''')

            self.__database.commit()



    def save_printing_task(self, task):


        msg = NewPrintingTaskMsg(self, "new printing task found", task)
        self.put_message(msg)
        c = self.__database.cursor()


        # insert job row
        c.execute(
                  'INSERT INTO jobs' +
                  '  (step_width, illumination_time, illumination_intensity, file_name, stl_file, slices)' +
                    ' VALUES ' +
                    '(' + str(task.step_width) + ', ' + str(task.illumination_time) + ', ' + str(task.illumination_intensity) + ', "'  +
                    str(task.file_name) + '", "' +  str(task.stl_file) + '", "' + str(task.slice_number) +'")'
                )

        jid = c.lastrowid
        #print("inserted :" + str() jid))

        slices = task.slices

        for slice in slices:

            # insert slice row
            c.execute('INSERT INTO slices' +
                '  (job) ' +
                ' VALUES ' +
                '(' + str(jid) + ')'
            )

            #print(jid)
            sid = c.lastrowid
            #print("sid="+str(sid))

            for p in slice:
                # insert point row
                c.execute(
                  'INSERT INTO points' +
                  '  (x,y, sid)' +
                    ' VALUES ' +
                    '(' + str(p[0]) + ', ' + str(p[1]) + ',' + str(sid) + ')'
                )

        self.__database.commit()


    def last_insert_id(self):
        c = self.__database.cursor()
        return c.lastrowid


    def release(self):
        self.__database.close()


    def get_all_slices(self):

        c = self.__database.cursor()


        # insert job row
        c.execute('''
                    SELECT * FROM slices
                ''')

        result = c.fetchone()
        return result








    #def save(self, printing_task):

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class PrintingTaskData(object):

    def __init__(self):
        self.slices = None
        self.stl_file =""
        self.illumination_time = 0
        self.illumination_intensity = 0

        self.step_width = 0
        self.slice_number = 0
        self.file_name = ""

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
                x = np.random.rand()
                y = np.random.rand()
                slice.append([x,y])

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
        print("printing slices: ")
        print(db_controller.get_all_slices())
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
    worker = lambda: task_worker(n)

    worker_process = m.Process(target=inserter)
    inserter_process = m.Process(target=worker)

    worker_process.start()
    inserter_process.start()

