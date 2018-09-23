import os

from hypothesis import settings

settings.register_profile("slow", settings(max_examples=200))
settings.register_profile("fast", settings(max_examples=20))
settings.load_profile(os.getenv(u"HYPOTHESIS_PROFILE", "fast"))
