from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def to_bogota_time(dt: datetime) -> datetime:
    """Convierte un datetime a la zona horaria de Bogotá (America/Bogota)"""
    if dt.tzinfo is None:
        # Assuming UTC if naive
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(ZoneInfo("America/Bogota"))

def get_current_bogota_time() -> datetime:
    """Retorna la hora actual en Bogotá"""
    return datetime.now(ZoneInfo("America/Bogota"))
