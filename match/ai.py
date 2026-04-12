import random


def simulate_moment(match):
    strength_a = match.player_team.get_team_strength()
    strength_b = match.opponent_team.get_team_strength()

    prob = strength_a / (strength_a + strength_b)

    if random.random() < prob:
        if random.random() < 0.25:
            match.score_player_team += 1
            match.events.append("Gol do seu time")
    else:
        if random.random() < 0.25:
            match.score_opponent += 1
            match.events.append("Gol adversário")
