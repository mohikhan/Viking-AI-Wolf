from Viking import *

# For the possessed role I have experimented it with 2 strategies : a friendly role which means if someone is 
# hostile to me then I will try to gain his confidence that i am not a werewolf and a negative role for which
# I have voted for the most hated agent 

#Update function for the villager
def possessed_update(base_info,diff_data,request,player_total,player_score,myid):
    
    logging.debug("# POSSESSED UPDATE")
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
            
            #Reduce the hate points for the players who think I am a human
            if "DIVINED Agent[{:02d}] HUMAN".format(myid)  in text:
                player_score[source - 1] -=20

            #Reduce the hate points for the players who wants the bodyguard to guard me
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
        
        # else

def possessed_talk(hate, strategy_no, day_no, myid, ind):

    logging.debug("# POSSESSED TALK")
  

  # 2 strategies for possessed 
  
  # In the first strategy the possessed will try to be friendly with the agent who he hates the most

  # In the second strategy the possessed will behave normally to eliminate the agent who he hates the most
   
    logging.debug("Strategy followed is {}".format(strategy_no))

    # First strategy#######################################

    sentence = [
     "REQUEST ANY (VOTE Agent[{:02d}])",
     "ESTIMATE Agent[{:02d}] WEREWOLF",
     "VOTE Agent[{:02d}]",
      ]

    if(strategy_no == 0 ):
        
        
        # I will come out as seer on day one and only one time
        if(day_no == 1 and ind == 0):
            logging.debug("The day number is {}".format(day_no))
            first_sentence = "COMINGOUT Agent[{:02d}] SEER".format(myid)
            return first_sentence

        # I will divine the most hated agent only one time per day at the 3rd talk by me
        elif(ind == 2):
            
            logging.debug("The ind is {}".format(day_no))
            return "DIVINED Agent[{:02d}] HUMAN".format(hate)
       
        # I will return friendly sentence to make him feel I am not hostile
        else:

            return "ESTIMATE Agent[{:02d}] VILLAGER".format(hate)

    # Second strategy ##########################################  

    elif(strategy_no == 1):

        strategytwo_sentences = ["REQUEST ANY (VOTE Agent[{:02d}])","REQUEST ANY (DIVINATION Agent[{:02d}])","ESTIMATE Agent[{:02d}] WEREWOLF","VOTE Agent[{:02d}]"]
        
        # Returning negative sentences by me
        logging.debug("The day number is {}".format(day_no))
        return strategytwo_sentences[randint(0,3)].format(hate)


