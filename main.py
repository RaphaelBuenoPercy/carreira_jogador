from season_file import Season
from player.player_model import Player
from ui.text_interface import TextUI
from league import create_league

ui = TextUI()


def create_player(ui):
    name = input("Nome do jogador: ")

    pos_choice = ui.choice(
        "Escolha a posição:",
        ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LW", "RW", "ST"],
    )

    positions = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LW", "RW", "ST"]
    position = positions[pos_choice - 1]

    # atributos base (simples por enquanto)
    attributes = {
        "finishing": 90,
        "passing": 90,
        "dribbling": 90,
        "defense": 90,
        "physical": 90,
        "pace": 90,
        "mental": 90,
    }

    return {"name": name, "position": position, "attributes": attributes}


def choose_team(ui, league):
    options = [team.name for team in league.teams]

    choice = ui.choice("Escolha seu time:", options)

    return league.teams[choice - 1]


# criar liga mock (ajusta conforme seu código real)
league = create_league()  # você deve ter isso

player_data = create_player(ui)
player_team = choose_team(ui, league)

player = Player(
    {
        "id": 999,
        "name": player_data["name"],
        "position": player_data["position"],
        "team_id": player_team.id,
        "attributes": player_data["attributes"],
    }
)

player_team.players.append(player)
print(f"Seu estilo: {player.playstyle}")


season = Season(league)
season.generate_schedule()


standings = league.get_standings()

print("\n📊 TABELA:\n")
for i, (team_id, data) in enumerate(standings, 1):
    team = next(t for t in league.teams if t.id == team_id)

    print(f"{i}. {team.name} - {data['points']} pts")


def show_menu(ui):
    return ui.choice(
        "O que deseja fazer?",
        ["Jogar próxima partida", "Ver tabela", "Ver histórico do jogador", "Sair"],
    )


# MOSTRAR HISTÓRICO DO JOGADOR


def show_player_history(player):
    print("\n📘 HISTÓRICO DE PARTIDAS:\n")

    if not player.match_history:
        print("Nenhum jogo ainda.")
        return

    for match in player.match_history:
        print(
            f"vs {match['opponent']} | {match['score']} | "
            f"Nota: {match['rating']:.1f}"
        )


# MOSTRAR TABELA LIGA


def show_table(league):
    standings = league.get_standings()

    print("\n📊 TABELA:\n")

    for i, (team_id, data) in enumerate(standings, 1):
        team = next(t for t in league.teams if t.id == team_id)

        saldo = data["goals_for"] - data["goals_against"]

        print(
            f"{i}. {team.name} | {data['points']} pts | "
            f"{data['wins']}V {data['draws']}E {data['losses']}D | "
            f"SG: {saldo}"
        )


while True:
    choice = show_menu(ui)

    if choice == 1:
        if season.is_finished():
            print("\n🏁 Temporada acabou!")
            continue

        season.play_next_round(player=player, ui=ui)

    elif choice == 2:
        show_table(league)

    elif choice == 3:
        show_player_history(player)

    elif choice == 4:
        print("Saindo...")
        break
