from data_loader import load_teams_and_players


def create_league():
    teams = load_teams_and_players()

    league = League(data={"id": 1, "name": "Liga"}, teams=teams)

    return league


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
                "goals_against": 0,
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
            key=lambda x: (x[1]["points"], x[1]["goals_for"] - x[1]["goals_against"]),
            reverse=True,
        )


def create_league():
    from league import League
    from team import Team
    from player.player_model import Player
    import random

    teams = []

    # cria 4 times simples (pode aumentar depois)
    for t_id in range(4):
        players = []

        for p_id in range(18):
            player = Player(
                {
                    "id": t_id * 100 + p_id,
                    "name": f"Player_{t_id}_{p_id}",
                    "position": random.choice(["ST", "CM", "CB", "LW", "RW"]),
                    "team_id": t_id,
                    "attributes": {
                        "finishing": random.randint(50, 90),
                        "passing": random.randint(50, 90),
                        "dribbling": random.randint(50, 90),
                        "defense": random.randint(50, 90),
                        "physical": random.randint(50, 90),
                        "pace": random.randint(50, 90),
                    },
                }
            )
            players.append(player)

        team = Team(
            data={"id": t_id, "name": f"Time {t_id}", "league_id": 1}, players=players
        )

        teams.append(team)

    league = League(data={"id": 1, "name": "Liga Teste"}, teams=teams)

    return league
