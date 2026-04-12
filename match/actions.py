import random


def finalization(match, long_shot=False):
    finishing = match.player.attributes["finishing"]

    base = finishing * (0.7 if long_shot else 1.0)

    if random.randint(0, 100) < base * 0.25:
        match.goal_player_team()
        match.ui.show("⚽ GOOOOOL!")
        match.player_stats["goals"] += 1
    else:
        match.ui.show("❌ Finalização ruim!")


def assist_attempt(match):
    passing = match.player.attributes["passing"]

    if random.randint(0, 100) < passing:
        match.ui.show("🅰️ Passe decisivo!")

        # chance de gol depois da assistência
        if random.randint(0, 100) < 50:
            match.goal_player_team()
            match.ui.show("⚽ Gol do companheiro!")
            match.player_stats["assists"] += 1
        else:
            match.ui.show("❌ Companheiro desperdiçou!")
    else:
        match.ui.show("❌ Passe interceptado!")
        match.player_stats["possession_lost"] += 1
