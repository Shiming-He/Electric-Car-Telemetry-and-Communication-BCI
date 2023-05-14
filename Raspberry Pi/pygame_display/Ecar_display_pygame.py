import pygame
import math
import random
import time



def hand_pos(deg, length, origin):
    '''hand_pos(deg, length, origin) -> tuple
    returns the tuple of the position'''
    #x and y pos
    if deg < 90:
        x_movement = math.sin(math.radians(deg))
        y_movement = -1*math.cos(math.radians(deg))
    elif deg < 180:
        x_movement = math.sin(math.radians(180 - deg))
        y_movement = math.cos(math.radians(180 - deg))
    elif deg < 270:
        x_movement = -1*math.sin(math.radians(deg-180))
        y_movement = math.cos(math.radians(deg-180))
    else:
        x_movement = -1*math.sin(math.radians(360 - deg))
        y_movement = -1*math.cos(math.radians(360 - deg))
    pos = [origin[0]+(x_movement*length), origin[1]+(y_movement*length)]
    
    return tuple(pos)

def right_curved_line(max_rad, width, degree, center, end_deg):
    '''right_curved_line(max_rad, width, degree, center, end_deg) -> list
    create the list for pos of the curved line'''
    #init var
    pos_list = []
    if (degree < end_deg):
        #get outer pos
        for deg in range(degree, 0, -1):
            pos = hand_pos(deg, max_rad-width, center)
            pos_list.append(pos)
        
        #get outer pos
        for deg in range(360, end_deg, -1):
            pos = hand_pos(deg, max_rad-width, center)
            pos_list.append(pos)
            
        # get inner pos
        for deg_val in range(end_deg, 360):
            pos = hand_pos(deg_val, max_rad, center)
            pos_list.append(pos)
            
        # get inner pos
        for deg_val in range(0,  degree+1):
            pos = hand_pos(deg_val, max_rad, center)
            pos_list.append(pos)
    else:
        #get outer pos
        for deg in range(end_deg, degree+1):
            pos = hand_pos(deg, max_rad-width, center)
            pos_list.append(pos)
            
        # get inner pos
        for deg_val in range(degree, end_deg+1, -1):
            pos = hand_pos(deg_val, max_rad, center)
            pos_list.append(pos)
        
    #make sure if it is empty there is something
    if len(pos_list) < 3:
        pos_list = [hand_pos(end_deg, max_rad, center), hand_pos(end_deg, max_rad-width, center), hand_pos(end_deg, max_rad-width, center)]
    return pos_list


def left_curved_line(max_rad, width, degree, center, end_deg):
    '''left_curved_line(max_rad, width, degree, center, end_deg) -> list
    create the list for pos of the curved line'''
    #init var
    pos_list = []
    if (degree > end_deg):
        #get outer pos
        for deg in range(degree, 360):
            pos = hand_pos(deg, max_rad-width, center)
            pos_list.append(pos)
        
        #get outer pos
        for deg in range(0, end_deg):
            pos = hand_pos(deg, max_rad-width, center)
            pos_list.append(pos)
            
        # get inner pos
        for deg_val in range(end_deg, 0, -1):
            pos = hand_pos(deg_val, max_rad, center)
            pos_list.append(pos)
            
        # get inner pos
        for deg_val in range(360,  degree+1, -1):
            pos = hand_pos(deg_val, max_rad, center)
            pos_list.append(pos)
    else:
        #get outer pos
        for deg in range(end_deg, degree, -1):
            pos = hand_pos(deg, max_rad-width, center)
            pos_list.append(pos)
            
        # get inner pos
        for deg_val in range(degree, end_deg+1):
            pos = hand_pos(deg_val, max_rad, center)
            pos_list.append(pos)
        
    #make sure if it is empty there is something
    if len(pos_list) < 3:
        pos_list = [hand_pos(0, max_rad, center), hand_pos(0, max_rad-width, center), hand_pos(0, max_rad-width, center)]
    return pos_list



