import re


class StringUtils(object):
    """
        A series of methods to help on the management of strings.
    """

    @staticmethod
    def camel_to_snake(s):
        """
        Used to convert the string in camelCase to snake case
        https://gist.github.com/jaytaylor/3660565

        :param s: String to convert.
        """
        _underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
        _underscorer2 = re.compile('([a-z0-9])([A-Z])')

        subbed = _underscorer1.sub(r'\1_\2', s)
        return _underscorer2.sub(r'\1_\2', subbed).lower()

    @staticmethod
    def choice_adapter(enumtype):
        """
        provides an adapter to use enums (as included in Python 3.4) as field choices.

        :param enumType: the enum to adapt.
        """
        return ((item.value, item.name.replace('_', ' ')) for item in enumtype)
