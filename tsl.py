import time, threading, random
from pynput import mouse, keyboard

GUN_TYPE = 0
GUN_PRESETS = [
	{ 'name': 'M4', 'delta': 15, 'cd': 0.086 },
	{ 'name': 'M16', 'delta': 11, 'cd': 0.075 },
	{ 'name': 'Scarl', 'delta': 19, 'cd': 0.096 },
	{ 'name': 'Mini14', 'delta': 11.2, 'cd': 0.1 },
	{ 'name': 'AKM', 'delta': 15, 'cd': 0.1 },
	{ 'name': 'UMP9', 'delta': 15, 'cd': 0.092 },
	{ 'name': 'Uzi', 'delta': 15, 'cd': 0.048 }
]

ON = False
TEST_MODE = False

MOUSE_LEFT_DOWN = False
MOUSE_RIGHT_DOWN = False
CLICK_SENT_BY_SCRIPT = 0

MOUSE_Y_DELTA = 15

controller = mouse.Controller()

def init_keyboard():
	def on_press(key):
		global ON, TEST_MODE, MOUSE_Y_DELTA, GUN_TYPE, GUN_PRESETS
		# turnOn/Off
		if key == keyboard.Key.f7:
			ON = not ON
			print 'Program %s' % ('ON' if ON else 'OFF')
		# do not handle other input when off
		if not ON:
			return True
		# switch test mode
		if key == keyboard.Key.f8:
			TEST_MODE = not TEST_MODE
			if TEST_MODE:
				print 'Test mode %s' % ('ON' if TEST_MODE else 'OFF')
		# page up
		elif key == keyboard.Key.page_up:
			if TEST_MODE:
				MOUSE_Y_DELTA += 1
				print 'Current mouse delta: %s' % MOUSE_Y_DELTA
			elif GUN_TYPE < len(GUN_PRESETS) - 1:
				GUN_TYPE += 1
				print 'Weapon mode switched to %s' % GUN_PRESETS[GUN_TYPE]['name']
		# page down
		elif key == keyboard.Key.page_down:
			if TEST_MODE:
				MOUSE_Y_DELTA -= 1
				print 'Current mouse delta: %s' % MOUSE_Y_DELTA
			elif GUN_TYPE > 0 :
				GUN_TYPE -= 1
				print 'Weapon mode switched to %s' % GUN_PRESETS[GUN_TYPE]['name']

	with keyboard.Listener(on_press=on_press) as listener:
	    listener.join()

k = threading.Thread(target=init_keyboard)
k.setDaemon(True)
k.start()

# --

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
	global MOUSE_LEFT_DOWN, CLICK_SENT_BY_SCRIPT, GUN_PRESETS, GUN_TYPE
	cooldown = 0.225
	while True:
		if MOUSE_LEFT_DOWN and GUN_PRESETS[GUN_TYPE]['name'] == 'M16':
			CLICK_SENT_BY_SCRIPT += 2
			controller.click(mouse.Button.left)
			cooldown = random.uniform(0.001, 0.225)
		time.sleep(cooldown)

t2 = threading.Thread(target=click_mouse)
t2.setDaemon(True)
t2.start()

# --

def on_click(x, y, button, pressed):
	global MOUSE_LEFT_DOWN, MOUSE_RIGHT_DOWN, CLICK_SENT_BY_SCRIPT
	if button == mouse.Button.left:
		# don't handle auto-sent left down
		if CLICK_SENT_BY_SCRIPT > 0:
			CLICK_SENT_BY_SCRIPT -= 1
		else:
			MOUSE_LEFT_DOWN = pressed
	elif button == mouse.Button.right and pressed:
		# change mouse right state
		MOUSE_RIGHT_DOWN = not MOUSE_RIGHT_DOWN

# listen
with mouse.Listener(on_click=on_click) as listener:
    listener.join()