# create screen
class Ecar_pygame_display:
    '''create Ecar_pygame_display object'''
    
    def __init__(self, display_speed = False):
        '''Ecar_pygame_display(display_speed = False) -> Ecar_pygame_display
        creates a Ecar_pygame_display
        this is a display that will appear on the moniter'''
        #initalize pygame window
        pygame.init()
        
        #initalize variables
        self.screen_size = 'small'# used to regulate screen size
        
        #set display mode
        self.screen = pygame.display.set_mode((800,400), pygame.RESIZABLE)
        
        #set the present screen size
        self.dis_width, self.dis_height = self.screen.get_size()
        print(self.dis_width, self.dis_height)
        
        #ste backgound colour
        self.screen.fill((0,0,0))
        

    def update(self, battery_percent, time_left, target_speed_different, speed = 0, total_time = 60):
        '''Ecar_pygame_display.update(battery_percent, time_left, target_speed_different, speed = 0) -> None
        updates display to the present values'''
        # set the new width and height
        self.dis_width, self.dis_height = self.screen.get_size()
        
        #set the new font size
        self.text_font = pygame.font.SysFont(None, int(self.dis_height/20))
        
        
        for event in pygame.event.get():
            # close the window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.type == pygame.QUIT:
                pygame.quit()
            # alternate between full screen and a smaller window size
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.screen_size == 'large':
                    self.screen = pygame.display.set_mode((800,400), pygame.RESIZABLE)
                    self.screen_size = 'small'
                elif self.screen_size == 'small':
                    self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
                    self.screen_size = 'large'
                    
        #initalize variables for the display elements
        curved_line_radius  = (self.dis_height/2)
        curved_line_width  = curved_line_radius/4
        boarder_width = int(self.dis_width/80)
        
        
        #Create a new background
        self.screen.fill((0,0,0))
        

            
        #Battery protion of the screen
        #make sure the battery percentage is below 0
        if battery_percent < 0:
            battery_percent = 0
            
        # find the ending point for the other moving side of the bar
        line_deg = int((battery_percent*100+220)%360)
        
        # Find the colour of the bar depending on the battery percentage
        if battery_percent > 0.75:
            colour = (0, 204, 0)# green
            
        elif battery_percent > 0.5:
            colour = (250, 240, 35)# yellow
            
        elif battery_percent > 0.25:
            colour = (255, 153, 51)# orange
            
        else:
            colour = (255, 0, 0)# red
            
        #display the bar for battery percentage on the screen. It is on the left side
        shape_pos = right_curved_line(curved_line_radius, curved_line_width, line_deg, (curved_line_radius+boarder_width, self.dis_height/2 ), 220)
        pygame.draw.polygon(self.screen, colour, shape_pos)
        
        
        # add battery label
        batt_name = self.text_font.render('Batt', True, (255,255,255))
        
        battery_name_text_rect = batt_name.get_rect()
        battery_name_text_rect.center = (boarder_width*8,19*self.dis_height/20)
        
        self.screen.blit(batt_name, battery_name_text_rect)
        
        
        # add the battery percentage label
        battery_per_text = self.text_font.render(str(round(battery_percent*100))+'%', True, (255,255,255))
        
        battery_per_text_rect = battery_per_text.get_rect()
        battery_per_text_rect.center = (boarder_width*8,self.dis_height/20)
        
        self.screen.blit(battery_per_text, battery_per_text_rect)
        
        
        #add the boader around the bettery arc
        pygame.draw.arc(self.screen, (20, 90, 235), [0, (self.dis_height/2)-curved_line_radius-boarder_width, 2*(curved_line_radius+boarder_width),2*(curved_line_radius+boarder_width)], math.radians(130), math.radians(230), int(boarder_width))
        
        #add the line in the battery percent bar
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(320, 2*curved_line_radius/3, (curved_line_radius, curved_line_radius)),hand_pos(320, curved_line_radius, (self.dis_height/2, curved_line_radius)),int(self.dis_width/80)) # 100%
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(295, 3*curved_line_radius/4, (curved_line_radius, curved_line_radius)),hand_pos(295, curved_line_radius, (self.dis_height/2, curved_line_radius)),int(self.dis_width/80)) # 75%
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(270, 2*curved_line_radius/3, (curved_line_radius, curved_line_radius)),hand_pos(270, curved_line_radius, (self.dis_height/2, curved_line_radius)),int(self.dis_width/80)) # 50%
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(245, 3*curved_line_radius/4, (curved_line_radius, curved_line_radius)),hand_pos(245, curved_line_radius, (self.dis_height/2, curved_line_radius)),int(self.dis_width/80)) # 25%
        
        
        
        #time portion of the diaplay
        
        #make sure the time will not be below 0
        if time_left < 0:
            time_left = 0
        line_deg2 = int((140-(time_left)*100)%360)
        
        #color for the time bar
        if time_left > 0.75:
            colour = (0, 204, 0)# green
            
        elif time_left > 0.5:
            colour = (250, 240, 35)# yellow
            
        elif time_left > 0.25:
            colour = (255, 153, 51)# orange
        else:
            colour = (255, 0, 0)# red
        
        #display the bar for time remaining. It is on the right side of the display
        shape_pos = left_curved_line(curved_line_radius, curved_line_width, line_deg2, (self.dis_width - curved_line_radius-boarder_width, curved_line_radius), 140)
        pygame.draw.polygon(self.screen, colour, shape_pos)
        
        
        # add the time label
        time_name = self.text_font.render('Time', True, (255,255,255))
        
        time_name_text_rect = time_name.get_rect()
        time_name_text_rect.center = (self.dis_width - boarder_width*8,19*self.dis_height/20)
        
        self.screen.blit(time_name, time_name_text_rect)
        
        
        # add the time remaining in minutes label
        time_left_text = self.text_font.render(str(int(time_left*total_time))+' min', True, (255,255,255))
        
        time_left_text_rect = time_left_text.get_rect()
        time_left_text_rect.center = (self.dis_width - boarder_width*8,self.dis_height/20)
        
        self.screen.blit(time_left_text, time_left_text_rect)
        
        #add the border around the time percent bar
        pygame.draw.arc(self.screen, (20, 90, 235), [self.dis_width - 2*(curved_line_radius+boarder_width), (self.dis_height/2)-curved_line_radius-boarder_width, 2*(curved_line_radius+boarder_width),2*(curved_line_radius+boarder_width)], math.radians(310), math.radians(410), int(boarder_width))
        
        #Add the lines in the time percent bar
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(40, 2*curved_line_radius/3, (self.dis_width - curved_line_radius, curved_line_radius)),hand_pos(40, curved_line_radius, (self.dis_width - curved_line_radius, curved_line_radius)),int(self.dis_width/80)) # 100%
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(65, 3*curved_line_radius/4, (self.dis_width - curved_line_radius, curved_line_radius)),hand_pos(65, curved_line_radius, (self.dis_width - curved_line_radius, curved_line_radius)),int(self.dis_width/80)) # 75%
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(90, 2*curved_line_radius/3, (self.dis_width - curved_line_radius, curved_line_radius)),hand_pos(90, curved_line_radius, (self.dis_width - curved_line_radius, curved_line_radius)),int(self.dis_width/80)) # 50%
        pygame.draw.line(self.screen, (20, 90, 235), hand_pos(115, 3*curved_line_radius/4, (self.dis_width - curved_line_radius, curved_line_radius)),hand_pos(115, curved_line_radius, (self.dis_width - curved_line_radius, curved_line_radius)),int(self.dis_width/80)) # 25%
        
        
        
        
        #draw the Speed Signal. It is in the center of the screen
        
        #initalize varbiables for the Speed Signals
        middle_x_pos = self.dis_width/2
        middle_y_pos = self.dis_height/2
        size = self.dis_width/5.5
        cicle_size = size *1
        center_off = cicle_size/15
        space = 3*size/4
        
        # these are the three speed signal
        if target_speed_different < -2: # This is slow down. Purple
            pygame.draw.polygon(self.screen, (255, 0, 212), [hand_pos(330, size, (middle_x_pos, 7*self.dis_height/8)), (middle_x_pos, 7*self.dis_height/8), hand_pos(30, size, (middle_x_pos, 7*self.dis_height/8)),
                                                              (middle_x_pos+(size/6), (7*self.dis_height/8)-(1.73*size/2)), (middle_x_pos+(size/6), (self.dis_height/8)),
                                                              (middle_x_pos-(size/6), (self.dis_height/8)), (middle_x_pos-(size/6), (7*self.dis_height/8)-(1.73*size/2))
                                                              ]) # the slow down arrow
            
        if target_speed_different > 2: # This is speed up. Blue
            pygame.draw.polygon(self.screen, (77, 195, 255), [hand_pos(210, size, (middle_x_pos, self.dis_height/8)), (middle_x_pos, self.dis_height/8), hand_pos(150, size, (middle_x_pos, self.dis_height/8)),
                                                              (middle_x_pos+(size/6), (self.dis_height/8)+(1.73*size/2)), (middle_x_pos+(size/6), (7*self.dis_height/8)),
                                                              (middle_x_pos-(size/6), (7*self.dis_height/8)), (middle_x_pos-(size/6), (self.dis_height/8)+(1.73*size/2))
                                                              ]) # the speed up arrow
        if -2 <= target_speed_different <= 2: # This is hold speed. Green
            #the hold speed circle
            pygame.draw.arc(self.screen, (0, 204, 0), [middle_x_pos +(-cicle_size/2 - center_off), middle_y_pos-cicle_size/2, cicle_size, cicle_size], math.radians(90), math.radians(270), int(self.dis_width/40))
            pygame.draw.arc(self.screen, (0, 204, 0), [middle_x_pos +(-cicle_size/2 + center_off), middle_y_pos-cicle_size/2, cicle_size, cicle_size], math.radians(270), math.radians(90), int(self.dis_width/40))
        
        #update the display
        pygame.display.update()
            