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
    def as_choices(cls):
        """
        Converts the dict to the format needed for Django choices in templates 
        
        :returns: the list of options with the value as id and the label (which can be translated) as text
        """
        local_list = []
        for item in cls:
            local_dict = {}
            local_dict['id'] = str(item.value)
            local_dict['text'] = str(item.label)
            local_list.append(local_dict)
        return local_list

    @classmethod
    def to_enum(cls, element):
        """
        Returns the enumeration value based on the element passed or none if nothing match
        
        :param element: the element to convert
        """
        if isinstance(element, cls):
            return cls

        for item in cls:
            if element.lower() == item.value.lower():
                return item
        return None
