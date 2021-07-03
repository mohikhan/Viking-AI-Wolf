
#Script file for agent Viking

from __future__ import print_function, division
import aiwolfpy
import aiwolfpy.contentbuilder as cb
import logging, json
from random import randint

#Linking different roles
from villager import *
from werewolf import *
from seer import *
from bodyguard import *
from medium import *
#from defaultrole import *
from possessed import *

#My agent name
myname = 'Vikings'

class Myagent(object):

    def __init__(self, agent_name):
        # myname
        self.myname = agent_name
        logging.basicConfig(filename=self.myname+".log",  level=logging.DEBUG,  format='')

    def getName(self):
        return self.myname
    
   #initialize is called for initializing the variables at the starting of game
    def initialize(self, base_info, diff_data, game_setting):
        
        # store my role in myrole
        self.myrole = base_info["myRole"] 
        #store my id in myid
        self.myid = base_info["agentIdx"]
        
        # Strategy number for the werewolf
        self.strategy_no = randint(0,1)

        # Day number
        self.day_no = base_info["day"]
        
        logging.debug("# INIT: I am agent {}".format(self.myid))
        logging.debug("# INIT: I am playing the role of {}".format(self.myrole))

        self.player_total = game_setting["playerNum"]
       
        # player_score for hate score of each player
        self.player_score = [0]*self.player_total

        # Vulnerability score for the bodyguard to guard the agent
        self.vulnerability = [0]*self.player_total
            
        #Reducing my own score to avoid targeting myself
        self.player_score[self.myid-1] = -10000

        #Increased my vulnerable score to avoid guarding myself
        self.vulnerability[self.myid-1] = -10000
        
        #show diff data
        logging.debug("Diff Data:")
        logging.debug(diff_data)
        
        # the hate attribute contains the player ID that I hate the most.
        self.hate = self.player_score.index(max(self.player_score)) + 1

        # # the ally attribute contains the player ID that considers me a villager 
        # self.ally = self.player_score.index(min(self.player_score)) + 1
         
        # the vulnerable attribute contains the player ID I have to guard as a bodyguard
        self.vulnerable = self.vulnerability.index( max(self.vulnerability)  ) + 1

        #Index for talk number
        self.ind = 0


    # vote function to vote for the most hated agent.
    def vote(self):
        logging.debug("# VOTE: "+str(self.hate))
        return self.hate
   
    #attack function for werewolf
    def attack(self):
        logging.debug("# ATTACK: "+str(self.hate))
        return self.hate

    #divine function for seer
    def divine(self):
        logging.debug("# DIVINE: "+str(self.hate))
        return self.hate
        # return 2

    # Updating informtion in the game
    def update(self, base_info, diff_data, request):

         # Day number
        self.day_no = base_info["day"]
        self.ind = self.ind + 1
        
        # logic if agent is villager
        if(self.myrole == "VILLAGER"):
            
            villager_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)
        
         # logic if agent is werewolf
        elif(self.myrole == "WEREWOLF"):
                      
            werewolf_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)
        

        # logic if agent is bodyguard
        elif(self.myrole == "BODYGUARD"):

            bodyguard_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid,self.vulnerability)
    
        # logic if agent is medium
        elif(self.myrole == "MEDIUM"):

            medium_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)
        
        # logic if agent is possessed
        elif(self.myrole == "POSSESSED"):
            
            possessed_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)

        # logic if agent is seer
        else:

            seer_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)


        # Hate score of different agents
        self.hate = self.player_score.index(max(self.player_score)) + 1
        logging.debug("Hate Score: "+", ".join(str(x) for x in self.player_score))
 
        # Vulnerability score of different agents
        self.vulnerable = self.vulnerability.index(max(self.vulnerability)) + 1
        logging.debug("Vulnerability Score: "+", ".join(str(y) for y in self.vulnerability))
     
        # # the ally attribute contains the player ID that considers me a villager 
        # self.ally = self.player_score.index(min(self.player_score)) + 1
    
    # Start of the day (no return)
    def dayStart(self):
        logging.debug("# DAYSTART")
        
        self.ind = -1
        return None

    #Conversation function
    def talk(self):
        logging.debug("# TALK")

        # Calls talk logic for VILLAGER
        if(self.myrole == "VILLAGER"):
            return villager_talk(self.hate,self.ind)
        
        # Calls talk logic for WEREWOLF
        elif(self.myrole == "WEREWOLF"):
          
            return werewolf_talk(self.hate, self.strategy_no, self.day_no, self.myid, self.ind)
        
        # Calls talk logic for BODYGUARD
        elif(self.myrole == "BODYGUARD"):
          
            return bodyguard_talk(self.hate,self.ind)
 
        # Calls talk logic for SEER
        elif(self.myrole == "SEER"):
            return seer_talk(self.hate, self.day_no, self.myid, self.ind)

        # Calls talk logic for MEDIUM
        elif(self.myrole == "MEDIUM"):
            return medium_talk(self.hate, self.day_no, self.myid, self.ind)


        # Calls talk logic for POSSESSED
        elif(self.myrole == "POSSESSED"):
          
            return possessed_talk(self.hate, self.strategy_no, self.day_no, self.myid, self.ind)

       
   # Whisper function for the werewolf
    def whisper(self):
        logging.debug("# WHISPER")
        return "ATTACK Agent[{:02d}]".format(self.hate)

   # Guard function for the bodyguard
    def guard(self):
        logging.debug("# GUARD")
        logging.debug("# guarded agent: "+str(self.vulnerable))
        return self.vulnerable

    # Finish (no return)
    def finish(self):
        logging.debug("# FINISH")
        return None

agent = Myagent(myname)

# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
