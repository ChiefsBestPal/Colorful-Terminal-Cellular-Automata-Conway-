import pygame
import pyperclip
import pyautogui
import time #gnnnn

SKIP_INSTRUCTIONS = True

def MakeTestCaseForConway(DIMENSIONS_X=25,DIMENSIONS_Y=25,):
    TEST_CASE = None
    pygame.init()
    RES_W,RES_H = pyautogui.size()

    x = 0
    y = 0
    
    size = RES_H//DIMENSIONS_Y 
    #!size = (size-2) if size > 2 else size
    array = []
    def text_objects(text, font):
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    def message_display(*,WINDOW,text,decalage=0):
        FONTSIZE = 42
        largeText = pygame.font.Font("freesansbold.ttf",FONTSIZE) #TODO custom font size
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = (size*(DIMENSIONS_X//2), size*(DIMENSIONS_Y//2) + decalage*size)
        WINDOW.blit(TextSurf, TextRect)
        pygame.display.update()
        if not SKIP_INSTRUCTIONS:#! <----------------------
            time.sleep(1)

        TextSurf, _ = text_objects("", largeText)
        WINDOW.blit(TextSurf, TextRect)
        pygame.display.update()
    
    win = pygame.display.set_mode((size*DIMENSIONS_X, size*DIMENSIONS_Y),pygame.FULLSCREEN)
    #//pygame.display.set_caption('Press CTRL to save Conway Test case,ALT to center cursor')
    pygame.key.set_repeat(1, 10)
    
    run = True
    message_display(WINDOW=win,text="CTRL:save Conway Test Case",decalage=0)
    message_display(WINDOW=win,text="ALT:CenterCursor",decalage=1)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    def func():
                        for square in array:
                            if square[0] == x and square[1] == y:
                                array.remove([square[0],square[1]])
                                return
                        array.append([x,y])
                    func()
                if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    x,y = size*(DIMENSIONS_X//2), size*(DIMENSIONS_Y//2)
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    copystring = ''
                    for yy in range(0, size*DIMENSIONS_Y, +size):
                        for xx in range(0, size*DIMENSIONS_X, +size):
                            if [xx, yy] not in array:
                                copystring += '0'   #'⬜'
                            else:
                                copystring += '1'   #'⬛'
                            copystring += " "
                        copystring += '\n'
                    pyperclip.copy(copystring)
                    TEST_CASE = list(map(lambda row: \
                        list(map(lambda i: bool(int(i)),row.split())),\
                        copystring.splitlines()))
                    pygame.display.set_caption('Saved!')
                    pygame.time.delay(100)#!0.1s
                    run = False#!end of program
                    #pygame.display.set_caption('Press CTRL to copy and save Conway Test case')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x >= size:
                    x -= size 
                if event.key == pygame.K_RIGHT and x < size*(DIMENSIONS_X-1):
                    x += size
                if event.key == pygame.K_UP and y >= size:
                    y -= size
                if event.key == pygame.K_DOWN and y < size*(DIMENSIONS_Y-1):
                    y += size
                if event.key == pygame.K_a and x >= size:
                    x -= size 
                if event.key == pygame.K_d and x < size*(DIMENSIONS_X-1):
                    x += size
                if event.key == pygame.K_w and y >= size:
                    y -= size
                if event.key == pygame.K_s and y < size*(DIMENSIONS_Y-1):
                    y += size
        win.fill((25,25,25))
        for square in array:
            pygame.draw.rect(win, (255, 255, 255), (square[0], square[1], size, size))
        rect1 = pygame.Rect(x, y, size, size)
        rect2 = pygame.Rect(x, y, round(size/1.75), round(size/1.75))
        rect2.center = rect1.center
        pygame.draw.rect(win, (0, 128, 128), rect1, 5)
        pygame.draw.rect(win, (0, 64, 64), rect2, 5)
        pygame.display.update()
        pygame.time.delay(100)

    pygame.quit()
    return TEST_CASE