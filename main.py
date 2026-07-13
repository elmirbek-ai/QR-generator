from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

import qrcode
from qrcode.exceptions import DataOverflowError


OUTPUT_DIRECTORY = Path("qr_codes")
INVALID_FILENAME_CHARACTERS = set('<>:"/\\|?*')
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def normalize_filename(filename: str) -> str:
    """Return a safe PNG filename without accepting path components."""
    name = filename.strip().rstrip(". ")
    if name.lower().endswith(".png"):
        name = name[:-4].strip()

    name = name.rstrip(". ")
    if not name:
        raise ValueError("Файлдын атын киргизүү керек.")
    if any(
        ord(character) < 32 or character in INVALID_FILENAME_CHARACTERS
        for character in name
    ):
        raise ValueError("Файлдын атында тыюу салынган белги бар.")
    if name.split(".", maxsplit=1)[0].upper() in WINDOWS_RESERVED_NAMES:
        raise ValueError("Бул файл аты Windows системасында колдонулбайт.")

    output_name = f"{name}.png"
    if len(output_name) > 255:
        raise ValueError("Файлдын аты өтө узун.")
    return output_name


def generate_qr(
    data: str,
    filename: str,
    output_directory: Path = OUTPUT_DIRECTORY,
) -> Path:
    """Generate a PNG QR code and return its path without overwriting files."""
    content = data.strip()
    if not content:
        raise ValueError("QR кодго текст же шилтеме киргизүү керек.")

    output_name = normalize_filename(filename)
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    output_path = output_directory / output_name

    image = qrcode.make(content)
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    with output_path.open("xb") as output_file:
        output_file.write(buffer.getvalue())

    return output_path


def main() -> int:
    try:
        filename = input("Файл атын киргиз: ")
        data = input("Текст же шилтеме киргиз: ")
        output_path = generate_qr(data, filename)
    except (ValueError, OSError, DataOverflowError) as error:
        print(f"Ката: {error}", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nИш токтотулду.", file=sys.stderr)
        return 130

    print(f"QR код сакталды: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
