class EnumUtilsMixin:
    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    @classmethod
    def as_dict(cls):
        """
        Converts the Enumeration into a dict
        
        :returns: the newly created dict
        """
        local_dict = {}
        for item in cls:
            local_dict[str(item.value)] = str(item.label)
        return local_dict


    @classmethod
    def to_enum(cls, element):
        """
        Returns the enumeration value based on the element passed or none if nothing match
        
        :param element: the element to convert
        """
        if element is None:
            return element

        if isinstance(element, cls):
            return element

        for item in cls:
            if str(element).lower() == str(item.value).lower():
                return item
        return None
