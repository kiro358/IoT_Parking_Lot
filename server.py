from fastapi import FastAPI, HTTPException, Body, Depends, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from gRPC_client import fetch_dynamic_pricing
from pricing_service import calculate_dynamic_pricing, time_based_pricing
from fastapi.responses import FileResponse
import time
from datetime import datetime, timedelta
import asyncio
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import bcrypt
from jose import JWTError, jwt


# environment variables
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # You could also add more checks here (e.g., token expiration)
    except JWTError:
        raise credentials_exception
    return username

app = FastAPI(title="Parking Lot Management System")

# @app.on_event("startup")
# async def startup_event():
#     await start_background_tasks()

# async def start_background_tasks():
#     asyncio.create_task(release_expired_reservations())

# Serve static files from the "public" directory
app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the port if your front-end runs on a different one
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return FileResponse('public/index.html')

@app.get("/index")
def read_root():
    return FileResponse('public/index.html')

@app.get("/login")
def read_root():
    return FileResponse('public/login.html')

@app.get("/register")
def read_root():
    return FileResponse('public/register.html')

@app.get("/find_parking")
def read_root():
    return FileResponse('public/find_parking.html')

@app.get("/reservation")
def read_root():
    return FileResponse('public/reservation.html')

# In-memory data storage
sensors_data = {}  # Format: {lot_id: {spot_id: bool}}
reservations_data = []
users_data = []
current_pricing = {"rate": 5}  # Assuming a simple structure for current pricing
pricing_history = []  # History of pricing updates

num_floors = 6
spots_per_floor = 20

# Populate sensors_data with floors (lot_id) and spots (spot_id) initialized to False
for floor in range(1, num_floors + 1):
    sensors_data[floor] = {}
    for spot in range(1, spots_per_floor + 1):
        sensors_data[floor][spot] = False

# Revised Pydantic models for request and response data
class LotSensorData(BaseModel):
    lot_id: int
    sensors: List[int]  # List of 0s and 1s representing each spot in the lot

class Reservation(BaseModel):
    lot_id: int
    spot_id: int
    user_id: str
    current_pricing: int
    duration: int
    reservation_id: str
    start_time: datetime = datetime.now()

class User(BaseModel):
    user_id: Optional[str] = None
    username: str
    email: str
    password: str

@app.get("/")
def read_root():
	return FileResponse('public/login.html')

@app.get("/login")
def read_root():
	return FileResponse('public/login.html')

@app.get("/register")
def read_root():
	return FileResponse('public/register.html')

@app.get("/find_parking")
def read_root():
	return FileResponse('public/find_parking.html')

@app.get("/reservation")
def read_root():
	return FileResponse('public/reservation.html')

user1 = User(
    user_id = "1",
    username = "Kiro",
    email = "kirolos358@gmail.com",
    password = bcrypt.hashpw("kiro".encode('utf-8'), bcrypt.gensalt())
    )
users_data.append(user1.model_dump())
                        
test_reservations = [
    {"reservation_id": "res4", "lot_id": "lot4", "spot_id": "spot4", "user_id": "1", "current_pricing": 8, "duration": 4},
    {"reservation_id": "res5", "lot_id": "lot5", "spot_id": "spot5", "user_id": "1", "current_pricing": 5, "duration": 2},
    {"reservation_id": "res6", "lot_id": "lot6", "spot_id": "spot6", "user_id": "1", "current_pricing": 9, "duration": 3},
]
reservations_data.extend(test_reservations)

# IoT Sensors endpoints
@app.post("/sensors/data")
async def receive_sensors_data(data: List[LotSensorData]):
    for lot_data in data:
        lot_id = lot_data.lot_id
        if lot_id not in sensors_data:
            sensors_data[lot_id] = {}
        for spot_id, status in enumerate(lot_data.sensors):
            sensors_data[lot_id][spot_id] = bool(status)
    return {"message": "Data received successfully", "data": data}

# User Interface for Drivers endpoints
@app.get("/parking/spots/{lot_id}")
async def list_parking_spots(lot_id: int):
    lot_data = sensors_data.get(lot_id)
    if lot_data is None:
        raise HTTPException(status_code=404, detail="Lot not found")
    return {"lot_id": lot_id, "spots": lot_data}

