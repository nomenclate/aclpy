import ipaddress

class Conditions(object):
    """Container class for Conditions"""
    pass

class Condition(object):
    """Conditions are a part of Entries"""
    pass

class Entries(list):
    """Container class for Entries"""
    pass

class Entry(object):
    """An Entry in an AccessList"""
    def __init__(self, name=None, line=None, action=None, conditions=None):
        self.name = name
        self.line = line
        self.action = action
        if conditions is None:
            self.conditions = Conditions()
        else:
            self.conditions = conditions

        @property
        def name(self):
            """Get name of Entry"""
            return self._name

        @property.setter
        def name(self, value):
            """Set Name"""
            self._name = value

        @property
        def line(self):
            """Get line of Entry"""
            return self._line

        @property.setter
        def line(self, value):
            """Set line"""
            self._line = value

        @property
        def action(self):
            """Get action of Entry"""
            return self._action

        @property.setter
        def action(self, value):
            """Set action"""
            #FIXME: need unit test for error
            if action in ('permit','deny'):
                self._action = value
            else:
                raise NotImplementedError('action {} not implemented'
                                          .format(value))

        @property
        def condition(self):
            """Get condition"""
            return self._condition

        @condition.setter
        def condition(self, value):
            """Set condition"""
            self._condition = value

        def check_for_match(self, arg):
            """Checks for matches agasint Conditions in AccessList"""
            pass


class AccessList(object):
    """An AccessList"""
    def __init__(self, entries=None, name=None):
        super(AccessList, self).__init__()
        if not entries:
            self.entries = Entries()
        else:
            self.entries = entries
        self.name = name

    @property
    def entries(self):
        """Get entries"""
        return self._entries

    @entries.setter
    def entries(self, value):
        """Set entries"""
        self._entries = value

    @property
    def name(self):
        """Name of access list"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
