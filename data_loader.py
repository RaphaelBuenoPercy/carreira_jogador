import json
from team import Team
from player.player_model import Player


def load_teams_and_players():
    # carregar arquivos
    with open("data/teams.json", encoding="utf-8") as f:
        teams_data = json.load(f)

    with open("data/players.json", encoding="utf-8") as f:
        players_data = json.load(f)

    # organizar jogadores por time
    players_by_team = {}

    for pdata in players_data:
        player = Player(pdata)

        tid = pdata.get("team_id")

        if tid not in players_by_team:
            players_by_team[tid] = []

        players_by_team[tid].append(player)

    # criar times com jogadores
    teams = []

    for tdata in teams_data:
        tid = tdata["id"]
        team_players = players_by_team.get(tid, [])

        team = Team(tdata, team_players)
        teams.append(team)

    return teams
