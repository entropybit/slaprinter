__author__ = 'mithrawnuruodo'

from GeneralMessages import Message

class GamePadConnected(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadDisconnected(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadUpPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadUpRightPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadDownPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadDownRightPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadRightPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadLeftPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadLeftDownPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class GamePadLeftUpPressed(Message):

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


class GamePadShoulderLPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class GamePadShoulderRPressed(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)




