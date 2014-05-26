from mft_attribute import *
from mft_entry_header import *
from rawdisk.util.rawstruct import RawStruct

MFT_ENTRY_SIZE = 1024
MFT_ENTRY_HEADER_SIZE = 48

# NTFS System files
MFT_ENTRY_MFT = 0x0
MFT_ENTRY_MFTMIRROR = 0x1
MFT_ENTRY_LOGFILE = 0x2
MFT_ENTRY_VOLUME = 0x3
MFT_ENTRY_ATTRDEF = 0x4
MFT_ENTRY_ROOT = 0x5
MFT_ENTRY_BITMAP = 0x6
MFT_ENTRY_BOOT = 0x7
MFT_ENTRY_BADCLUS = 0x8
MFT_ENTRY_SECURE = 0x9
MFT_ENTRY_UPCASE = 0xA
MFT_ENTRY_EXTEND = 0xB


class MftEntry(RawStruct):
    def __init__(self, offset, data):
        RawStruct.__init__(self, data)
        self.offset = offset
        self.attributes = []

        # TODO: mft entry header size might be different, doublecheck
        # read http://ftp.kolibrios.org/users/Asper/docs/NTFS/ntfsdoc.html#concept_attribute_header
        header_data = self.get_chunk(0, MFT_ENTRY_HEADER_SIZE)
        self.header = MftEntryHeader(header_data)

        # attr_offset = self.header.first_attr_offset
        # attr = self.get_attribute(attr_offset)
        # print "Attr Length: %d" % attr.header.length
        # attr.hexdump()
        self.load_attributes()

    @property
    def end_offset(self):
        return self.offset + self.header.allocated_size

    @property
    def used_size(self):
        return self.header.used_size

    @property
    def size(self):
        return self.header.allocated_size

    def load_attributes(self):
        free_space = MFT_ENTRY_SIZE - MFT_ENTRY_HEADER_SIZE
        offset = self.header.first_attr_offset

        while free_space > 0:
            attr = self.get_attribute(offset)

            if (attr is not None):
                self.attributes.append(attr)
                free_space = free_space - attr.header.length
                offset = offset + attr.header.length
            else:
                break

    def get_attribute(self, offset):
        attr_type = self.get_uint(offset)
        # Attribute length is in header @ offset 0x4
        length = self.get_uint(offset + 0x04)
        data = self.get_chunk(offset, length)

        if attr_type == MFT_ATTR_STANDARD_INFORMATION:
            return MftAttrStandardInformation(data)
        elif attr_type == MFT_ATTR_ATTRIBUTE_LIST:
            return MftAttrAttributeList(data)
        elif attr_type == MFT_ATTR_FILENAME:
            return MftAttrFilename(data)
        elif attr_type == MFT_ATTR_OBJECT_ID:
            return MftAttrObjectId(data)
        elif attr_type == MFT_ATTR_SECURITY_DESCRIPTOR:
            return MftAttrSecurityDescriptor(data)
        elif attr_type == MFT_ATTR_VOLUME_NAME:
            return MftAttrVolumeName(data)
        elif attr_type == MFT_ATTR_VOLUME_INFO:
            return MftAttrVolumeInfo(data)
        elif attr_type == MFT_ATTR_DATA:
            return MftAttrData(data)
        elif attr_type == MFT_ATTR_INDEX_ROOT:
            return MftAttrIndexRoot(data)
        elif attr_type == MFT_ATTR_INDEX_ALLOCATION:
            return MftAttrIndexAllocation(data)
        elif attr_type == MFT_ATTR_BITMAP:
            return MftAttrBitmap(data)
        elif attr_type == MFT_ATTR_REPARSE_POINT:
            return MftAttrReparsePoint(data)
        elif attr_type == MFT_ATTR_LOGGED_TOOLSTREAM:
            return MftAttrLoggedToolstream(data)
        else:
            return None

    def __str__(self):
        return "MFT Record no: %d, " \
            "Offset: 0x%x, " \
            "Size: %d, " \
            "Used Size: %d, " \
            "Signature: %s" % (
                self.header.mft_record_number,
                self.offset,
                self.size,
                self.used_size,
                self.header.file_signature
            )