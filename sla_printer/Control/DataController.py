__author__ = 'mithrawnuruodo'


from threading import Thread
from MessageHandler import Observable, Dispatcher, Observer
import Control
from multiprocessing import Queue
#from Queue import Queue
import Model

class DataPool(Thread, Observable):

    pool = set()

    def __init__(self, dispatcher=Dispatcher()):

        Thread.__init__(self)
        Observable.__init__(self, dispatcher)



    def add(self, data):

        if isinstance(data, Model.Data):
            self.pool.add(data)
            self.put_message(Control.Messages.DataReceivedMessage(self, data))

            tasks = PrintingTaskController()
            tasks.handle_new_task(data)

            return True

        return False

    def get_by_id(self, id):

        for d in self.pool:
            if d.__hash__() == int(id):
                return d

        return None


    def remove(self, data):

        if isinstance(data, Model.data):
            self.pool.remove(data)
            self.put_message(Control.Messages.DataDeletedMessage(self, data))
            return True

        return False

    def get_data_str(self):
        return [str(d) for d in list(self.pool)]

    def get_data(self):
        return [d for d in list(self.pool)]



class PrintingTaskController(Observer):

    active_task = None
    task_stack = Queue()

    def __init__(self, dispatcher=Dispatcher()):
        dispatcher.register_observer(self)



    def notify(self,msg):

        print("received msg :: " + str(msg))
        if isinstance(msg, Control.Messages.DataReceivedMessage):
            data = msg.msg
            sender = msg.sender

            if isinstance(sender, DataPool):

                if isinstance(data, Model.PrintingTaskData):
                    self.handle_new_task(data)




    def handle_new_task(self, data):
        '''
        handle new incoming PrintingTaskData

        :param data:    a PrintingTaskData object representing the newest incominc data

        '''

        #print("handling incoming printing task")


        if PrintingTaskController.active_task is None:
            PrintingTaskController.active_task = data
            #print("new active task")
            #print(PrintingTaskController.active_task)
        else:
            PrintingTaskController.task_stack.put(data)


    @property
    def printing_tasks(self):
        '''

        :return: a list of printing task dicts
        '''

        data = DataPool().get_data()

        task_list = []

        if len(data) > 0:

            for d in data:
                if isinstance(d, Model.PrintingTaskData):

                    PrintingTaskController.active_task

                    dict = {}
                    dict['id'] = d.__hash__()
                    dict['active'] = (d == PrintingTaskController.active_task)
                    dict['finished'] = d.finished
                    dict['time'] = d.time
                    dict['filename'] = d.file_name
                    dict['file'] = d.stl_file


                    #print("")
                    #print(str(d))


                    task_list.append(dict)


        return task_list

    def active_job(self):
        '''

        :return: a dictonary containing the current active jobs data
        '''

        d = PrintingTaskController.active_task

        if d is not None:
            dict = {}

            dict['id'] = d.__hash__()
            dict['active'] = (d == PrintingTaskController.active_task)
            dict['time'] = d.time
            dict['filename'] = d.file_name
            dict['file'] = d.stl_file

            slices = []
            for i in range(0,len(d.slices)):
                slices.append([d.slices[i], d.slices_todo[i]])

            dict['slices'] = slices
            #dict['slices_todo'] = d.slices_todo
            #dict['slice_number'] = d.slice_number
            dict['progress'] = d.slices_todo.count(True)/(1.0*d.slice_number)
            dict['illumination_time'] = d.illumination_time
            [mins, secs] = divmod(d.illumination_time*2*len(d.slices), 60)
            dict['eta'] = str(mins) + "mins " + str(secs) + "s "

            return dict
        else:
            return None















