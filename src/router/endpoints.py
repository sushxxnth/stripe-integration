from fastapi import APIRouter

from src.user.api import router as user_router
from src.core.stripe_api import router as stripe_router  

api_router = APIRouter()
include_api = api_router.include_router

routers = (

    (user_router, "users", "users"),
    (stripe_router, "stripe", "payments"), 
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
