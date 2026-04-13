def init_stats(player):
    return {
        "passes_attempted": 0,
        "passes_completed": 0,
        "forward_passes": 0,
        "lateral_passes": 0,
        "backward_passes": 0,
        "shots": 0,
        "shots_on_target": 0,
        "goals": 0,
        "xG": 0,
        "assists": 0,
        "xA": 0,
        "key_passes": 0,
        "pre_assists": 0,
        "dribbles_attempted": 0,
        "dribbles_completed": 0,
        "fouls_suffered": 0,
        "possession_lost": 0,
        "possession_won": 0,
        "tackles": 0,
        "interceptions": 0,
        "blocks": 0,
        "dribbled_past": 0,
        "saves": 0,
    }


def register_save(match):
    match.player_stats["saves"] += 1


def register_pass(match, success, direction):
    s = match.player_stats
    s["passes_attempted"] += 1

    if success:
        s["passes_completed"] += 1

    if direction == "forward":
        s["forward_passes"] += 1
    elif direction == "lateral":
        s["lateral_passes"] += 1
    else:
        s["backward_passes"] += 1


def register_shot(match, on_target, xg):
    s = match.player_stats
    s["shots"] += 1
    s["xG"] += xg

    if on_target:
        s["shots_on_target"] += 1


def register_dribble(match, success):
    s = match.player_stats
    s["dribbles_attempted"] += 1

    if success:
        s["dribbles_completed"] += 1
    else:
        s["possession_lost"] += 1


def register_tackle(match, success):
    s = match.player_stats

    if success:
        s["tackles"] += 1
        s["possession_won"] += 1
    else:
        s["dribbled_past"] += 1


def register_goal(match):
    match.player_stats["goals"] += 1


def calculate_rating(player, stats):
    rating = 6.0  # base

    # -------------------
    # PASSES
    # -------------------
    if stats["passes_attempted"] > 0:
        accuracy = stats["passes_completed"] / stats["passes_attempted"]
        rating += (accuracy - 0.7) * 2

    # -------------------
    # CRIAÇÃO
    # -------------------
    rating += stats["key_passes"] * 0.3
    rating += stats["assists"] * 1.5
    rating += stats["xA"] * 0.5

    # -------------------
    # FINALIZAÇÃO
    # -------------------
    rating += stats["shots_on_target"] * 0.2
    rating += stats["xG"] * 0.5

    # -------------------
    # DRIBLE
    # -------------------
    if stats["dribbles_attempted"] > 0:
        dribble_rate = stats["dribbles_completed"] / stats["dribbles_attempted"]
        rating += dribble_rate - 0.5

    # -------------------
    # DEFESA
    # -------------------
    rating += stats["tackles"] * 0.2
    rating += stats["interceptions"] * 0.2
    rating += stats["blocks"] * 0.2

    # -------------------
    # ERROS
    # -------------------
    rating -= stats["possession_lost"] * 0.1
    rating -= stats["dribbled_past"] * 0.2

    # ==================================================
    # 🎯 AJUSTE POR POSIÇÃO (ESSENCIAL)
    # ==================================================
    pos = player.position

    # ZAGUEIRO
    if pos == "CB":
        rating += stats["tackles"] * 0.3
        rating += stats["interceptions"] * 0.3
        rating -= stats["shots"] * 0.1

    # LATERAIS
    elif pos in ["LB", "RB"]:
        rating += stats["tackles"] * 0.2
        rating += stats["dribbles_completed"] * 0.2
        rating += stats["key_passes"] * 0.2

    # VOLANTE
    elif pos == "CDM":
        rating += stats["tackles"] * 0.3
        rating += stats["interceptions"] * 0.3
        rating += stats["passes_completed"] * 0.05

    # MEIA CENTRAL
    elif pos == "CM":
        rating += stats["passes_completed"] * 0.08
        rating += stats["key_passes"] * 0.25

    # MEIA OFENSIVO
    elif pos == "CAM":
        rating += stats["key_passes"] * 0.4
        rating += stats["assists"] * 1.2
        rating += stats["xA"] * 0.7

    # PONTAS
    elif pos in ["LW", "RW"]:
        rating += stats["dribbles_completed"] * 0.3
        rating += stats["shots_on_target"] * 0.3

    # ATACANTE
    elif pos == "ST":
        rating += stats["shots_on_target"] * 0.4
        rating += stats["xG"] * 0.7
        rating -= stats["passes_completed"] * 0.03

    # GOLEIRO (simples por enquanto)
    elif pos == "GK":
        rating += stats["blocks"] * 0.5

    # clamp final
    return max(3.0, min(10.0, rating))
