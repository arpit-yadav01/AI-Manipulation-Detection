from PIL import Image
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import IFDRational


def _safe_value(value):
    """
    Convert EXIF values into Mongo-safe types
    """
    if isinstance(value, IFDRational):
        return float(value)
    if isinstance(value, bytes):
        return value.decode(errors="ignore")
    if isinstance(value, (int, float, str)):
        return value
    if isinstance(value, tuple):
        return [_safe_value(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _safe_value(v) for k, v in value.items()}
    return str(value)


def extract_exif(path: str) -> dict:
    try:
        image = Image.open(path)
        raw_exif = image._getexif() or {}

        exif = {}
        for tag_id, value in raw_exif.items():
            tag_name = TAGS.get(tag_id, f"UNKNOWN_{tag_id}")
            exif[str(tag_name)] = _safe_value(value)  # ✅ FORCE STRING KEY

        return exif

    except Exception:
        return {}
