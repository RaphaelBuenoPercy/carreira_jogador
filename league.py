class League:
    def __init__(self, data, teams):
        self.id = data["id"]
        self.name = data["name"]
        self.teams = teams

        self.table = {
            team.id: {
                "points": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0
            }
            for team in teams
        }

    def register_result(self, match, team_a, team_b):
        ta = self.table[team_a.id]
        tb = self.table[team_b.id]

        ta["goals_for"] += match.score_a
        ta["goals_against"] += match.score_b

        tb["goals_for"] += match.score_b
        tb["goals_against"] += match.score_a

        result = match.get_result()

        if result == "A":
            ta["points"] += 3
            ta["wins"] += 1
            tb["losses"] += 1
        elif result == "B":
            tb["points"] += 3
            tb["wins"] += 1
            ta["losses"] += 1
        else:
            ta["points"] += 1
            tb["points"] += 1
            ta["draws"] += 1
            tb["draws"] += 1

    def get_standings(self):
        return sorted(
            self.table.items(),
            key=lambda x: (
                x[1]["points"],
                x[1]["goals_for"] - x[1]["goals_against"]
            ),
            reverse=True
        )