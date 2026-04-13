import random
import time
from ..actions import assist_attempt, finalization

# -------------------------
# 🔥 ATACANTE
# -------------------------


def handle(match):
    _striker_moment(match)


def _striker_moment(self):
    self.ui.show("🎯 Você está na área!")

    situation = random.choice(["finalizacao", "pivo", "corrida", "reacao"])

    if situation == "finalizacao":
        _st_finish(self)
    elif situation == "pivo":
        _st_hold_up(self)
    elif situation == "corrida":
        _st_run(self)
    else:
        _st_reaction(self)


def _st_finish(self):
    choice = self.ui.choice(
        "Você está na área!",
        ["Chute de primeira", "Dominar e bater", "Cabeceio colocado"],
    )

    finishing = self.player.attributes["finishing"]

    if choice == 1:
        chance = finishing + 10  # rápido, mais fácil errar
        xg = 0.25
    elif choice == 2:
        self.ui.show("👌 Dominou com calma.")
        chance = finishing
        xg = 0.35
    else:
        chance = finishing - 5
        xg = 0.3

    if random.randint(0, 100) < chance:
        time.sleep(2)
        finalization(self, xg)
        self.player_stats["shots"] += 1
        self.player_stats["shots_on_target"] += 1
        self.player_stats["xG"] += xg
    else:
        time.sleep(2)
        self.ui.show("❌ Finalização ruim!")
        self.player_stats["shots"] += 1
        self.player_stats["xG"] += xg


def _st_hold_up(self):
    choice = self.ui.choice(
        "Você recebe de costas:",
        ["Proteger e tocar", "Girou pra chutar", "Fazer parede rápida"],
    )

    physical = self.player.attributes["physical"]
    passing = self.player.attributes["passing"]

    if choice == 1:
        if random.randint(0, 100) < physical:
            time.sleep(2)
            self.ui.show("🧱 Segurou bem!")
            assist_attempt(self)
        else:
            time.sleep(2)
            self.ui.show("❌ Perdeu a bola!")
            self.player_stats["possession_lost"] += 1

    elif choice == 2:
        if random.randint(0, 100) < physical:
            time.sleep(2)
            self.ui.show("🔥 Girou bonito!")
            self.player_stats["dribbles_attempted"] += 1
            self.player_stats["dribbles_completed"] += 1
            _st_finish(self)
        else:
            time.sleep(2)
            self.ui.show("❌ Desarmado!")
            self.player_stats["possession_lost"] += 1
            self.player_stats["dribbles_attempted"] += 1

    else:
        if random.randint(0, 100) < passing:
            time.sleep(2)
            self.ui.show("🔁 Tabela rápida funcionou!")
            self.player_stats["passes_attempted"] += 1
            self.player_stats["passes_completed"] += 1
            assist_attempt(self)
        else:
            time.sleep(2)
            self.ui.show("❌ Passe saiu errado!")
            self.player_stats["possession_lost"] += 1
            self.player_stats["passes_attempted"] += 1


def _st_run(self):
    choice = self.ui.choice(
        "Você dispara nas costas da zaga:",
        ["Chutar", "Driblar goleiro", "Tocar pro lado"],
    )

    pace = self.player.attributes["pace"]

    if choice == 1:
        _st_finish(self)

    elif choice == 2:
        if random.randint(0, 100) < pace:
            time.sleep(2)
            self.ui.show("😎 Passou do goleiro!")
            self.player_stats["dribbles_attempted"] += 1
            self.player_stats["dribbles_completed"] += 1
            finalization(self, xg=0.95)
        else:
            time.sleep(2)
            self.ui.show("❌ Goleiro levou!")
            self.player_stats["dribbles_attempted"] += 1
            self.player_stats["possession_lost"] += 1

    else:
        attempt_pass_or_recycle(self, difficulty=0.6)


def _st_1v1(self):
    choice = self.ui.choice(
        "Você tá no mano a mano contra o zagueiro:",
        ["Chutar", "Driblar", "Segurar e esperar apoio"],
    )

    pace = self.player.attributes["pace"]
    passing = self.player.attributes["passing"]
    dribbling = self.player.attributes["dribbling"]

    if choice == 1:
        _st_finish(self)

    elif choice == 2:
        if random.randint(0, 100) < dribbling:
            time.sleep(2)
            self.ui.show("😎 Passou do zagueiro")
            self.player_stats["dribbles_attempted"] += 1
            self.player_stats["dribbles_completed"] += 1
            choice = self.ui.choice(
                "Você passou do zagueiro",
                ["Chutar", "Tocar"],
            )

            if choice == 1:
                finalization(self)

            elif choice == 2:

                if random.randint(0, 100) < passing:
                    time.sleep(2)
                    self.ui.show("🔁 Passe deu bom")
                    self.player_stats["passes_attempted"] += 1
                    self.player_stats["passes_completed"] += 1
                    assist_attempt(self)
                else:
                    time.sleep(2)
                    self.ui.show("❌ Passe saiu errado!")
                    self.player_stats["possession_lost"] += 1
                    self.player_stats["passes_attempted"] += 1

        else:
            time.sleep(2)
            self.ui.show("❌ Zagueiro pegou!")
            self.player_stats["dribbles_attempted"] += 1
            self.player_stats["possession_lost"] += 1

    else:
        attempt_pass_or_recycle(self, difficulty=0.3)


