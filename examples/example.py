import dj_database_url
from twelvefactor import config

globals().update(
    config(
        {
            "DEBUG": {"type": bool, "default": False},
            "SECRET_KEY": str,
            "DATABASES": {
                "key": "DATABASE_URL",
                "default": "sqlite:///",
                "mapper": lambda v: {"default": dj_database_url.parse(v)},
            },
        }
    )
)

print(DEBUG)  # noqa
