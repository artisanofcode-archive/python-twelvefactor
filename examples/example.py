import dj_database_url
import twelvefactor

SCHEMA: twelvefactor.Schema = {
    "DEBUG": {"type": bool, "default": False},
    "SECRET_KEY": str,
    "DATABASES": {
        "key": "DATABASE_URL",
        "default": "sqlite:///",
        "mapper": lambda v: {"default": dj_database_url.parse(v)},
    },
}

CONFIG = twelvefactor.config(SCHEMA)

print(CONFIG["DEBUG"])
