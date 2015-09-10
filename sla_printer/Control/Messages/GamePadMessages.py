__author__ = 'mithrawnuruodo'

class Message(object):

    def __init__(self,sender,msg):
        self.sender = sender
        self.msg = msg

    def __str__(self):
        return "[" + str(self.sender) + "]: " + str(self.msg)

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

class GamePadRightPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadLeftPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadSelectPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadStartPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadYPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadXPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadAPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadBPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


