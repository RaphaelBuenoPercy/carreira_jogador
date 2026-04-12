from email.mime import base
import random
from soupsieve import match
from match.stats_file import init_stats, calculate_rating
from . import ai
from .positions import gk, cb, fullback, cdm, cm, cam, winger, striker
from .events import foul, red, yellow, penalty


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

        base = self._calculate_match_tempo()
        total_events = random.randint(base - 5, base + 5)

        for i in range(total_events):
            self.minute = int((i / total_events) * 90)

            if self._is_player_involved():
                self._player_moment()
            else:
                ai.simulate_moment(self)
                self._simulate_player_offball()

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

        self.ui.show("\n🏁 Fim de jogo!")
        self.ui.show(
            f"{self.player_team.name} {self.score_a} x {self.score_b} {self.opponent_team.name}"
        )

        if self.score_a > self.score_b:
            self.player_team.update_team_form("win")
            self.opponent_team.update_team_form("loss")
        elif self.score_a < self.score_b:
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
            "score": f"{self.score_a}-{self.score_b}",
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

    def _simulate_player_offball(self):
        stats = self.player_stats
        pos = self.player.position

        # frequência base (quantas ações por tick)
        activity = self.player.get_match_rating() / 100

        if random.random() > activity:
            return

        # -------------------
        # MEIAS (mais ativos)
        # -------------------
        if pos in ["CM", "CAM", "CDM"]:
            stats["passes_attempted"] += 1

            if random.random() < 0.85:
                stats["passes_completed"] += 1

            if random.random() < 0.2:
                stats["key_passes"] += 1

        # -------------------
        # PONTAS
        # -------------------
        elif pos in ["LW", "RW"]:
            stats["dribbles_attempted"] += 1

            if random.random() < 0.6:
                stats["dribbles_completed"] += 1
            else:
                stats["possession_lost"] += 1

        # -------------------
        # ATACANTE
        # -------------------
        elif pos == "ST":
            if random.random() < 0.08:
                stats["shots"] += 1
                stats["xG"] += random.uniform(0.05, 0.3)

                if random.random() < 0.4:
                    stats["shots_on_target"] += 1

        # -------------------
        # DEFESA
        # -------------------
        elif pos in ["CB", "LB", "RB"]:
            if random.random() < 0.4:
                stats["tackles"] += 1
                stats["possession_won"] += 1

            if random.random() < 0.3:
                stats["interceptions"] += 1

        # -------------------
        # GOLEIRO
        # -------------------
        elif pos == "GK":
            if random.random() < 0.3:
                stats["blocks"] += 1

    def _calculate_match_tempo(self):
        strength_a = self.player_team.get_team_strength()
        strength_b = self.opponent_team.get_team_strength()

        avg_strength = (strength_a + strength_b) / 2
        diff = abs(strength_a - strength_b)

        # base de eventos
        base_events = 10

        # times melhores → jogo mais intenso
        quality_bonus = (avg_strength - 70) * 0.5

        # jogo equilibrado → mais eventos
        balance_bonus = max(0, 10 - diff) * 1.5

        # estilos
        style_bonus = 0

        for team in [self.player_team, self.opponent_team]:
            if team.style == "offensive":
                style_bonus += 5
            elif team.style == "defensive":
                style_bonus -= 3
            elif team.style == "counter":
                style_bonus += 2

        total = base_events + quality_bonus + balance_bonus + style_bonus

        return int(max(5, min(15, total)))

    def goal_player_team(self):
        self.score_a += 1
        self.ui.show(f"⚽ {self.minute}' - GOL DO {self.player_team.name}!!!")
        self.ui.show(
            f"📊 {self.player_team.name} {self.score_a} x {self.score_b} {self.opponent_team.name}"
        )

    def goal_opponent_team(self):
        self.score_b += 1
        self.ui.show(f"⚽ {self.minute}' - GOL DO {self.opponent_team.name}!!!")
        self.ui.show(
            f"📊 {self.player_team.name} {self.score_a} x {self.score_b} {self.opponent_team.name}"
        )
