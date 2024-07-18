# importing time and threading 
import time 
import threading 
from pynput.mouse import Button, Controller 
import pyautogui
import numpy as np
from pyscreeze import Box
import PIL
PIL.Image.ANTIALIAS = PIL.Image.LANCZOS # Cuz some version mismaches and ANTIALIAS is depricated

# pynput.keyboard is used to watch events of  
# keyboard for start and stop of auto-clicker 
from pynput.keyboard import Listener, KeyCode 
  
  
# four variables are created to  
# control the auto-clicker
start_stop_key = KeyCode(char='i') # go (i)dle 
stop_key = KeyCode(char='k') # (k)ill program

def modBox(box, left=0, top=0, width=0, height=0):
    # Optional parameters describe the change (addative) from the original
    # move = change left/top; scale (from top left corner) = change width/height
    # scale (from center) = change -x/-y of left/top and 2x/2y of width/height
    return Box(left=box.left+left, top=box.top+top, width=box.width+width, height=box.height+height)

def increaseBox(box, increase=3):
    return modBox(box, left=-increase, top=-increase, width=2*increase, height=2*increase)

# threading.Thread is used  
# to control clicks 
class ClickMouse(threading.Thread): 
    
    def __init__(self): 
        super(ClickMouse, self).__init__()
        self.running = False
        self.program_running = True
  
    def start_clicking(self): 
        self.running = True
  
    def stop_clicking(self): 
        self.running = False
  
    def exit(self): 
        self.stop_clicking() 
        self.program_running = False
  
    # method to check and run loop until  
    # it is true another loop will check  
    # if it is set to true or not,  
    # for mouse click it set to button  
    # and delay. 
    def run(self):
        # foundIconWhack = False
        # # Should the regions be pre-searched? If not, set any of the above to True
        # foundIconWhack = True
        
        doTimeturning = True
        # Which parts should be active? Set any of the above to False if you do not want to include them
        # doInv = doRestart = False

        lstWindows = pyautogui.getWindowsWithTitle(" Discord")
        print(lstWindows)
        print([win.title for win in lstWindows])
        mainWindow = lstWindows[0]
        # print(settingsWindow)

        numDay = 1
        numMonth = 1

        # Set regions (used in fast-finding) to default None
        regionIconWhack = None
        
        while self.program_running:
            while self.running:
                # Try finding each thing general location first
                    
                # # Timeturning presearch
                # if not foundIconWhack:
                #     try:
                #         regionIconWhack = increaseBox(pyautogui.locateOnScreen("IconWhack.PNG", confidence=0.8))
                #         pyautogui.click(pyautogui.center(regionIconWhack))
                #         for _ in range(5): # To wait the screen to open but no more than X attempts
                #             try:
                #                 regionWhackField = increaseBox(pyautogui.locateOnScreen("WhackField.PNG", confidence=0.8))
                #                 break
                #             except Exception as e: time.sleep(0.2)
                #         else: raise ValueError("Could not pre-find Whack Field! " + e)
                #         pyautogui.alert(text="Found 'Whack' stuff", title='Whack', button='OK', timeout=1000*2)
                #         pyautogui.press("esc")
                #         foundIconWhack = True
                #         print("Found 'Whack' stuff:", regionIconWhack, regionWhackField)
                #     except Exception as e: pass #print(e)
                #     if not self.running: break # Include after things that might take awhile within single iteration
                
                # Clicking Timeturning
                if doTimeturning:
                    try:
                        # pyautogui.press("esc")
                        # print("Wat?")
                        pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonChange.PNG", confidence=0.7, region=regionIconWhack))
                        time.sleep(1)

                        # Update date and click "Change"

                        # Day
                        if numDay <= 28:
                            pyautogui.press("down")
                            numDay += 1
                        else:
                            pyautogui.press("1")
                            numDay = 1
                        pyautogui.press("tab")

                        # Month
                        if numMonth > 12:
                            self.exit()
                            break
                        elif numDay == 1:
                            pyautogui.press("down")
                            numMonth += 1
                        else: pass
                        pyautogui.press("tab", presses=4, interval=0.1)
                        pyautogui.press("enter")
                        print(numDay, numMonth)
                        time.sleep(1)
                        
                        # Swap to discord
                        mainWindow.maximize()
                        time.sleep(1)
                        
                        # Init game
                        pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonLeaveGame.PNG", confidence=0.9, region=regionIconWhack))
                        time.sleep(1)
                        pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonStartGame.PNG", confidence=0.9, region=regionIconWhack))
                        time.sleep(1)
                        pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonStartGame2.PNG", confidence=0.9, region=regionIconWhack))
                        time.sleep(10)

                        if not self.running: break # Optional break-point
                        # In-game actions
                        for _ in range(30): # To wait the screen to open but no more than X attempts
                            try:
                                pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonCollect.PNG", confidence=0.95, region=regionIconWhack))
                                break
                            except Exception as e: time.sleep(1)
                        time.sleep(1)
                        # Try one more time because previous might have not worked as the thing was moving around
                        try:
                            pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonCollect.PNG", confidence=0.9, region=regionIconWhack))
                            print("'Collect' worked 2nd time")
                        except Exception as e: pass

                        time.sleep(2)
                        pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonMarketMain.PNG", confidence=0.95, region=regionIconWhack))
                        
                        time.sleep(1)
                        # Fastclicks
                        for i, button in enumerate(["Free", "Energy", "Free", "Gems", "Free"]):
                            pyautogui.click(pyautogui.locateCenterOnScreen("TimeButtonMarket" + button + ".PNG", confidence=0.7, region=regionIconWhack))
                            time.sleep(0.1)
                        time.sleep(1)

                        mainWindow.minimize()
                        time.sleep(1)

                    except Exception as e: pass #print("b2", e)
                    # if not self.running: break # Include after things that might take awhile within single iteration
                
            time.sleep(1) # When program loops emptily then save recources with longer sleep times
  
  
# instance of mouse controller is created
mouse = Controller() 
click_thread = ClickMouse() 
click_thread.start() 
  
  
# on_press method takes  
# key as argument 
def on_press(key): 
    
  # start_stop_key will stop clicking  
  # if running flag is set to true 
    if key == start_stop_key: 
        if click_thread.running: 
            click_thread.stop_clicking()
        else: 
            click_thread.start_clicking() 
              
    # here exit method is called and when  
    # key is pressed it terminates auto clicker 
    elif key == stop_key: 
        click_thread.exit() 
        listener.stop() 
  
  
with Listener(on_press=on_press) as listener: 
    listener.join()
