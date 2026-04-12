import random

# -------------------------
# 🛡️ MEIO CENTRAL
# -------------------------


def _cm_moment(self):
    self.ui.show("⚙️ Você está no coração do jogo!")

    situation = random.choice(["controle", "criacao", "pressao", "finalizacao"])

    if situation == "controle":
        self._cm_control()
    elif situation == "criacao":
        self._cm_creation()
    elif situation == "pressao":
        self._cm_press()
    else:
        self._cm_shot()


def _cm_control(self):
    choice = self.ui.choice(
        "Você dita o ritmo:", ["Passe curto", "Virar jogo", "Segurar posse"]
    )

    passing = self.player.attributes["passing"]

    if choice == 1:
        self.ui.show("✅ Jogo fluindo.")
    elif choice == 2:
        if random.randint(0, 100) < passing:
            self.ui.show("🎯 Virada excelente!")
            self._assist_attempt()
        else:
            self.ui.show("❌ Erro na virada.")
    else:
        self.ui.show("⏳ Você controla o tempo.")


def _cm_creation(self):
    passing = self.player.attributes["passing"]

    if random.randint(0, 100) < passing:
        self.ui.show("🎯 Você quebra linhas!")
        self._assist_attempt()
    else:
        self.ui.show("❌ Tentativa falhou.")


def _cm_press(self):
    stamina = self.player.attributes.get("physical", 70)

    if random.randint(0, 100) < stamina:
        self.ui.show("🔥 Você pressiona e recupera!")
        self._cm_control()
    else:
        self.ui.show("❌ Pressão falhou.")


def _cm_shot(self):
    finishing = self.player.attributes["finishing"]

    if random.randint(0, 100) < finishing - 10:
        self.score_player_team += 1
        self.ui.show("⚽ Gol de fora da área!")
        self.player.record_match(7, goals=1)
    else:
        self.ui.show("❌ Chute sem perigo.")
