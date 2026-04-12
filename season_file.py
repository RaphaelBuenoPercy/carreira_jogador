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
        round_matches = self.schedule[self.current_round]
        print(f"\n📅 Rodada {self.current_round + 1}")

        for team_a, team_b in round_matches:
            print(f"{team_a.name} vs {team_b.name}")

            if player and (player.team_id == team_a.id or player.team_id == team_b.id):
                player_team = team_a if player.team_id == team_a.id else team_b
                opponent = team_b if player_team == team_a else team_a

                match = InteractiveMatch(player, player_team, opponent, ui)
                match.play()
            else:
                match = Match(team_a, team_b)
                match.simulate()

            self.league.register_result(match, team_a, team_b)

        print(f"{team_a.name} vs {team_b.name}")

        if self.current_round >= len(self.schedule):
            return None

        for team in self.league.teams:
            team.recover_players()

        # 👉 se o jogador está em campo
        if player and (player.team_id == team_a.id or player.team_id == team_b.id):

            player_team = team_a if player.team_id == team_a.id else team_b
            opponent = team_b if player_team == team_a else team_a

            match = InteractiveMatch(player, player_team, opponent, ui)
            match.play()

        else:
            match = Match(team_a, team_b)
            match.simulate()

        self.league.register_result(match, team_a, team_b)

        self.current_round += 1

        return match

    def is_finished(self):
        return self.current_round >= len(self.schedule)
