from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from dotenv import load_dotenv
from routes.user import router as userRouter
from routes.videoCall import router as videoCallRouter
from routes.auth import router as authRouter

from middlewares.verification import PermissionMiddleware


# Cargar variables de entorno
load_dotenv()

# Crear instancia FastAPI base
fastapi_app = FastAPI()

@fastapi_app.on_event("startup")
def on_startup():
    print("🛠️ Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas.")

# Middleware de CORS
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware personalizado
fastapi_app.add_middleware(PermissionMiddleware)

# Ruta base
@fastapi_app.get("/")
async def read_root():
    return {"message": "Home page"}

# Registrar routers
fastapi_app.include_router(userRouter, prefix="/users", tags=["Users"])
fastapi_app.include_router(videoCallRouter, prefix="/videoCalls", tags=["videoCalls"])
fastapi_app.include_router(authRouter, prefix="/auth", tags=["auth"])

# Socket.IO + Señalización WebRTC
import socketio
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=fastapi_app, socketio_path="/socket.io")

@sio.event
async def connect(sid, environ, auth):
    print(f"🟢 Usuario conectado: {sid}")

@sio.event
async def disconnect(sid):
    print(f"🔴 Usuario desconectado: {sid}")

@sio.event
async def join_room(sid, data):
    room = data.get("room")
    username = data.get("username")
    
    print(f"👥 {sid} ({username}) se unió a la sala {room}")
    await sio.enter_room(sid, room)

    await sio.emit("peer_joined", {
        "sid": sid,
        "room": room,
        "fromUsername": username
    }, skip_sid=sid, to=room)

@sio.event
async def register_user(sid, data):
    username = data["username"]
    await sio.save_session(sid, {"username": username})
    print(f"✅ Usuario registrado para recibir llamadas: {username}")

@sio.event
async def create_room(sid, data):
    room = data.get("room")
    username = data.get("username")
    print(f"🛠️ {username} ({sid}) creó la sala {room}")

    # Notificar a otros usuarios en la sala que un nuevo peer se ha unido
    await sio.emit("room_created", {
        "username": username,
        "sid": sid,
        "room": room
    }, skip_sid=sid)

@sio.event
async def sendOffer(sid, data):
    to_sid = data.get("toSid")
    offer = data.get("offer")
    room = data.get("room")
    session = await sio.get_session(sid)
    from_username = session.get("username", "desconocido")

    print(f"📡 {from_username} ({sid}) sent offer to {to_sid} in room {room}")

    await sio.emit("offer", {
        "offer": offer,
        "fromSid": sid,
        "fromUsername": from_username,
        "room": room
    }, to=to_sid)

@sio.event
async def sendAnswer(sid, data):
    from_sid = data.get("fromSid")
    to_sid = data.get("toSid")
    answer = data.get("answer")
    room = data.get("room")
    session = await sio.get_session(sid)
    from_username = session.get("username", "desconocido")

    print(f"📡 {from_username} ({sid}) sent answer to {to_sid} in room {room}")

    await sio.emit("answer", {
        "answer": answer,
        "fromSid": sid,
        "receiver_id": from_sid,
        "fromUsername": from_username,
        "room": room
    }, to=to_sid)