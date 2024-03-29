import logging, json
from random import randint

#Update function for the werewolf
def werewolf_update(base_info,diff_data,request,player_total,player_score,myid):
    
    # logging.debug("# WEREWOLF UPDATE")
    if (request == "DAILY_INITIALIZE"):
        for i in range(player_total):
            if (base_info["statusMap"][str(i+1)] == "DEAD"):
                player_score[i] -= 10000

    
    for row in diff_data.itertuples():
        type = getattr(row,"type")
        text = getattr(row,"text")


        # Voting in diff data
        if (type == "vote"):
            voter = getattr(row,"idx")
            target = getattr(row,"agent")

            # If the voter has voted for me to be a werewolf I will give him 100 hate points
            if (target == myid):
                logging.debug("Agent {} voted for me!".format(voter))
                player_score[voter-1] += 100
      

        elif (type == "talk" and "[{:02d}]".format(myid) in text):
            
            # they are talking about me
            source = getattr(row,"agent")
            logging.debug("Sentence containing me: {}".format(text))
            
            # Reduce the hate points for the players who think I am a human
            if "DIVINED Agent[{:02d}] HUMAN".format(myid)  in text:
                player_score[source - 1] -=20

            # Reduce the hate points for the players who wants the bodyguard to guard me
            elif "(GUARD Agent[{:02d}])".format(myid) in text:
                player_score[source - 1] -= 40
            
            # Increase the hate points for the agent who divines me as a werewolf 
            elif "DIVINED Agent[{:02d}] WEREWOLF".format(myid)  in text:
                player_score[source - 1] +=50 
            
            # Reduce the hate points for the players who estimate me in the human team
            elif "ESTIMATE Agent[{:02d}] VILLAGER".format(myid) in text or "ESTIMATE Agent[{:02d}] SEER".format(myid) in text or "ESTIMATE Agent[{:02d}] MEDIUM".format(myid) in text or "ESTIMATE Agent[{:02d}] BODYGUARD".format(myid) in text:
                player_score[source - 1] -=50 
            
            # Increase the hate points of the players who estimate me in the werewolf team
            elif "ESTIMATE Agent[{:02d}] WEREWOLF".format(myid) in text or "ESTIMATE Agent[{:02d}] POSSESSED".format(myid) in text:
                player_score[source - 1] +=50 

            # Increase hate points if someone wants to vote for me or asks someone to vote for me 
            elif "VOTE Agent[{:02d}]".format(myid) in text:
                player_score[source - 1] +=70
        
        # Useful for targeting the real seer in strategy 1 of werewolf
        elif(type =="talk" and  "SEER" in text):
            source = getattr(row,"agent")
            logging.debug("The seer is coming out")

            if "COMINGOUT Agent[{:02d}] SEER".format(source) in text:
                player_score[source-1] += 10

# talk function for werewolf
def werewolf_talk(hate, strategy_no, day_no, myid, ind):

    logging.debug("# WEREWOLF TALK")
  
    # I have implemented 2 strategies for the werewolf agent which will be implemented randomly for each game
   
    logging.debug("Strategy followed is {}".format(strategy_no))

    # First strategy#######################################

    # In this strategy I will act as a SEER and I will try to eliminate the real seer(if exists)
    # and also, I will try to remove the other players by divining them as werewolf

    sentence = [
     "REQUEST ANY (VOTE Agent[{:02d}])",
     "ESTIMATE Agent[{:02d}] WEREWOLF",
     "VOTE Agent[{:02d}]",
      ]

    if(strategy_no == 0 ):
        
        strategyone_sentences = ["REQUEST ANY (VOTE Agent[{:02d}])","ESTIMATE Agent[{:02d}] WEREWOLF","VOTE Agent[{:02d}]"]

        # I will come out as seer on day one and only one time
        if(day_no == 1 and ind == 0):
            logging.debug("The day number is {}".format(day_no))
            first_sentence = "COMINGOUT Agent[{:02d}] SEER".format(myid)
            return first_sentence

        # I will divine the most hated agent only one time per day at the 4th talk by me
        elif(ind == 3):
            
            logging.debug("The ind is {}".format(day_no))
            return "DIVINED Agent[{:02d}] WEREWOLF".format(hate)

        else:
            return strategyone_sentences[randint(0,2)].format(hate)


    #Second strategy ##########################################  

    # # In this strategy I will pretend to be a normal villager and I will try to gain trust of other agents 
    elif(strategy_no == 1):

        strategytwo_sentences = ["REQUEST ANY (VOTE Agent[{:02d}])","ESTIMATE Agent[{:02d}] WEREWOLF","VOTE Agent[{:02d}]","REQUEST ANY (DIVINATION Agent[{:02d}])"]

        # logging.debug("The day number is {}".format(day_no))
        return strategytwo_sentences[randint(0,3)].format(hate)


