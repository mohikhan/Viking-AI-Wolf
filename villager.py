from Viking import *

#Update function for the villager
def villager_update(base_info,diff_data,request,player_total,player_score,myid):

    logging.debug("# Villager UPDATE")
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
