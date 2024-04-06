from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
from typing import Dict
from fastapi.responses import FileResponse


app = FastAPI(title="Parking Lot Management System")

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
    sensors: Dict[int, bool]


class Reservation(BaseModel):
    lot_id: int
    spot_id: int
    user_id: str
    current_pricing: int
    duration: int
    reservation_id: str

class User(BaseModel):
    user_id: str
    username: str
    email: str

@app.get("/")
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


# IoT Sensors endpoints
@app.post("/sensors/data")
async def receive_sensors_data(data: List[LotSensorData]):
    for lot_data in data:
        lot_id = lot_data.lot_id
        if lot_id not in sensors_data:
            sensors_data[lot_id] = {}
        for spot_id, status in lot_data.sensors.items():
            sensors_data[lot_id][spot_id] = status
    # return sensors_data # uncomment this line to see the data in all parking lots 
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
    sensors_data[lot_id][spot_id] = True
    total_cost = reservation.current_pricing * reservation.duration
    reservation_data = reservation.dict()
    reservation_data["total_cost"] = total_cost
    reservations_data.append(reservation_data)
    return {"message": "Reservation created successfully", "reservation": reservation, "total_cost": total_cost}

# Pricing Endpoints
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
    users_data.append(user.model_dump())
    return {"message": "User registered successfully", "user": user}

@app.post("/users/login")
async def login_user(username: str = Body(...), password: str = Body(...)):
    return {"message": "User logged in successfully", "username": username}

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
async def delete_user(user_id: str):
    global users_data
    users_data = [u for u in users_data if u['user_id'] != user_id]
    return {"message": "User deleted successfully"}

# Admin Endpoints
@app.get("/system/status")
async def system_status():
    return {"status": "All systems operational"}

@app.post("/feedback")
async def submit_feedback(feedback: str = Body(...)):
    return {"message": "Feedback received", "feedback": feedback}
