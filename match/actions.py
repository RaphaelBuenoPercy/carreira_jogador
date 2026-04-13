import random
import time
from .stats_file import (
    register_save,
    register_pass,
    register_shot,
    register_dribble,
    register_tackle,
    register_goal,
)
from soupsieve import match


def pick_rebound_player(team, original_shooter):
    players = [p for p in team.get_starting_xi() if p != original_shooter]

    weights = []
    for p in players:
        positioning = p.attributes.get("iq", 70)
        finishing = p.attributes.get("finishing", 70)

        # atacante e ponta pegam mais rebote
        pos_bonus = {
            "ST": 1.4,
            "LW": 1.2,
            "RW": 1.2,
            "CAM": 1.1,
            "CM": 0.8,
            "CDM": 0.5,
            "CB": 0.7,
            "LB": 0.2,
            "RB": 0.2,
        }

        weight = (positioning + finishing) * pos_bonus.get(p.position, 1)
        weights.append(weight)

    return random.choices(players, weights=weights, k=1)[0]


def get_opponent_goalkeeper(match):
    xi = match.opponent_team.get_starting_xi()

    for p in xi:
        if p.position == "GK":
            return p

    return xi[0]  # fallback


def calculate_save_chance(gk, xg):
    reflex = gk.attributes.get("defense", 70)
    positioning = gk.attributes.get("iq", 70)

    base = (reflex * 0.7 + positioning * 0.3) / 100

    # quanto maior o xG, mais difícil defender
    difficulty = 1 - xg

    return base * difficulty


def calculate_goal_chance(player, xg, match):
    finishing = player.attributes["finishing"]
    fitness = player.fitness / 100
    form = player.form / 100

    # -------------------
    # 🧱 GOLEIRO ADVERSÁRIO
    # -------------------
    opponent_gk = get_opponent_goalkeeper(match)
    gk_skill = opponent_gk.attributes.get("defense", 70) / 100

    # quanto maior o GK, menor a chance
    gk_factor = 1 - (gk_skill * 0.5)  # reduz até 50%

    # -------------------
    # 🎯 POSIÇÃO
    # -------------------
    pos_bonus = {
        "ST": 1.3,
        "LW": 1.1,
        "RW": 1.1,
        "CAM": 1.0,
        "CM": 0.8,
        "CDM": 0.6,
        "CB": 0.4,
        "LB": 0.5,
        "RB": 0.5,
        "GK": 0.1,
    }

    base = finishing / 100

    return (
        base
        * pos_bonus.get(player.position, 1)
        * xg
        * fitness  # cansaço
        * form  # fase
        * gk_factor  # goleiro adversário
    )


def pick_scorer(team):
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
            "CB": 0.3,
            "LB": 0.4,
            "RB": 0.4,
            "GK": 0.1,
        }

        weight = finishing * pos_weight.get(p.position, 1)
        weights.append(weight)

    return random.choices(xi, weights=weights, k=1)[0]


def calculate_assist_chance(player):
    passing = player.attributes["passing"]

    pos_bonus = {
        "CAM": 1.3,
        "CM": 1.1,
        "LW": 1.0,
        "RW": 1.0,
        "LB": 0.9,
        "RB": 0.9,
        "CDM": 0.8,
        "ST": 0.6,
        "CB": 0.3,
    }

    return (passing / 100) * pos_bonus.get(player.position, 1)


