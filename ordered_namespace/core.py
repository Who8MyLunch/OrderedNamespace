from collections import OrderedDict
import re

try:
    import IPython
except ImportError:
    IPython = None


class OrderedNamespace:

    # Regular expression pattern for valid Python attributes
    # https://docs.python.org/3/reference/lexical_analysis.html#identifiers
    # _valid_key_pattern = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')
    _valid_key_pattern = re.compile('[a-zA-Z][a-zA-Z0-9_]*')
    _special_names = ['_odict']

#     _odict = None
    def __init__(self, *args, **kwargs):
#         self._odict = OrderedDict()
        self.__dict__['_odict'] = OrderedDict()

        self.update(*args, **kwargs)

#     @property
#     def _odict(self):
#         if not self._odict:
#             self.__
#         return self._odict

    def update(self, *args, **kwargs):
        d = {}
        d.update(*args, **kwargs)
        for key, value in d.items():
            self[key] = value

    def _valid_key(self, key):
        """Return True if supplied key string serves as a valid attribute name: alphanumeric strings
        beginning with a letter.  Leading underscore not allowed.  Also test for conflict with protected
        attribute names (e.g. dict class instance methods).
        """
        if not isinstance(key, str):
            return False
        elif hasattr({}, key):
            return False
        elif key in self._special_names:
            return True
        else:
            return self._valid_key_pattern.match(key)

    #--------------------------------
    # Expose standard dict methods
    def items(self):
        return self._odict.items()

    def keys(self):
        return self._odict.keys()

    def values(self):
        return self._odict.values()

    def pop(self, key):
        return self._odict.pop(key)

    #--------------------------------
    # Expose internal dict methods
    def __setattr__(self, key, value):
        """Set an item with dot-style access while testing for invalid names
        """
        if not self._valid_key(key):
            raise AttributeError('Invalid attribute name: {}'.format(key))

        try:
            self[key] = value
        except KeyError as e:
            raise AttributeError(e)

    def __setitem__(self, key, value):
        if not self._valid_key(key):
            raise KeyError('Invalid attribute name: {}'.format(key))

        if isinstance(value, dict) and key not in self._special_names:
            value = OrderedNamespace(value)

        self._odict[key] = value

    def __getattr__(self, key):
        return self._odict[key]

    def __getitem__(self, key):
        return self._odict[key]

    def __delitem__(self, key):
        del self._odict[key]

    def __iter__(self):
        return self._odict.__iter__()

    def __len__(self):
        return self._odict.__len__()

    def __contains__(self, key):
        return self._odict.__contains__(key)

    def __dir__(self):
        """http://ipython.readthedocs.io/en/stable/config/integrating.html#tab-completion
        """
        return self._odict.keys()

    def __eq__(self, other):
        return self._odict.__eq__(other)

    def __repr__(self):
        return dict(self._odict).__repr__()

#         items = ("{}={}".format(k, v) for k, v in self._odict.items())
#         return "{}({})".format(type(self).__name__, ", ".join(items))

    # IPython/Jupyter rich display
    def _ipython_key_completions_(self):
        """http://ipython.readthedocs.io/en/stable/config/integrating.html#tab-completion
        """
        return self.__dir__()

#     _formatter_plain = ip.display_formatter.formatters['text/plain']
#     def _repr_pretty_(self, p, cycle):
#         """http://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html
#         """
#         _plain_repr_pretty = self._formatter_plain.lookup_by_type(dict)

#         _plain_repr_pretty(dict(self), p, cycle)


    def _ipython_display_(self):
        print('dsf')
#         text = json.dumps(self._odict, indent=2)
#         text = repr(self._odict)
#         data = {'text/plain': text}
#         IPython.display.display(ata, raw=True)
        if IPython:
            IPython.display.display(dict(self._odict))
        # IPython.display.display(self._odict)
