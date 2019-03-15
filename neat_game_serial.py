from snake_class import *
import neat
import numpy as np
'''
Written by:Sushil Ragoonath
https://github.com/SushilRagoonath/
'''

def output_to_nn(cnake=Snake()):
    #distance

    x=cnake.head.rect.x-cnake.f_size[0]
    y=cnake.head.rect.y-cnake.f_size[1]

    #bools
    snake_xl=0
    snake_xr=0
    snake_yd=0
    snake_yu=0
    can_go_r=0
    can_go_l=0
    can_go_d=0
    can_go_u=0
    if cnake.head.d_snake==0:
        can_go_l=1
    if cnake.head.d_snake==3:
        can_go_r=1
    if cnake.head.d_snake==1:
        can_go_d=1
    if cnake.head.d_snake==2:
        can_go_u=1

    if x >0:
        snake_xl =1 # go left
    else :
        snake_xr=1 # go right
    if y>0:
        snake_yd=1 # go down
    else :
        snake_yu=1 # go up
    #return np.array([snake_xl,can_go_l,snake_xr,can_go_r,snake_yd,can_go_d,snake_yu,can_go_u])

    #return np.array([abs(cnake.head.rect.x/800),abs(cnake.head.rect.y/800),cnake.head.d_snake/4,abs(cnake.f_size[0]/800),abs(cnake.f_size[1]/800)]) # giving only x and y of food and head
    #return np.array([abs(cnake.head.rect.x/800),abs(cnake.head.rect.y/800),cnake.head.d_snake/4,abs(cnake.f_size[0]/800),abs(cnake.f_size[1]/800)]) # giving only x and y of food and head
    return np.array([snake_xl,snake_xr,snake_yd,snake_yu,cnake.head.d_snake/4,
    cnake.previous_moves[len(cnake.previous_moves)-1],
    cnake.previous_moves[len(cnake.previous_moves)-2],
    cnake.previous_moves[len(cnake.previous_moves)-3]])  #usually the features i want to use
    #print([abs(cnake.head.rect.x/800),abs(cnake.head.rect.y/800),abs(cnake.f_size[0]/800),abs(cnake.f_size[1]/800),cnake.head.d_snake/4])
    #return np.array([abs(cnake.head.rect.x/800),abs(cnake.head.rect.y/800),cnake.head.d_snake/4,abs(cnake.f_size[0]/800),abs(cnake.f_size[1]/800)]) # giving only x and y of food and head
    #return np.array([cnake.loops_alive,x,y])
def run(snake,outputs):
    #while True:

    disp.fill([0,0,0])

    clock.tick(7000)
    #p.display.update()
    for event in p.event.get():
        if event.type == QUIT:
             p.quit()
             sys.exit(0)

    #snake.head.key_d_snake()
    snake.head.self_key(outputs)
    snake.movement()
    #snake.draw()
    snake.kill()
    snake.reset()
    #snake.score_print()
    #p.display.update()
    #cv2.namedWindow("main", cv2.WINDOW_NORMAL)
def eval_genomes(genomes, config):
    for genome_id,genome in genomes:
        snake= Snake()
        snake.movement()
        snake.food()
        snake.score+=1
        inputs=output_to_nn(snake)
        net=neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
       # net=neat.nn.recurrent.RecurrentNetwork.create(genome,config)


        while snake.reset_times <=1:
            inputs=output_to_nn(snake)
            outputs=net.activate(inputs)
            run(snake,outputs)
            genome.fitness=(snake.best_score-1) *(snake.best_score-1)*(snake.best_score-1)+(snake.loops_last_eaten/20)
        #print(genome_id, genome.fitness)
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')


population =neat.Population(config)
#population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-719')
population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)
population.add_reporter(neat.Checkpointer(10))

p.init()
clock = p.time.Clock()
p.display.set_caption('test')




winner=population.run(eval_genomes)
'''
winner_net= neat.nn.feed_forward.FeedForwardNetwork.create(winner,config)
snake= Snake()
snake.movement()
snake.food()
snake.score+=1
while True:

    inputs=output_to_nn(snake)
    outputs=winner_net.activate(inputs)
    disp.fill([0,0,0])
    p.display.update()
    clock.tick(40)
    p.display.update()
    for event in p.event.get():
        if event.type == QUIT:
             p.quit()
             sys.exit(0)

    #snake.head.key_d_snake()
    snake.head.self_key(outputs)
    snake.movement()
    snake.draw()
    snake.kill()
    snake.reset()
    #snake.score_print()
    p.display.update()
    '''
