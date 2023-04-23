from fastapi import FastAPI

from server.routes.user import router as UserRouter
from server.routes.organization import router as OrganizationRouter
from server.routes.permission import router as PermissionRouter


app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(OrganizationRouter, tags=["Organization"], prefix="/organization")
app.include_router(PermissionRouter, tags=["Permission"], prefix="/permission")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this Cosmo Admin!"}