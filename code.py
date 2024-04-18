from time import sleep, time as now
import board
import digitalio
import rotaryio
import pwmio
import usb_hid
from lib.keyboard import Keyboard
from lib.mouse import Mouse
from lib.keycode import Keycode
from lib.consumer_control import ConsumerControl
from lib.consumer_control_code import ConsumerControlCode


class Button(object):
    def __init__(self, button):
        self.button = button
        self.state_last = self.button.value

    def handle(self):
        self.state_last = self.button.value

    @property
    def rising(self):
        if self.state_last != self.button.value and self.button.value is True:
            return True
        else:
            return False

    @property
    def falling(self):
        if self.state_last != self.button.value and self.button.value is False:
            return True
        else:
            return False
        
    @property
    def value(self):
        return self.button.value


kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
m = Mouse(usb_hid.devices)

button_prev = Button(digitalio.DigitalInOut(board.GP12))
button_prev.button.switch_to_input(pull=digitalio.Pull.UP)

button_play = Button(digitalio.DigitalInOut(board.GP13))
button_play.button.switch_to_input(pull=digitalio.Pull.UP)

button_next = Button(digitalio.DigitalInOut(board.GP14))
button_next.button.switch_to_input(pull=digitalio.Pull.UP)

button_enter = Button(digitalio.DigitalInOut(board.GP15))
button_enter.button.switch_to_input(pull=digitalio.Pull.UP)

# rotary_a = Button(digitalio.DigitalInOut(board.GP6))
# rotary_a.button.switch_to_input(pull=digitalio.Pull.UP)
# 
# rotary_b = Button(digitalio.DigitalInOut(board.GP7))
# rotary_b.button.switch_to_input(pull=digitalio.Pull.UP)

# rotary_button = Button(digitalio.DigitalInOut(board.GP8))
# rotary_button.button.switch_to_input(pull=digitalio.Pull.UP)

led_r = digitalio.DigitalInOut(board.GP11)
led_b = digitalio.DigitalInOut(board.GP9)

led_r.direction = digitalio.Direction.OUTPUT
led_b.direction = digitalio.Direction.OUTPUT

led_g = pwmio.PWMOut(board.GP10, frequency=5000, duty_cycle=0)

counter = 0
led_g_state = False

loop_counter = 0
moved_left = False
moved_right = True
mouse_automove = False
mouse_automove_time = now()
mouse_automove_interval = 1.0
mouse_step = 3
led_b.value = False
#dzialajtykurwo
try:
    print("Code start")
except:
    pass


while True:
    if button_play.rising:
        try:
            print("Button pushed!", counter)
        except:
            pass

        counter += 1
        cc.send(ConsumerControlCode.PLAY_PAUSE)

    if button_prev.rising:
        try:
            print("Button pushed!", counter)
        except:
            pass
        counter += 1
        cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)

    if button_next.rising:
        try:
            print("Button pushed!", counter)
        except:
            pass
        counter += 1
        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        
#     if rotary_a.rising:
#         if rotary_b.value:            
#             try:
#                 print("A rising B ON", counter)
#                 print("Volume up A!", counter)
#             except:
#                 pass
#             counter += 1
#             cc.send(ConsumerControlCode.VOLUME_DECREMENT)
# 
#         else:
#             try:
#                 print("A rising B OFF", counter)
#                 print("Volume down A!", counter)
#             except:
#                 pass
#             counter += 1
#             cc.send(ConsumerControlCode.VOLUME_INCREMENT)
#             
#     if rotary_a.falling:
#         if rotary_b.value:            
#             try:
#                 print("A falling B ON", counter)
#                 print("Volume up A!", counter)
#             except:
#                 pass
#             counter += 1
#             cc.send(ConsumerControlCode.VOLUME_INCREMENT)
# 
#         else:
#             try:
#                 print("A falling B OFF", counter)
#                 print("Volume down A!", counter)
#             except:
#                 pass
#             counter += 1
#             cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            

            
#     if rotary_a.falling:
#         if rotary_b.value:
#             try:
#                 print("Volume down B!", counter)
#             except:
#                 pass
#             counter += 1
#             cc.send(ConsumerControlCode.VOLUME_DECREMENT)

    if button_enter.rising:
        try:
            print("Button pushed!", counter)
        except:
            pass
        counter += 1
        mouse_automove = not mouse_automove
        if mouse_automove:
            mouse_automove_time = now()
            try:
                print("Automove ON")
            except:
                pass
        else:
            mouse_automove_time = now()
            try:
                print("Automove OFF")
            except:
                pass
            

    if mouse_automove:
        led_b.value = False
        if now() - mouse_automove_time > mouse_automove_interval:
            try:
                print("MOVE ", end='')
            except:
                pass
            led_g_state = not led_g_state
            if led_g_state:
                led_g.duty_cycle = int(65535/100)
            else:
                led_g.duty_cycle = 0
            mouse_automove_time = now()
            if moved_left is True and moved_right is False:
                try:
                    print("RIGHT")
                except:
                    pass
                moved_left = False
                moved_right = True
                m.move(mouse_step, 0, 0)

            elif moved_left is False and moved_right is True:
                try:
                    print("LEFT")
                except:
                    pass
                moved_left = True
                moved_right = False
                m.move(-mouse_step, 0, 0)

    else:
        led_g.duty_cycle = 0
        #led_b.value = True

    button_play.handle()
    button_prev.handle()
    button_next.handle()
    button_enter.handle()
#     rotary_a.handle()
#     rotary_b.handle()
#     rotary_button.handle()
    sleep(0.01)

