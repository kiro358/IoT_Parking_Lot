import requests

def send_sensor_data(lot_id, spot_number, status):
    url = "http://127.0.0.1:8000/sensors/data"  # Assuming the server is running locally on port 8000
    payload = [{"lot_id": lot_id, "sensors": {spot_number: status}}]
    response = requests.post(url, json=payload)
    return response.json()

while True:
    command = input("Enter command ('enter' or 'leave') followed by lot_id and spot_number (e.g., 'enter 1 2'): ")
    parts = command.split()
    if len(parts) == 3:
        action, lot_id, spot_number = parts
        lot_id = int(lot_id)
        spot_number = int(spot_number)
        if action == "enter":
            status = True
        elif action == "leave":
            status = False
        else:
            print("Invalid command. Please enter 'enter' or 'leave'.")
            continue
        response = send_sensor_data(lot_id, spot_number, status)
        # response = {"lot_id": lot_id, spot_number : status}
        print(response)
    else:
        print("Invalid command format. Please enter in the format: 'enter/leave <lot_id> <spot_number>'.")
