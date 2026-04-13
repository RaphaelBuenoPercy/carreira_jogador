from email.mime import base
import random
import time
from match.stats_file import init_stats, calculate_rating
from team import FORMATIONS
import team
from ui.text_interface import show_team_lineup
from . import ai
from .positions import gk, cb, fullback, cdm, cm, cam, winger, striker
from .events import foul, red, yellow, penalty


class InteractiveMatch:

    def __init__(self, player, player_team, opponent_team, ui):
        self.player = player

        self.player_team = player_team
        self.opponent_team = opponent_team
        self.ui = ui

        self.score_a = 0
        self.score_b = 0

        self.minute = 0
        self.events = []

        self.mentality = {
            self.player_team.id: "balanced",
            self.opponent_team.id: "balanced",
        }

        # disciplina
        self.yellow_cards = set()
        self.red_cards = set()

        self.substitutions_done = {
            self.player_team.id: 0,
            self.opponent_team.id: 0,
        }

        self.max_subs = 5

        self.match_player_stats = {
            p.id: init_stats(p)
            for p in (
                self.player_team.get_starting_xi()
                + self.opponent_team.get_starting_xi()
            )
        }

        self.lineups = {
            self.player_team.id: {
                "xi": [],
                "bench": [],
                "positions": {},  # player_id -> posição no campo
            },
            self.opponent_team.id: {"xi": [], "bench": [], "positions": {}},
        }

        self.player_stats = self.match_player_stats[self.player.id]

    def _update_mentality(self):
        for team in [self.player_team, self.opponent_team]:
            if team == self.player_team:
                gf, ga = self.score_a, self.score_b
            else:
                gf, ga = self.score_b, self.score_a

            if self.minute > 70:
                if gf < ga:
                    self.mentality[team.id] = "all_out_attack"
                elif gf > ga:
                    self.mentality[team.id] = "park_the_bus"
                else:
                    self.mentality[team.id] = "attacking"

    def _apply_mentality_modifier(self, team, value):
        m = self.mentality[team.id]

        if m == "all_out_attack":
            return value * 1.3
        elif m == "attacking":
            return value * 1.15
        elif m == "defensive":
            return value * 0.9
        elif m == "park_the_bus":
            return value * 0.75

        return value

    def _get_current_xi(self, team):
        return self.lineups[team.id]["xi"]

    def _initialize_lineups(self):
        for team in [self.player_team, self.opponent_team]:
            formation = team.formation
            formation_positions = FORMATIONS.get(formation)

            xi = team.get_starting_xi()
            bench = team.get_bench()

            self.lineups[team.id]["xi"] = xi
            self.lineups[team.id]["bench"] = bench

            # associa jogador à posição tática
            for player, pos in zip(xi, formation_positions):
                self.lineups[team.id]["positions"][player.id] = pos

    def _find_replacement(self, out_player, bench):
        candidates = [p for p in bench if p.position == out_player.position]

        if not candidates:
            candidates = bench  # improviso

        return max(candidates, key=lambda p: p.get_match_rating(), default=None)

    def _pick_offensive_player(self, players):
        return max(
            players,
            key=lambda p: p.attributes["finishing"] + p.attributes["dribbling"],
            default=None,
        )

    def _pick_defensive_player(self, players):
        return max(
            players,
            key=lambda p: p.attributes["defense"] + p.attributes["physical"],
            default=None,
        )

    def _pick_balanced_player(self, players):
        return max(players, key=lambda p: sum(p.attributes.values()), default=None)

    def _make_sub(self, team, out_player, in_player, reason):
        lineup = self.lineups[team.id]

        xi = lineup["xi"]
        bench = lineup["bench"]

        if out_player not in xi or in_player not in bench:
            return

        # mantém posição do jogador substituído
        pos = lineup["positions"][out_player.id]

        xi.remove(out_player)
        bench.remove(in_player)

        xi.append(in_player)
        bench.append(out_player)

        lineup["positions"][in_player.id] = pos
        del lineup["positions"][out_player.id]

        self.substitutions_done[team.id] += 1

        self.ui.show(
            f"\n🔄 Substituição ({reason}): {out_player.name} ⬇️ | {in_player.name} ⬆️"
        )

    def _try_substitute(self, team, is_player_team):
        if self.substitutions_done[team.id] >= self.max_subs:
            return

        xi = self._get_current_xi(team)
        bench = team.get_bench()

        # -------------------
        # 📊 SITUAÇÃO DO JOGO
        # -------------------
        if team == self.player_team:
            goals_for = self.score_a
            goals_against = self.score_b
        else:
            goals_for = self.score_b
            goals_against = self.score_a

        losing = goals_for < goals_against
        winning = goals_for > goals_against

        # -------------------
        # 🎯 PRIORIDADE 1: CANSAÇO
        # -------------------
        tired_players = [p for p in xi if p.fitness < 60]

        if tired_players:
            out_player = min(tired_players, key=lambda p: p.fitness)
            in_player = self._find_replacement(out_player, bench)

            if in_player:
                self._make_sub(team, out_player, in_player, "fatigue")
                return

        # -------------------
        # 🎯 PRIORIDADE 2: TÁTICA
        # -------------------
        mentality = self.mentality[team.id]

        if mentality in ["all_out_attack", "attacking"]:
            # time perdendo → entra jogador ofensivo
            out_player = self._pick_defensive_player(xi)
            in_player = self._pick_offensive_player(bench)

            if out_player and in_player:
                self._make_sub(team, out_player, in_player, "offensive")
                return

        elif winning:
            # time ganhando → reforça defesa
            out_player = self._pick_offensive_player(xi)
            in_player = self._pick_defensive_player(bench)

            if out_player and in_player:
                self._make_sub(team, out_player, in_player, "defensive")
                return

        else:
            # empate → depende do estilo
            if team.style == "offensive":
                out_player = self._pick_defensive_player(xi)
                in_player = self._pick_offensive_player(bench)
            else:
                out_player = self._pick_offensive_player(xi)
                in_player = self._pick_balanced_player(bench)

            if out_player and in_player:
                self._make_sub(team, out_player, in_player, "tactical")

    def _handle_substitutions(self):
        # só começa a substituir depois dos 55 min
        if self.minute < 55:
            return

        self._try_substitute(self.player_team, is_player_team=True)
        self._try_substitute(self.opponent_team, is_player_team=False)

    def play(self):
        self.ui.show(f"\n🏟️ {self.player_team.name} vs {self.opponent_team.name}")
        self.ui.show("Apito inicial!\n")
        self._initialize_lineups()

        choice = self.ui.choice("Antes do jogo:", ["Ver escalações", "Ir para o jogo"])

        if choice == 1:
            show_team_lineup(self, self.player_team, highlight_player=self.player)
            show_team_lineup(self, self.opponent_team)

        base = self._calculate_match_tempo()
        total_events = random.randint(base - 5, base + 5)

        for i in range(total_events):
            self.minute = int((i / total_events) * 90)

            self._handle_substitutions()

            if self._is_player_involved():
                self._player_moment()
                time.sleep(1)
            else:
                happened = ai.simulate_moment(self)
                time.sleep(1)

                if happened:
                    print("\n📢 Jogada longe de você...")
                    time.sleep(1)

        self._final_whistle()
        return self

    def _player_moment(self):
        pos = self.player.position

        print("\n" + "-" * 30)
        self.ui.show(f"⏱️ {self.minute}' - A jogada passa por você!")

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

        self.simulate_full_match_stats()

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
        chance = 0.20 + (self.player.get_match_rating() / 400)
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

    def goal_player_team(self, scorer=None, assist=None):
        self.score_a += 1

        print("\n" + "=" * 40)

        if scorer and assist:
            self.ui.show(f"⚽ {self.minute}' - GOL! {scorer} (assist: {assist})")
        elif scorer:
            self.ui.show(f"⚽ {self.minute}' - GOL! {scorer}")
        else:
            self.ui.show(f"⚽ {self.minute}' - Gol do {self.player_team.name}")

        self.ui.show(
            f"📊 {self.player_team.name} {self.score_a} x {self.score_b} {self.opponent_team.name}"
        )

        print("=" * 40 + "\n")

    def goal_opponent_team(self, scorer=None, assist=None):
        self.score_b += 1

        if scorer and assist:
            self.ui.show(f"⚽ {self.minute}' - GOL! {scorer} (assist: {assist})")
        elif scorer:
            self.ui.show(f"⚽ {self.minute}' - GOL! {scorer}")
        else:
            self.ui.show(f"⚽ {self.minute}' - Gol do {self.opponent_team.name}")

        self.ui.show(
            f"📊 {self.player_team.name} {self.score_a} x {self.score_b} {self.opponent_team.name}"
        )

    def _get_opponent_gk(self, player):
        if player.team_id == self.player_team.id:
            team = self.opponent_team
        else:
            team = self.player_team

        for p in self._get_current_xi(team):
            if p.position == "GK":
                return p

        return self._get_current_xi(team)()[0]

    def simulate_full_match_stats(self):
        strength_a = self.player_team.get_team_strength()
        strength_b = self.opponent_team.get_team_strength()

        total_strength = strength_a + strength_b

        # posse baseada na força
        possession_a = strength_a / total_strength
        possession_b = 1 - possession_a

        # intensidade baseada no estilo
        intensity = 1.0
        for team in [self.player_team, self.opponent_team]:
            if team.style == "offensive":
                intensity += 0.2
            elif team.style == "defensive":
                intensity -= 0.1

        players_a = self._get_current_xi(self.player_team)
        players_b = self._get_current_xi(self.opponent_team)

        all_players = players_a + players_b

        for p in all_players:
            if p.id == self.player.id:
                continue
            stats = self.match_player_stats[p.id]

            # -------------------
            # base de atividade
            # -------------------
            involvement = (
                p.get_match_rating()
                / 100
                * (possession_a if p in players_a else possession_b)
                * intensity
            )

            actions = int(random.randint(20, 40) * involvement)

            for _ in range(actions):

                # PASSES
                if p.position in ["CM", "CAM", "CDM", "CB", "LB", "RB"]:
                    stats["passes_attempted"] += 1

                    success = random.random() < (p.attributes["passing"] / 100)
                    if success:
                        stats["passes_completed"] += 1

                        if random.random() < 0.2:
                            stats["key_passes"] += 1
                            stats["xA"] += random.uniform(0.05, 0.2)
                    else:
                        stats["possession_lost"] += 1

                # DRIBLE
                if p.position in ["LW", "RW", "CAM"]:
                    stats["dribbles_attempted"] += 1

                    if random.random() < (p.attributes["dribbling"] / 100):
                        stats["dribbles_completed"] += 1
                    else:
                        stats["possession_lost"] += 1

                # DEFESA
                if p.position in ["CB", "CDM", "LB", "RB"]:
                    if random.random() < 0.4:
                        stats["tackles"] += 1
                        stats["possession_won"] += 1

                    if random.random() < 0.3:
                        stats["interceptions"] += 1

                # FINALIZAÇÃO
                if p.position in ["ST", "LW", "RW", "CAM"]:
                    if random.random() < 0.1:
                        stats["shots"] += 1

                        xg = random.uniform(0.05, 0.4)
                        stats["xG"] += xg

                        if random.random() < 0.4:
                            stats["shots_on_target"] += 1

                            # GOLEIRO
                            opponent_gk = self._get_opponent_gk(p)

                            save_chance = opponent_gk.attributes.get("reflex", 70) / 100

                            if random.random() > save_chance:
                                stats["goals"] += 1
                            else:
                                gk_stats = self.match_player_stats[opponent_gk.id]
                                gk_stats["saves"] = gk_stats.get("saves", 0) + 1
