import random


def finalization(match, long_shot=False):
    finishing = match.player.attributes["finishing"]

    base = finishing * (0.7 if long_shot else 1.0)

    if random.randint(0, 100) < base:
        match.score_player_team += 1
        match.ui.show("⚽ GOOOOOL!")
        match.player.record_match(8, goals=1)
    else:
        match.ui.show("❌ Finalização ruim!")
