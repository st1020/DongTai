"""
Django settings for dongtai_conf project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import random
import sys
from ast import literal_eval
from configparser import ConfigParser
from urllib.parse import urljoin

import pymysql
from django.utils.translation import gettext_lazy as _

from dongtai_conf.utils import get_config

pymysql.install_as_MySQLdb()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

get_config(BASE_DIR, os.getenv("TARGET_SECRETSMANAGER", ""))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
# or os.getenv('environment', None) in ('TEST',)
DEBUG = os.environ.get("debug", "false") == "true"

# READ CONFIG FILE
config = ConfigParser()
status = config.read(os.path.join(BASE_DIR, "dongtai_conf/conf/config.ini"))
if len(status) == 0:
    print("config file not exist. stop running")
    sys.exit(0)


def ranstr(num):
    H = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()`-{}|:?><>?"
    salt = ""
    for _i in range(num):
        salt += random.choice(H)
    return salt


# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = config.get("security", "secret_key")
except Exception:
    SECRET_KEY = ranstr(50)
ALLOWED_HOSTS = ["*"]

# Application definition
TOKEN_EXP_DAY = 14

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "corsheaders",
    "captcha",
    "modeltranslation",
    "django_celery_beat",
    "deploy.commands",
    "test.debug",
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.contrib.redis",
    "django_prometheus",
]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


def get_installed_apps():
    from os import chdir, getcwd, walk

    previous_path = getcwd()
    master = []
    APPS_ROOT_PATH = BASE_DIR
    chdir(APPS_ROOT_PATH)
    for root, _directories, files in walk(top=getcwd(), topdown=False):
        for file_ in files:
            if (
                "apps.py" in file_
                and len(list(filter(lambda x: x != "", root.replace(getcwd(), "").split(os.sep)))) == 1
            ):
                app_path = f"{root.replace(BASE_DIR + os.sep, '').replace(os.sep, '.')}"
                master.append(app_path)
    chdir(previous_path)
    return master


CUSTOM_APPS = get_installed_apps()
INSTALLED_APPS.extend(CUSTOM_APPS)


MODELTRANSLATION_LANGUAGES = ("en", "zh")
MODELTRANSLATION_DEFAULT_LANGUAGE = "zh"
REST_FRAMEWORK = {
    "PAGE_SIZE": 20,
    "DEFAULT_PAGINATION_CLASS": ["django.core.paginator"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "dongtai_common.common.utils.ProjectTokenAuthentication",
        "dongtai_common.common.utils.DepartmentTokenAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_THROTTLE_CLASSES": (),
    "DEFAULT_THROTTLE_RATES": {},
}

basedir = os.path.dirname(os.path.realpath(__file__))
LANGUAGE_CODE = "zh"
LANGUAGES = (
    ("en", "English"),
    ("zh", "简体中文"),
)
USE_I18N = True
LOCALE_PATHS = (os.path.join(BASE_DIR, "static/i18n"),)
USE_L10N = True
MODELTRANSLATION_FALLBACK_LANGUAGES = ("zh", "en")
MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    #    'dongtai_common.common.utils.CSPMiddleware',
    #    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "xff.middleware.XForwardedForMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

PROMETHEUS_LATENCY_BUCKETS = (
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
    25.0,
    50.0,
    75.0,
    float("inf"),
)
if os.getenv("METRICS", None) == "true":
    MIDDLEWARE.extend(
        [
            "django_prometheus.middleware.PrometheusBeforeMiddleware",
            "django_prometheus.middleware.PrometheusAfterMiddleware",
        ]
    )
try:
    from dongtai_conf.settings_extend import MIDDLEWARE as MIDDLEWARE_EXTEND

    MIDDLEWARE.extend(MIDDLEWARE_EXTEND)
except ImportError:
    pass

XFF_TRUSTED_PROXY_DEPTH = 20

CSRF_COOKIE_NAME = "DTCsrfToken"
CSRF_HEADER_NAME = "HTTP_CSRF_TOKEN"


def safe_execute(default, exception, function, *args):
    try:
        return function(*args)
    except exception:
        return default


CSRF_TRUSTED_ORIGINS = tuple(
    filter(
        lambda x: x != "",
        safe_execute("", BaseException, config.get, "security", "csrf_trust_origins").split(","),
    )
)
CSRF_COOKIE_AGE = 60 * 60 * 24

AGENT_UPGRADE_URL = "https://www.huoxian.cn"
CORS_ALLOWED_ORIGINS = [
    "https://dongtai.io",
]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.huoxian.cn:(\:\d+)?$",
    r"^https://\w+\.dongtai_common.io:(\:\d+)?$",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "OPTIONS", "POST", "PUT", "DELETE"]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "referer",
    "x-token",
    "user-agent",
    "x-csrftoken",
    "csrf-token",
    "x-requested-with",
    "x_http_method_override",
]

ROOT_URLCONF = "dongtai_conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "static/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dongtai_conf.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "USER": config.get("mysql", "user"),
        "NAME": config.get("mysql", "name"),
        "PASSWORD": config.get("mysql", "password"),
        "HOST": config.get("mysql", "host"),
        "PORT": config.get("mysql", "port"),
        "OPTIONS": {
            #            'init_command':
            "charset": "utf8mb4",
            "use_unicode": True,
        },
        "TEST": {
            "USER": config.get("mysql", "user"),
            "NAME": config.get("mysql", "name"),
            "PASSWORD": config.get("mysql", "password"),
            "HOST": config.get("mysql", "host"),
            "PORT": config.get("mysql", "port"),
        },
    },
    "timeout10": {
        "ENGINE": "django.db.backends.mysql",
        "USER": config.get("mysql", "user"),
        "NAME": config.get("mysql", "name"),
        "PASSWORD": config.get("mysql", "password"),
        "HOST": config.get("mysql", "host"),
        "PORT": config.get("mysql", "port"),
        "OPTIONS": {
            "init_command": "SET max_execution_time=10000;",  # Here is ms.
            "charset": "utf8mb4",
            "use_unicode": True,
        },
        "TEST": {
            "USER": config.get("mysql", "user"),
            "NAME": config.get("mysql", "name"),
            "PASSWORD": config.get("mysql", "password"),
            "HOST": config.get("mysql", "host"),
            "PORT": config.get("mysql", "port"),
        },
    },
}
REDIS_URL = "redis://:{password}@{host}:{port}/{db}".format(
    password=config.get("redis", "password"),
    host=config.get("redis", "host"),
    port=config.get("redis", "port"),
    db=config.get("redis", "db"),
)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
]
AUTH_USER_MODEL = "dongtai_common.User"
TIME_ZONE = "Asia/Shanghai"
STATIC_URL = "/static/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/static")
MEDIA_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/static/media/"
CAPTCHA_IMAGE_SIZE = (80, 45)
CAPTCHA_LENGTH = 4
CAPTCHA_TIMEOUT = 1
LOGGING_LEVEL = "DEBUG" if DEBUG else "ERROR"
if os.getenv("environment", None) == "TEST":
    LOGGING_LEVEL = "INFO"
LOGGING_LEVEL = safe_execute(LOGGING_LEVEL, BaseException, config.get, "other", "logging_level")
# 报告存储位置
try:
    TMP_COMMON_PATH = config.get("common_file_path", "tmp_path")
except Exception:
    TMP_COMMON_PATH = "/tmp/logstash"

# 图片二级存储路径
try:
    REPORT_IMG_FILES_PATH = config.get("common_file_path", "report_img")
except Exception:
    REPORT_IMG_FILES_PATH = "report/img"

# report html二级存储路径
try:
    REPORT_HTML_FILES_PATH = config.get("common_file_path", "report_html")
except Exception:
    REPORT_HTML_FILES_PATH = "report/html"

# report pdf二级存储路径
try:
    REPORT_PDF_FILES_PATH = config.get("common_file_path", "report_pdf")
except Exception:
    REPORT_PDF_FILES_PATH = "report/pdf"
# report word 二级存储路径
try:
    REPORT_WORD_FILES_PATH = config.get("common_file_path", "report_word")
except Exception:
    REPORT_WORD_FILES_PATH = "report/word"
# report excel 二级存储路径
try:
    REPORT_EXCEL_FILES_PATH = config.get("common_file_path", "report_excel")
except Exception:
    REPORT_EXCEL_FILES_PATH = "report/excel"
FILES_SIZE_LIMIT = 1024 * 1024 * 50
# # 报告二级存储路径


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} [{module}.{funcName}:{lineno}] {message}",
            "style": "{",
        },
        "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "dongtai-webapi": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/tmp/webapi.log",
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "dongtai.openapi": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/tmp/openapi.log",
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "dongtai-core": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/tmp/core.log",
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "celery.apps.worker": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/tmp/worker.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else LOGGING_LEVEL,
            "propagate": False,
            "encoding": "utf-8",
        },
        "dongtai-webapi": {
            "handlers": [
                "console",
            ],
            "propagate": True,
            "level": LOGGING_LEVEL,
        },
        "dongtai.openapi": {
            "handlers": [
                "console",
            ],
            "propagate": True,
            "level": LOGGING_LEVEL,
        },
        "dongtai-core": {
            "handlers": [
                "console",
            ],
            "propagate": True,
            "level": LOGGING_LEVEL,
        },
        "django": {
            "handlers": [
                "console",
            ],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "dongtai-engine": {
            "handlers": [
                "console",
            ],
            "propagate": True,
            "level": LOGGING_LEVEL,
        },
        "celery.apps.worker": {
            "handlers": [
                "console",
            ],
            "propagate": True,
            "level": LOGGING_LEVEL,
        },
        #        'jsonlogger': {  # it use to logging to local logstash file
        #        },
    },
}
REST_PROXY = {
    "HOST": config.get("engine", "url"),
}

OPENAPI = config.get("apiserver", "url")

# notify
EMAIL_SERVER = config.get("smtp", "server")
EMAIL_USER = config.get("smtp", "user")
EMAIL_PASSWORD = config.get("smtp", "password")
EMAIL_FROM_ADDR = config.get("smtp", "from_addr")
EMAIL_PORT = config.get("smtp", "port")
ENABLE_SSL = config.get("smtp", "ssl") == "True"
ADMIN_EMAIL = config.get("smtp", "cc_addr")
SESSION_COOKIE_DOMAIN = None
SESSION_ENGINE = "dongtai_common.utils.db_session_engine"
CSRF_COOKIE_DOMAIN = None

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

TEST_RUNNER = "test.NoDbTestRunner"

if os.getenv("environment", None) == "TEST" or os.getenv("REQUESTLOG", None) == "TRUE":
    MIDDLEWARE.insert(0, "apitimelog.middleware.RequestLogMiddleware")

if os.getenv("PYTHONAGENT", None) == "TRUE":
    MIDDLEWARE.insert(0, "dongtai_agent_python.middlewares.django_middleware.FireMiddleware")
if os.getenv("environment", None) == "TEST" or os.getenv("SAVEEYE", None) == "TRUE":
    CAPTCHA_NOISE_FUNCTIONS = ("captcha.helpers.noise_null",)


INSTALLED_APPS.append("drf_spectacular")
SPECTACULAR_SETTINGS = {
    "TITLE": "DongTai WebApi Doc",
    "VERSION": "1.1.0",
    "PREPROCESSING_HOOKS": ["drf_spectacular.hooks.preprocess_exclude_path_format"],
    "URL_FORMAT_OVERRIDE": None,
    "DESCRIPTION": _(
        """Here is the API documentation in dongtai_conf. The corresponding management part API can be found through the relevant tag.

