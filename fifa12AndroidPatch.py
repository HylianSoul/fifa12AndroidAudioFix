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
        print(f"Uso: {Path(sys.argv[0]).name} <archivo.apk>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"Error: no existe el archivo: {input_path}")
        sys.exit(1)

    if input_path.suffix.lower() != ".apk":
        print("Error: el archivo indicado no tiene extensión .apk")
        sys.exit(1)

    output_path = input_path.with_name(
        input_path.stem + "_patched" + input_path.suffix
    )

    print(f"APK de entrada: {input_path}")
    print(f"APK de salida:  {output_path}")
    print()

    with zipfile.ZipFile(input_path, "r") as zin:

        if LIB_PATH not in zin.namelist():
            print(f"Error: no se encuentra {LIB_PATH} en el APK.")
            sys.exit(1)

        original_so = zin.read(LIB_PATH)

    print(f"Tamaño de {LIB_PATH}: {len(original_so):,} bytes")

    original_hash = sha256(original_so)

    print(f"SHA-256: {original_hash}")

    if original_hash != EXPECTED_SHA256:
        print()
        print("ERROR: la libFIFA12.so no coincide con la versión esperada.")
        print("No se ha aplicado ningún parche.")
        sys.exit(1)

    print("Versión de libFIFA12.so reconocida correctamente.")

    if original_so[PATCH_OFFSET:PATCH_OFFSET + 4] != ORIGINAL_BYTES:
        print()
        print("ERROR: los bytes en el offset esperado no coinciden.")
        print("No se ha aplicado ningún parche.")
        sys.exit(1)

    patched_so = bytearray(original_so)

    patched_so[PATCH_OFFSET:PATCH_OFFSET + 4] = PATCHED_BYTES

    patched_so = bytes(patched_so)

    print(
        f"Parche aplicado en 0x{PATCH_OFFSET:X}: "
        f"{ORIGINAL_BYTES.hex(' ')} -> {PATCHED_BYTES.hex(' ')}"
    )

    patched_hash = sha256(patched_so)

    print(f"SHA-256 nuevo: {patched_hash}")

    # Crear el APK nuevo.
    with zipfile.ZipFile(input_path, "r") as zin, \
         zipfile.ZipFile(output_path, "w") as zout:

        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == LIB_PATH:
                data = patched_so

            zout.writestr(item, data)

    print()
    print("Parche aplicado correctamente.")
    print(f"APK generado: {output_path}")
    print()
    print("IMPORTANTE: el APK ha sido modificado y su firma original")
    print("ya no es válida. Debes volver a firmarlo antes de instalarlo.")


if __name__ == "__main__":
    main()
