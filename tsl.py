import time, threading, random
from pynput import mouse

TEST_MODE = True

GUN_TYPE = 0
GUN_PRESETS = [
	{ 'name': 'M4', 'delta': 15, 'cd': 0.086 },
	{ 'name': 'M16', 'delta': 11, 'cd': 0.075 },
	{ 'name': 'Scarl', 'delta': 15, 'cd': 0.096 },
	{ 'name': 'AKM', 'delta': 15, 'cd': 0.1 },
	{ 'name': 'UMP9', 'delta': 15, 'cd': 0.092 },
	{ 'name': 'Uzi', 'delta': 15, 'cd': 0.048 }
]

MOUSE_LEFT_DOWN = False
MOUSE_RIGHT_DOWN = False

MOUSE_Y_DELTA = 15

controller = mouse.Controller()

def move_mouse():
	global TEST_MODE, MOUSE_Y_DELTA, MOUSE_LEFT_DOWN, MOUSE_RIGHT_DOWN, GUN_PRESETS, GUN_TYPE
	while True:
		if MOUSE_LEFT_DOWN and MOUSE_RIGHT_DOWN:
			controller.move(0, GUN_PRESETS[GUN_TYPE]['delta'] if not TEST_MODE else MOUSE_Y_DELTA)
		time.sleep(GUN_PRESETS[GUN_TYPE]['cd'] if not TEST_MODE else 0.1)

t = threading.Thread(target=move_mouse)
t.setDaemon(True)
t.start()

# --
# auto send click for M16A4
def click_mouse():
	global MOUSE_LEFT_DOWN, GUN_PRESETS, GUN_TYPE
	cooldown = 0.24
	while True:
		if MOUSE_LEFT_DOWN and GUN_PRESETS[GUN_TYPE]['name'] == 'm16':
			controller.click(mouse.Button.left)
			cooldown = Math.uniform(0.2, 0.5)
		time.sleep(cooldown)

t2 = threading.Thread(target=click_mouse)
t2.setDaemon(True)
t2.start()

# --

def on_click(x, y, button, pressed):
	global MOUSE_LEFT_DOWN, MOUSE_RIGHT_DOWN
	if button == mouse.Button.left:
		MOUSE_LEFT_DOWN = pressed
	elif button == mouse.Button.right and pressed:
		# change mouse right state
		MOUSE_RIGHT_DOWN = not MOUSE_RIGHT_DOWN

def on_scroll(x, y, dx, dy):
	global TEST_MODE, MOUSE_Y_DELTA, GUN_TYPE, GUN_PRESETS
	if not TEST_MODE:
		# normal mode: scroll to switch weapon presets
		if dy < 0 and GUN_TYPE > 0:
			GUN_TYPE -= 1
		elif dy > 0 and GUN_TYPE < len(GUN_PRESETS) - 1:
			GUN_TYPE += 1
		print 'Weapon mode switched to %s' % GUN_PRESETS[GUN_TYPE]['name']
	else:
		# test mode: scroll to incr/decr y delta
		if dy < 0 and MOUSE_Y_DELTA > 0:
			MOUSE_Y_DELTA -= 1
		elif dy > 0:
			MOUSE_Y_DELTA += 1
		print 'Current mouse delta: %s' % MOUSE_Y_DELTA


# listen
with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()