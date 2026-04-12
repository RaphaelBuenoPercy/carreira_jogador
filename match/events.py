import random


def foul(match, in_box=False):
    match.ui.show("🚨 Falta cometida!")

    severity = random.random()

    if severity < 0.6:
        match.ui.show("⚠️ Só falta.")
    elif severity < 0.9:
        yellow(match)
    else:
        red(match)

    if in_box:
        penalty(match)


def yellow(match):
    if match.player.id in match.yellow_cards:
        match.ui.show("🟥 Segundo amarelo! Expulso!")
        match.red_cards.add(match.player.id)
    else:
        match.ui.show("🟨 Cartão amarelo!")
        match.yellow_cards.add(match.player.id)


def red(match):
    match.ui.show("🟥 Cartão vermelho direto!")
    match.red_cards.add(match.player.id)


def penalty(match):
    match.ui.show("⚡ PÊNALTI!")

    choice = match.ui.choice("Como você bate?", ["Colocado", "Forte", "Cavadinha"])

    finishing = match.player.attributes["finishing"]

    if choice == 1:
        chance = finishing * 0.9
    elif choice == 2:
        chance = finishing * 1.1
    else:
        chance = finishing * 0.7

    if random.randint(0, 100) < chance:
        match.score_player_team += 1
        match.ui.show("⚽ Gol de pênalti!")
    else:
        match.ui.show("❌ Perdeu o pênalti!")
