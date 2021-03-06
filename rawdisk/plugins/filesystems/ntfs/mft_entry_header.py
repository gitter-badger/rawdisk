# -*- coding: utf-8 -*-


from rawdisk.util.rawstruct import RawStruct


class MftEntryHeader(RawStruct):
    """Represents MFT entry header.

    Attributes:
        file_signature (string): Entry signature (4 bytes) \
        (eg. 'FILE' or 'BAAD').
        update_seq_array_offset (ushort): The offset to the update sequence \
        array, from the start of this structure. The update sequence array \
        must end before the last USHORT value in the first sector.
        update_seq_array_size (ushort): The size of the update sequence \
        array, in bytes.
        logfile_seq_number (ulonglong): ?? (reserved in Microsoft website)
        seq_number (ushort): The sequence number. This value is incremented \
        each time that a file record segment is freed; \
        it is 0 if the segment is not used.
        hard_link_count (ushort): ?? (reserved in Microsoft website)
        first_attr_offset (ushort): The offset of the first attribute \
        record, in bytes.
        flags (ushort): The file flags (FILE_RECORD_SEGMENT_IN_USE (0x0001), \
            FILE_FILE_NAME_INDEX_PRESENT (0x0002)).
        base_file_record (ulonglong): A file reference to the base file \
        record segment for this file. \
        If this is the base file record, the value is 0.

    See Also:
        http://msdn.microsoft.com/en-us/library/bb470124(v=vs.85).aspx
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.file_signature = self.get_string(0, 4)
        self.update_seq_array_offset = self.get_ushort_le(4)
        self.update_seq_array_size = self.get_ushort_le(6)
        self.logfile_seq_number = self.get_ulonglong_le(8)
        self.seq_number = self.get_ushort_le(16)
        self.hard_link_count = self.get_ushort_le(18)
        self.first_attr_offset = self.get_ushort_le(20)
        self.flags = self.get_ushort_le(22)
        self.used_size = self.get_uint_le(24)
        self.allocated_size = self.get_ushort_le(28)
        self.base_file_record = self.get_ulonglong_le(30)
        self.next_attr_id = self.get_ushort_le(38)
        self.mft_record_number = self.get_uint_le(42)
