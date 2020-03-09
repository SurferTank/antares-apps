class EnumUtilsMixin:
    
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
            if str(element).lower() == str(item).lower():
                return item
        return None
