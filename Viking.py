#Werewolf agent made taking inspiration from the OMGUS agent
from __future__ import print_function, division
import aiwolfpy
import aiwolfpy.contentbuilder as cb
import logging, json
from random import randint

#Importing different characters
from villager import *
from werewolf import *


myname = 'Viking'

class SampleAgent(object):
    def __init__(self, agent_name):
        # myname
        self.myname = agent_name
        logging.basicConfig(filename=self.myname+".log",  level=logging.DEBUG,  format='')

    def getName(self):
        return self.myname
    

    def initialize(self, base_info, diff_data, game_setting):
        # New game init:
        # Store my own ID:
        self.myrole = base_info["myRole"] #Storing my role
        self.myid = base_info["agentIdx"]
        self.dani=0
        logging.debug("# INIT: I am agent {}".format(self.myid))
        # logging.debug("# INIT: I am playing the role of {}".format(self.myrole))

        if(self.myrole == "VILLAGER"):
            logging.debug("Hello Mohiuddeen write here only")

        self.player_total = game_setting["playerNum"]
        #logging.debug("My role is {}".format(self.myRole))
        # Initialize a list with the hate score for each player
        # Also reduce own-hate score by 10k
        self.player_score = [0]*self.player_total
        self.player_score[self.myid-1] = -10000
        #
        self.dani=0
        # the hate attribute contains the player ID that I hate the most.
        self.hate = self.player_score.index(max(self.player_score)) + 1

    # I will vote, attack and divine the most hated player so far.
    def vote(self):
        logging.debug("# VOTE: "+str(self.hate))
        return self.hate

    def attack(self):
        logging.debug("# ATTACK: "+str(self.hate))
        return self.hate

    def divine(self):
        logging.debug("# DIVINE: "+str(self.hate))
        return self.hate

    # new information (no return)
    def update(self, base_info, diff_data, request):
        if(self.myrole == "VILLAGER"):
            # logging.debug("Villager Update")
            villager_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)
        
        elif(self.myrole == "WEREWOLF"):
            werewolf_update(base_info,diff_data,request,self.player_total,self.player_score,self.myid)




        # Print Current Hate list:
        self.hate = self.player_score.index(max(self.player_score)) + 1
        logging.debug("Hate Score: "+", ".join(str(x) for x in self.player_score))
   
    
    # Start of the day (no return)
    def dayStart(self):
        logging.debug("# DAYSTART")
        return None

    # conversation actions: require a properly formatted
    # protocol string as the return.
    def talk(self):
        logging.debug("# TALK")
        if(self.myrole == "VILLAGER"):
            return villager_talk(self.hate)
        
        elif(self.myrole == "WEREWOLF"):
            return werewolf_talk(self.hate)

        else:
            return normal_talk(self.hate)

       

    def whisper(self):
        logging.debug("# WHISPER")
        # We just affirm the desire to attack the hated player
        # We can probably remove werewolves from hated player list in this case
        return "ATTACK Agent[{:02d}]".format(self.hate)


    def guard(self):
        logging.debug("# GUARD")
        return self.myid

    # Finish (no return)
    def finish(self):
        logging.debug("# FINISH")
        return None

agent = SampleAgent(myname)

# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
