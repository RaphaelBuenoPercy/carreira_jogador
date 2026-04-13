import random


def pick_attacker(team):
    xi = team.get_starting_xi()

    weights = []
    for p in xi:
        finishing = p.attributes["finishing"]

        pos_weight = {
            "ST": 1.5,
            "LW": 1.2,
            "RW": 1.2,
            "CAM": 1.0,
            "CM": 0.7,
            "CDM": 0.5,
            "CB": 0.4,
            "LB": 0.3,
            "RB": 0.3,
            "GK": 0.01,
        }

        weights.append(finishing * pos_weight.get(p.position, 1))

    return random.choices(xi, weights=weights, k=1)[0]


def pick_assister(team, scorer):
    xi = [p for p in team.get_starting_xi() if p != scorer]

    weights = []
    for p in xi:
        passing = p.attributes["passing"]

        pos_weight = {
            "CAM": 1.3,
            "CM": 1.1,
            "LW": 1.1,
            "RW": 1.1,
            "LB": 0.9,
            "RB": 0.9,
            "CDM": 0.8,
            "ST": 0.7,
            "CB": 0.3,
        }

        weights.append(passing * pos_weight.get(p.position, 1))

    return random.choices(xi, weights=weights, k=1)[0]


def simulate_moment(match):
    strength_a = match.player_team.get_team_strength()
    strength_b = match.opponent_team.get_team_strength()

    prob = strength_a / (strength_a + strength_b)

    # -------------------
    # TIME DO JOGADOR ATACA
    # -------------------
    if random.random() < prob:
        if random.random() < 0.08:

            scorer = pick_attacker(match.player_team)
            while scorer == match.player:
                scorer = pick_attacker(match.player_team)

            assister = pick_assister(match.player_team, scorer)
            while assister == match.player:
                assister = pick_assister(match.player_team, scorer)

            match.goal_player_team(scorer=scorer.name, assist=assister.name)

    # -------------------
    # ADVERSÁRIO ATACA
    # -------------------
    else:
        if random.random() < 0.08:
            scorer = pick_attacker(match.opponent_team)
            assister = pick_assister(match.opponent_team, scorer)

            match.goal_opponent_team(scorer=scorer.name, assist=assister.name)
