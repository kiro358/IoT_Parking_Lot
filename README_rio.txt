some notes based on what i've done:

changes to server.py: 

    changed the List in the LotSensorData class to be a Dict instead
also changed:
        # if lot_id not in sensors_data:
        if sensors_data.get(lot_id) is None:






the data format i will be sending is: 
sensors_data = {}  # Format: {lot_id: {spot_id: bool}}

that being said, the lots themselves are never 'instantiated' or capped 
so for now im operating on the assumption that as a car "parks" it 
sends a payload json to <localhost>/sensors/data with the bool set to 'True',
to handle the instantiation issue i mentioned above, we can just check if
sensor_data[lot_id][spot_id] exists, a good way to do this is with the python dictionary
function .get(), which you can use like this: 

    sensor_data[lot_id].get(spot_id)   : returns the value of sensor_data[lot_id][spot_id] if it exists, otherwise returns 'None'






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





## suggestion for algorithm : 
take percent of spots taken like : # of spots take / # of spots instantiated 
use that as a cost multiplier or something like : flat_rate + ( multiplier * $0.50 ) 

we could argue it doesnt matter that this will not consider uninstantiated spots because we could say that means the lot_data
has low traffic  -\_0_/-

