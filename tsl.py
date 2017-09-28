import time, threading, random
from pynput import mouse

MOUSE_LEFT_DOWN = False
GUN_TYPE = 0
GUN_PRESETS = [
	{ 'name': 'm4', 'value': 500 },
	{ 'name': 'm16', 'value': 1000 },
	{ 'name': 'AKM', 'value': 1500 },
	{ 'name': 'UMP9', 'value': 900 },
	{ 'name': 'Uzi', 'value': 1500 },
	{ 'name': 'Groza', 'value': 1100 },
	{ 'name': 'Vector', 'value': 1100}
]

controller = mouse.Controller()

def move_mouse():
	global MOUSE_LEFT_DOWN, GUN_PRESETS, GUN_TYPE
	cooldown = 0.01
	while True:
		if MOUSE_LEFT_DOWN:
			distance = GUN_PRESETS[GUN_TYPE]['value'] * cooldown
			controller.move(0, int(distance + random.uniform(-0.3, 0.3)))
			cooldown = random.uniform(0, 0.05)
		time.sleep(cooldown)

def on_click(x, y, button, pressed):
	global MOUSE_LEFT_DOWN
	MOUSE_LEFT_DOWN = pressed

def on_scroll(x, y, dx, dy):
	global GUN_TYPE, GUN_PRESETS
	if dy < 0 and GUN_TYPE > 0:
		GUN_TYPE -= 1
	elif dy > 0 and GUN_TYPE < len(GUN_PRESETS) - 1:
		GUN_TYPE += 1
	print 'Weapon mode switched to %s' % GUN_PRESETS[GUN_TYPE]['name']

t = threading.Thread(target=move_mouse)
t.setDaemon(True)
t.start()

# Collect events until released
with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()