__author__ = 'mithrawnuruodo'

from GeneralMessages import Message

class RequestActiveTaskMessage(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class ActiveTaskMessage(Message):

    def __init__(self, sender, msg, jid=-1):
        Message.__init__(self,sender, msg)
        self.__jid = jid

    @property
    def jid(self):
        return self.__jid


class SetNewActiveTaskMessage(Message):

    def __init__(self, sender, msg, jid):
        Message.__init__(self,sender, msg)
        self.__jid = jid

    @property
    def jid(self):
        return self.__jid


class SliceFinishedMessage(Message):

    def __init__(self, sender, msg, sid):
        Message.__init__(self,sender, msg)
        self.__sid = sid

    @property
    def sid(self):
        return self.__sid



