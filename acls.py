"""Provides AccessList realted objects"""

from ipaddress import IPv4Address, IPv4Network
from collections import namedtuple

_counter = namedtuple('counter', ['hits', 'delta'])

_condition = namedtuple('condtion', ['protocol',
                           'srcip',
                           'dstip',
                           'srcport',
                           'dstport',
                           'code']

def string_to_ip(ipaddress):
    """Converts ip address as string to an IPv4Address (if host address)
    or IPv4Network (if network address) uses ipaddress from std lib
    Args:
        ipaddress (str): an IP address as a string either as a host
            address (i.e. 10.0.0.0) or as a CIDR network (i.e. 10.0.0.0/8)
    Returns:
        either an IPv4Address or IPv4Network depending on contents of
            ipaddress
    """
    if '/' in ipaddress:
        return IPv4Network(ipaddress)
    else:
        return IPv4Address(ipaddress)

class _Address(object):
    def __init__(self, addresses):
        self._data = [string_to_ip(n) for n in addresses]
    def __iter__(self):
        return iter(self._data)
    def contains(self, matchip):
        if isinstance(matchip, IPv4Network):
            raise ValueError
        return any([(matchip in address) for address in self._data])

class _Condition(object):
    """A match condition for an AccessList Entry"""
    # pylint: disable=too-many-instance-attributes
    # I'm cool with this
    # pylint: disable=too-many-arguments
    # I'm cool with this too


    def __init__(self,
                 protocol=None,
                 srcip=None,
                 dstip=None,
                 srcport=None,
                 dstport=None,
                 code=None):
        pass


class Entry(object):
    """An Entry in an AccessList"""

    # pylint: disable=too-many-instance-attributes
    # I'm cool with this
    # pylint: disable=too-many-arguments
    # I'm cool with this too
    def __init__(self,
                 name=None,
                 index=None,
                 action=None,
                 condition=None,
                 counter=None):

        self._name = None
        self.name = name
        self._index = None
        self.index = index
        self._action = None
        if action is None:
            self.action = 'permit'
        else:
            self.action = action
        if condition is None:
            self.condition = _Condition()
        else:
            self.condition = _Condition(**condition)
        if counter is None:
            self.counter = _counter(None, None)
        else:
            self.counter = _counter(int(counter['hits']), counter['delta'])

    @property
    def name(self):
        """Get name of Condition"""
        return self._name

    @name.setter
    def name(self, value):
        """Set Name"""
        self._name = value

    @property
    def index(self):
        """Get index of Condition"""
        return self._index

    @index.setter
    def index(self, value):
        """Set index"""
        self._index = value

    @property
    def action(self):
        """Get action of Condition"""
        return self._action

    @action.setter
    def action(self, action):
        """Set action"""
        if action in ('permit', 'deny'):
            self._action = action
        else:
            raise NotImplementedError('action {} not implemented'.format(action))

    def check_for_match(self, arg):
        """Checks for matches agasint Conditions in AccessList"""
        pass


class AccessList(object):
    """a List like object for interacting with access lists
    Attributes:
        name (str): A string that functions as the name of the access lists.
            Used as the name when outputing named access-lists """

    def __init__(self, name=None):
        self.__entries = []
        self._name = None
        self.name = name

    def __len__(self):
        return len(self.__entries)

    def __getitem__(self, key):
        return self.__entries[key]

    def __setitem__(self, key, value):
        self.__entries[key] = value

    def __delitem__(self, key):
        del self.__entries[key]

    def __iter__(self):
        return iter(self.__entries)

    def output(self):
        """Placeholder for output method"""
        pass

    def append(self, entry):
        """Appends Entry object to AccessList"""
        if isinstance(entry, Entry):
            self.__entries.append(entry)
        else:
            raise TypeError('{} is not a supported type'.format(type(entry)))

    def insert(self, key, entry):
        """Inserts an Entry object after the entry indicated by key"""
        if isinstance(entry, Entry):
            self.__entries.insert(self, key, entry)
        else:
            raise TypeError('{} is not a supported type'.format(type(entry)))

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

        for entry, number in zip(self, range(step, len(self)*step+step, step)):
            entry.line = number

    @property
    def name(self):
        """Name of access list"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
