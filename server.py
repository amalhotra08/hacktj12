import io
import base64
import numpy as np
from PIL import Image
from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

CONNECTED_DEVICES = {}

f = open("coordinates.txt", "w")
@sock.route('/ws/location/<dname>')
def echo(ws, dname):
    if dname not in CONNECTED_DEVICES:
        print(f"New device Detected: {dname}")
        CONNECTED_DEVICES[dname] = []
    
    f = open(f"{dname}.txt", "w")
    while True:
        data = ws.receive()
        data = eval(data)

        f.write(f"{data['x']} {data['y']} {data['z']} \n")
        f.flush()
        """data = {key:float(value) for key, value in data.items()}
        print((data))
        ws.send(f"Server received: {data}")
        print(f"I was sent {data} by {dname}") 
        CONNECTED_DEVICES[dname].append(data)
        f.write(f"{data['lat']} {data['long']}\n")
        f.flush()"""
        #f.write(f"{data['lat']} {data['long']}\n")
        #f.flush()
        print(CONNECTED_DEVICES)

@sock.route('/ws/img/<deviceclass>')
def path(ws, deviceclass):
    while True:
        data = ws.receive()
        if not data:
            break

        print("Received image from client")

        image_data = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_data))

        np_image = np.array(image.convert("L"))

        processed_image = Image.fromarray(np_image)

        buffered = io.BytesIO()
        processed_image.save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode("utf-8")

        ws.send(encoded_img)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
