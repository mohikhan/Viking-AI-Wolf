from Viking import *

#Update function for the villager
def default_update(base_info,diff_data,request,player_total,player_score,myid):

    logging.debug("# DEFAULT UPDATE")
    if (request == "DAILY_INITIALIZE"):
        for i in range(player_total):
            if (base_info["statusMap"][str(i+1)] == "DEAD"):
                player_score[i] -= 10000

    
    for row in diff_data.itertuples():
        type = getattr(row,"type")
        text = getattr(row,"text")
        if (type == "vote"):
            voter = getattr(row,"idx")
            target = getattr(row,"agent")
            if target == myid:
                # They voted for me!
                logging.debug("Agent {} voted for me!".format(voter))
                player_score[voter-1] += 100
        elif (type == "talk" and "[{:02d}]".format(myid) in text):
            # they are talking about me
            source = getattr(row,"agent")
            logging.debug("Talking about me: {}".format(text))
            if "WEREWOLF" in text or "VOTE" in text:
                # Are you calling me a werewolf!?
                # Are you threateningto vote me?
                player_score[source-1] += 10
            else:
                # Stop talking about me!
                player_score[source-1] += 1

    # Print Current Hate list:
    # hate = player_score.index(max(player_score)) + 1
    # logging.debug("Hate Score: "+", ".join(str(x) for x in player_score))

def default_talk(hate):

    logging.debug("# TALK")
    #Here the wolf will firstly say that he is a seer 
    #and after that he will try to prove that the agent he hates
    #the most is a werewolf

    hatecycle = [
    "REQUEST ANY (VOTE Agent[{:02d}])",
    "ESTIMATE Agent[{:02d}] WEREWOLF",
    "VOTE Agent[{:02d}]",
    ]

    return hatecycle[randint(0,2)].format(hate)

