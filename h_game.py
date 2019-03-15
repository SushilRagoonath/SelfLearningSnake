from snake_class import *

p.init()
clock = p.time.Clock()
p.display.set_caption('test')

'''
Written by: Sushil Ragoonath
https://github.com/SushilRagoonath/
'''

snake =Snake()
snake.movement()
snake.food()
snake.score+=1
while True:
    
    disp.fill([0,0,0])
    
    clock.tick(15)
    p.display.update()
    for event in p.event.get():
        if event.type == QUIT:
             p.quit()
             sys.exit(0)
    
    snake.head.key_d_snake()
    snake.movement()
    snake.draw()
    snake.reset()
    snake.score_print()
    p.display.update()
