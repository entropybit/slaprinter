__author__ = 'mithrawnuruodo'

class Message(object):

    def __init__(self,sender,msg):
        self.sender = sender
        self.msg = msg

class GamePadConnected(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadDisconnected(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadUpPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadDownPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadStartPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)