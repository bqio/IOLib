from enum import Enum
import struct
import json

class Endian(Enum):
    Little = 0
    Big = 1


class Reader:
    def __init__(self, f, endian: Endian = Endian.Little):
        self.f = f
        if endian == Endian.Little:
            self.e = "<"
        else:
            self.e = ">"
    def read(self, count: int):
        return self.f.read(count)
    def read_8(self):
        buf = self.read(1)
        return struct.unpack(self.e + "b", buf)[0]
    def read_16(self):
        buf = self.read(2)
        return struct.unpack(self.e + "h", buf)[0]
    def read_32(self):
        buf = self.read(4)
        return struct.unpack(self.e + "i", buf)[0]
    def read_64(self):
        buf = self.read(8)
        return struct.unpack(self.e + "q", buf)[0]
    def read_u8(self):
        buf = self.read(1)
        return struct.unpack(self.e + "B", buf)[0]
    def read_u16(self):
        buf = self.f.read(2)
        return struct.unpack(self.e + "H", buf)[0]
    def read_u32(self):
        buf = self.read(4)
        return struct.unpack(self.e + "I", buf)[0]
    def read_u64(self):
        buf = self.read(8)
        return struct.unpack(self.e + "Q", buf)[0]
    def read_nt_utf8_str(self, sb = 0):
        len = 0
        pos = self.tell()
        while self.read_8() != sb:
            len += 1
        self.seek(pos)
        line = self.read(len).decode('utf-8')
        self.skip(1)
        return line
    def seek(self, offset: int):
        self.f.seek(offset)
    def tell(self):
        return self.f.tell()
    def skip(self, count: int):
        self.seek(self.tell() + count)

def dump_json(name, data, indent: int = 0):
    with open(name, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=indent)
        json_file.close()