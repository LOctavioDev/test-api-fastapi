"""
This is a principal Module FastApi
"""

from fastapi import FastAPI
from routes.user import user
from routes.material import material
from routes.loans import loan
from routes.auth import auth
from middleware.token_middlware import TokenMiddleware

app = FastAPI()

app.include_router(auth, prefix="/api/auth")
app.include_router(user, prefix="/api")
app.include_router(material, prefix="/api")
app.include_router(loan, prefix="/api")
app.add_middleware(TokenMiddleware)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    