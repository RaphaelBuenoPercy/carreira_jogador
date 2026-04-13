import random

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


POSITION_TEMPLATES = {
    "ST": {
        "finishing": (70, 90),
        "pace": (65, 85),
        "dribbling": (60, 80),
        "passing": (40, 70),
        "defense": (20, 40),
    },
    "CM": {
        "passing": (65, 90),
        "dribbling": (60, 80),
        "defense": (50, 75),
        "finishing": (50, 70),
    },
    "CAM": {
        "passing": (75, 90),
        "dribbling": (70, 90),
        "finishing": (60, 80),
        "defense": (30, 50),
    },
    "CDM": {
        "defense": (70, 90),
        "passing": (60, 80),
        "physical": (65, 85),
        "finishing": (30, 50),
    },
    "CB": {
        "defense": (75, 95),
        "physical": (70, 90),
        "passing": (40, 65),
        "finishing": (20, 40),
    },
    "LB": {"defense": (65, 85), "pace": (70, 90), "passing": (55, 75)},
    "RB": {"defense": (65, 85), "pace": (70, 90), "passing": (55, 75)},
    "LW": {"pace": (75, 95), "dribbling": (75, 95), "finishing": (60, 80)},
    "RW": {"pace": (75, 95), "dribbling": (75, 95), "finishing": (60, 80)},
    "GK": {"defense": (75, 95), "physical": (60, 80)},
}


def generate_attributes(position):
    base = {
        "finishing": 50,
        "passing": 50,
        "dribbling": 50,
        "defense": 50,
        "physical": 50,
        "pace": 50,
        "mental": 50,
    }

    template = POSITION_TEMPLATES[position]

    for attr, (low, high) in template.items():
        base[attr] = random.randint(low, high)

    return base


FIRST_NAMES = [
    "Lucas",
    "Mateus",
    "Rafael",
    "João",
    "Pedro",
    "Cauã",
    "Arthur",
    "Guilherme",
    "Leonardo",
    "Felipe",
    "Gabriel",
    "Enzo",
    "Bruno",
    "Felipe",
    "Diego",
    "Emanuel",
    "Gustavo",
    "Leonardo",
    "Thiago",
    "Vitor",
    "Samuel",
    "Murilo",
    "Davi",
    "Matheus",
    "Rodrigo",
    "Fernando",
    "Eduardo",
    "André",
    "Vinícius",
    "Caio",
    "Ramon",
    "Alexandre",
    "Enak",
    "César",
    "Fábio",
    "Rômulo",
    "Gustavo",
    "Ruan",
]

LAST_NAMES = [
    "Silva",
    "Souza",
    "Oliveira",
    "Santos",
    "Pereira",
    "Costa",
    "Rodrigues",
    "Almeida",
    "Nascimento",
    "Lima",
    "Araújo",
    "Fernandes",
    "Carvalho",
    "Gomes",
    "Martins",
    "Rocha",
    "Dias",
    "Alves",
    "Melo",
    "Ribeiro",
    "Barbosa",
    "Teixeira",
    "Moreira",
    "Moura",
    "Cardoso",
    "Pinto",
    "Freitas",
    "Castro",
    "Campos",
    "Vasconcelos",
    "Cavalcanti",
    "Figueiredo",
    "Siqueira",
    "Macedo",
    "Duarte",
    "Lopes",
    "Vieira",
    "Monteiro",
    "Cruz",
    "Gonçalves",
    "Mendes",
    "Carneiro",
    "Viana",
    "Neves" "Reis",
    "Borges",
]

POSITIONS_DISTRIBUTION = [
    "GK",
    "CB",
    "CB",
    "LB",
    "RB",
    "CDM",
    "CM",
    "CM",
    "CAM",
    "LW",
    "RW",
    "ST",
    "ST",
    # resto aleatório
]


def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


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
            position = random.choice(POSITIONS_DISTRIBUTION)
            player = Player(
                {
                    "id": t_id * 100 + p_id,
                    "name": f"Player_{t_id}_{p_id}",
                    "position": position,
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
