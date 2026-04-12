import random
from soupsieve import match
from match.stats_file import init_stats, calculate_rating
from . import ai
from .positions import gk, cb, fullback, cdm, cm, cam, winger, striker


class InteractiveMatch:

    def __init__(self, player, player_team, opponent_team, ui):
        self.player = player
        self.player_stats = init_stats(self.player)
        self.player_team = player_team
        self.opponent_team = opponent_team
        self.ui = ui

        self.score_a = 0
        self.score_b = 0

        self.minute = 0
        self.events = []

        # disciplina
        self.yellow_cards = set()
        self.red_cards = set()

    def play(self):
        self.ui.show(f"\n🏟️ {self.player_team.name} vs {self.opponent_team.name}")
        self.ui.show("Apito inicial!\n")

        total_events = random.randint(10, 18)

        for i in range(total_events):
            self.minute = int((i / total_events) * 90)

            if self._is_player_involved():
                self._player_moment()
            else:
                ai.simulate_moment(self)

        self._final_whistle()
        return self

    def _player_moment(self):
        pos = self.player.position

        self.ui.show(f"\n⏱️ {self.minute}' - A jogada passa por você!")

        if pos == "GK":
            gk.handle(self)
        elif pos == "CB":
            cb.handle(self)
        elif pos in ["LB", "RB"]:
            fullback.handle(self)
        elif pos == "CDM":
            cdm.handle(self)
        elif pos == "CM":
            cm.handle(self)
        elif pos == "CAM":
            cam.handle(self)
        elif pos in ["LW", "RW"]:
            winger.handle(self)
        elif pos == "ST":
            striker.handle(self)

    # -------------------------
    # 🏁 FINAL
    # -------------------------
    def _final_whistle(self):
        self.score_a = self.score_player_team
        self.score_b = self.score_opponent

        self.ui.show("\n🏁 Fim de jogo!")
        self.ui.show(
            f"{self.player_team.name} {self.score_player_team} x {self.score_opponent} {self.opponent_team.name}"
        )

        if self.score_player_team > self.score_opponent:
            self.player_team.update_team_form("win")
            self.opponent_team.update_team_form("loss")
        elif self.score_player_team < self.score_opponent:
            self.player_team.update_team_form("loss")
            self.opponent_team.update_team_form("win")
        else:
            self.player_team.update_team_form("draw")
            self.opponent_team.update_team_form("draw")

        self.ui.show("\n📊 Estatísticas do jogador:\n")

        for k, v in self.player_stats.items():
            self.ui.show(f"{k}: {v}")

        rating = calculate_rating(self.player, self.player_stats)

        self.ui.show(f"⭐ Nota final: {rating:.1f}\n")

        match_data = {
            "opponent": self.opponent_team.name,
            "score": f"{self.score_player_team}-{self.score_opponent}",
            "rating": rating,
            "stats": self.player_stats.copy(),
        }

        self.player.record_match_detailed(match_data)

    def get_result(self):
        if self.score_a > self.score_b:
            return "A"
        elif self.score_b > self.score_a:
            return "B"
        return "draw"

    def _is_player_involved(self):
        chance = 0.35 + (self.player.get_match_rating() / 220)
        return random.random() < chance
