import json
import os

os_env = os.environ

SQLALCHEMY_DATABASE_URI = os_env.get("SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.path.abspath('database/video_library.db')}")
SCHEDULER_INTERVAL = os_env.get("SCHEDULER_INTERVAL", int(2))
YOUTUBE_KEYS = json.loads(os_env.get("YOUTUBE_KEYS", []))
