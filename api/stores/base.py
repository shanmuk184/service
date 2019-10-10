import datetime

class BaseStoreModel:
    def __init__(self):
        self._data_dict = {}

    class BaseProperties:
        CreatedAt = 'created_at'
        UpdatedAt = 'updated_at'
    _reverseMapping = {}

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
            if not self.BaseProperties.CreatedAt not in _flat_dict:
                _flat_dict[self.BaseProperties.CreatedAt]=datetime.datetime.now()
            if not self.BaseProperties.UpdatedAt not in _flat_dict:
                _flat_dict[self.BaseProperties.UpdatedAt] = datetime.datetime.now()
        return _flat_dict

    def populate_data_dict(self, dictParam=None):
        _flat_dict=dictParam
        if self._reverseMapping:
            for key in _flat_dict:
                reverseMapping = self._reverseMapping.get(key)
                value = dictParam[key]
                if reverseMapping:
                    if len(reverseMapping) == 2:
                        if not isinstance(value, reverseMapping[1]):
                            value = reverseMapping[1](dictParam[key])
                        self.set_value(key, value)
                    elif len(reverseMapping) == 3:
                        valueList = dictParam[key]
                        values = []
                        for value in valueList:
                            holding_container = reverseMapping[2]()
                            holding_container.populate_data_dict(value)
                            values.append(holding_container)
                        self.set_value(key, values)
                    else:
                        self.set_value(key, value)



    def __getattr__(self, item):
        item_key = [key for key in self._reverseMapping if self._reverseMapping[key][0] ==item]
        if item_key:
            return self._data_dict.get(item_key[0])
        # return super().__g(item)


    def __setattr__(self, item, value):
        item_key = [key for key in self._reverseMapping if self._reverseMapping[key][0] == item]
        if item_key:
            self._data_dict[item_key[0]] = value
        super().__setattr__(item, value)

# For future
# class BaseApiModel(object):
#     def __init__(self):
#         self._data_dict = {}
#     def populate_data_dict(self, dictParam):
#         if not dictParam:
#             raise NotImplementedError()
#         missing_fields = list(set(list(self._fields)).difference(set(dictParam.keys())))
#         if missing_fields:
#             raise ValueError(missing_fields)
#         for key in dictParam:
#             self._data_dict[key] = dictParam.get(key)
#


    def get_value(self, key):
        if not key:
            raise NotImplementedError()
        return self._data_dict.get(key)

    def set_value(self, key, value):
        if not key or not value:
            raise NotImplementedError()
        self._data_dict[key] = value


    _fields = ()

