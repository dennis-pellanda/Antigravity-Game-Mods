import zipfile
import re
import os
import shutil
import struct
import sys

pak_path = r"E:\Giochi\RoadCraft\root\paks\client\default\default_other.pak"
bak_path = r"E:\Giochi\RoadCraft\root\paks\client\default\default_other.pak.bak"
tmp_pak = r"E:\Giochi\RoadCraft\root\paks\client\default\default_other.pak.tmp"

cache_path = r"E:\Giochi\RoadCraft\root\paks\client\default\default_other.pak.cache"
cache_bak_path = r"E:\Giochi\RoadCraft\root\paks\client\default\default_other.pak.cache.bak"
tmp_cache = r"E:\Giochi\RoadCraft\root\paks\client\default\default_other.pak.cache.tmp"

print("=========================================================")
print("Starting RoadCraft v6.0 Comprehensive Custom Modification")
print("=========================================================")

assert os.path.exists(bak_path), "Pristine backup .pak does not exist!"
assert os.path.exists(cache_bak_path), "Pristine backup .pak.cache does not exist!"

quarry_count = 0
truck_torque_count = 0
dump_truck_count = 0
roller_count = 0
paver_count = 0
dozer_flattener_count = 0

with zipfile.ZipFile(bak_path, "r") as in_zip, zipfile.ZipFile(tmp_pak, "w") as out_zip:
    infolist = in_zip.infolist()
    print(f"Total entries in PAK: {len(infolist)}")

    for info in infolist:
        name = info.filename
        raw_bytes = in_zip.read(name)

        # -------------------------------------------------------------
        # 1. VOLUME CARICO BASE (prop_load_volume.prop) - spawnFull = True
        # -------------------------------------------------------------
        if name == "ssl/terraforming/prop_load_volume.prop":
            text = raw_bytes.decode("utf-8", errors="ignore")
            if "spawnFull" in text:
                text = re.sub(r'spawnFull\s*=\s*\w+', 'spawnFull   =   True', text)
            else:
                text = text.replace('__type   =   "prop_base"', 'spawnFull   =   True\n__type   =   "prop_base"')
            raw_bytes = text.encode("utf-8")
            print(" -> Patched prop_load_volume.prop (spawnFull = True)")

        # -------------------------------------------------------------
        # 2. VEICOLI (.cls) - COPPIA 10x, CASSONE INFINITO, LARGHEZZE RULLO/ASFALTO/DOZER
        # -------------------------------------------------------------
        elif name.endswith(".cls") and "trucks" in name:
            text = raw_bytes.decode("utf-8", errors="ignore")
            modified = False

            # A. Camion ribaltabili: volumeChangeMult = 0.0 (sabbia infinita nativa)
            if "prop_load_volume" in text:
                # 1. volumeChangeMult = 0.0
                if "volumeChangeMult" in text:
                    text = re.sub(r'volumeChangeMult\s*=\s*[0-9\.]+', 'volumeChangeMult   =   0.0', text)
                else:
                    text = re.sub(r'(prop_load_volume\s*=\s*\{)', r'\1\n      volumeChangeMult   =   0.0', text)

                # 2. spawnFull = True
                if "spawnFull" in text:
                    text = re.sub(r'spawnFull\s*=\s*\w+', 'spawnFull   =   True', text)
                else:
                    text = re.sub(r'(prop_load_volume\s*=\s*\{)', r'\1\n      spawnFull   =   True', text)

                # 3. fakeSandConsumption = 0.0
                if "fakeSandConsumption" in text:
                    text = re.sub(r'fakeSandConsumption\s*=\s*[0-9\.]+', 'fakeSandConsumption   =   0.0', text)
                elif "prop_load_volume_controller" in text:
                    text = re.sub(r'(prop_load_volume_controller\s*=\s*\{)', r'\1\n      fakeSandConsumption   =   0.0', text)

                modified = True
                dump_truck_count += 1

            # B. Coppia Motore 10x (Torque x10)
            def mul_torque(m):
                val = int(m.group(2))
                return f"{m.group(1)}{val * 10}"

            new_text, n_subs = re.subn(r'(\bengine\s*=\s*\{.*?torque\s*=\s*)(\d+)', mul_torque, text, count=1, flags=re.DOTALL)
            if n_subs > 0:
                text = new_text
                modified = True
                truck_torque_count += 1

            # C. Rulli compattatori (Asphalt Roller Working Width)
            # Arling 750R -> 15.3
            if "arling_750r_roller" in name:
                text = re.sub(r'(prop_truck_asphalt_roller.*?size\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>15.3', text, flags=re.DOTALL)
                text = re.sub(r'(rollUpForwardSize\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>15.3', text)
                text = re.sub(r'(rollUpRearSize\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>15.3', text)
                modified = True
                roller_count += 1
            # DS-55 Katok -> 10.0
            elif "ds_55katok_roller" in name:
                text = re.sub(r'(prop_truck_asphalt_roller.*?size\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>10.0', text, flags=re.DOTALL)
                text = re.sub(r'(rollUpForwardSize\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>10.0', text)
                text = re.sub(r'(rollUpRearSize\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>10.0', text)
                modified = True
                roller_count += 1

            # D. Asfaltatrici (Asphalter Working Width & Height)
            # Arling 120 Special -> 10.6, height 0.065
            if "arling_120special_paver" in name:
                text = re.sub(r'(prop_truck_asphalter.*?size\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>10.6', text, flags=re.DOTALL)
                text = re.sub(r'asphaltHeight\s*=\s*[0-9\.]+', 'asphaltHeight   =   0.065', text)
                modified = True
                paver_count += 1
            # DS-135 Bunker Paver -> 10.4, height 0.065
            elif "ds_135bunker_paver" in name:
                text = re.sub(r'(prop_truck_asphalter.*?size\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>10.4', text, flags=re.DOTALL)
                text = re.sub(r'asphaltHeight\s*=\s*[0-9\.]+', 'asphaltHeight   =   0.065', text)
                modified = True
                paver_count += 1

            # E. Dozer / Wheel Loader (Spianamento sabbia - Flattener Width) -> 12.0
            if any(k in name for k in ["kronenwerk_l34_dozer", "kronenwerk_l34_cargo_dozer", "vostok_atm53pioneer_dozer", "greenway_ht500_dozer"]):
                if "prop_truck_flattener" in text:
                    text = re.sub(r'(prop_truck_flattener.*?size\s*=\s*\{\s*x\s*=\s*)[0-9\.]+', r'\g<1>12.0', text, flags=re.DOTALL)
                    modified = True
                    dozer_flattener_count += 1

            if modified:
                raw_bytes = text.encode("utf-8")

        out_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        out_info.compress_type = info.compress_type
        out_info.comment = info.comment
        out_info.extra = b""
        out_zip.writestr(out_info, raw_bytes)

