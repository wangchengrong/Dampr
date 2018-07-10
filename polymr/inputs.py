import os
from .dataset import MemoryDataset, TextLineDataset

class Chunker(object):
    def chunks(self):
        raise NotImplementedError()

class TextInput(Chunker):
    def __init__(self, path, chunk_size=64*1024**2):
        self.path = path
        self.chunk_size = chunk_size

    def chunks(self):
        file_size = os.stat(self.path).st_size
        offset = 0
        while offset < file_size:
            yield TextLineDataset(self.path, offset, offset + self.chunk_size)
            offset += self.chunk_size

class MemoryInput(Chunker):
    def __init__(self, items, partitions=50):
        self.items = items
        self.partitions = min(len(items), partitions)

    def chunks(self):
        chunk_size = int(len(self.items) // float(self.partitions))
        for start in range(0, len(self.items), chunk_size):
            yield MemoryDataset(self.items[start:start+chunk_size])

class DMChunker(Chunker):
    def __init__(self, data_mapping):
        self.dm = data_mapping

    def chunks(self):
        for vs in self.dm.values():
            for v in vs:
                yield v


