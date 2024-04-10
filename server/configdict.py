import json


class ConfigDict:
    def __init__(self, filename):
        self.__dict__["_filename"] = filename
        self.__dict__["_data"] = self._load()

    def _load(self):
        try:
            with open(self._filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save(self):
        with open(self._filename, "w") as f:
            json.dump(self._data, f, indent=4)

    def __getattr__(self, name):
        return self._data.get(name)

    def __setattr__(self, name, value):
        self._data[name] = value
        self._save()

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def __delattr__(self, name):
        if name in self._data:
            del self._data[name]
            self._save()

    def __delitem__(self, key):
        if key in self._data:
            del self._data[key]
            self._save()

    def __repr__(self):
        return repr(self._data)

    def default(self, k, v):
        # set a value if key does not exist
        if self[k] is None:
            self[k] = v


if __name__ == "__main__":
    # DELETEME: test functions
    config = ConfigDict("test_config.json")

    config["this"] = "that"

    try:
        assert config["this"] == "something"
    except AssertionError:
        print("assertion working as intended")

    assert config["this"] == "that"

    config.default("this", "the other")

    assert config["this"] == "that"

    config.default("something", "works")

    assert config["something"] == "works"


# Usage:
# config = ConfigDict("config.json")
# config.db_host = "localhost"  # Sets an attribute and writes to the file
# print(config.db_host)  # Reads the attribute directly from the file
# config["db_port"] = 3306  # Sets an item and writes to the file
# print(config["db_port"])  # Reads the item directly from the file
