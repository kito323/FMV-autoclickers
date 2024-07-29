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

# print(pyautogui.__version__) 

np.set_printoptions(linewidth=400)
  
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

        borderChar = "###"
        emptyChar = "___"
        def getEmptyBoard():
            dimX = 18; dimY = 17
            board = np.empty([dimX, dimY], dtype='<U3')
            board[:, :] = emptyChar
            # print(board[:2, :2])
            # Remove corners
            for x in range(9, dimX):
                for y in range(x-9+1):
                    board[x, y] = borderChar
            for y in range(9, dimY):
                for x in range(y-9+1):
                    board[x, y] = borderChar
            # Railroads and station
            board[:, 9] = borderChar
            board[4:8, 7:9] = borderChar
            board[:10, 10:12] = borderChar
            board[10, 10] = borderChar
            # Northen end
            board[-2:, -1] = borderChar
            return board

        # Entities
        lstEnts = []
        speciesCounts = [6, 4]
        for i, letter in enumerate(["A", "B"]):
            for j in range(1, speciesCounts[i]+1):
                for k in range(1, 4):
                    lstEnts.append(letter+str(j)+str(k))
        print(lstEnts)

        # space conversions
        def imgpx2mtxID(locs, o, dXY):
            # locs  - array of coordinate vectors in pixel coordinates (whole screen)
            # o     - tuple (as numpy array?) of (0,0) origin in pixel coordinates (whole screen)
            # dXY   - tuple (as numpy array?) of step sizes in pixel coordinates
            # mtxID - array of id vectors in matrix coordinates
            
            # ID locations on screen
            imgID = np.rint((locs - o)/dXY).astype(int)

            # convert screen IDs to matrix IDs
            mtxID = imgID.copy()
            mtxID[:, 0] = (imgID[:, 0] + imgID[:, 1])/2 # (x+y)/2
            mtxID[:, 1] = (-imgID[:, 0] + imgID[:, 1])/2 # (-x+y)/2

            return np.rint(mtxID).astype(int) # make sure that int
        
        def mtxID2imgpx(mtxID, o, dXY):
            # mtxID - array of id vectors in matrix coordinates
            # o     - tuple (as numpy array?) of (0,0) origin in pixel coordinates (whole screen)
            # dXY   - tuple (as numpy array?) of step sizes in pixel coordinates
            # locs  - array of coordinate vectors in pixel coordinates (whole screen)
            
            # matrix IDs to image IDs
            imgID = mtxID.copy()
            imgID[:, 0] = mtxID[:, 0] - mtxID[:, 1] # x-y
            imgID[:, 1] = mtxID[:, 0] + mtxID[:, 1] # x+y

            # image IDs to screen locations
            locs = imgID*dXY + o

            return np.rint(locs).astype(int) # make sure that int
        
        # Uniqueness
        def uniques(arr, opt=None):
            # Should work with both ID and screen locs coordinates but in later has to be pixel perfect to find duplicate
            _, arrUniqueIDs = np.unique(arr, axis=0, return_index=True)
            if len(arrUniqueIDs) != len(arr):
                print("Less unique values", opt, arrUniqueIDs)
                # print(arr, arrUniqueIDs) # print only the duplicate situation info
            return arrUniqueIDs

        # Moves
        def AtoB(A, B=None):
            if B is None:
                AtoB(A[0], A[1])
            else:
                pyautogui.moveTo(tuple(A))
                pyautogui.mouseDown()
                pyautogui.moveTo(tuple(B))
                time.sleep(0.4) # sleep after movement before releasing is actually faster because dragging is laggy and insta-release drops things at wrong places
                pyautogui.mouseUp()
            return None

        # Set regions (used in fast-finding) to default None
        regionIconWhack = None
        
        while self.program_running:
            while self.running:
                time.sleep(1)
                # Clicking Timeturning
                if doTimeturning:
                    # try:
                    # Swap to discord if not on it already
                    if mainWindow.isMinimized: mainWindow.restore() # Do not maximise, just undo minimzation
                    if not mainWindow.isActive: mainWindow.activate() # Can be not minimized and also not active at the same time
                    # Set approriate constant window size and position if not yet done
                    if not mainWindow.width == 1100: mainWindow.width = 1100
                    if not mainWindow.height == 1040: mainWindow.height = 1040
                    if not mainWindow.right == 1920: mainWindow.right = 1920
                    if not mainWindow.bottom == 1040: mainWindow.bottom = 1040
                    # mainWindow.bottomright = (1920, 1040) # screen res
                    # print(mainWindow.topleft, mainWindow.bottomright)
                    time.sleep(1)

                    # Find anchor and use it to calculate steps delta x and y in pixels
                    anchor1 = np.array(pyautogui.locateCenterOnScreen("merge/Anchor_-3_12.png", confidence=0.9))
                    anchor2 = np.array(pyautogui.locateCenterOnScreen("merge/Anchor_8_30.png", confidence=0.9))
                    # print(anchor1, anchor2)
                    deltaXY = (anchor2-anchor1)/(8-(-3), 30-12)
                    # print(deltaXY)
                    # pyautogui.press("k"); break

                    # Get origin (0,0) location
                    origin = anchor1 + (3, -12)*deltaXY
                    # print(origin)

                    # Init gameboard
                    board = getEmptyBoard()
                    # Find the 9 placeholders and confirm they are good to go
                    PHlocs = np.array([pyautogui.center(p) for p in pyautogui.locateAllOnScreen("merge/R11.png", confidence=0.92)])
                    PHid2s = imgpx2mtxID(PHlocs, origin, deltaXY)
                    PHid2sAll = np.stack(np.meshgrid([0,1,2], [0,1,2]), -1).reshape(-1, 2) # Already sorted
                    # print(PHid2sAll == PHid2s[np.lexsort(PHid2s.T)])
                    board[PHid2s[:, 0], PHid2s[:, 1]] = "P00"
                    # Remove duplicates if any
                    PHid2s = PHid2s[uniques(PHid2s, opt="P00")]
                    PHid2s = PHid2s[np.lexsort(PHid2s.T)] # sorted by row, Important to do after uniques
                    # Also have always-empty one with only regular restrictions
                    emptyBoard = board.copy()
                    print(board)
                    print(np.sum(board == emptyChar))
                    if len(PHid2s) == len(PHid2sAll):
                        if not (PHid2sAll == PHid2s).all():
                            print("Placeholders aren't in correct places")
                            print(np.concatenate((PHid2sAll, PHid2s.T), axis=1))
                            continue
                    else:
                        print("Placeholders amount is not correct", len(PHid2s), len(PHid2sAll))
                        continue
                    # pyautogui.press("k"); break

                    # Find items and do merging
                    PHlocsMerg = []
                    totalMerges = 0
                    mergeLocs = mtxID2imgpx(np.array([[0,0], [0,1], [1,0], [1,1], [0,0]]), origin, deltaXY)
                    # print(mergeCount, mergeLocs)
                    print(sorted(lstEnts, key=lambda x:x[2]))
                    for name in sorted(lstEnts, key=lambda x:x[2]):
                        time.sleep(1.5)
                        if not self.running: break # Include after things that might take awhile within single iteration
                        try:
                            # lvl 3 cow tends to fail by scrolling map up
                            # UPDATE: it is because it recognises some of them twice. ~~Better leave unrecognised than match twice (raise confidence)~~
                            # lower confidence is OK, if later duplicates are removed using coordinate transformations
                            locs = np.array([pyautogui.center(p) for p in pyautogui.locateAllOnScreen("merge/" + name + ".png", confidence=0.84)])
                            ID2s = imgpx2mtxID(locs, origin, deltaXY)
                            if any:
                                pass
                        except:
                            print("Didnt find any:", name) # Can be that no instances of the specific type (aka. name) are on the field, but it is OK to happen especially with higher lvl ones
                            continue
                        time.sleep(1)
                        # if name == "B23":
                        #     print(np.array(locs))
                        #     time.sleep(3)
                        #     for p in locs:
                        #         pyautogui.moveTo(tuple(p))
                        #         time.sleep(3)
                        
                        if not (emptyBoard[ID2s[:, 0], ID2s[:, 1]] == emptyChar).all():
                            if not (getEmptyBoard()[ID2s[:, 0], ID2s[:, 1]] == emptyChar).all():
                                print("Found '" + name + "' item in placeholder area. Skipping it...")
                                continue
                            print("Found '" + name + "' item in restricted area. Stopping program...")
                            print(ID2s)
                            pyautogui.press("k"); break
                        board[ID2s[:, 0], ID2s[:, 1]] = name
                        # Remove duplicates if any
                        ID2UniqueIDs = uniques(ID2s, opt=name)
                        locs = locs[ID2UniqueIDs] # locs and ID2s are equivalent arrays in different coordinate systems

                        # Merging
                        mergeCount = 0
                        for i, loc in enumerate(locs):
                            if len(locs)-i < 5 and mergeCount == 0: break # how many instances left (including current) < 5 while new merging cycle starts
                            time.sleep(0.2)
                            # if name == "B23": time.sleep(2)
                            AtoB(loc, mergeLocs[mergeCount])
                            if mergeCount == 4:
                                # After merging lvl 3 entities click on the majority level 4 results to get the produce of level 5
                                # They might also need special handling at some point
                                if name[2] == "3":
                                    for mergeLoc in mergeLocs[:-1]:
                                        time.sleep(1)
                                        pyautogui.click(mergeLoc[0], mergeLoc[1])
                                mergeCount = 0
                                totalMerges += 1
                            else: mergeCount += 1
                            
                            # Where placeholders go
                            if len(PHlocsMerg) < 4:
                                PHlocsMerg.append(loc)
                                if len(PHlocsMerg) == 4:
                                    PHlocsMerg = np.array(PHlocsMerg)
                                    # break # temp break when four moved
                    
                    if not self.running: break # Include after things that might take awhile within single iteration

                    # Move placeholders back where they should be
                    print(imgpx2mtxID(PHlocsMerg, origin, deltaXY))
                    for i, PHlocMerg in enumerate(PHlocsMerg): AtoB(PHlocMerg, mergeLocs[i])

                    print(board)
                    # Move leftover movables to the far corner
                    leftOvers = np.argwhere(board == emptyChar)
                    try:
                        clocks = imgpx2mtxID(np.array([pyautogui.center(p) for p in pyautogui.locateAllOnScreen("merge/E11.png", confidence=0.95)]), origin, deltaXY)
                    except:
                        print("Didnt find any:", name) # Can be that no instances are on the field, but it is OK
                        continue
                    leftOvers = mtxID2imgpx(np.unique(np.concatenate((leftOvers, clocks), axis=0), axis = 0), origin, deltaXY)
                    # leftOvers = leftOvers[np.lexsort(leftOvers.T)] # sorted by row
                    openSpots = mtxID2imgpx(np.argwhere(emptyBoard == emptyChar)[::-1], origin, deltaXY)
                    # print(imgpx2mtxID(leftOvers, origin, deltaXY), imgpx2mtxID(openSpots[:5], origin, deltaXY))
                    for openSpot in openSpots:
                        # In case all leftovers have been decided, quit the loop
                        if len(leftOvers) == 0:
                            break
                        leftOverFakeID = (leftOvers == openSpot).all(axis=1).nonzero()[0]
                        # print((leftOvers == openSpot)[:3])
                        # print((leftOvers == openSpot).all(axis=1)[:3])
                        # print(leftOverFakeID)
                        if len(leftOverFakeID) == 0: # Normal moving case
                            time.sleep(0.3)
                            AtoB(leftOvers[0], openSpot)
                            leftOvers = np.delete(leftOvers, 0, axis=0)
                        elif len(leftOverFakeID) == 1: # Case where leftover is already where it should be
                            fakeRowID = leftOverFakeID[0]
                            leftOvers = np.delete(leftOvers, fakeRowID, axis=0)
                        else:
                            print("Something wrong with detecting and moving leftovers:")
                            print(leftOverFakeID, imgpx2mtxID(openSpot, origin, deltaXY))
                    if not self.running: break # Include after things that might take awhile within single iteration

                    time.sleep(2)
                    # Fill board with stuff again
                    for _ in range(10):
                        try:
                            crateLoc = pyautogui.locateCenterOnScreen("merge/K00.png", confidence=0.95) 
                            break
                        except Exception as e: time.sleep(0.2)
                    # divider = 10
                    freeSpaceMulti = 3
                    pyautogui.click(crateLoc, clicks=totalMerges*freeSpaceMulti, interval=0.1)
                    time.sleep(3)
                    if not self.running: break # Include after things that might take awhile within single iteration

                    # mainWindow.minimize()
                    time.sleep(1)

                    # except Exception as e: print("b2", e)
                    if not self.running: break # Include after things that might take awhile within single iteration
                    # pyautogui.press("k"); break
                
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
