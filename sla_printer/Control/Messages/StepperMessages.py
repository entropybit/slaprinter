__author__ = 'mithrawnuruodo'

from GeneralMessages import Message


class OneStepDown(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)

class OneStepUp(Message):

    def __init__(self, sender, msg):
        Message.__init__(self,sender, msg)


class SeveralStepsUp(Message):

    def __init__(self, sender, msg, steps):
        Message.__init__(self,sender, msg)
        self.steps = steps


class SeveralStepsDown(Message):

    def __init__(self, sender, msg, steps):
        Message.__init__(self,sender, msg)
        self.steps = steps


class SeveralStepsUpAndDown(Message):

    def __init__(self, sender, msg, steps):
        Message.__init__(self,sender, msg)
        self.steps = steps

class SeveralStepsDownAndUp(Message):

    def __init__(self, sender, msg, steps):
        Message.__init__(self,sender, msg)
        self.steps = steps
