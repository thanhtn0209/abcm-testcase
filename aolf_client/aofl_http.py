import requests
from utils.datatime import get_next_billing_time
from config.logger import LOGGER
from config.constant import *
import jwt

# constant for creating
ACTION_SOURCE_UNKNOWN = "source_unknown"
# constants for cancellation
DEFAULT_PAYMENT_PROVIDER = "momotoken"
CANCELLATION_REASON_UNKNOWN = "reason_unknown"
# constants for termination
TERMINATION_TYPE_UNKNOWN = "type_unknown"
TERMINATION_CATEGORY_UNKNOWN = "category_unknown"
TERMINATION_REASON = "unknown_reason"


class AoflClient:
    def __init__(self, url_prefix, partner, aofl_jwt_secret, aofl_product):
        self.url_prefix = url_prefix
        self.partner = partner
        self.aofl_jwt_secret = aofl_jwt_secret
        self.aofl_product = aofl_product

    def create_jwt(self, data: dict, algorithm: str) -> str:
        headers = {
            "typ": "JWT",
            "alg": algorithm,
            "partner": self.partner,
        }
        encoded_jwt = jwt.encode(
            payload=data,
            key=self.aofl_jwt_secret,
            algorithm=algorithm,
            headers=headers
        )

        return encoded_jwt

    @staticmethod
    def http_post(jwt_encoded: str, url: str) -> dict:
        try:
            res = requests.post(
                data={"request_token": jwt_encoded},
                url=url,
            )
            LOGGER.info({
                "message": "sent message to aofl",
                "payload_resp": res.json()
            })
        except Exception as e:
            LOGGER.error({
                "message": "can't sent aolf request",
                "error": str(e)
            })
            return {"SUCCESS": "FALSE", "payload": str(e)}

        return res.json()["success"]

    def aofl_create(self, galaxy_id: str, product_key: str, period: int) -> str:
        url = self.url_prefix + "/Galaxy/Create/"
        data = {
            "context_info": DEFAULT_CONTEXT_INFO,
            "galaxy_id": galaxy_id,
            "product_key": product_key,
            "expires_timestamp": get_next_billing_time(period),
            "is_test": False,
            "next_billing_timestamp": get_next_billing_time(period),
            "payment_provider": DEFAULT_PAYMENT_PROVIDER,
            "aofl_product": self.aofl_product
        }

        LOGGER.info({"payload": data})
        encoded_jwt = self.create_jwt(data=data, algorithm="HS512")
        result = self.http_post(encoded_jwt, url)

        return result

    def aolf_switch_product(
            self,
            galaxy_id: str,
            product_key: str,
            old_product_key: str,
            period: int,
            old_period: int,
            switch_type: str
    ):
        url = self.url_prefix + "/Galaxy/SwitchProduct/"
        data = {
            "context_info": DEFAULT_CONTEXT_INFO,
            "galaxy_id": galaxy_id,
            "product_key": product_key,
            "old_product_key": old_product_key,
            "switch_type": switch_type,  # downgrade, change_with_charge, upgrade
            "expires_timestamp": get_next_billing_time(old_period + period),
            "next_billing_timestamp": get_next_billing_time(old_period + period),
            "aofl_product": self.aofl_product
        }

        LOGGER.info({"payload": data})
        encoded_jwt = self.create_jwt(data=data, algorithm="HS512")
        result = self.http_post(encoded_jwt, url)

        return result

    def aofl_cancel(self, galaxy_id: str, product_key: str, period: int) -> str:
        url = self.url_prefix + "/Galaxy/OptOut/"
        data = {
            "context_info": DEFAULT_CONTEXT_INFO,
            "galaxy_id": galaxy_id,
            "product_key": product_key,
            "aofl_product": self.aofl_product,
            "action_source": ACTION_SOURCE_UNKNOWN,
            "cancellation_timestamp": get_next_billing_time(period),
            "cancellation_reason": CANCELLATION_REASON_UNKNOWN,
        }

        LOGGER.info({"payload": data})
        encoded_jwt = self.create_jwt(data=data, algorithm="HS512")
        result = self.http_post(encoded_jwt, url)

        return result

    def aofl_terminate(self, galaxy_id, product_key):
        url = self.url_prefix + "/Galaxy/Terminate/"
        data = {
            "context_info": DEFAULT_CONTEXT_INFO,
            "galaxy_id": galaxy_id,
            "product_key": product_key,
            "aofl_product": self.aofl_product,
            "action_source": ACTION_SOURCE_UNKNOWN,
            "termination_type": TERMINATION_TYPE_UNKNOWN,
            "termination_category": TERMINATION_CATEGORY_UNKNOWN,
            "termination_reason": TERMINATION_REASON
        }
        LOGGER.info({"payload": data})
        encoded_jwt = self.create_jwt(data=data, algorithm="HS512")
        result = self.http_post(encoded_jwt, url)

        return result

    def aofl_renew(self, galaxy_id, period, old_period):
        url = self.url_prefix + "/Galaxy/Renew/"
        data = {
            "context_info": DEFAULT_CONTEXT_INFO,
            "galaxy_id": galaxy_id,
            "payment_provider": DEFAULT_PAYMENT_PROVIDER,
            "aofl_product": self.aofl_product,
            "expires_timestamp": get_next_billing_time(old_period + period),
            "next_billing_timestamp": get_next_billing_time(old_period + period),
            "renewal_status": "active"
        }

    
