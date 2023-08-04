"""
For the first MAX6675 module:

MAX6675 CLK to Pico pin GP2 (Pin 4)
MAX6675 CS to Pico pin GP3 (Pin 5)
MAX6675 DO to Pico pin GP4 (Pin 6)
MAX6675 VCC to Pico 3V3 (Pin 36)
MAX6675 GND to Pico GND (Pin 38)

For the second MAX6675 module:

MAX6675 CLK to Pico pin GP10 (Pin 21)
MAX6675 CS to Pico pin GP11 (Pin 22)
MAX6675 DO to Pico pin GP12 (Pin 24)
MAX6675 VCC to Pico 3V3 (Pin 36)
MAX6675 GND to Pico GND (Pin 38)
"""

import ujson as json
import websocket
import max6675

# Constants for your Artisan Roast server details
WEBSOCKET_SERVER_URL = "ws://your-artisan-roast-server.com/ws"
WEBSOCKET_PORT = 80


# Function to read temperature from MAX6675
def read_temperature(cs_pin):
    cs = machine.Pin(cs_pin, machine.Pin.OUT)
    thermocouple = max6675.MAX6675(machine.SPI(0), cs)

    try:
        temp = thermocouple.read()
        return temp
    except max6675.MAX6675Error:
        # If an error occurs during communication, return None
        return None

# Initialize CS pins for both MAX6675 modules
cs_pin_1 = 3
cs_pin_2 = 11

def on_open(ws):
    print("WebSocket connection established.")

def on_message(ws, message):
    # Process incoming message from the server
    data = json.loads(message)
    if "command" in data and data["command"] == "getData":
        # If the server requests data, send the temperature readings
        bt_temperature = read_temperature(cs_pin_1)
        et_temperature = read_temperature(cs_pin_2)
        send_data(data["id"], bt_temperature, et_temperature)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed.")

def read_bean_temperature():
    # Implement your code to read bean temperature data from the BT sensor
    bt_temperature = max6675.read_temp()  # You'll need to adapt this based on your max6675.py library
    return bt_temperature

def read_environment_temperature():
    # Implement your code to read environment temperature data from the ET sensor
    # Return a sample value for demonstration purposes
    et_temperature = 22.5
    return et_temperature

def send_data(request_id, bt_temperature, et_temperature):
    # Create the response message with the provided data
    response_data = {
        "id": request_id,
        "data": {
            "BT": bt_temperature,
            "ET": et_temperature
        }
    }
    message = json.dumps(response_data)
    ws.send(message)

if __name__ == "__main__":
    # Establish WebSocket connection to Artisan Roast server
    ws = websocket.WebSocketApp(WEBSOCKET_SERVER_URL, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

    # Main loop (if needed)
    while True:
        # Perform any other tasks if required
        pass
