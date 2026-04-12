def get_playstyle(player):
    pos = player.position
    attr = player.attributes

    if pos == "GK":
        if attr.get("passing", 0) > 75:
            return "sweeper_keeper"
        elif attr.get("reflex", 0) > 80:
            return "shot_stopper"
        else:
            return "safe_keeper"

    elif pos == "CB":
        if attr["physical"] > 80:
            return "stopper"
        elif attr.get("iq", 0) > 75:
            return "ball_playing"
        else:
            return "balanced_cb"

    elif pos in ["LB", "RB"]:
        if attr["pace"] > 80:
            return "attacking_fullback"
        elif attr["defense"] > 75:
            return "defensive_fullback"
        else:
            return "balanced_fullback"

    elif pos == "CDM":
        if attr["defense"] > 80:
            return "destroyer"
        elif attr["passing"] > 75:
            return "deep_lying_playmaker"
        else:
            return "balanced_cdm"

    elif pos == "CM":
        if attr["passing"] > 80:
            return "playmaker"
        elif attr["physical"] > 75:
            return "box_to_box"
        else:
            return "balanced_cm"

    elif pos == "CAM":
        if attr["passing"] > 80:
            return "creator"
        elif attr["finishing"] > 75:
            return "goal_threat"
        else:
            return "free_roamer"

    elif pos in ["LW", "RW"]:
        if attr["dribbling"] > 80:
            return "dribbler"
        elif attr["pace"] > 80:
            return "speedster"
        else:
            return "wide_playmaker"

    elif pos == "ST":
        if attr["finishing"] > 85:
            return "poacher"
        elif attr["physical"] > 80:
            return "target_man"
        else:
            return "mobile_forward"
