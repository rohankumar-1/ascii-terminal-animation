from ascii_magic import AsciiArt, Front, Back
import time
import sys
import os
from PIL import ImageOps, Image, ImageEnhance, ImageShow
import cursor

IMAGE_PATH = "images/bent_classic.jpg"      # path to image
MAX_SIZE, MIN_SIZE, STEP_SIZE = 55, 5, 5    # max, min, and step size of frames
SPEED = 0.04                                # speed of animation (i.e. seconds between each frame)
RUNTIME = 10                                # max seconds

BANNER_TEXT = \
"\
-------------\n\
 TAU BETA PI \n\
-------------\
" 

BANNER_TEXT = \
"""


  _________   __  __   ____  _______________       ____  ____
 /_  __/   | / / / /  / __ )/ ____/_  __/   |     / __ \/  _/
  / / / /| |/ / / /  / __  / __/   / / / /| |    / /_/ // /  
 / / / ___ / /_/ /  / /_/ / /___  / / / ___ |   / ____// /   
/_/ /_/  |_\____/  /_____/_____/ /_/ /_/  |_|  /_/   /___/     
                                                            
The Engineering Honor Society
"""

TERMINAL_COL, TERMINAL_ROW = os.get_terminal_size() # terminal info
ITERATIONS = (MAX_SIZE - MIN_SIZE) // STEP_SIZE     # total number of iterations calculation

def convert_banner_to_grid(banner: str) -> list[list[str]]:
    rows = banner.split("\n")
    
    cols = max([len(row) for row in rows])
    
    grid: list[list[str]] = []
    for i, row in enumerate(rows):
        grid.append([])
        for j in range(cols):
            if j < len(row):
                grid[i].append(row[j])
            else:
                grid[i].append(" ")
    
    return grid

def draw_frame(art: AsciiArt, iter: int, direction: bool, banner: list[list[str]] = None) -> None:
    """ draws a frame given current iteration "iter" and direction True=up, False=down """
    if direction:
        num_col = MIN_SIZE + STEP_SIZE*iter
    else:
        num_col = MAX_SIZE - STEP_SIZE*iter
        
    # create art string using num_col
    art_string = art.to_ascii(columns=num_col, width_ratio=2.4)
    
    # split into rows (lines)
    lines = art_string.split("\n")
    
    # calculate column and row buffer to center art
    row_buffer = ((TERMINAL_ROW - len(lines)) // 2)
    column_buffer = ((TERMINAL_COL - num_col) // 2)
    
    # build text to print
    res = ""
    
    # if we have a banner, add it centered to the top
    banner_lines = 0
    if banner:
        banner_lines = len(banner)
        banner_column_buffer = ((TERMINAL_COL - len(banner[0])) // 2)
        for row in banner:
            res += " "*banner_column_buffer + "".join(row) + "\n"
    
    # start with row_buffer new lines
    res += "\n"*(row_buffer - banner_lines)
    
    # add column buffer to each line of ascii art
    # for line in lines:
    res += "\n".join([(" "*column_buffer + line) for line in lines])
    
    # clear, write, flush
    sys.stdout.write("\033[H\033[J")
    sys.stdout.write("\r" + res)
    sys.stdout.flush()


def main():
    image = Image.open(IMAGE_PATH).convert('RGB')
    image = ImageOps.invert(image)
    art = AsciiArt.from_pillow_image(image)

    
    banner = convert_banner_to_grid(BANNER_TEXT)
    
    # clear console, hide cursor
    print("\033[2J", end="")
    cursor.hide()
    start_time = time.time()
    while True:
        
        # up
        for i in range(ITERATIONS):
            time.sleep(SPEED)  
            draw_frame(art, i, True, banner=banner)
            
        # top
        for i in range(6):
            time.sleep(SPEED)
            draw_frame(art, ITERATIONS-1, True, banner=banner)
            
        # down
        for i in range(1, ITERATIONS):
            time.sleep(SPEED)  
            draw_frame(art, i, False, banner=banner)
            
        # break after 20s
        if time.time() - start_time > RUNTIME:  # The animation will last for 10 seconds
            break
        
    

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    
    cursor.show()
    sys.stdout.write("\033[H\033[J")