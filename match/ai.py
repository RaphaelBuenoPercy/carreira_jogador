import random


def simulate_moment(match):
    strength_a = match.player_team.get_team_strength()
    strength_b = match.opponent_team.get_team_strength()

    prob = strength_a / (strength_a + strength_b)

    if random.random() < prob:
        if random.random() < 0.08:
            match.score_a += 1
            match.events.append("Gol do seu time")
    else:
        if random.random() < 0.08:
            match.score_b += 1
            match.events.append("Gol adversário")
