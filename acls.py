import ipaddress

class Entries(list):
    """Container class for Entries"""
    pass

class Entry(object):
    """An Entry in an AccessList"""
    def __init__(self, name=None, line=None, action=None, condition=None):
        self.name = name
        self.line = line
        self.action = action
        if condition is None:
            self.condition = Conditions()
        else:
            self.condition = condition

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
            self._action = value

        @property
        def condition(self):
            """Get condition"""
            return self._condition

        @condition.setter
        def condition(self, value):
            """Set condition"""
            self._condition = value


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
