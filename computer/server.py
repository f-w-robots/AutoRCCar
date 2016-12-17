from bottle import route, run, template


import sys
import tornado.websocket
import time
import thread


class RCControl(object):

    def __init__(self):
        # self.serial_port = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)
        self.serial_port = WSSerial()
        print 'started'
        while self.serial_port.no_connected:
            time.sleep(1)
            print 'wait ESP'

    def steer(self, prediction):
        if prediction == "Forward":
            self.serial_port.write(str('20'))
            print("Forward")
        elif prediction == "Left":
            self.serial_port.write(str('12'))
            print("Left")
        elif prediction == "Right":
            self.serial_port.write(str('11'))
            print("Right")
        elif prediction == "On":
            self.serial_port.write(str('001'))
            print("On")
            self.serial_port.write(str('000'))
        elif prediction == "SoundOff":
            self.serial_port.write(str('0001'))
            print("Sounds")
            self.serial_port.write(str('0000'))
        elif prediction == "Reverse":
            self.serial_port.write(str('10'))
            print("Reverse")
        else:
            self.stop()
            # self.serial_port.write(str('0000'))

    def stop(self):
        self.serial_port.write(str('00'))

class Move(object):

    def __init__(self):
        self.rc_car = RCControl()

    def command(self, command):
    	self.rc_car.steer(command)
        time.sleep(1)

class WSSerial(object):
    def __init__(self):
        self.no_connected = True
        class WSHandler(tornado.websocket.WebSocketHandler):
            def check_origin(self, origin):
                return True

            def open(self):
                global weight
                weight.connection = self
                weight.no_connected = False
                print 'connection opened...'

            def on_message(self, message):
                print 'received:', message

            def on_close(self):
                print 'connection closed...'

        application = tornado.web.Application([
            (r'/', WSHandler)
        ])

        global weight
        weight = self

        def someFunc():
            application.listen(3030)
            tornado.ioloop.IOLoop.instance().start()

        thread.start_new_thread(someFunc, ())

    def write(self, chr):
        print 'write'
        self.connection.write_message(chr)




@route('/on')
def index():
	vsh.command('On')
	time.sleep(2)
	vsh.command('SoundOff') #forward
	return "On"

@route('/off')
def index():
	vsh.command('On')
	# time.sleep(2)
	# vsh.command('Off') #forward
	return "Off"

@route('/stop')
def index():
	vsh.command('Stop')
	return "Stop"

@route('/forward')
def index():
	vsh.command('Forward')
	return "Forward"

@route('/reverse')
def index():
	vsh.command('Reverse')
	return "Reverse"


@route('/left')
def index():
	vsh.command('Left')
	return "Left"

@route('/right')
def index():
	vsh.command('Right')
	return "Right"

global vsh
vsh = Move()
run(host='192.168.43.198', port=3000)
