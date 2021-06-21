from Viking import *

# Update function for the medium
def medium_update(base_info,diff_data,request,player_total,player_score,myid):

    logging.debug("# MEDIUM UPDATE")
    if (request == "DAILY_INITIALIZE"):
        for i in range(player_total):
            #Reducing the score of dead players
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
        

        #  I will increase the hate points of any other MEDIUM becuause probably he is lying as there
        #  is only one medium in the game   
        elif(type =="talk" and  "MEDIUM" in text):
            
            source = getattr(row,"agent")
            logging.debug("The medium is coming out")

            if "COMINGOUT Agent[{:02d}] MEDIUM".format(source) in text:
                player_score[source-1] += 60  
             
            # Increase the hate score for the agents talking like medium
            elif "IDENTIFIED" in text:
                player_score[source-1] += 10


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

            #Increase the hate points for the agent who divines me as a werewolf 
            #Also this agent is guaranteed werewolf because he wrongly divines me as a werewolf as I am in the  villager team in reality
            elif "DIVINED Agent[{:02d}] WEREWOLF".format(myid)  in text:
                player_score[source - 1] +=50 
            
            #Reduce the hate points for the players who estimate me in the human team
            elif "ESTIMATE Agent[{:02d}] VILLAGER".format(myid) in text or "ESTIMATE Agent[{:02d}] SEER".format(myid) in text or "ESTIMATE Agent[{:02d}] MEDIUM".format(myid) in text or "ESTIMATE Agent[{:02d}] BODYGUARD".format(myid) in text:
                player_score[source - 1] -=50 
            
            #Increase the hate points of the players who estimate me in the werewolf team
            elif "ESTIMATE Agent[{:02d}] WEREWOLF".format(myid) in text or "ESTIMATE Agent[{:02d}] POSSESSED".format(myid) in text:
                player_score[source - 1] +=50 

            #Increase hate points if someone wants to vote for me or asks someone to vote for me 
            elif "VOTE Agent[{:02d}]".format(myid) in text:
                player_score[source - 1] +=70

# talk function for the medium
def medium_talk(hate, day_no, myid, ind):

    logging.debug("# MEDIUM TALK")   
        
    strategyone_sentences = ["REQUEST ANY (VOTE Agent[{:02d}])","ESTIMATE Agent[{:02d}] WEREWOLF","VOTE Agent[{:02d}]","REQUEST ANY (DIVINATION Agent[{:02d}])"]

    # I will come out as medium on day one and only one time
    if(day_no == 1 and ind == 0):
        logging.debug("The day number is {}".format(day_no))
        first_sentence = "COMINGOUT Agent[{:02d}] MEDIUM".format(myid)
        return first_sentence

    else:

        return strategyone_sentences[randint(0,3)].format(hate)


    # Any other strategy.....
    # ....

 








