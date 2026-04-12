import random

class Match:
    def __init__(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b

        self.score_a = 0
        self.score_b = 0

        self.events = []
        self.player_stats = {}

    def simulate(self):
        strength_a = self.team_a.get_team_strength()
        strength_b = self.team_b.get_team_strength()

        total = strength_a + strength_b

        prob_a = strength_a / total

        # número de eventos (momentos de ataque)
        events_count = random.randint(5, 12)

        for minute in range(events_count):
            if random.random() < prob_a:
                self._attempt_goal(self.team_a, "A")
            else:
                self._attempt_goal(self.team_b, "B")

        self._finalize()

        return self

    def _attempt_goal(self, team, label):
        player = random.choice(team.get_starting_xi())

        chance = player.attributes["finishing"] / 100

        if random.random() < chance:
            if label == "A":
                self.score_a += 1
            else:
                self.score_b += 1

            self.events.append(f"⚽ Gol de {player.name}")
            self._record_player(player, goal=True)
        else:
            self.events.append(f"❌ {player.name} perdeu chance")

    def _record_player(self, player, goal=False):
        if player.id not in self.player_stats:
            self.player_stats[player.id] = {
                "goals": 0,
                "rating": 6
            }

        if goal:
            self.player_stats[player.id]["goals"] += 1
            self.player_stats[player.id]["rating"] += 1

    def _finalize(self):
        self.team_a.apply_fatigue()
        self.team_b.apply_fatigue()

        result = self.get_result()

        if result == "A":
            self.team_a.update_team_form("win")
            self.team_b.update_team_form("loss")
        elif result == "B":
            self.team_b.update_team_form("win")
            self.team_a.update_team_form("loss")
        else:
            self.team_a.update_team_form("draw")
            self.team_b.update_team_form("draw")

    def get_result(self):
        if self.score_a > self.score_b:
            return "A"
        elif self.score_b > self.score_a:
            return "B"
        return "draw"