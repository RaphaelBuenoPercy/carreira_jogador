from player.playstyles import get_playstyle


class Player:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.position = data["position"]
        self.team_id = data.get("team_id")

        self.attributes = data["attributes"]

        self.form = data.get("form", 70)
        self.morale = data.get("morale", 70)
        self.fitness = data.get("fitness", 100)

        self.traits = data.get("traits", [])
        self.role = data.get("role", "normal")  # star, captain, prospect
        self.playstyle = get_playstyle(self)

        self.match_history = []  # lista de partidas detalhadas
        # estatísticas da temporada
        self.stats = {"games": 0, "goals": 0, "assists": 0, "rating_sum": 0}

    def get_rating(self):
        return sum(self.attributes.values()) / len(self.attributes)

    def get_match_rating(self):
        base = self.get_rating()
        fatigue_penalty = (100 - self.fitness) * 0.05

        modifier = (self.form * 0.2 + self.morale * 0.1 + fatigue_penalty * 0.08) / 10

        return base + modifier

    def apply_fatigue(self):
        self.fitness = max(0, self.fitness - 5)

    def recover(self):
        self.fitness = min(100, self.fitness + 10)

    def update_form(self, delta):
        self.form = max(0, min(100, self.form + delta))

    def update_morale(self, delta):
        self.morale = max(0, min(100, self.morale + delta))

    def record_match(self, rating, goals=0, assists=0):
        self.stats["games"] += 1
        self.stats["goals"] += goals
        self.stats["assists"] += assists
        self.stats["rating_sum"] += rating

        # impacto na moral
        if rating > 7:
            self.update_morale(3)
        elif rating < 5:
            self.update_morale(-3)

    def record_match_detailed(self, match_data):
        """
        match_data = {
            "opponent": str,
            "score": "2-1",
            "rating": float,
            "stats": dict (player_stats)
        }
        """
        self.match_history.append(match_data)

        # também atualiza o resumo da temporada
        self.record_match(
            rating=match_data["rating"],
            goals=match_data["stats"].get("goals", 0),
            assists=match_data["stats"].get("assists", 0),
        )

    def get_season_stats(self):
        aggregate = {}

        for match in self.match_history:
            for k, v in match["stats"].items():
                aggregate[k] = aggregate.get(k, 0) + v

        return aggregate

    def get_average_rating(self):
        if self.stats["games"] == 0:
            return 0
        return self.stats["rating_sum"] / self.stats["games"]
