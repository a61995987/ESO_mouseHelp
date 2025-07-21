import threading
from pynput.mouse import Button,Controller as MouseController
from pynput.keyboard import Key ,Controller as KeyboardController
import time
import os
import pygame
from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener

# 用于记录鼠标左键点击次数和连续点击的间隔时间
click_count = 0
last_click_time = time.time()
os.system("cls")
# 用于控制连续点击的线程是否运行
running_continuous_click = False
# 记录大写锁定键的状态 因ctypes有时会不准确 故使用此方法
caps_lock_state = False
#音频线程锁
audio_lock = threading.Lock()
#初始化鼠标按键时间
left_click_press_time = None
key_hold_time = 0
# 定义定时器对象
timer = None
#初始化鼠标按住状态
left_pressed = False

#音频播放逻辑
def play_sound(audio_file_path):
    audio_lock.acquire()
    try:
        # 加载音频文件
        sound = pygame.mixer.Sound(audio_file_path)
        # 播放音频
        sound.play()
    finally:
        audio_lock.release()

def update_hold_time():
    global key_hold_time,left_click_press_time,left_pressed
    while left_click_press_time is not None:
        key_hold_time = time.time() - left_click_press_time
        print(key_hold_time)
        if key_hold_time >=1 and not left_pressed:
            audio_file_path = "tik.mp3"
            audio_thread = threading.Thread(target=play_sound, args=(audio_file_path,))
            audio_thread.start()
            left_click_press_time = None
        time.sleep(0.1)  # 更新时间间隔为0.1秒

def on_key_release(key):
    global caps_lock_state

    if key == Key.caps_lock and not caps_lock_state:
        audio_file_path = "tik.mp3"
        audio_thread = threading.Thread(target=play_sound, args=(audio_file_path,))
        audio_thread.start()
        caps_lock_state = True        
        hold_shift_key_thread = threading.Thread(target=hold_shift_key)
        hold_shift_key_thread.start()
    elif key == Key.caps_lock and caps_lock_state:
        audio_file_path = "tok.mp3"
        audio_thread = threading.Thread(target=play_sound, args=(audio_file_path,))
        audio_thread.start()
        caps_lock_state = False
        end_hold_shift_key_thread = threading.Thread(target=end_hold_shift_key)
        end_hold_shift_key_thread.start()

def on_click(x, y, button, pressed):
    global click_count, last_click_time, running_continuous_click, left_click_press_time, key_hold_time, timer, left_pressed

    if button == Button.left and not pressed:
        current_time = time.time()
        click_interval = current_time - last_click_time
        last_click_time = current_time

        if click_interval < 0.2:
            click_count += 1
        else:
            click_count = 1
        if click_count >= 3:
            if not running_continuous_click:
                # 启动连续点击线程
                running_continuous_click = True
                continuous_click_thread = threading.Thread(target=continuous_click)
                continuous_click_thread.start()
            click_count = 0  # 重置点击次数
        if key_hold_time < 1 and not left_pressed:
            left_click_press_time = None
            key_hold_time = 0  # 重置按键按住的时间
        elif key_hold_time >= 1 and not left_pressed:
            left_pressed = True
            hold_letf_button_thread = threading.Thread(target=hold_letf_button)
            hold_letf_button_thread.start()
    elif button == Button.left and pressed:
        if left_click_press_time is None and not left_pressed:
            left_click_press_time = time.time()
            timer = threading.Thread(target=update_hold_time)
            timer.start()

    elif button == Button.right and pressed and (running_continuous_click or left_pressed):
        audio_file_path = "tok.mp3"
        audio_thread = threading.Thread(target=play_sound, args=(audio_file_path,))
        audio_thread.start()
        end_of_mouse_thread = threading.Thread(target=end_of_mouse)
        end_of_mouse_thread.start()

def continuous_click():
    global running_continuous_click, click_count

    audio_file_path = "tik.mp3"
    audio_thread = threading.Thread(target=play_sound, args=(audio_file_path,))
    audio_thread.start()
    # 鼠标连点逻辑
    while running_continuous_click:
        MouseController().click(Button.left)
        time.sleep(0.1)

    # 重置点击次数和连续点击状态
    click_count = 0
    running_continuous_click = False

def hold_letf_button():
    MouseController().press(Button.left)

def end_of_mouse():
    global running_continuous_click,click_count,left_pressed
    # 停止所有鼠标线程
    MouseController().release(Button.left)
    running_continuous_click = False
    click_count = 0  # 重置点击次数
    left_pressed = False
    
def hold_shift_key():
    KeyboardController().press(Key.shift)

def end_hold_shift_key():
    KeyboardController().release(Key.shift)

class Main_Logic():
    @staticmethod
    def listener_def():
        with Listener(on_click=on_click) as listener, \
                KeyboardListener(on_release=on_key_release) as keyboard_listener:
            listener.join()
            keyboard_listener.join()