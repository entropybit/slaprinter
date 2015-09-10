__author__ = 'mithrawnuruodo'

from GamePadMessages import Message



class DataReceivedMessage(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class DataDeletedMessage(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)



class NewPrintingTaskMsg(Message):

    def __init__(self, sender, description, task):
        Message.__init__(self, sender, description)
        self.task = task