__author__ = 'mithrawnuruodo'


class Message(object):

    def __init__(self,sender,msg):
        self.sender = sender
        self.msg = msg

    def __str__(self):
        return "[" + str(self.sender) + "]: " + str(self.msg)

class QuitMessage(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)