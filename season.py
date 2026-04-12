from match import Match
import random

class Season:
    def __init__(self, league):
        self.league = league
        self.schedule = []
        self.current_round = 0

    def generate_schedule(self):
        teams = self.league.teams[:]
        random.shuffle(teams)

        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                self.schedule.append((teams[i], teams[j]))

    def play_next_round(self):
        if self.current_round >= len(self.schedule):
            return None

        team_a, team_b = self.schedule[self.current_round]

        match = Match(team_a, team_b)
        match.simulate()

        self.league.register_result(match, team_a, team_b)

        self.current_round += 1

        return match

    def is_finished(self):
        return self.current_round >= len(self.schedule)