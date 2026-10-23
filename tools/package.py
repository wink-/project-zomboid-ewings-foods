"""Build and verify a deterministic install ZIP; never installs anything."""
from pathlib import Path
import argparse, hashlib, io, zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"
RUNTIME = ["42/mod.info", "42/media/scripts/ewingsfoods_cheese.txt",
           "42/media/lua/shared/Translate/EN/Recipes.json",
           "42/media/lua/shared/Translate/EN/Tooltip.json", "42/media/lua/shared/EwingsFoodsHeat.lua",
           "42/media/scripts/ewingsfoods_tomatopaste.txt", "42/media/lua/shared/EwingsFoodsTomatoPaste.lua",
           "42/media/scripts/ewingsfoods_nachos.txt", "42/media/lua/shared/EwingsFoodsNachos.lua",
           "42/media/lua/shared/Translate/EN/ItemName.json", "common/media/textures/Item_EwingsFoods_LoadedNachos.png"]
DOCS = ["README.md", "CHANGELOG.md", "docs/VALIDATION.md", "docs/ACCEPTANCE.md", "docs/BASELINE.md", "docs/NACHOS.md", "docs/ART.md"]
EXPECTED = {"EwingsFoods/" + p for p in RUNTIME + DOCS} | {"EwingsFoods/common/"}
TOOLS = ['tools/classfile.py', 'tools/package.py', 'tools/validate.py', 'tools/test_heat.lua',
         'tools/test_heat.py', 'tools/test_tomatopaste.lua', 'tools/test_tomatopaste.py',
         'tools/build_nachos_icon.py', 'tools/test_nachos.py', 'tools/test_nachos.lua', 'tools/native_food_vm.py']
ART = ['art/loaded-nachos-source.png', 'art/loaded-nachos-icon-qa.png']
SOURCE = {f'EwingsFoods-{VERSION}/'+p for p in DOCS+TOOLS+ART+['.gitignore','.gitattributes']}
SOURCE |= {f'EwingsFoods-{VERSION}/EwingsFoods/'+p for p in RUNTIME+['common/']}


def archive_bytes(source=False):
    entries = {"EwingsFoods/" + p: (ROOT / "EwingsFoods" / p).read_bytes() for p in RUNTIME}
    entries.update({"EwingsFoods/" + p: (ROOT / p).read_bytes() for p in DOCS})
    entries["EwingsFoods/common/"] = b""
    if source:
        entries = {f'EwingsFoods-{VERSION}/'+p: (ROOT/p).read_bytes() for p in DOCS+TOOLS+ART+['.gitignore','.gitattributes']}
        entries.update({f'EwingsFoods-{VERSION}/EwingsFoods/'+p: (ROOT/'EwingsFoods'/p).read_bytes() for p in RUNTIME})
        entries[f'EwingsFoods-{VERSION}/EwingsFoods/common/'] = b''
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED) as z:
        for name, data in sorted(entries.items()):
            entry = zipfile.ZipInfo(name, (2026, 10, 23, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = ((0o40755 if name.endswith("/") else 0o100644) << 16)
            if name.endswith("/"):
                entry.external_attr |= 0x10
            z.writestr(entry, data)
    return out.getvalue()


def verify(path, source=False):
    source = source or path.name.endswith('-source.zip')
    data = path.read_bytes()
    checksum = path.with_suffix(path.suffix + ".sha256").read_text("ascii").strip()
    digest = hashlib.sha256(data).hexdigest()
    assert checksum == f"{digest}  {path.name}", "checksum mismatch"
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        expected = SOURCE if source else EXPECTED
        assert set(z.namelist()) == expected and len(z.namelist()) == len(expected)
        assert all(i.date_time == (2026, 10, 23, 0, 0, 0) for i in z.infolist())
        assert all(i.compress_type == zipfile.ZIP_STORED for i in z.infolist())
        for p in RUNTIME:
            prefix = f'EwingsFoods-{VERSION}/EwingsFoods/' if source else 'EwingsFoods/'
            assert z.read(prefix + p) == (ROOT / "EwingsFoods" / p).read_bytes()
    assert data == archive_bytes(source), "release differs from reviewed source"
    print(f"PASS ZIP layout, CRC, byte comparison, timestamp, SHA-256: {digest}")
    return digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        verify(args.verify)
    else:
        for source in (False, True):
            first, second = archive_bytes(source), archive_bytes(source)
            assert first == second, "non-deterministic archive"
            suffix = '-source' if source else '-install'
            target = ROOT / "dist" / f"EwingsFoods-{VERSION}{suffix}.zip"
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(first)
            target.with_suffix(".zip.sha256").write_bytes(
                (hashlib.sha256(first).hexdigest() + "  " + target.name + "\n").encode("ascii"))
            print("PASS two independent package builds are byte-identical")
            verify(target, source)
