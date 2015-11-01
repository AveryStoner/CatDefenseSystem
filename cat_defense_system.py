##
## Code patterns and snippets from:
##   -   Making Games with Python and Pygame by Al Sweigart, 2012
##         http://inventwithpython.com/pygame
##   -   Making games with Pygame by (Tom Chance?), 2003
##         https://www.pygame.org/docs/tut/tom/games6.html

import pygame
# SDL_FBDEV environment variable is required for the Raspberry Pi PiTFT by AdaFruit
import os
os.environ["SDL_FBDEV"] = "/dev/fb1"

# Constants to be used for Raspberry Pi with PiTFT LCD touchscreen
FPS = 15
WIDTH = 320
HEIGHT = 240
WINDOW_SIZE = (WIDTH,HEIGHT)
YOFFSET = 27

# colors are specified using RGB
# see: https://drafts.csswg.org/css-color/
#
# COLOR = (Red, Green, Blue [,alpha])
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (32, 32, 32)
RED = (255, 127, 80)
GREEN = (173, 255, 47)
BLUE = (130, 200, 225)
DARK_BLUE = (0, 0, 128)


# Customize
TITLE_TEXT = "Cat Defense System"
SCANNING_TEXT = "Waiting for Cats..."
ALERT_TEXT = "CATS ARE HERE!!!"
ALERT_SOUND = 'sounds/Alert_2_and_improved.wav'
CODES = ("01907121", "02026993", "01661313", "02225937", "01435009")


def quit_program():
    print "QUIT requested. Shutting down..."
    raise SystemExit

def poll(code,status):
    print "%% mwahahaha %%"
    # put the process to sleep to share CPU and reduce resource consumption while idling
    pygame.time.wait(15)  # time in ms
    for event in pygame.event.get():
        if status.status == "alarming":
            if event.type == pygame.QUIT:
                quit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                code.reset()
                status.change_to_Scanning()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    code.reset()
                    status.change_to_Scanning()
        elif status.status == "scanning":
            if event.type == pygame.QUIT:
                quit_program()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_program()
                elif event.key == pygame.K_RETURN:
                    code.found = code.check_code()
                    if code.found:
                        status.change_to_Alarming()
                        code.reset()
                    else:
                        code.reset()
                elif chr(event.key).isalnum():
                    code.append(chr(event.key))
                    print "debug - code ======= ", code.word        
    return True


class Status:

    def __init__ (self):
        self.change_to_Alarming()

    def change_to_Scanning (self):
        self.textcolor = RED
        self.backgroundcolor = DARK_BLUE
        self.statustext = SCANNING_TEXT
        self.status = "scanning"

    def change_to_Alarming (self):
        self.textcolor = GREEN
        self.backgroundcolor = BLUE
        self.statustext = ALERT_TEXT
        self.status = "alarming"

        
class Code:

    def __init__ (self):
        self.reset()

    def reset (self):
        self.word = ""
        self.found = False

    def check_code (self):
        if self.word in CODES:
            self.found = True
            return True
        else:
            self.found = False
            return False

    def append (self,letter):
        self.word += letter

        
def paint (surface, statusobject):
    newtext = font.render(statusobject.statustext, 1, statusobject.textcolor)
    newtextpos = newtext.get_rect()
    newtextpos.centerx = surface.get_rect().centerx
    newtextpos.centery = surface.get_rect().centery
    pygame.draw.rect(surface, statusobject.backgroundcolor, (0, YOFFSET, WIDTH, HEIGHT))
    surface.blit(newtext, newtextpos)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption('CAT DEFENSE SYSTEM')
    fpsClock = pygame.time.Clock()
    DisplaySurface = pygame.display.set_mode(WINDOW_SIZE)
    DisplaySurface.fill(GREEN)
    font = pygame.font.Font(None, 36)
    title = font.render(TITLE_TEXT, 1, RED)
    titlepos = title.get_rect()
    titlepos.centerx = DisplaySurface.get_rect().centerx
    DisplaySurface.blit(title, titlepos)

    MyStatus = Status()
    MyCode = Code()

    MyStatus.change_to_Alarming()
    print MyStatus.statustext
    paint(DisplaySurface,MyStatus)
    pygame.display.flip()
    sound = pygame.mixer.Sound(ALERT_SOUND)
    
    # Main Loop!
    while True:
        poll(MyCode,MyStatus)
        paint(DisplaySurface,MyStatus)
        pygame.display.flip()
        if MyStatus.status == 'alarming':
            sound.play()
            pygame.time.wait(1000)  # time in ms
        else:
            pygame.time.wait(50)  # time in ms
        fpsClock.tick(FPS)
    raise SystemExit

