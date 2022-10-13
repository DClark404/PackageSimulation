class HashMap:

    # Constructor function that initializes a list of buckets based on the instance variable "self.size".
    # instance variable "self.data_count" is included to keep track of the total number of entries stored,
    # and increments during the insert_data function when data is added.
    # Space-time complexity is O(1)
    def __init__(self):
        self.size = 10
        self.map = []
        self.data_count = 0
        for i in range(self.size):
            self.map.append([])

    # Hashing function to store data within the hashmap.
    # Space-time complexity is O(1)
    def _get_hash(self, key):
        hash_value = int(key) % len(self.map)
        return hash_value

    # This is the insertion, update, and chaining function of the hashmap. If appropriate bucket is empty,
    # data is stored there. Otherwise, checks to see if the key already exists. If the key exists then the value is
    # updated, and if not the key-value pair is chained to the bucket.
    # Space-time complexity is O(N)
    def insert_data(self, key, value):
        key_hash = self._get_hash(key)
        key_values = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_values])
            self.data_count = self.data_count + 1
            return True
        else:
            for data in self.map[key_hash]:
                if data[0] == key:
                    data[1] = value
                    return True
            self.map[key_hash].append(key_values)
            self.data_count = self.data_count + 1
            return True

    # The lookup function that returns all data associated with a key, if it exists.
    # Space-time complexity is O(N)
    def lookup_data(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for data in self.map[key_hash]:
                if data[0] == key:
                    return data[1]
        return None

    # This function returns the number of data entries present within the hashmap at any point.
    # Space-time complexity is O(1)
    def return_size(self):
        current_size = int(self.data_count)
        return current_size
