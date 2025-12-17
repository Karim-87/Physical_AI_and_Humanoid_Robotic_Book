from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth_routes import router as auth_router
from src.api.oauth_routes import router as oauth_router
from src.config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routers only
app.include_router(auth_router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(oauth_router, prefix=f"{settings.API_V1_STR}/oauth", tags=["oauth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth-api"}

@app.get("/auth-info")
def auth_info():
    """Provides information about authentication endpoints and usage."""
    return {
        "message": "Authentication Information",
        "endpoints": {
            "traditional_auth": {
                "register": f"{settings.API_V1_STR}/auth/register (POST)",
                "login": f"{settings.API_V1_STR}/auth/login (POST)",
                "logout": f"{settings.API_V1_STR}/auth/logout (POST)",
                "preferences": {
                    "get": f"{settings.API_V1_STR}/auth/preferences (GET)",
                    "update": f"{settings.API_V1_STR}/auth/preferences (PUT)"
                }
            },
            "oauth": {
                "providers": ["facebook", "google"],
                "auth_url": f"{settings.API_V1_STR}/oauth/{{provider}}/auth-url (GET)",
                "login": f"{settings.API_V1_STR}/oauth/{{provider}} (POST)",
                "callback": f"{settings.API_V1_STR}/oauth/{{provider}}/callback (GET)"
            }
        },
        "docs": [
            f"{settings.API_V1_STR}/docs - Interactive API documentation",
            f"{settings.API_V1_STR}/redoc - Alternative API documentation"
        ],
        "oauth_flow": {
            "step_1": "GET /api/v1/oauth/{provider}/auth-url to get authorization URL",
            "step_2": "Redirect user to the authorization URL to grant permissions",
            "step_3": "Handle the redirect back to your callback URL with 'code' parameter",
            "step_4": "POST /api/v1/oauth/{provider} with the code to exchange for token",
            "alternative_step_4": "Or let the callback endpoint handle the redirect automatically"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)