import datetime
import os

import dotenv

dotenv.load_dotenv()

# import sentry_sdk
# from sentry_sdk.integrations.redis import RedisIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPIRE_TIME = 30  # 单位是秒
DEBUG = os.getenv("DEBUG") == "True"
MEDIA_ROOT = "media"
PROJECT_ID = [
    "bb",
]
CACHE = "MEMORY"
# redis配置

# sentry配置
# sentry_sdk.init(
#     dsn=os.getenv("SENTRY_DSN"),
#     environment=os.getenv("ENVIRONMENT", "development"),
#     integrations=[RedisIntegration()],
# )
# logging
# LOGGER = logging.getLogger("example")
# if DEBUG:
#     LOGGER.setLevel(logging.DEBUG)
# else:
#     LOGGER.setLevel(logging.INFO)
# sh = logging.StreamHandler(sys.stdout)
# sh.setLevel(logging.DEBUG)
# sh.setFormatter(
#     logging.Formatter(
#        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )
# )
# LOGGER.addHandler(sh)
