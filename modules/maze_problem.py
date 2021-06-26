import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib import animation, rc
from IPython.display import HTML,Image
rc('animation', html='html5')


class Maze:
    def __init__(self,world):
        rows = world.shape[0]
        cols = world.shape[1]
        all_possible_positions = []
        starting_position = []
        state_map = np.ones_like(world).astype(int)*-1
        gold_states = []
        index = 0
        for row in range(rows):
            for col in range(cols):
                if(not world[row,col]=='W'):
                    all_possible_positions.append([row,col])
                    state_map[row,col]=index
                    if(world[row,col]=='S'):
                        starting_position = [row,col]
                    if(world[row,col]=='G'):
                        gold_states.append(index)
                    index+=1
        number_of_states = len(all_possible_positions)
        
        def get_position_index(position):
            for i in range(number_of_states):
                if(position[0]==all_possible_positions[i][0] and position[1]==all_possible_positions[i][1]):
                    return i
            return None
        
        initial_state = get_position_index(starting_position)
        
        left_transition_matrix = np.zeros((number_of_states,number_of_states))
        for i in range(number_of_states):
            pos = all_possible_positions[i]
            
            left_pos = [pos[0],pos[1]-1]
            left_move_index = get_position_index(left_pos)
            if left_move_index==None:
                left_transition_matrix[i,i]+=0.7
            else:
                left_transition_matrix[left_move_index,i]+=0.7
            
            up_pos = [pos[0]-1,pos[1]]
            up_move_index = get_position_index(up_pos)
            if up_move_index==None:
                left_transition_matrix[i,i]+=0.15
            else:
                left_transition_matrix[up_move_index,i]+=0.15
            
            down_pos = [pos[0]+1,pos[1]]
            down_move_index = get_position_index(down_pos)
            if down_move_index==None:
                left_transition_matrix[i,i]+=0.15
            else:
                left_transition_matrix[down_move_index,i]+=0.15
        
        right_transition_matrix = np.zeros((number_of_states,number_of_states))
        for i in range(number_of_states):
            pos = all_possible_positions[i]
            
            right_pos = [pos[0],pos[1]+1]
            right_move_index = get_position_index(right_pos)
            if right_move_index==None:
                right_transition_matrix[i,i]+=0.7
            else:
                right_transition_matrix[right_move_index,i]+=0.7
            
            up_pos = [pos[0]-1,pos[1]]
            up_move_index = get_position_index(up_pos)
            if up_move_index==None:
                right_transition_matrix[i,i]+=0.15
            else:
                right_transition_matrix[up_move_index,i]+=0.15
            
            down_pos = [pos[0]+1,pos[1]]
            down_move_index = get_position_index(down_pos)
            if down_move_index==None:
                right_transition_matrix[i,i]+=0.15
            else:
                right_transition_matrix[down_move_index,i]+=0.15
        
        down_transition_matrix = np.zeros((number_of_states,number_of_states))
        for i in range(number_of_states):
            pos = all_possible_positions[i]
            
            down_pos = [pos[0]+1,pos[1]]
            down_move_index = get_position_index(down_pos)
            if down_move_index==None:
                down_transition_matrix[i,i]+=0.7
            else:
                down_transition_matrix[down_move_index,i]+=0.7
            
            right_pos = [pos[0],pos[1]+1]
            right_move_index = get_position_index(right_pos)
            if right_move_index==None:
                down_transition_matrix[i,i]+=0.15
            else:
                down_transition_matrix[right_move_index,i]+=0.15
            
            left_pos = [pos[0],pos[1]-1]
            left_move_index = get_position_index(left_pos)
            if left_move_index==None:
                down_transition_matrix[i,i]+=0.15
            else:
                down_transition_matrix[left_move_index,i]+=0.15
        
        up_transition_matrix = np.zeros((number_of_states,number_of_states))
        for i in range(number_of_states):
            pos = all_possible_positions[i]
            
            up_pos = [pos[0]-1,pos[1]]
            up_move_index = get_position_index(up_pos)
            if up_move_index==None:
                up_transition_matrix[i,i]+=0.7
            else:
                up_transition_matrix[up_move_index,i]+=0.7
            
            right_pos = [pos[0],pos[1]+1]
            right_move_index = get_position_index(right_pos)
            if right_move_index==None:
                up_transition_matrix[i,i]+=0.15
            else:
                up_transition_matrix[right_move_index,i]+=0.15
            
            left_pos = [pos[0],pos[1]-1]
            left_move_index = get_position_index(left_pos)
            if left_move_index==None:
                up_transition_matrix[i,i]+=0.15
            else:
                up_transition_matrix[left_move_index,i]+=0.15
            
        left_transition_matrix[:,gold_states]=0
        left_transition_matrix[initial_state,gold_states]=1
        right_transition_matrix[:,gold_states]=0
        right_transition_matrix[initial_state,gold_states]=1
        up_transition_matrix[:,gold_states]=0
        up_transition_matrix[initial_state,gold_states]=1
        down_transition_matrix[:,gold_states]=0
        down_transition_matrix[initial_state,gold_states]=1

        self.left_transition_matrix = left_transition_matrix
        self.right_transition_matrix = right_transition_matrix
        self.up_transition_matrix = up_transition_matrix
        self.down_transition_matrix = down_transition_matrix
        self.state_map = state_map
        self.world = world
        self.policy_matrix = np.nan
        self.initial_state = get_position_index(starting_position)
        
    def print_to_size(array,size):
        last_row_sizes = np.array([len(v) for v in array[:,-1]])
        max_last_row_size = np.max(last_row_sizes)
        all_rows_str = ""
        for r in range(array.shape[0]):
            row = array[r]
            if(r>0):
                row_str = " ["
            else:
                row_str = "[["
            for e in range(len(row)):
                gap = size
                if(e==len(row)-1):
                    gap=max_last_row_size
                element_str = str(row[e])
                dif = gap-len(element_str)
                element_str = "".join([element_str]+[" " for space in range(dif)])
                row_str=row_str+element_str
            if(r<array.shape[0]-1):
                row_str=row_str+" ] \n"
            else:
                row_str=row_str+" ]]"
            all_rows_str=all_rows_str+row_str
        return all_rows_str
    
    def __repr__(self):
        size = len(str(np.max(self.state_map)))+1
        world_str = Maze.print_to_size(self.world.astype(str),size)
        state_str = Maze.print_to_size(np.char.replace(self.state_map.astype(str),"-1","W"),size).replace("W"," ")
        return world_str + " world map" "\n" + state_str + " state map"
    
    def get_policy_matrix(self,policy_vals):        
        policy_matrix = np.zeros_like(self.left_transition_matrix)
        for p in range(len(policy_vals)):
            state_p_policy = policy_vals[p]
            if(state_p_policy=='U'):
                policy_matrix[:,p]=self.up_transition_matrix[:,p]
            if(state_p_policy=='D'):
                policy_matrix[:,p]=self.down_transition_matrix[:,p]
            if(state_p_policy=='L'):
                policy_matrix[:,p]=self.left_transition_matrix[:,p]
            if(state_p_policy=='R'):
                policy_matrix[:,p]=self.right_transition_matrix[:,p]        
        
        policy_map = self.world.copy()
        for row in range(policy_map.shape[0]):
            for col in range(policy_map.shape[1]):
                if(self.state_map[row,col]!=-1):
                    policy_map[row,col] = policy_vals[self.state_map[row,col]]
                else:
                    policy_map[row,col] = "W"
        
        size = len(str(np.max(self.state_map)))+1
        policy_map_str = Maze.print_to_size(policy_map.astype(str),size)
        policy_map_str = policy_map_str.replace("W"," ")
        print(policy_map_str+" policy map")
        return policy_matrix
    
    def sample_policy(self,transition_matrix,steps):
        if(not np.isnan(transition_matrix).any()):
            state_index = self.initial_state
            state_hist = [state_index]
            for iteration in range(steps):
                state_index = np.random.choice(transition_matrix.shape[1],p=transition_matrix[:,state_index])
                state_hist.append(state_index)
            return state_hist
        else:
            print("no policy yet")
            return
    
    def make_animation(self,transition_matrix,steps):
        empty_tile = np.zeros((8,8))
        wall_tile = np.ones((8,8))
        fire_tile = np.array([[0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,1,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,1,0,0,0],
                              [0,0,1,0,1,0,0,0],
                              [0,0,1,1,0,1,0,0],
                              [0,1,1,0,1,1,1,0]])*2
        gold_tile = np.array([[0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,1,1,0,0,0],
                              [0,0,1,0,0,1,0,0],
                              [0,0,1,0,0,1,0,0],
                              [0,0,0,1,1,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0]])*3
        person_tile = np.array([[0,0,0,1,0,0,0,0],
                                [0,1,1,1,1,1,0,0],
                                [0,0,0,1,0,0,0,0],
                                [0,0,0,1,0,0,0,0],
                                [0,0,1,1,1,0,0,0],
                                [0,0,1,0,1,0,0,0],
                                [0,0,1,0,1,0,0,0],
                                [0,0,1,0,1,0,0,0]])*4
        symbol_to_tile = dict(zip(['B','W','F','G','S'],[empty_tile,wall_tile,fire_tile,gold_tile,empty_tile]))
    
        states = self.sample_policy(transition_matrix,steps)
        world = self.world
        state_map = self.state_map
        
        images = []
        for i in range(len(states)):
            state = states[i]
            image = np.zeros((world.shape[0]*8,world.shape[1]*8))
            for row in range(world.shape[0]):
                for col in range(world.shape[1]):
                    tile = symbol_to_tile[world[row,col]]
                    image[row*8:(row+1)*8,col*8:(col+1)*8]=tile
                    if(state_map[row,col]==state):
                        image[row*8:(row+1)*8,col*8:(col+1)*8][person_tile>0]=person_tile[person_tile>0]
            images.append(image)
        
        fig = plt.figure(figsize=(world.shape[1]/2,world.shape[0]/2))
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        im = plt.imshow(images[0],cmap=colors.ListedColormap(['grey','black','red','yellow','pink']))

        def animate_func(i):
            im.set_array(images[i])
            return
        
        anim = animation.FuncAnimation(fig, 
                                       animate_func,
                                       frames=len(states), 
                                       interval=200
                                       )
        
        html = HTML(anim.to_jshtml())
        display(html)
        plt.close()

