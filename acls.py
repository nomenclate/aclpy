import ipaddress

protocolnames = {
                }

portnames = {
            }

codenames = {
            }


class _Condition(object):
    """A match condition for an AccessList Entry"""
    def __init__(self,
                 protocol='ip',
                 srcip=None,
                 dstip=None,
                 srcport=None,
                 dstport=None,
                 code=None):

        self.protocol = protocol
        self.srcip = srcip
        self.dstip = dstip
        self.srcport = srcport
        self.dstport = dstport
        self.code = code

    @property
    def protocol(self):
        """Get protocol of Condition"""
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        """Set protocol"""
        self._protocol = value

    @property
    def srcip(self):
        """Get srcip of Condition"""
        return self._srcip

    @srcip.setter
    def srcip(self, value):
        """Set prototocol"""
        self._srcip = value

    @property
    def dstip(self):
        """Get dstip of Condition"""
        return self._dstip

    @dstip.setter
    def dstip(self, value):
        """Set prototocol"""
        self._dstip = value

    @property
    def srcport(self):
        """Get srcport of Condition"""
        return self._srcport

    @srcport.setter
    def srcport(self, value):
        """Set prototocol"""
        self._srcport = value

    @property
    def dstport(self):
        """Get dstport of Condition"""
        return self._dstport

    @dstport.setter
    def dstport(self, value):
        """Set prototocol"""
        self._dstport = value

    @property
    def code(self):
        """Get code of Condition"""
        return self._code

    @code.setter
    def code(self, value):
        """Set prototocol"""
        self._code = value

class Entry(object):
    """An Entry in an AccessList"""
    def __init__(self, name=None, line=None, action=None, condition=None):
        self.name = name
        self.line = line
        self.action = action
        if condition is None:
            self.condition = _Condition()
        else:
            self.condition = _Condition(**condition)

    @property
    def name(self):
        """Get name of Condition"""
        return self._name

    @name.setter
    def name(self, value):
        """Set Name"""
        self._name = value

    @property
    def line(self):
        """Get line of Condition"""
        return self._line

    @line.setter
    def line(self, value):
        """Set line"""
        self._line = value

    @property
    def action(self):
        """Get action of Condition"""
        return self._action

    @action.setter
    def action(self, value):
        """Set action"""
        #FIXME: need unit test for error
        if value in ('permit','deny'):
            self._action = value
        else:
            raise NotImplementedError('action {} not implemented'.format(value))

    def check_for_match(self, arg):
        """Checks for matches agasint Conditions in AccessList"""
        pass


class AccessList(object):
    """a List like object for interacting with access lists

    Attributes:
        name (str): A string that functions as the name of the access lists.
            Used as the name when output named access-lists """

    def __init__(self, entries=None, name=None):
        if entries is None:
            self.entries = []
        else:
            self.entries = entries
        self.name = name

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __delitem__(self, key):
        del self.entries[key]

    def __iter__(self):
        return iter(self.entries)

    def append(self, entry):
        if isinstance(entry, Entry):
            self.entries.append(entry)
        else:
            raise TypeError('{} is not a supported type'.format(type(value)))

    def resequence(self, step=1):
        """Resequences line numbers of accesslist incrementing by step
        value

        Args:
            step (Optional[int]): the value to increment by. Defaults to 1

        Raises:
            ValueError: If step is less than or equal to zero
        """
        if step <= 0:
            raise ValueError('step must be positive non zero value')

        for entry,n in zip(self, range(step, len(self)*step+step, step)):
            entry.line = n

    @property
    def name(self):
        """Name of access list"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
