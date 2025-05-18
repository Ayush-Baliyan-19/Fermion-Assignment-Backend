from fastapi import FastAPI
import socketio
from fastapi.middleware.cors import CORSMiddleware
from rooms import get_users_in_room
from socket_events import register_socket_events  # Your custom event file

# Create Socket.IO server (Async)
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    always_connect=True
)

# Create FastAPI app for HTTP routes
fastapi_app = FastAPI()

# Allow CORS
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
    expose_headers=["*"],
)

# Example HTTP route
@fastapi_app.get("/")
async def root():
    return {"message": "Fermion FastAPI signaling server running"}

@fastapi_app.get('/api/stream-count')
async def get_stream_users():
    return get_users_in_room('room1')
# Register your custom socket events
register_socket_events(sio)

# Wrap FastAPI with Socket.IO ASGI app
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
