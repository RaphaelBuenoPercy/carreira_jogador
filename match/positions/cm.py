import random
from ..actions import assist_attempt, finalization


# -------------------------
# 🛡️ MEIO CENTRAL
# -------------------------
def handle(match):
    _cm_moment(match)


def _cm_moment(self):
    self.ui.show("⚙️ Você está no coração do jogo!")

    situation = random.choice(["controle", "criacao", "pressao", "finalizacao"])

    if situation == "controle":
        _cm_control(self)
    elif situation == "criacao":
        _cm_creation(self)
    elif situation == "pressao":
        _cm_press(self)
    else:
        _cm_shot(self)


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
            assist_attempt(self)
        else:
            self.ui.show("❌ Erro na virada.")
    else:
        self.ui.show("⏳ Você controla o tempo.")


def _cm_creation(self):
    passing = self.player.attributes["passing"]

    if random.randint(0, 100) < passing:
        self.ui.show("🎯 Você quebra linhas!")
        assist_attempt(self)
    else:
        self.ui.show("❌ Tentativa falhou.")


def _cm_press(self):
    stamina = self.player.attributes.get("physical", 70)

    if random.randint(0, 100) < stamina:
        self.ui.show("🔥 Você pressiona e recupera!")
        _cm_control(self)
    else:
        self.ui.show("❌ Pressão falhou.")


def _cm_shot(self):
    finalization(self)
