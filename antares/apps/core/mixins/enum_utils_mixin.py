class EnumUtilsMixin:
    
    @classmethod
    def to_enum(cls, element):
        """
        Returns the enumeration value based on the element passed or none if nothing match
        
        :param element: the element to convert
        """
        if element is None:
            return element

        for item in cls:
            if str(element).lower() == str(item).lower():
                return item
        return None
    
    @classmethod
    def to_list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def to_dict(cls):
        return dict(cls.__members__)
        
   
        