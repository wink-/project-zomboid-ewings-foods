"""Build and verify a deterministic install ZIP; never installs anything."""
from pathlib import Path
import argparse, hashlib, io, zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
RUNTIME = ["42/mod.info", "42/media/scripts/ewingsfoods_cheese.txt",
           "42/media/lua/shared/Translate/EN/Recipes.json"]
DOCS = ["README.md", "CHANGELOG.md", "docs/VALIDATION.md", "docs/ACCEPTANCE.md"]
EXPECTED = {"EwingsFoods/" + p for p in RUNTIME + DOCS} | {"EwingsFoods/common/"}


def archive_bytes():
    entries = {"EwingsFoods/" + p: (ROOT / "EwingsFoods" / p).read_bytes() for p in RUNTIME}
    entries.update({"EwingsFoods/" + p: (ROOT / p).read_bytes() for p in DOCS})
    entries["EwingsFoods/common/"] = b""
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED) as z:
        for name, data in sorted(entries.items()):
            entry = zipfile.ZipInfo(name, (2026, 10, 22, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = ((0o40755 if name.endswith("/") else 0o100644) << 16)
            if name.endswith("/"):
                entry.external_attr |= 0x10
            z.writestr(entry, data)
    return out.getvalue()


def verify(path):
    data = path.read_bytes()
    checksum = path.with_suffix(path.suffix + ".sha256").read_text("ascii").strip()
    digest = hashlib.sha256(data).hexdigest()
    assert checksum == f"{digest}  {path.name}", "checksum mismatch"
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == EXPECTED and len(z.namelist()) == len(EXPECTED)
        assert all(i.date_time == (2026, 10, 22, 0, 0, 0) for i in z.infolist())
        assert all(i.compress_type == zipfile.ZIP_STORED for i in z.infolist())
        for p in RUNTIME:
            assert z.read("EwingsFoods/" + p) == (ROOT / "EwingsFoods" / p).read_bytes()
    assert data == archive_bytes(), "release differs from reviewed source"
    print(f"PASS ZIP layout, CRC, byte comparison, timestamp, SHA-256: {digest}")
    return digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        verify(args.verify)
    else:
        first, second = archive_bytes(), archive_bytes()
        assert first == second, "non-deterministic archive"
        target = ROOT / "dist" / f"EwingsFoods-{VERSION}.zip"
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(first)
        target.with_suffix(".zip.sha256").write_bytes(
            (hashlib.sha256(first).hexdigest() + "  " + target.name + "\n").encode("ascii"))
        print("PASS two independent package builds are byte-identical")
        verify(target)
