import random

FORMATIONS = {
    "4-4-2": ["GK", "RB", "CB", "CB", "LB", "RM", "CM", "CM", "LM", "ST", "ST"],
    "4-3-3": ["GK", "RB", "CB", "CB", "LB", "CDM", "CM", "CM", "RW", "LW", "ST"],
    "4-2-3-1": ["GK", "RB", "CB", "CB", "LB", "CDM", "CDM", "CAM", "RW", "LW", "ST"],
    "4-3-1-2": ["GK", "RB", "CB", "CB", "LB", "RM", "CDM", "LM", "CAM", "ST", "ST"],
    "3-4-3": ["GK", "CB", "CB", "CB", "RWB", "CM", "CM", "LWB", "RW", "LW", "ST"],
    "3-5-2": ["GK", "CB", "CB", "CB", "RWB", "CM", "CM", "LWB", "CAM", "ST", "ST"],
    "3-2-4-1": ["GK", "CB", "CB", "CB", "RM", "CDM", "CDM", "CAM", "CAM", "LM", "ST"],
}

POSITION_COMPATIBILITY = {
    "CB": ["CB"],
    "LB": ["LB", "LWB"],
    "RB": ["RB", "RWB"],
    "CDM": ["CDM", "CM"],
    "CM": ["CM", "CDM", "CAM"],
    "CAM": ["CAM", "CM"],
    "LW": ["LW", "LM"],
    "RW": ["RW", "RM"],
    "LM": ["LM", "LW"],
    "RM": ["RM", "RW"],
    "ST": ["ST"],
    "GK": ["GK"],
}


class Team:
    def __init__(self, data, players):
        self.id = data["id"]
        self.name = data["name"]
        self.league_id = data["league_id"]

        self.reputation = data.get("reputation", 70)
        self.style = data.get("style", "balanced")
        self.formation = data.get("formation", "4-4-2")

        self.form = data.get("form", 70)
        self.morale = data.get("morale", 70)
        self.chemistry = data.get("chemistry", 70)

        self.players = players

    def get_starting_xi(self):
        formation = FORMATIONS.get(self.formation, FORMATIONS["4-4-2"])

        xi = []
        used_players = set()

        for pos in formation:
            # filtra jogadores da posição
            candidates = [
                p
                for p in self.players
                if p.position in POSITION_COMPATIBILITY.get(pos, [pos])
                and p.id not in used_players
            ]

            # fallback: se não tiver jogador da posição
            if not candidates:
                candidates = [p for p in self.players if p.id not in used_players]

            # escolhe o melhor
            best = max(candidates, key=lambda p: (p.get_match_rating(), p.fitness))

            xi.append(best)
            used_players.add(best.id)

        return xi

    def get_bench(self):
        return sorted(self.players, key=lambda p: p.get_match_rating(), reverse=True)[
            11:18
        ]

    def get_team_strength(self):
        xi = self.get_starting_xi()

        base = sum(p.get_match_rating() for p in xi) / len(xi)

        tactical_bonus = self._get_tactical_bonus()
        condition_bonus = self.form * 0.1 + self.morale * 0.05 + self.chemistry * 0.05

        return base + tactical_bonus + condition_bonus

    def _get_tactical_bonus(self):
        if self.style == "offensive":
            return 2
        elif self.style == "defensive":
            return 1
        elif self.style == "counter":
            return random.uniform(0, 3)
        return 1.5

    def update_team_form(self, result):
        if result == "win":
            self.form += 4
            self.morale += 5
        elif result == "loss":
            self.form -= 4
            self.morale -= 6
        else:
            self.form += 1

        self.form = max(0, min(100, self.form))
        self.morale = max(0, min(100, self.morale))

    def apply_fatigue(self):
        for p in self.get_starting_xi():
            p.apply_fatigue()

    def recover_players(self):
        for p in self.players:
            p.recover()