@app.post("/parking/reservations")
async def create_reservation(reservation: Reservation):
    lot_id = reservation.lot_id
    spot_id = reservation.spot_id
    if lot_id in sensors_data and sensors_data[lot_id].get(spot_id):
        raise HTTPException(status_code=400, detail="Spot is already occupied")
    # Store reservation data
    reservation_data = reservation.model_dump()
    reservation_data["start_time"] = time.time()  
    reservations_data.append(reservation_data)

    sensors_data[lot_id][spot_id] = True
    current_time_str = datetime.now().strftime("%H:%M")
    if time_based_pricing(current_time_str) is None:
        print(current_time_str)
        price=5
    else:
        price = time_based_pricing(current_time_str) * reservation.current_pricing 
    total_cost = price * reservation.duration
    
    reservation_data["total_cost"] = total_cost
    reservations_data.append(reservation_data)
    return {"message": "Reservation created successfully", "reservation": reservation, "total_cost": total_cost}

@app.get("/users/{user_id}/reservations")
async def get_reservations(user_id: str, current_user: str = Depends(get_current_user)):
    # Assuming `get_current_user` returns the ID of the currently logged-in user
    # and you're storing reservations in `reservations_data`
    
    # For demonstration, we're not checking the user_id against the current_user for authorization
    user_reservations = [reservation for reservation in reservations_data if reservation["user_id"] == user_id]
    return user_reservations

# Pricing Endpoints
@app.get("/dynamic-pricing")
async def dynamic_pricing(demand_factor: str, current_time: str):
    # Using the gRPC client to fetch pricing
    grpc_price = fetch_dynamic_pricing(demand_factor)
    
    # Optionally using the local calculate_dynamic_pricing function for additional calculations
    price = calculate_dynamic_pricing(demand_factor, current_time, grpc_price)
    
    return {"price": price}

@app.get("/pricing/current")
async def get_current_pricing():
    return {"pricing": current_pricing}

@app.post("/pricing/update")
async def update_pricing(new_rate: int = Body(...)):
    global current_pricing
    pricing_history.append(current_pricing)
    current_pricing = {"rate": new_rate}
    return {"message": "Pricing updated successfully", "new_rate": new_rate}

@app.get("/pricing/history")
async def get_pricing_history():
    return {"history": pricing_history}

# User Management Endpoints
@app.post("/users/register")
async def register_user(user: User):
    user.user_id = str(len(users_data) + 1)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    users_data.append({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })
    return {"message": "User registered successfully", "user": user}

@app.post("/users/login")
async def login_user(email: str = Body(...), password: str = Body(...)):
    print("Attempting login with:", email, password)
    print("Available users:", users_data)
    user = next((u for u in users_data if u['email'] == email), None)
    hashed_password = user['password'].encode('utf-8')
    if user is None or not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return {"message": "User logged in successfully", "email": email, "access_token": access_token, "token_type": "bearer"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = next((u for u in users_data if u['user_id'] == user_id), None)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
async def update_user(user_id: str, updated_user: User):
    global users_data
    users_data = [u for u in users_data if u['user_id'] != user_id] + [updated_user.model_dump()]
    return {"message": "User updated successfully", "user": updated_user}

@app.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: str = Depends(get_current_user)):
    global users_data
    user = next((u for u in users_data if u['username'] == current_user), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Only allow a user to delete their own account, unless they're an admin
    if user['user_id'] != user_id and not user.get('is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized to delete this user.")
    
    users_data = [u for u in users_data if u['user_id'] != user_id]
    return {"message": "User deleted successfully"}

# Admin Endpoints
@app.get("/system/status")
async def system_status():
    return {"status": "All systems operational"}

@app.post("/feedback")
async def submit_feedback(feedback: str = Body(...)):
    return {"message": "Feedback received", "feedback": feedback}

async def release_expired_reservations():
    while True:
        # Check reservations periodically
        current_time = time.time()

        for reservation in reservations_data:
            start_time = reservation.get("start_time", 0)
            duration = reservation.get("duration", 0)
            if current_time >= start_time + duration * 3600:  
                lot_id = reservation["lot_id"]
                spot_id = reservation["spot_id"]

                if lot_id not in sensors_data:
                    sensors_data[lot_id] = {}

                sensors_data[lot_id][spot_id] = False  


        # Sleep for a period before checking again (e.g., every hour)
        await asyncio.sleep(3600)  # Sleep for 1 hour (3600 seconds)

# Start the background task
async def start_background_tasks():
    asyncio.create_task(release_expired_reservations())

app.add_event_handler("startup", start_background_tasks)