from fastapi import APIRouter


api_router = APIRouter()

include_api = api_router.include_router

routers = (
    # (router, prefix, tags),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
