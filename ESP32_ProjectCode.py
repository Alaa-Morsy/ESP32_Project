import socket

from machine import pin
import network
import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Alaa Mory'
password = '0158978341'

station = network.WLAN(network.STA_IF)
station.active (True)
station.connect(ssid,password)
while station.isconnected() == False:
	pass
	
print ('Connected Successfully')
print (station.ifconfig())

relay = Pin(27, Pin.OUT)
a = Pin(25, Pin.OUT)
b = Pin(26, Pin.OUT)
c = Pin(18, Pin.OUT)
d = Pin(19, Pin.OUT)
e = Pin(21, Pin.OUT)
f = Pin(33, Pin.OUT)
g = Pin(32, Pin.OUT)

num=0
a.value(0),b.value(0),c.value(0),d.value(0),e.value(0),f.value(0),g.value(1)

def seg_disp(num)
	if num == 0 :
		a.value(0),b.value(0),c.value(0),d.value(0),e.value(0),f.value(0),g.value(1)
	elif num ==1 :
		a.value(1),b.value(0),c.value(0),d.value(1),e.value(1),f.value(1),g.value(1)
	elif num ==2 :
		a.value(0),b.value(0),c.value(1),d.value(0),e.value(0),f.value(1),g.value(0)
	elif num ==3 :
		a.value(0),b.value(0),c.value(0),d.value(0),e.value(1),f.value(1),g.value(0)
	elif num ==4 :
		a.value(1),b.value(0),c.value(0),d.value(1),e.value(1),f.value(0),g.value(0)
	elif num ==5 :
		a.value(0),b.value(1),c.value(0),d.value(0),e.value(1),f.value(0),g.value(0)
	elif num ==6 :
		a.value(0),b.value(1),c.value(0),d.value(0),e.value(0),f.value(0),g.value(0)
	elif num ==7 :
		a.value(0),b.value(0),c.value(0),d.value(1),e.value(1),f.value(1),g.value(1)
	elif num ==8 :
		a.value(0),b.value(0),c.value(0),d.value(0),e.value(0),f.value(0),g.value(0)
	elif num ==9 :
		a.value(0),b.value(0),c.value(0),d.value(0),e.value(1),f.value(0),g.value(0)


def web_page():
	display= ('%s'% str(num))
	html = """
	<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:Arial; margin: 0px auto; padding-top:30px;text-align: center}
    h1 { font-size: 30px;}
    h2 { font-size: 20px;}
    h3 { font-size: 16px;}
    h4 { font-size: 24px; }
    h5 {font-size: 20px; }

    .button{display: inline-block; background-color: #2196F3; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .switch{position:relative;display:inline-block;width:150px;height:68px}
    .switch input{display:none}
    .slider{position:absolute;top:0;left:0;right:0;bottom:0;background-color:#f56464;border-radius:34px}
    .slider:before{position:absolute;content:"";height:52px;width:52px;left:8px;bottom:8px;
                   background-color:#fff;-webkit-transition:.4s;transition:.4s;border-radius:68px}
    input:checked+.slider{background-color:#90ee90}
    input:checked+.slider:before{-webkit-transform:translateX(80px);-ms-transform:translateX(80px);transform:translateX(80px)}
    </style>
    <script>
    function toggleCheckbox(element) { var xhr = new XMLHttpRequest();
     if(element.checked){ xhr.open("GET", "/?relay=on", true); }
     else { xhr.open("GET", "/?relay=off", true); } 
     xhr.send(); }</script></head>
    <body>
    <h1>Welcome !</h1>
    <h2>  ESP32 Relay Control </h2>
    <h3>This project is prepared by IDs:4 5 214 215 216</h3>
    <p>To Turn the lamp ON/OFF </p>
    <label class="switch">
    <input type="checkbox" onchange="toggleCheckbox(this)" %s>
    <span class="slider"></span></label>
    <h4>7-Segment</h4>
    <h5>Currently Displaying: """ + display +"""</h5>
    <p1><a href="/?Req=1"><button class="button">INC</button></a></p1>
    <p2><a href="/?Req=2"><button class="button button2">DEC</button></a></p2>
    <p><a href="/?Req=3"><button class="button button3">RESET</button></a></p></body></html>"""
	return html
	
s = socket.socket (socket.AF_INET ,socket.SOCK_STREAM)
s.blind(('',80))
s.listen(5)

while True :
	try:
		if gc.mem_free() < 102000:
			gc.collect()
		
		conn, addr = s.accept()
		conn.settimeout(3.0)
		print('Got a connection from %s'% str(addr))
		
		request = conn.recv(1024)
		conn.settimeout(None)
		request = str(request)
		print('Content = %s'% request)
		
		relay_on = request.find('/?relay=on')
		relay_off = request.find('/?relay=off')
		inc = request.find('/?Req=1')
		dec = request.find('/?Req=2')
		reset = request.find('/?Req=3')
		
		if relay_on == 6 :
			relay.value(0)
			
		if relay_off ==6:
			relay.value(1)
			
		if inc == 6:
			num += 1
			seg_disp(num)
		
		if dec == 6:
			num -= 1
			seg_disp(num)
		
		if reset == 6:
			num =0
			seg_disp(num)
			
		response = web_page()
		conn.send('HTTP/1.1 200 OK\n')
		conn.send ('content-Type: text/html\n')
		conn.send('Connection: close \n\n')
		conn.sendall(response)
		conn.close()
		
	except OSError as err:
		conn.close()
		print('Connection closed')