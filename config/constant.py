from utils.datatime import get_current_time

PARTNER = "galaxy"
AOFL_JWT_SECRET = "38EF91CF56F35F7E181264F41004B1C2E2F078AFAF7A44CD55719A369D935E15"
AOFL_API_PREFIX = "https://partner.stg.vn.iell.aofk.net/ws/ampsl/0.1/jwt"
AOFL_PRODUCT = "abcmouse_english_vn"


FMF_ONE_MONTH_SUBS = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv55.sub.1month299000fmf",
    "period": 1
}
FMF_HALF_YEAR_SUBS = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv55.sub.6month999000fmf",
    "period": 2
}
FMF_ONE_YEAR_SUB = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv55.sub.1year1499000fmf",
    "period": 3
}
ONE_MONTH_PACKAGE = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv79.sub.1month299000",
    "period": 1
}
HALF_YEAR_PACKAGE = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv79.sub.6month999000",
    "period": 2
}
ONE_YEAR_PACKAGE = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv79.sub.1year1499000",
    "period": 3
}
ONE_MONTH_SUBS = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv55.sub.1month299000",
    "period": 1
}
HALF_YEAR_SUBS = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv55.sub.6month999000",
    "period": 2
}
ONE_YEAR_SUBS = {
    "product_key": "vn.aofl.abcmouseenglish.aoflsrv55.sub.1year1499000",
    "period": 3
}

DEFAULT_CONTEXT_INFO = {
    "app_store": "unknown",
    "device_platform": "unknown",
    "device_id": "unknown",
    "geo_ip_info": {
        "ip": "0.0.0.0"
    },
    "user_agent": "unknown",
    "test_user": False,
    "timestamp": get_current_time()
}
