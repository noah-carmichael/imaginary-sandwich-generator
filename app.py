from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import threading
import os
from time import sleep
from gpiozero import Button, LED, Buzzer, PWMLED
import RPi.GPIO as GPIO
import time
import busio
import board
import requests
from PIL import Image
from io import BytesIO
import random
import subprocess

# analog
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
photoRes = AnalogIn(ads, ADS.P0)


button = Button(19)
global led
led = PWMLED(21)
buzzer = Buzzer(13)
doBuzz = True
ledValue = 1
# picture number gets changed when picture is taken, so that new pictures can be saved every time
global picture_number
picture_number = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
@app.route('/')
def index():
    return render_template('index.html')

GPIO.setmode(GPIO.BCM)


# this calls an api to change the background to randomly generated noise images
def background():
    # don't make the colours too dark
    r = random.randint(153, 255)
    g = random.randint(153, 255)
    b = random.randint(153, 255)

    # change the sizes of the pixels
    size = random.randint(10, 30)

    # get an image that contains noise, different colour each time
    url = f'https://php-noise.com/noise.php?r=${r}&g=${g}&b=${b}&tiles=${100}&tileSize=${size}&borderWidth=${0}&mode=${1}&json'

    # make request and store image
    response = requests.get(url)
    json_data = response.json()
    image_url = json_data.get('uri')
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.save('static/background.png')

    socketio.emit('updatePic', {'data': f'/static/photo{picture_number}.jpg'})

# flashlight on/off
def light():
    # Read the value from the photoresistor
    while(True):
        phoValue = photoRes.value
        print(f"Photoresistor value: {phoValue}")
        time.sleep(1)
        if phoValue >= 3000:
            socketio.emit('day', {'data': phoValue})
            led.off()
        else:
            socketio.emit('night', {'data': phoValue})
            global ledValue
            print(f"LED value: {ledValue}")
            led.value = ledValue
            print(f"LED value: {led.value}")

light_thread = threading.Thread(target=light)
light_thread.start()


# this is the remote camera button
@socketio.on('button')
def test_message(message):
    # only play buzzer if the user wants to
    print(doBuzz)
    if (doBuzz == True):
        for i in range(20):
            buzzer.on()
            sleep(0.01)
            buzzer.off()
            sleep(0.01)
    # turn off the motion in order to use fswebcam
    subprocess.run(['sudo', 'systemctl', 'stop', 'motion'])
    global picture_number
    picture_number += 1

    os.rename(f'static/photo.jpg', f'static/photo{picture_number}.jpg')
    os.system(f'fswebcam static/photo.jpg')

    subprocess.run(['sudo', 'systemctl', 'start', 'motion'])
    print(f"button: {message}")
    background()
    sleep(2)

    return render_template('index.html')


# set the buzzer to go off or on
@socketio.on('changeBuzzer')
def buzz(message):
    global doBuzz
    doBuzz = not doBuzz
    return render_template('index.html')


# get from input field to adjust flashlight
@socketio.on('adjust brightness')
def buzz(message):
    print(message)
    new_message = int(message.get('inputValue'))
    new_message = new_message/100
    if new_message > 1:
        new_message = 1
    if new_message < 0:
        new_message = 0
    print(new_message)
    global ledValue
    ledValue = new_message
    print(led.value)
    sleep(1)
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    image_names = [img for img in os.listdir('images') if img.endswith(".jpg")]
    print(image_names)
    return render_template('index.html', image_names=image_names)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# this is the button directly attached to the pi
def button_pressed():
    # only play buzzer if the user wants to
    print(doBuzz)
    if (doBuzz == True):
        for i in range(20):
            buzzer.on()
            sleep(0.01)
            buzzer.off()
            sleep(0.01)
    subprocess.run(['sudo', 'systemctl', 'stop', 'motion'])
    global picture_number
    picture_number += 1
    os.rename(f'static/photo.jpg', f'static/photo{picture_number}.jpg')
    os.system(f'fswebcam static/photo.jpg')
    # os.system(f'fswebcam /home/student/mqtt/websocketsTest/static/photo{picture_number}.jpg')
    subprocess.run(['sudo', 'systemctl', 'start', 'motion'])
    background()
    sleep(2)
    # socketio.emit('updatePic', {'data': f'/templates/images/photo{picture_number}.jpg'})
    socketio.emit('button', {'data': 'button pressed'})
    # socketio.emit('button', {'data': f'/static/photo{picture_number}.jpg'})
    
button.when_pressed = button_pressed

# run the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
