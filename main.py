import uuid
from config.constant import *
from aolf_client.aofl_http import AoflClient

aofl_client = AoflClient(
    url_prefix=AOFL_API_PREFIX,
    partner=PARTNER,
    aofl_jwt_secret=AOFL_JWT_SECRET,
    aofl_product=AOFL_PRODUCT
)

galaxy_id = str(uuid.uuid4())
print(galaxy_id)
terminated_result = aofl_client.aofl_terminate(
    galaxy_id=galaxy_id,
    product_key=""
)
print(terminated_result)
