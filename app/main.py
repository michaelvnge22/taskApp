from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auths, users, groups, tasks

app = FastAPI(title="TaskGroup App")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include APIs first
app.include_router(auths.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(tasks.router)

# mount frontend after routers so API routes are not intercepted by static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
