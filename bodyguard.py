from Viking import *

#Update function for the bodyguard
def bodyguard_update(base_info,diff_data,request,player_total,player_score,myid,vulnerability):

    logging.debug("# BODYGUARD UPDATE")

    #Reduce the score of dead players
    if (request == "DAILY_INITIALIZE"):
        for i in range(player_total):
            if (base_info["statusMap"][str(i+1)] == "DEAD"):
                player_score[i] -= 10000
                vulnerability[i] -= 10000

    
    for row in diff_data.itertuples():
        type = getattr(row,"type")
        text = getattr(row,"text") 
        

       #########################################################################################
        # I will figure out who is the most vulnerable agent to the attack of wolves and I will guard him

        if(type == "talk" and   ("SEER" in text  or "MEDIUM" in text)):
            
            source = getattr(row,"agent")
            logging.debug("Sentence containing me: {}".format(text))

            if "COMINGOUT Agent[{:02d}] SEER".format(source) in text or "COMINGOUT Agent[{:02d}] MEDIUM".format(source) in text:
                vulnerability[source-1] += 20


       #If someone else is coming out as bodyguard he is probably lying
        if(type == "talk" and   "BODYGUARD" in text):

            source = getattr(row,"agent")

            if "COMINGOUT Agent[] BODYGUARD".format(source) in text:

                player_score[source-1] += 20
                vulnerability[source-1] -= 20

            

        # Voting in diff data
        if (type == "vote"):
            voter = getattr(row,"idx")
            target = getattr(row,"agent")
            # If the voter has voted for me to be a werewolf I will give him 100 hate points
            if (target == myid):
                logging.debug("Agent {} voted for me!".format(voter))
                player_score[voter-1] += 100

                # I will reduce his vulnerability score so that I will never guard him
                vulnerability[voter - 1] -=200


       # I will also reduce the vulnerability to avoid guarding enemy agents###############################################

        elif (type == "talk" and "[{:02d}]".format(myid) in text):
            
            # they are talking about me
            source = getattr(row,"agent")
            logging.debug("Sentence containing me: {}".format(text))
            
            #Reduce the hate points for the players who think I am a human
            if "DIVINED Agent[{:02d}] HUMAN".format(myid)  in text:
                player_score[source - 1] -=60

                vulnerability[source-1] += 60

               #Reduce the hate points for the players who wants the bodyguard to guard me
            elif "(GUARD Agent[{:02d}])".format(myid) in text:
                player_score[source - 1] -= 40

                vulnerability[source-1] += 40
            
            #Increase the hate points for the agent who divines me as a werewolf 
            #Also this agent is guaranteed werewolf because he wrongly divines me as a werewolf as I am avillager
            elif "DIVINED Agent[{:02d}] WEREWOLF".format(myid)  in text:
                player_score[source - 1] +=50 

                vulnerability[source-1] -= 50
            
            #Reduce the hate points for the players who estimate me in the human team
            elif "ESTIMATE Agent[{:02d}] VILLAGER".format(myid) in text or "ESTIMATE Agent[{:02d}] SEER".format(myid) in text or "ESTIMATE Agent[{:02d}] MEDIUM".format(myid) in text or "ESTIMATE Agent[{:02d}] BODYGUARD".format(myid) in text:
                player_score[source - 1] -=50 

                vulnerability[source-1] += 50
            
            #Increase the hate points of the players who estimate me in the werewolf team
            elif "ESTIMATE Agent[{:02d}] WEREWOLF".format(myid) in text or "ESTIMATE Agent[{:02d}] POSSESSED".format(myid) in text:
                player_score[source - 1] +=50 

                vulnerability[source-1] -= 50

            #Increase hate points if someone wants to vote for me or asks someone to vote for me 
            elif "VOTE Agent[{:02d}]".format(myid) in text:
                player_score[source - 1] +=70

                vulnerability[source-1] -= 70



def bodyguard_talk(hate,ally,ind):

    logging.debug("# TALK")
    
    

    #Taking help from allies
    # allysentence0 = ["REQUEST Agent[{:02d}] (VOTE Agent[{:02d}])", "REQUEST ANY (GUARD Agent[{:02d}])" ,"ESTIMATE AGENT[]"]
    
    #sentences for the players i hate
    hatesentence = [
    "REQUEST ANY (VOTE Agent[{:02d}])", "ESTIMATE Agent[{:02d}] WEREWOLF","VOTE Agent[{:02d}]","REQUEST ANY (DIVINATION Agent[{:02d}])"
    ]
    
    # if(ind%4 == 0):

    #     return allysentence[]


    return hatesentence[randint(0,3)].format(hate)
