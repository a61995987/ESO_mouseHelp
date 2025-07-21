#coding=utf-8
#import libs 
from click_ui import Ui_MainWindow
from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener
import gpt
import threading

#Add your Varial Here: (Keep This Line of comments)
#Define UI Class
class  main:
    def __init__(self):
        super(main,self).__init__()
        self.setup

def listener_def():
    with Listener(on_click=gpt.on_click) as listener:
        with KeyboardListener(on_release=gpt.on_key_release) as keyboard_listener:
            listener.join()
            keyboard_listener.join()
#Create the root of Kinter 
if  __name__ == '__main__':
    root = tkinter.Tk()
    MyDlg = click(root)
    listenner_thread = threading.Thread(target=listener_def)
    listenner_thread.start()
    root.mainloop()
