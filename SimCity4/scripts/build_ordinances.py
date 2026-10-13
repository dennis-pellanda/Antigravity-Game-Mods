import struct, os

def qfs_decompress(raw):
    pos = 4 if len(raw) >= 9 and raw[4:6] in (b'\x10\xfb', b'\x11\xfb') else 0
    pos += 2
    b_flags = raw[pos-2]
    if b_flags & 0x01:
        uncompressed_len = struct.unpack('>I', raw[pos:pos+4])[0]
        pos += 4
    else:
        uncompressed_len = (raw[pos] << 16) | (raw[pos+1] << 8) | raw[pos+2]
        pos += 3
    out = bytearray()
    while pos < len(raw) and len(out) < uncompressed_len:
        b0 = raw[pos]; pos += 1
        if b0 < 0x80:
            if pos >= len(raw): break
            b1 = raw[pos]; pos += 1
            n = b0 & 3
            if n: out.extend(raw[pos:pos+n]); pos += n
            off = ((b0 & 0x60) << 3) + b1 + 1; cnt = ((b0 & 0x1C) >> 2) + 3
            for _ in range(cnt): out.append(out[-off])
        elif b0 < 0xC0:
            if pos + 1 >= len(raw): break
            b1, b2 = raw[pos], raw[pos+1]; pos += 2
            n = (b1 >> 6) & 3
            if n: out.extend(raw[pos:pos+n]); pos += n
            off = ((b1 & 0x3F) << 8) + b2 + 1; cnt = (b0 & 0x3F) + 4
            for _ in range(cnt): out.append(out[-off])
        elif b0 < 0xE0:
            if pos + 2 >= len(raw): break
            b1, b2, b3 = raw[pos], raw[pos+1], raw[pos+2]; pos += 3
            n = b0 & 3
            if n: out.extend(raw[pos:pos+n]); pos += n
            off = ((b0 & 0x10) << 12) + (b1 << 8) + b2 + 1; cnt = (((b0 & 0x0C) << 6) | b3) + 5
            for _ in range(cnt): out.append(out[-off])
        elif b0 <= 0xFB:
            n = ((b0 - 0xDF) << 2); out.extend(raw[pos:pos+n]); pos += n
        else:
            n = b0 & 3
            if n: out.extend(raw[pos:pos+n]); pos += n
            break
    return bytes(out)

def make_ltext(text: str) -> bytes:
    u16 = text.encode('utf-16le')
    char_count = len(text)
    return struct.pack('<HH', char_count, 0x1000) + u16

def parse_exemplar_props(dec):
    pos = 20
    prop_count, = struct.unpack('<I', dec[pos:pos+4]); pos += 4
    props = []
    for _ in range(prop_count):
        pid, dt, kt, fl = struct.unpack('<IHHB', dec[pos:pos+9]); pos += 9
        is_arr = bool(kt & 0x80)
        if is_arr:
            cnt, = struct.unpack('<I', dec[pos:pos+4]); pos += 4
            elem_sz = 1 if dt in (0x0C00, 0x0100, 0x0B00) else 2 if dt == 0x0200 else 8 if dt == 0x0800 else 4
            data = dec[pos:pos+cnt*elem_sz]; pos += cnt*elem_sz
            props.append({'id': pid, 'type': dt, 'key_type': kt, 'flag': fl, 'is_arr': True, 'count': cnt, 'raw_data': data})
        else:
            sz = 1 if dt in (0x0100, 0x0B00) else 2 if dt == 0x0200 else 8 if dt == 0x0800 else 4
            data = dec[pos:pos+sz]; pos += sz
            props.append({'id': pid, 'type': dt, 'key_type': kt, 'flag': fl, 'is_arr': False, 'raw_data': data})
    return props

def serialize_exemplar(header_24, props):
    out = bytearray(header_24[:20])
    out.extend(struct.pack('<I', len(props)))
    for p in props:
        out.extend(struct.pack('<IHHB', p['id'], p['type'], p['key_type'], p['flag']))
        if p['is_arr']:
            out.extend(struct.pack('<I', p['count']))
        out.extend(p['raw_data'])
    return bytes(out)

def build_dbpf(entries_dict):
    header = bytearray(96)
    header[:4] = b'DBPF'
    struct.pack_into('<II', header, 4, 1, 0)
    struct.pack_into('<I', header, 32, 7)
    body = bytearray()
    idx_records = []
    current_offset = 96
    for (t, g, i), data in entries_dict.items():
        body.extend(data)
        idx_records.append((t, g, i, current_offset, len(data)))
        current_offset += len(data)
    index_offset = current_offset
    index_size = len(idx_records) * 20
    struct.pack_into('<III', header, 36, len(idx_records), index_offset, index_size)
    struct.pack_into('<I', header, 60, 1)
    index_bytes = bytearray()
    for rec in idx_records:
        index_bytes.extend(struct.pack('<IIIII', *rec))
    return bytes(header) + bytes(body) + bytes(index_bytes)

def set_scalar_sint32(props, prop_id, val):
    for p in props:
        if p['id'] == prop_id:
            p['raw_data'] = struct.pack('<i', val)
            return
    props.append({'id': prop_id, 'type': 0x0700, 'key_type': 0, 'flag': 0, 'is_arr': False, 'raw_data': struct.pack('<i', val)})

def set_scalar_uint32(props, prop_id, val):
    for p in props:
        if p['id'] == prop_id:
            p['raw_data'] = struct.pack('<I', val)
            return
    props.append({'id': prop_id, 'type': 0x0300, 'key_type': 0, 'flag': 0, 'is_arr': False, 'raw_data': struct.pack('<I', val)})

def set_scalar_float32(props, prop_id, val):
    for p in props:
        if p['id'] == prop_id:
            p['raw_data'] = struct.pack('<f', float(val))
            return
    props.append({'id': prop_id, 'type': 0x0900, 'key_type': 0, 'flag': 0, 'is_arr': False, 'raw_data': struct.pack('<f', float(val))})\n