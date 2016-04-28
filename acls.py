"""Provides AccessList related objects"""

from ipaddress import IPv4Address, IPv4Network
from collections import namedtuple

_counter = namedtuple('counter', ['hits', 'delta'])
ThreeTuple = namedtuple('three_tuple', ['protocol', 'srcip', 'dstip'])

class _Protocol(object):
    def __init__(self, protocols):
        if protocols is None:
            self._data = ['ip']
        else:
            self._data = [n for n in protocols]
    def __iter__(self):
        return iter(self._data)
    def contains(self, other):
        if not isinstance(other, _Protocol):
            raise TypeError('{} is not _Protocol'.format(type(other)))
        return any([(other in protocol) for protocol in self._data])

class _Port(object):
    def __init__(self, ports):
        self._data = []
    def contains():
        return True

class _Address(object):
    def __init__(self, addresses):
        if addresses is None:
            self._data = [IPv4Network('0.0.0.0/0')]
        else:
            self._data = [self.string_to_ip(n) for n in addresses]
    def __iter__(self):
        return iter(self._data)

    @staticmethod
    def string_to_ip(ipaddress):
        """Converts ip address as string to an IPv4Address (if host address)
    or IPv4Network (if network address) uses ipaddress from std lib
    Args:
        ipaddress (str): an IP address as a string either as a host
            address (i.e. 10.0.0.0) or as a CIDR network (i.e. 10.0.0.0/8)
    Returns:
        IPv4Network(object)
    """
        if '/' in ipaddress:
            return IPv4Network(ipaddress)
        else:
            return IPv4Network(ipaddress+'/32')

    def contains(self, matchip):
        """Comapares two isntances of _Address class to determine if they
        overlap"""
        if isinstance(matchip, IPv4Network):
            return any([(address.overlaps(matchip)) for address in self._data])
        else:
            raise TypeError('{} is not IPv4Network')

class Condition(object):
    """Container class for condition objects"""
    conditions = {'protocol': _Protocol,
                  'srcip': _Address,
                  'dstip': _Address,
                  'srcport': _Port,
                  'dstport': _Port}

    def __init__(self):
        self.__data = {}

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, key):
        return self.__data[key]

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    @classmethod
    def condition(cls, **kwargs):
        condition = Condition()
        for key, value in kwargs.items():
            if key in cls.conditions.keys():
                if not isinstance(value, list):
                    value = [value]
                condition[key] = cls.conditions[key](value)
        return condition

class Entry(object):
    """An Entry in an AccessList"""

    # pylint: disable=too-many-arguments
    # I'm cool with this
    def __init__(self,
                 name=None,
                 index=None,
                 action=None,
                 condition=None,
                 counter=None):

        self.__data = {}
        self.__data['name'] = name
        if index is None:
            self.__data['index'] = index
        else:
            self.__data['index'] = int(index)
        self.__data['action'] = action
        if action is None:
            self.__data['action'] = 'permit'
        else:
            self.__data['action'] = action
        self.__data['condition'] = Condition.condition(**condition)
        if counter is None:
            self.__data['counter'] = counter
        else:
            self.__data['counter'] = counter

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    @property
    def name(self):
        """Get name of Condition"""
        return self.__getitem__('name')

    @property
    def index(self):
        """Get index of Condition"""
        return self.__getitem__('index')

    @property
    def action(self):
        """Get action"""
        return self.__getitem__('action')

    @property
    def condition(self):
        """Get condition"""
        return self.__getitem__('condition')

    @property
    def hits(self):
        """Get hits"""
        return self.__getitem__('counter')['hits']

    @property
    def delta(self):
        """Get delta"""
        return self.__getitem__('counter')['delta']

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

    def ismatch(self, match):
        return self.condition == match

    def output(self):
        """Placeholder for output method"""
        pass

    def create_entry(self, **kwargs):
        self.append(Entry(**kwargs))

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
