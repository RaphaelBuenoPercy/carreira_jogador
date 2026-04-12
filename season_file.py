from match_class import Match
import random
from match.interactive_match import InteractiveMatch


class Season:
    def __init__(self, league):
        self.league = league
        self.schedule = []
        self.current_round = 0

    def generate_schedule(self):
        teams = self.league.teams[:]

        if len(teams) % 2 != 0:
            teams.append(None)  # bye se ímpar

        n = len(teams)
        rounds = n - 1
        half = n // 2

        schedule = []

        for r in range(rounds):
            round_matches = []

            for i in range(half):
                t1 = teams[i]
                t2 = teams[n - 1 - i]

                if t1 is not None and t2 is not None:
                    round_matches.append((t1, t2))

            schedule.append(round_matches)

            # rotação (round robin)
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]

        self.schedule = schedule

    def play_next_round(self, player=None, ui=None):
        print(f"\n📅 Rodada {self.current_round + 1}")

        round_matches = self.schedule[self.current_round]

        for team_a, team_b in round_matches:
            print(f"{team_a.name} vs {team_b.name}")

            # 👉 verifica se é jogo do player
            is_player_match = player and (
                player.team_id == team_a.id or player.team_id == team_b.id
            )

            if is_player_match:
                player_team = team_a if player.team_id == team_a.id else team_b
                opponent = team_b if player_team == team_a else team_a

                match = InteractiveMatch(player, player_team, opponent, ui)
                match.play()
            else:
                match = Match(team_a, team_b)
                match.simulate()

            # 🔥 ISSO TEM QUE RODAR PRA TODOS
            self.league.register_result(match, team_a, team_b)

        self.current_round += 1

        return match

    def is_finished(self):
        return self.current_round >= len(self.schedule)
