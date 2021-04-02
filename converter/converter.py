from mappings import PYTHON_TO_MONGO, MONGO_TO_PYTHON


class Converter:
    supported_targets = ('python', 'mongo')

    def __init__(self):
        pass

    @classmethod
    def change_type(cls, input_value, value_type, target):
        """
        # TODO: uzupełnić docs
        Parameters
        ----------
        input_value
        value_type
        target

        Returns
        -------

        """

        if target not in cls.supported_targets:
            raise NotImplemented("Target {} not implemented.".format(target))

        if target == 'python':
            mapping = MONGO_TO_PYTHON
        else:
            mapping = PYTHON_TO_MONGO
        return cls.__get_mapped_value(input_value, value_type, mapping)

    @classmethod
    def __get_mapped_value(cls, input_value, value_type, mapping):
        mapping_instructions = mapping.get(value_type)
        if not mapping_instructions:
            raise NotImplemented('No mapping for {}'.format(value_type))
        if mapping_instructions['string_first']:
            str_value = str(input_value)
        return mapping_instructions['map_to'](str_value)