print("\n--- Summary of Applied Changes ---")
print(f"  Dump trucks patched with volumeChangeMult=0.0: {dump_truck_count}")
print(f"  Vehicles patched with 10x Torque: {truck_torque_count}")
print(f"  Rollers widened (Arling 750R: 15.3m, DS-55: 10m): {roller_count}")
print(f"  Pavers widened (Arling 120: 10.6m, DS-135: 10.4m): {paver_count}")
print(f"  Dozers / Loaders flattener widened (12.0m): {dozer_flattener_count}")

assert dump_truck_count > 0, "No dump trucks were patched!"
assert truck_torque_count > 0, "No trucks received 10x torque!"
assert roller_count > 0, "No rollers were patched!"
assert paver_count > 0, "No pavers were patched!"
assert dozer_flattener_count > 0, "No dozers were patched!"

# Rebuild binary .pak.cache table
print("\nRebuilding synchronized default_other.pak.cache table...")
cache_bytes = bytearray()
with zipfile.ZipFile(tmp_pak, "r") as check_zip:
    for info in check_zip.infolist():
        bname = info.filename.encode("utf-8")
        cache_bytes += struct.pack("<IBI", 6, 0x3f, len(bname))
        cache_bytes += bname
        data_off = info.header_offset + 30 + len(bname)
        cache_bytes += struct.pack("<QQQHI", data_off, info.file_size, info.compress_size, info.compress_type, info.CRC)

with open(tmp_cache, "wb") as f:
    f.write(cache_bytes)
print(f"Generated binary cache: {len(cache_bytes)} bytes.")

# Verification step
print("Verifying patched assets inside new PAK...")
with zipfile.ZipFile(tmp_pak, "r") as test_zip:
    # Check dump truck
    b_cls = test_zip.read("ssl/autogen_designer_wizard/trucks/auto_aramatsu_bowhead_heavy_dumptruck_new/auto_aramatsu_bowhead_heavy_dumptruck_new.cls").decode("utf-8")
    assert "volumeChangeMult   =   0.0" in b_cls
    assert "spawnFull   =   True" in b_cls

    # Check roller
    r_cls = test_zip.read("ssl/autogen_designer_wizard/trucks/auto_arling_750r_roller_new/auto_arling_750r_roller_new.cls").decode("utf-8")
    assert "15.3" in r_cls

    # Check paver
    p_cls = test_zip.read("ssl/autogen_designer_wizard/trucks/auto_arling_120special_paver_new/auto_arling_120special_paver_new.cls").decode("utf-8")
    assert "10.6" in p_cls
    assert "0.065" in p_cls

    # Check dozer
    d_cls = test_zip.read("ssl/autogen_designer_wizard/trucks/auto_kronenwerk_l34_dozer_res/auto_kronenwerk_l34_dozer_res.cls").decode("utf-8")
    assert "12.0" in d_cls

print("All verifications PASSED cleanly!")

# Atomic file replacement
print("Replacing game files...")
os.replace(tmp_pak, pak_path)
os.replace(tmp_cache, cache_path)
print("SUCCESS: RoadCraft v6.0 fully modified and ready to play!")
