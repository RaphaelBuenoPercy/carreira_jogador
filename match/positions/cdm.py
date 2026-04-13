import random
from ..actions import assist_attempt, finalization
from ..events import foul, red, yellow, penalty


# -------------------------
# 🛡️ VOLANTE
# -------------------------
def handle(match):
    _cdm_moment(match)


def _cdm_moment(self):
    self.ui.show("🛡️ Você está protegendo a defesa!")

    situation = random.choice(["marcacao", "interceptacao", "transicao", "pressao"])

    if situation == "marcacao":
        _cdm_marking(self)
    elif situation == "interceptacao":
        _cdm_interception(self)
    elif situation == "transicao":
        _cdm_transition(self)
    else:
        _cdm_press(self)


def _cdm_marking(self):
    choice = self.ui.choice(
        "Meia adversário com a bola:",
        ["Desarme forte", "Desarme limpo", "Acompanhar"],
    )

    defense = self.player.attributes["defense"]

    if choice == 3:
        self.ui.show("👣 Você acompanha e fecha espaço.")
        return

    if choice == 1:
        chance = defense + 5
        foul_risk = 0.5
    else:
        chance = defense
        foul_risk = 0.2

    if random.randint(0, 100) < chance:
        self.ui.show("🛡️ Desarme feito!")
    else:
        if random.random() < foul_risk:
            foul(self)
        else:
            self.ui.show("❌ Ele passou!")


def _cdm_interception(self):
    iq = self.player.attributes.get("iq", 70)

    if random.randint(0, 100) < iq:
        self.ui.show("🧠 Você lê o jogo e intercepta!")
        _cdm_transition(self)
    else:
        self.ui.show("⚠️ Não conseguiu cortar.")


def _cdm_transition(self):
    choice = self.ui.choice(
        "Você recupera a bola:", ["Passe seguro", "Virar jogo", "Lançamento longo"]
    )

    passing = self.player.attributes["passing"]

    if choice == 1:
        self.ui.show("✅ Mantém a posse.")
    elif choice == 2:
        if random.randint(0, 100) < passing:
            self.ui.show("🎯 Virada de jogo perfeita!")
            assist_attempt(self)
        else:
            self.ui.show("❌ Erro na virada.")
    else:
        if random.randint(0, 100) < passing - 5:
            self.ui.show("🚀 Lançamento perigoso!")
            assist_attempt(self)
        else:
            self.ui.show("❌ Bola perdida.")


def _cdm_press(self):
    stamina = self.player.attributes.get("physical", 70)

    if random.randint(0, 100) < stamina:
        self.ui.show("🔥 Pressão alta! Você rouba a bola!")
        _cdm_transition(self)
    else:
        self.ui.show("❌ Pressão falhou.")
