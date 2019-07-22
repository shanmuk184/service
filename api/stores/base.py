

class BaseStoreModel:
    def __init__(self):
        self._data_dict = {}

    class BaseProperties:
        CreatedAt = 'created_at'
        UpdatedAt = 'updated_at'

    class PropertyNames:
        pass

    class ReverseMapping:
        pass

    @property
    def datadict(self):
        _flat_dict = {}
        for key in self._data_dict:
            value = self._data_dict.get(key)
            if isinstance(value, BaseStoreModel):
                _flat_dict[key] = value.datadict
            elif isinstance(value, list):
                entries = []
                for listItem in value:
                    if isinstance(listItem, BaseStoreModel):
                        entries.append(listItem.datadict)
                    else:
                        entries.append(listItem)
                _flat_dict[key] = entries
            else:
                _flat_dict[key] = value
        return _flat_dict

    def populate_data_dict(self, dictParam=None):
        self._data_dict = dictParam


    def get_value(self, key):
        if not key:
            raise NotImplementedError()
        return self._data_dict.get(key)

    def set_value(self, key, value):
        if not (key and value):
            raise NotImplementedError()
        print(key)
        self._data_dict[key] = value
