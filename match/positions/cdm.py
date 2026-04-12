import random

# -------------------------
# 🛡️ VOLANTE
# -------------------------


def _cdm_moment(self):
    self.ui.show("🛡️ Você está protegendo a defesa!")

    situation = random.choice(["marcacao", "interceptacao", "transicao", "pressao"])

    if situation == "marcacao":
        self._cdm_marking()
    elif situation == "interceptacao":
        self._cdm_interception()
    elif situation == "transicao":
        self._cdm_transition()
    else:
        self._cdm_press()


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
            self._foul_event()
        else:
            self.ui.show("❌ Ele passou!")


def _cdm_interception(self):
    iq = self.player.attributes.get("iq", 70)

    if random.randint(0, 100) < iq:
        self.ui.show("🧠 Você lê o jogo e intercepta!")
        self._cdm_transition()
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
            self._assist_attempt()
        else:
            self.ui.show("❌ Erro na virada.")
    else:
        if random.randint(0, 100) < passing - 5:
            self.ui.show("🚀 Lançamento perigoso!")
            self._assist_attempt()
        else:
            self.ui.show("❌ Bola perdida.")


def _cdm_press(self):
    stamina = self.player.attributes.get("physical", 70)

    if random.randint(0, 100) < stamina:
        self.ui.show("🔥 Pressão alta! Você rouba a bola!")
        self._cdm_transition()
    else:
        self.ui.show("❌ Pressão falhou.")
