import app.main as main

import app.api.users.users_router as users_router


def include_routers():
    main.app.include_router(users_router.router, prefix="/api/users", tags=["users"])
    #더 추가해야함