def _st_reaction(self):
    choice = self.ui.choice(
        "Bola sobra na área!", ["Chutar rápido", "Dominar", "Procurar passe"]
    )

    finishing = self.player.attributes["finishing"]

    if choice == 1:
        if random.randint(0, 100) < finishing - 5:
            finalization(self)
        else:
            self.ui.show("❌ Isolou!")
            self.player_stats["shots"] += 1

    elif choice == 2:
        self.ui.show("👌 Dominou com calma.")
        _st_finish(self)

    else:
        attempt_pass_or_recycle(self, difficulty=0.4)


def calculate_pass_difficulty(match, player):
    team = match.player_team
    opponent = match.opponent_team

    # -------------------
    # 🧠 BASE
    # -------------------
    difficulty = 0.5

    # -------------------
    # ⚙️ ESTILO DO TIME
    # -------------------
    style_bonus = {
        "offensive": -0.15,  # mais opções
        "balanced": 0.0,
        "counter": -0.05,
        "defensive": +0.15,  # menos opções
    }

    difficulty += style_bonus.get(team.style, 0)

    # -------------------
    # 🧱 ESTILO DO ADVERSÁRIO
    # -------------------
    opponent_bonus = {
        "offensive": -0.05,  # deixam espaço
        "balanced": 0.0,
        "counter": +0.05,
        "defensive": +0.15,  # fecham linhas
    }

    difficulty += opponent_bonus.get(opponent.style, 0)

    # -------------------
    # 💪 FORÇA DOS TIMES
    # -------------------
    strength_a = team.get_team_strength()
    strength_b = opponent.get_team_strength()

    diff = strength_b - strength_a  # se positivo → adversário mais forte

    difficulty += diff / 100  # escala suave

    # -------------------
    # ⏱️ MOMENTO DO JOGO
    # -------------------
    difficulty += (match.minute / 120) * 0.1  # fim de jogo mais difícil

    # -------------------
    # 🎯 POSIÇÃO (opcional mas forte)
    # -------------------
    pos_modifier = {
        "ST": +0.1,
        "CAM": -0.05,
        "CM": -0.05,
        "CDM": 0.0,
        "LW": 0.0,
        "RW": 0.0,
    }

    difficulty += pos_modifier.get(player.position, 0)

    # clamp
    return max(0.1, min(0.9, difficulty))


def attempt_pass_or_recycle(self, difficulty=0.5):
    """
    difficulty: 0 a 1 → quanto mais alto, mais difícil achar opção
    """
    difficulty = calculate_pass_difficulty(self, self.player)
    passing = self.player.attributes["passing"]
    composure = self.player.attributes.get("mental", 70)
    physical = self.player.attributes["physical"]

    # chance de NÃO ter opção
    no_option_chance = difficulty

    if random.random() < no_option_chance:
        time.sleep(2)
        self.ui.show("🚫 Sem opções de passe!")

        # decisão sob pressão
        if random.randint(0, 100) < composure:
            time.sleep(2)
            self.ui.show("🧠 Você mantém a calma e reinicia a jogada.")

            choice = self.ui.choice(
                "O que fazer agora?",
                ["Voltar a bola", "Segurar e girar", "Forçar passe mesmo assim"],
            )

            if choice == 1:
                self.player_stats["passes_attempted"] += 1
                self.player_stats["passes_completed"] += 1
                time.sleep(2)
                self.ui.show("↩️ Você recua e mantém a posse.")

            elif choice == 2:
                if random.randint(0, 100) < physical - 5:
                    # pode voltar pro fluxo ofensivo
                    time.sleep(2)
                    self.ui.show("🧱 Protegeu bem!")
                    _st_1v1(self)
                else:
                    time.sleep(2)
                    self.ui.show("❌ Perdeu a bola!")
                    self.player_stats["possession_lost"] += 1

            else:
                self.player_stats["passes_attempted"] += 1

                if random.randint(0, 100) < passing - 20:
                    self.player_stats["passes_completed"] += 1
                    time.sleep(2)
                    self.ui.show("😬 Deu certo no limite!")
                    assist_attempt(self)
                else:
                    time.sleep(2)
                    self.ui.show("❌ Passe forçado interceptado!")
                    self.player_stats["possession_lost"] += 1

        else:
            time.sleep(2)
            self.ui.show("❌ Pressionado e perdeu a bola!")
            self.player_stats["possession_lost"] += 1

        return False

    # tem opção → fluxo normal
    self.player_stats["passes_attempted"] += 1
    self.player_stats["passes_completed"] += 1

    time.sleep(2)
    self.ui.show("🟢 Encontrou um companheiro livre!")
    assist_attempt(self)

    return True
