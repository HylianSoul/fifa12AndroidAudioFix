#!/usr/bin/env python3

import hashlib
import sys
import zipfile
from pathlib import Path


LIB_PATH = "lib/armeabi/libFIFA12.so"

EXPECTED_SHA256 = (
    "e37b4dd96a117ba3d745c9ba3dabfc5fd51d6a21436c5473ee4db82d65ea98c9"
)

PATCH_OFFSET = 0x65992C

ORIGINAL_BYTES = bytes.fromhex("01 30 A0 13")
PATCHED_BYTES = bytes.fromhex("00 30 A0 13")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <file.apk>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"ERROR: {input_path} not exists!")
        sys.exit(1)

    if input_path.suffix.lower() != ".apk":
        print("ERROR: the file has not the .apk extension.")
        sys.exit(1)

    output_path = input_path.with_name(
        input_path.stem + "_patched" + input_path.suffix
    )

    # Check is the libFIFA12.so library is the expected.
    with zipfile.ZipFile(input_path, "r") as zin:

        if LIB_PATH not in zin.namelist():
            print(f"ERROR: {LIB_PATH} not found inside the APK.")
            sys.exit(1)

        original_so = zin.read(LIB_PATH)

    original_hash = sha256(original_so)

    print(f"SHA-256: {original_hash}")

    if original_hash != EXPECTED_SHA256:
        print()
        print("ERROR: libFIFA12.so has not the expected SHA-256 checksum.")
        print("Any patch is applied.")
        sys.exit(1)

    print("The libFIFA12.so version is correct. Applying the patch...")

    # Patch the libFIFA12.so file.
    if original_so[PATCH_OFFSET:PATCH_OFFSET + 4] != ORIGINAL_BYTES:
        print()
        print("ERROR: the bytes to modify are not the expected.")
        print("Any patch is applied.")
        sys.exit(1)

    patched_so = bytearray(original_so)

    patched_so[PATCH_OFFSET:PATCH_OFFSET + 4] = PATCHED_BYTES

    patched_so = bytes(patched_so)

    print(
        f"Patch applied in 0x{PATCH_OFFSET:X}: "
        f"{ORIGINAL_BYTES.hex(' ')} -> {PATCHED_BYTES.hex(' ')}"
    )

    patched_hash = sha256(patched_so)
    print(f"New libFIFA12.so SHA-256 checksum: {patched_hash}")


    # Creating the new APK.
    with zipfile.ZipFile(input_path, "r") as zin, \
         zipfile.ZipFile(output_path, "w") as zout:

        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == LIB_PATH:
                data = patched_so

            zout.writestr(item, data)

    print()
    print("Patch successfully applied.")
    print(f"New APK: {output_path}")
    print()
    #print("IMPORTANTE: el APK ha sido modificado y su firma original")
    #print("ya no es válida. Debes volver a firmarlo antes de instalarlo.")


if __name__ == "__main__":
    main()