def finalization(match, xg=None, long_shot=False):
    player = match.player

    # -------------------
    # 🎯 DEFINIÇÃO DO xG
    # -------------------
    if xg is None:
        xg = random.uniform(0.05, 0.2) if long_shot else random.uniform(0.2, 0.5)

    # registra stats básicos SEMPRE
    match.player_stats["shots"] += 1
    match.player_stats["xG"] += xg

    # -------------------
    # 🧠 FADIGA AFETA FINALIZAÇÃO
    # -------------------
    fatigue_factor = player.fitness / 100  # 0 a 1

    # -------------------
    # 🎯 CHANCE DE GOL
    # -------------------
    chance = calculate_goal_chance(player, xg, match) * fatigue_factor

    # -------------------
    # 🧤 GOLEIRO ADVERSÁRIO
    # -------------------
    gk = get_opponent_goalkeeper(match)

    # goleiro mais forte → mais defesa
    gk_skill = gk.attributes.get("defense", 70)
    save_chance = calculate_save_chance(gk, xg) * (gk_skill / 100)

    # -------------------
    # ⚽ GOL DIRETO
    # -------------------
    if random.random() < chance:
        time.sleep(2)
        match.goal_player_team(scorer=player.name, assist=None)
        match.player_stats["goals"] += 1
        match.player_stats["shots_on_target"] += 1
        return

    # -------------------
    # 🧤 DEFESA DO GOLEIRO
    # -------------------
    if random.random() < save_chance:
        register_save(match)
        match.player_stats["shots_on_target"] += 1

        saves = [
            "🧤 DEFESAÇA DO GOLEIRO!!!",
            "🚀 DEFESA IMPRESSIONANTE!",
            "😱 MILAGRE DO GOLEIRO!",
            "🧱 PAREDE HUMANA!",
        ]

        time.sleep(2)
        match.ui.show("\n" + random.choice(saves))

        # -------------------
        # 🔁 REBOTE
        # -------------------
        if random.random() < 0.4:
            rebound_player = pick_rebound_player(match.player_team, player)

            time.sleep(1)
            match.ui.show(f"💥 Rebote sobra para {rebound_player.name}!")

            rebound_xg = xg * 0.7

            # rebote NÃO é do player → não atualiza stats dele
            rebound_chance = calculate_goal_chance(rebound_player, rebound_xg, match)

            if random.random() < rebound_chance:
                time.sleep(2)
                match.goal_player_team(scorer=rebound_player.name, assist=None)
            else:
                time.sleep(2)
                match.ui.show("❌ Perdeu o rebote!")

    # -------------------
    # ❌ FORA
    # -------------------
    else:
        time.sleep(2)
        match.ui.show("❌ Finalização pra fora!")


def assist_attempt(match):
    passing = match.player.attributes["passing"]
    fitness = match.player.fitness / 100

    chance_pass = (passing / 100) * fitness

    if random.random() < chance_pass:
        print("\n>>> CHANCE CLARA <<<")
        time.sleep(2)
        match.ui.show("🅰️ Passe decisivo!")
        assister = match.player
        scorer = pick_scorer(match.player_team)

        xg = random.uniform(0.1, 0.4)

        chance = calculate_goal_chance(scorer, xg, match)

        gk = get_opponent_goalkeeper(match)
        save_chance = calculate_save_chance(gk, xg)

        if random.random() < chance:
            time.sleep(2)
            match.goal_player_team(scorer=scorer.name, assist=assister.name)
            match.player_stats["assists"] += 1

        else:

            if random.random() < save_chance:
                time.sleep(2)
                saves = [
                    "🧤 DEFESAÇA DO GOLEIRO!!!",
                    "🚀 DEFESA IMPRESSIONANTE!",
                    "😱 MILAGRE DO GOLEIRO!",
                    "🧱 PAREDE HUMANA!",
                ]

                match.ui.show("\n" + random.choice(saves))
                match.player_stats["shots_on_target"] += 1
                if random.random() < 0.4:
                    rebound_player = pick_rebound_player(match.player_team, scorer)
                    time.sleep(1)
                    match.ui.show(f"💥 Rebote sobra para {rebound_player.name}!")

                    if random.random() < calculate_goal_chance(
                        rebound_player, xg * 0.7, match
                    ):
                        time.sleep(2)
                        match.goal_player_team(
                            scorer=rebound_player.name, assist=assister.name
                        )
                    else:
                        time.sleep(2)
                        match.ui.show("❌ Perdeu o rebote!")
            else:
                time.sleep(2)
                match.ui.show("❌ Finalização ruim!")

    else:
        time.sleep(2)
        match.ui.show("❌ Passe interceptado!")
        match.player_stats["possession_lost"] += 1
