import zipfile
import re
import os
import shutil
import struct
import sys

pak_path = r"E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak"
bak_path = r"E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.bak"
tmp_pak = r"E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.tmp"

cache_path = r"E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.cache"
cache_bak_path = r"E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.cache.bak"
tmp_cache = r"E:\Giochi\RoadCraft (2025)\RoadCraft\root\paks\client\default\default_other.pak.cache.tmp"

print("Starting comprehensive RoadCraft patch from pristine backup...")
assert os.path.exists(bak_path), "Backup pak does not exist!"
assert os.path.exists(cache_bak_path), "Backup cache does not exist!"

quarry_count = 0
truck_count = 0
prop_quarry_patched = False
prop_controller_patched = False
smart_truck_storage_patched = False

with zipfile.ZipFile(bak_path, "r") as in_zip, zipfile.ZipFile(tmp_pak, "w") as out_zip:
    infolist = in_zip.infolist()
    print(f"Total entries: {len(infolist)}")

    for info in infolist:
        name = info.filename
        raw_bytes = in_zip.read(name)

        # 1. Quarry building files (21 files)
        if "quarry" in name and name.endswith(".cls"):
            text = raw_bytes.decode("utf-8")
            new_text = re.sub(
                r'(SandStorage\s*=\s*\{.*?UsableCheckerDistance\s*=\s*\{\s*distance\s*=\s*)\d+',
                r'\g<1>999999',
                text,
                flags=re.DOTALL
            )
            new_text = re.sub(
                r'(fuelCoinsForActivate\s*=\s*)\d+',
                r'\g<1>0',
                new_text
            )
            if new_text != text:
                raw_bytes = new_text.encode("utf-8")
                quarry_count += 1

        # 2. prop_sand_quarry.prop (the core quarry parameter definitions)
        elif name == "ssl/game/buildings/sand/prop_sand_quarry.prop":
            text = raw_bytes.decode("utf-8")
            text = re.sub(r'sandDistance\s*=\s*\d+', 'sandDistance   =   999999', text)
            text = re.sub(r'maxSand\s*=\s*\d+', 'maxSand   =   99999', text)
            text = re.sub(r'sandReceivingDistance\s*=\s*\d+', 'sandReceivingDistance   =   999999', text)
            text = re.sub(r'isOBBCheck\s*=\s*True', 'isOBBCheck   =   False', text)
            raw_bytes = text.encode("utf-8")
            prop_quarry_patched = True
            print("Patched prop_sand_quarry.prop successfully.")

        # 3. Base load volume controller property definition
        elif name == "ssl/game/truck/prop_load_volume_controller.prop":
            text = raw_bytes.decode("utf-8")
            text = re.sub(r'refillSpeed\s*=\s*[0-9\.]+', 'refillSpeed   =   5.0', text)
            if "sandDistance" in text:
                text = re.sub(r'sandDistance\s*=\s*\d+', 'sandDistance   =   999999', text)
            else:
                text = text.replace('__type   =   "prop_base"', 'sandDistance   =   999999\n__type   =   "prop_base"')
            raw_bytes = text.encode("utf-8")
            prop_controller_patched = True
            print("Patched prop_load_volume_controller.prop successfully.")

        # 4. Smart entry point for truck sand storage (allow self-refill / remove ignore-self)
        elif name == "ssl/game/truck/heavy_dump/smart_entry_point_truck_sand_storage.sso":
            text = raw_bytes.decode("utf-8")
            text = re.sub(r'UsableCheckerIgnoreSelf\s*=\s*\{\s*\}', '', text)
            raw_bytes = text.encode("utf-8")
            smart_truck_storage_patched = True
            print("Patched smart_entry_point_truck_sand_storage.sso successfully.")

        # 5. Dumptruck vehicles .cls files
        elif name.endswith(".cls") and "trucks" in name:
            text = raw_bytes.decode("utf-8")
            modified = False
            if "prop_load_volume_controller" in text:
                if "sandDistance" in text:
                    text = re.sub(r'sandDistance\s*=\s*\d+', 'sandDistance   =   999999', text)
                    modified = True
                if "refillSpeed" in text:
                    text = re.sub(r'refillSpeed\s*=\s*[0-9\.]+', 'refillSpeed   =   5.0', text)
                    modified = True
                else:
                    text = text.replace('prop_load_volume_controller   =   {', 'prop_load_volume_controller   =   {\n      refillSpeed   =   5.0')
                    modified = True
                if "focusDistance" in text:
                    text = re.sub(r'focusDistance\s*=\s*\d+', 'focusDistance   =   999999', text)
                    modified = True
                if modified:
                    raw_bytes = text.encode("utf-8")
                    truck_count += 1

        out_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        out_info.compress_type = info.compress_type
        out_info.comment = info.comment
        out_info.extra = b""
        out_zip.writestr(out_info, raw_bytes)

print(f"Summary of patches:")
print(f"  Quarry .cls files: {quarry_count}/21")
print(f"  Truck .cls files: {truck_count}/14")
print(f"  prop_sand_quarry.prop: {prop_quarry_patched}")
print(f"  prop_load_volume_controller.prop: {prop_controller_patched}")
print(f"  smart_entry_point_truck_sand_storage.sso: {smart_truck_storage_patched}")

assert quarry_count == 21, f"Expected 21 quarry files, got {quarry_count}"
assert truck_count >= 14, f"Expected at least 14 truck files, got {truck_count}"
assert prop_quarry_patched, "prop_sand_quarry.prop was not patched"
assert prop_controller_patched, "prop_load_volume_controller.prop was not patched"
assert smart_truck_storage_patched, "smart_entry_point_truck_sand_storage.sso was not patched"

# Generate synchronized default_other.pak.cache
print("Generating synchronized default_other.pak.cache...")
cache_bytes = bytearray()

with zipfile.ZipFile(tmp_pak, "r") as test_zip:
    infolist = test_zip.infolist()
    for info in infolist:
        bname = info.filename.encode("utf-8")
        cache_bytes += struct.pack("<IBI", 6, 0x3f, len(bname))
        cache_bytes += bname
        data_off = info.header_offset + 30 + len(bname)
        cache_bytes += struct.pack("<QQQHI", data_off, info.file_size, info.compress_size, info.compress_type, info.CRC)

with open(tmp_cache, "wb") as f:
    f.write(cache_bytes)

print(f"Generated cache size: {len(cache_bytes)} bytes.")

# Verification
print("Verifying patched contents...")
with zipfile.ZipFile(tmp_pak, "r") as test_zip:
    q_prop = test_zip.read("ssl/game/buildings/sand/prop_sand_quarry.prop").decode("utf-8")
    assert "sandDistance   =   999999" in q_prop
    assert "maxSand   =   99999" in q_prop
    assert "sandReceivingDistance   =   999999" in q_prop
    assert "isOBBCheck   =   False" in q_prop

    t_cls = test_zip.read("ssl/autogen_designer_wizard/trucks/auto_aramatsu_bowhead_heavy_dumptruck_new/auto_aramatsu_bowhead_heavy_dumptruck_new.cls").decode("utf-8")
    assert "sandDistance   =   999999" in t_cls
    assert "refillSpeed   =   5.0" in t_cls

    sso_t = test_zip.read("ssl/game/truck/heavy_dump/smart_entry_point_truck_sand_storage.sso").decode("utf-8")
    assert "UsableCheckerIgnoreSelf" not in sso_t

print("All verifications passed! Swapping files...")
os.replace(tmp_pak, pak_path)
os.replace(tmp_cache, cache_path)
print("SUCCESS: Full synchronized patch applied successfully!")