There are two authentication methods. You can obtain csrf_token and sessionid through the login process, or access the corresponding API through the user's corresponding Token.

The Token method is recommended here, and users can find it in the Agent installation interface such as -H
  'Authorization: Token {token}', here is the token corresponding to the user, the token method also requires a token like this on the request header."""
    ),
    "COMPONENT_SPLIT_REQUEST": True,
    "DISABLE_ERRORS_AND_WARNINGS": True,
}
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

if os.getenv("environment", None) == "TEST" or os.getenv("CPROFILE", None) == "TRUE":
    DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False
    MIDDLEWARE.insert(0, "django_cprofile_middleware.middleware.ProfilerMiddleware")

try:
    SCA_BASE_URL = config.get("sca", "base_url")
    SCA_TIMEOUT = config.getint("sca", "timeout")
    SCA_MAX_RETRY_COUNT = config.getint("sca", "max_retry_count", fallback=3)
    SCA_TOKEN = config.get("sca", "token")
    SCA_SETUP = bool(SCA_TOKEN)
except BaseException:
    SCA_BASE_URL = ""
    SCA_TIMEOUT = 0
    SCA_TOKEN = ""
    SCA_SETUP = False
DOMAIN = config.get("other", "domain", fallback="")

if os.getenv("environment", None) in ("TEST", "PROD"):
    SESSION_COOKIE_DOMAIN = config.get("other", "demo_session_cookie_domain")
    CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN

try:
    DOMAIN_VUL = config.get("other", "domain_vul")
except Exception:
    DOMAIN_VUL = "http://localhost"

# OPENAPI
BUCKET_URL = "https://oss-cn-beijing.aliyuncs.com"
BUCKET_NAME = "dongtai"
BUCKET_NAME_BASE_URL = "agent/" if os.getenv("active.profile", None) != "TEST" else "agent_test/"
VERSION = "latest"
# CONST
PENDING = 1
VERIFYING = 2
CONFIRMED = 3
IGNORE = 4
SOLVED = 5
ENGINE_URL = config.get("engine", "url")
HEALTH_ENGINE_URL = urljoin(ENGINE_URL, "/api/engine/health")
BASE_ENGINE_URL = config.get("engine", "url") + "/api/engine/run?method_pool_id={id}"
SCA_ENGINE_URL = (
    config.get("engine", "url")
    + "/api/engine/sca?agent_id={agent_id}"
    + "&package_path={package_path}&package_signature={package_signature}"
    + "&package_name={package_name}&package_algorithm={package_algorithm}"
)
REPLAY_ENGINE_URL = config.get("engine", "url") + "/api/engine/run?method_pool_id={id}&model=replay"

CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/{db}".format(
    password=config.get("redis", "password"),
    host=config.get("redis", "host"),
    port=config.get("redis", "port"),
    db=config.get("redis", "db"),
)
CELERY_RESULT_EXPIRES = 600
CELERY_WORKER_TASK_LOG_FORMAT = "%(message)s"
CELERY_WORKER_LOG_FORMAT = "%(message)s"
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_REDIRECT_STDOUTS = True
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = "ERROR"
CELERY_WORKER_MAX_TASKS_PER_CHILD = 5000

CELERY_TASK_SOFT_TIME_LIMIT = 3600
CELERY_TASK_REJECT_ON_WORKER_LOST = True
DJANGO_CELERY_BEAT_TZ_AWARE = False

DONGTAI_CELERY_CACHE_PREHEAT = safe_execute(
    True,
    BaseException,
    lambda x, y: literal_eval(config.get(x, y)),
    "other",
    "cache_preheat",
)
DEFAULT_CIRCUITCONFIG = {
    "SYSTEM": {
        "name": "系统配置",
        "metric_group": 1,
        "interval": 1,
        "deal": 2,
        "is_enable": 1,
        "is_deleted": 0,
        "targets": [],
        "metrics": [
            {"metric_type": 1, "opt": 5, "value": 100},
            {"metric_type": 2, "opt": 5, "value": 100},
        ],
    },
    "JVM": {
        "name": "JVM",
        "metric_group": 2,
        "interval": 1,
        "deal": 1,
        "is_enable": 1,
        "is_deleted": 0,
        "targets": [],
        "metrics": [
            {"metric_type": 4, "opt": 5, "value": 100},
            {"metric_type": 5, "opt": 5, "value": 1000000000},
            {"metric_type": 6, "opt": 5, "value": 1000000},
            {"metric_type": 7, "opt": 5, "value": 1000000},
            {"metric_type": 8, "opt": 5, "value": 1000000},
        ],
    },
    "APPLICATION": {
        "name": "应用配置",
        "metric_group": 3,
        "interval": 1,
        "deal": 1,
        "is_enable": 1,
        "is_deleted": 0,
        "targets": [],
        "metrics": [
            {"metric_type": 9, "opt": 5, "value": 10000},
            {"metric_type": 10, "opt": 5, "value": 100000000},
        ],
    },
}
DEFAULT_IAST_VALUE_TAG = [
    "cross-site",
    "xss-encoded",
    "html-encoded",
    "html-decoded",
    "url-encoded",
    "url-decoded",
    "base64-encoded",
    "base64-decoded",
    "xml-encoded",
    "xml-decoded",
    "sql-encoded",
    "sql-decoded",
    "xpath-encoded",
    "xpath-decoded",
    "ldap-encoded",
    "ldap-decoded",
    "http-token-limited-chars",
    "numeric-limited-chars",
    "custom-encoded-cmd-injection",
    "custom-decoded-cmd-injection",
    "custom-encoded-jnd-injection",
    "custom-decoded-jnd-injection",
    "custom-encoded-hql-injection",
    "custom-decoded-hql-injection",
    "custom-encoded-nosql-injection",
    "custom-decoded-nosql-injection",
    "custom-encoded-smtp-injection",
    "custom-decoded-smtp-injection",
    "custom-encoded-xxe",
    "custom-decoded-xxe",
    "custom-encoded-el-injection",
    "custom-decoded-el-injection",
    "custom-encoded-reflection-injection",
    "custom-decoded-reflection-injection",
    "custom-encoded-ssrf",
    "custom-decoded-ssrf",
    "custom-encoded-path-traversal",
    "custom-decoded-path-traversal",
    "custom-encoded-file-write",
    "custom-encoded-file-write",
    "custom-encoded-redos",
    "custom-decoded-redos",
]
DEFAULT_TAINT_VALUE_RANGE_COMMANDS = [
    "KEEP",
    "APPEND",
    "SUBSET",
    "INSERT",
    "REMOVE",
    "REPLACE",
    "CONCAT",
    "TRIM",
    "TRIM_RIGHT",
    "TRIM_LEFT",
    "OVERWRITE",
]
DEFAULT_CODE_DETECT_BLACK_LIST = [
    "aj.",
    "akka.",
    "android.",
    "antlr.",
    "apple.",
    "aQute.",
    "brave.",
    "bsh.",
    "ch.qos.",
    "co.paralleluniverse.",
    "com.acumenat.",
    "com.alibaba.arthas.",
    "com.alibaba.cloud.",
    "com.alibaba.cola.",
    "com.alibaba.com.caucho.",
    "com.alibaba.crr.",
    "com.alibaba.csp.",
    "com.alibaba.datax.",
    "com.alibaba.druid.",
    "com.alibaba.dubbo.",
    "com.alibaba.fastjson.",
    "com.alibaba.fastjson2.",
    "com.alibaba.google.",
    "com.alibaba.jvm.",
    "com.alibaba.metrics.",
    "com.alibaba.nacos.",
    "com.alibaba.otter.",
    "com.alibaba.rocketmq.",
    "com.alibaba.rsqldb.",
    "com.alibaba.spring.",
    "com.alibaba.ttl3.",
    "com.alipay.common.",
    "com.alipay.disruptor.",
    "com.alipay.hessian.",
    "com.alipay.lookout.",
    "com.alipay.remoting.",
    "com.alipay.sofa.",
    "com.aliyun.openservices.",
    "com.arjuna.",
    "com.asn1c.",
    "com.atomikos.",
    "com.baidu.bjf.",
    "com.baidu.brpc.",
    "com.baidu.jprotobuf.",
    "com.baomidou.",
    "com.bea.",
    "com.beust.",
    "com.carrotsearch.",
    "com.caucho.",
    "com.certicom.",
    "com.codahale.",
    "com.corundumstudio.",
    "com.ctc.",
    "com.datastax.",
    "com.ddtek.",
    "com.dyuproject.",
    "com.esotericsoftware.",
    "com.esri.",
    "com.fasterxml.",
    "com.flipkart.",
    "com.github.",
    "com.google.",
    "com.googlecode.",
    "com.headius.",
    "com.ibm.",
    "com.intellij.",
    "com.jayway.",
    "com.jcraft.",
    "com.kenai.",
    "com.linar.",
    "com.linecorp.",
    "com.mchange.",
    "com.merant.",
    "com.microsoft.",
    "com.mkyong.",
    "com.mongodb.",
    "com.mysql.",
    "com.navercorp.",
    "com.netflix.",
    "com.networknt.",
    "com.nimbusds.",
    "com.nulabinc.",
    "com.octetstring.",
    "com.octo.",
    "com.opensymphony.",
    "com.oracle.",
    "com.querydsl.",
    "com.rabbitmq.",
    "com.rsa.",
    "com.screener.",
    "com.secnium.",
    "com.solarmetric.",
    "com.squareup.",
    "com.stoyanr.",
    "com.sun.",
    "com.tdunning.",
    "com.terracotta.",
    "com.thetransactioncompany.",
    "com.thoughtworks.",
    "com.twitter.",
    "com.typesafe.",
    "com.vividsolutions.",
    "com.weibo.api.motan.",
    "com.xxl.",
    "com.yahoo.",
    "com.zaxxer.",
    "com.zeroturnaround.",
    "commonj.",
    "dagger.",
    "de.javakaffee.",
    "edu.emory.",
    "feign.",
    "freemarker.",
    "gnu.",
    "google.",
    "graphql.",
    "groovy.",
    "io.dongtai.",
    "io.dropwizard.",
    "io.github.",
    "io.grpc.",
    "io.jsonwebtoken.",
    "io.lettuce.",
    "io.micrometer.",
    "io.netty.",
    "io.opencensus.",
    "io.opentelemetry.",
    "io.opentracing.",
    "io.perfmark.",
    "io.reactivex.",
    "io.restassured.",
    "io.shardingjdbc.",
    "io.shardingsphere.",
    "io.swagger.",
    "io.undertow.",
    "io.vavr.",
    "io.vertx.",
    "jain.",
    "jakarta.",
    "java.",
    "javafx.",
    "javassist.",
    "javax.",
    "javelin.",
    "jdk.",
    "jersey.",
    "jline.",
    "jnr.",
    "jodd.",
    "joptsimple.",
    "jregex.",
    "junit.",
    "kodo.",
    "lbmq.",
    "mazz.",
    "me.qmx.",
    "microsoft.",
    "mozilla.",
    "mssql.",
    "net.bytebuddy.",
    "net.iharder.",
    "net.jcip.",
    "net.jpountz.",
    "net.logstash.",
    "net.minidev.",
    "net.n3.",
    "net.rubyeye.",
    "net.sf.",
    "net.sourceforge.",
    "net.spy.",
    "netscape.",
    "nu.xom.",
    "ognl.",
    "okhttp3.",
    "okio.",
    "oracle.",
    "org.abego.",
    "org.ajax4jsf.",
    "org.antlr.",
    "org.aopalliance.",
    "org.apache.",
    "org.apiguardian.",
    "org.asciidoctor.",
    "org.aspectj.",
    "org.assertj.",
    "org.attoparser.",
    "org.bouncycastle.",
    "org.bson.",
    "org.ccil.",
    "org.checkerframework.",
    "org.codehaus.",
    "org.custommonkey.",
    "org.dataloader.",
    "org.dom4j.",
    "org.eclipse.",
    "org.elasticsearch.",
    "org.flywaydb.",
    "org.fusesource.",
    "org.gjt.",
    "org.glassfish.",
    "org.h2.",
    "org.hamcrest.",
    "org.hdiv.",
    "org.HdrHistogram.",
    "org.hibernate.",
    "org.hornetq.",
    "org.hotswap.",
    "org.hsqldb.",
    "org.I0Itec.",
    "org.ietf.",
    "org.jacoco.",
    "org.jaxen.",
    "org.jboss.",
    "org.jcodings.",
    "org.jcp.",
    "org.jctools.",
    "org.jdom.",
    "org.jetbrains.",
    "org.jfree.",
    "org.jledit.",
    "org.jnp.",
    "org.joda.",
    "org.joni.",
    "org.jose4j.",
    "org.jruby.",
    "org.json.",
    "org.jsoup.",
    "org.junit.",
    "org.jvnet.",
    "org.knopflerfish.",
    "org.LatencyUtils.",
    "org.locationtech.",
    "org.mariadb.",
    "org.mockito.",
    "org.mortbay.",
    "org.msgpack.",
    "org.mybatis.",
    "org.neo4j.",
    "org.noggit.",
    "org.nutz.",
    "org.oasisopen.",
    "org.objectweb.",
    "org.objenesis.",
    "org.omg.",
    "org.openjdk.",
    "org.opentest4j.",
    "org.ops4j.",
    "org.osgi.",
    "org.osoa.",
    "org.owasp.",
    "org.pentaho.",
    "org.picketbox.",
    "org.postgresql.",
    "org.powermock.",
    "org.python.",
    "org.quartz.",
    "org.reactivestreams.",
    "org.redisson.",
    "org.relaxng.",
    "org.rhq.",
    "org.richfaces.",
    "org.roaringbitmap.",
    "org.skyscreamer.",
    "org.slf4j.",
    "org.sonatype.",
    "org.springdoc.",
    "org.springframework.",
    "org.synchronoss.",
    "org.terracotta.",
    "org.thymeleaf.",
    "org.tukaani.",
    "org.unbescape.",
    "org.w3c.",
    "org.webjars.",
    "org.wildfly.",
    "org.xerial.",
    "org.xml.",
    "org.xmlpull.",
    "org.xmlunit.",
    "org.xnio.",
    "org.yaml.",
    "org.znerd.",
    "oshi.",
    "play.",
    "reactor.",
    "redis.",
    "ru.yandex.",
    "rx.",
    "scala.",
    "serp.",
    "sun.",
    "weblogic.",
    "workshop.",
    "zipkin2.",
]

DONGTAI_MAX_RATE_LIMIT = 10
DONGTAI_REDIS_ES_UPDATE_BATCH_SIZE = 500
DONGTAI_MAX_BATCH_TASK_CONCORRENCY = 5


try:
    TANTIVY_STATE = config.get("tantivy", "enable") == "true"
except Exception:
    TANTIVY_STATE = True
try:
    TANTIVY_INDEX_PATH = config.get("tantivy", "index_path")
except Exception:
    TANTIVY_INDEX_PATH = os.path.join(TMP_COMMON_PATH, "tantivy")


ELASTICSEARCH_STATE = config.get("elastic_search", "enable") == "true"


def get_elasticsearch_conf() -> list[str]:
    hoststr = config.get("elastic_search", "host")
    return hoststr.split(",")


if ELASTICSEARCH_STATE:
    INSTALLED_APPS.append("django_elasticsearch_dsl")
    ELASTICSEARCH_DSL = {
        "default": {"hosts": get_elasticsearch_conf()},
    }
    ASSET_VUL_INDEX = config.get("elastic_search", "asset_vul_index")
    VULNERABILITY_INDEX = config.get("elastic_search", "vulnerability_index")
    ASSET_AGGR_INDEX = config.get("elastic_search", "asset_aggr_index")
    METHOD_POOL_INDEX = config.get("elastic_search", "method_pool_index")
    ASSET_INDEX = config.get("elastic_search", "asset_index")
    ELASTICSEARCH_DSL_PARALLEL = True
    ELASTICSEARCH_DSL_AUTO_REFRESH = False
    ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = "dongtai_common.utils.es.DTCelerySignalProcessor"
    import elasticsearch
    from elasticsearch import logger as es_logger

    es_logger.setLevel(elasticsearch.logging.DEBUG)
else:
    ELASTICSEARCH_DSL = {
        "default": {},
    }
    ASSET_VUL_INDEX = ""
    VULNERABILITY_INDEX = ""
    ASSET_AGGR_INDEX = ""
    METHOD_POOL_INDEX = ""
    ASSET_INDEX = ""

AUTO_UPDATE_HOOK_STRATEGY = config.getboolean("other", "auto_update_hook_strategy", fallback=False)


def is_gevent_monkey_patched() -> bool:
    try:
        from gevent import monkey
    except ImportError:
        return False
    else:
        return bool(monkey.saved)


def set_asyncio_policy():
    state = is_gevent_monkey_patched()
    print(f"is in gevent patched : {state}")


#   disable until this package update
#    if state:


AGENT_LOG_DIR = os.path.join(TMP_COMMON_PATH, "batchagent")

# check path exists
for _dir in (TMP_COMMON_PATH, AGENT_LOG_DIR):
    if not os.path.exists(_dir):
        print(f"{_dir} is not exists, check the init.")
        sys.exit(0)

DAST_TOKEN = config.get("other", "dast_token", fallback="")

set_asyncio_policy()

if os.getenv("DJANGOSILK", None) == "TRUE":
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")
    INSTALLED_APPS.append("silk")
    SILKY_PYTHON_PROFILER = True
    SILKY_ANALYZE_QUERIES = True
    SILKY_EXPLAIN_FLAGS = {"format": "JSON", "costs": True}
    SILKY_SENSITIVE_KEYS = {
        "username",
        "api",
        "token",
        "key",
        "secret",
        "password",
        "signature",
    }
    SILKY_PYTHON_PROFILER_BINARY = True


# Baseline configuration.
AUTH_LDAP_SERVER_URI = config.get("ldap", "server_uri", fallback="")

AUTH_LDAP_BIND_DN = config.get("ldap", "ldap_bind_dn", fallback="")
AUTH_LDAP_BIND_PASSWORD = config.get("ldap", "ldap_bind_password", fallback="")

AUTH_LDAP_ALWAYS_UPDATE_USER = False
AUTH_LDAP_READY = AUTH_LDAP_SERVER_URI != ""
# useless
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=users,dc=example,dc=com"


# report upload throttle
REPORT_UPLOAD_THROTTLE = config.get("throttle", "report_upload", fallback="")

# log service timeout
LOG_SERVICE_TIMEOUT = config.getint("log_service", "port", fallback=10)

# enable token login
TOKEN_LOGIN = config.getboolean("other", "token_login", fallback=False)
