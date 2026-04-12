import random
from ..actions import assist_attempt, finalization


def handle(match):
    _cb_moment(match)


# -------------------------
# 🛡️ ZAGUEIRO
# -------------------------
def _cb_moment(self):
    self.ui.show("🛡️ Você está na defesa!")

    situation = random.choice(["marcacao", "cruzamento", "antecipacao", "saida_bola"])

    if situation == "marcacao":
        _cb_marking(self)
    elif situation == "cruzamento":
        _cb_aerial_duel(self)
    elif situation == "antecipacao":
        _cb_interception(self)
    else:
        _cb_build_up(self)


def _cb_marking(self):
    choice = self.ui.choice(
        "Atacante tentando passar:", ["Desarme forte", "Desarme limpo", "Segurar"]
    )

    defense = self.player.attributes["defense"]

    if choice == 1:
        chance = defense + 5
        foul_risk = 0.4
    elif choice == 2:
        chance = defense
        foul_risk = 0.2
    else:
        self.ui.show("⏳ Você segura o jogador.")
        return

    if random.randint(0, 100) < chance:
        self.ui.show("🛡️ Desarme feito!")
    else:
        if random.random() < foul_risk:
            self._foul_event()
        else:
            self.ui.show("❌ Ele passou!")


def _cb_aerial_duel(self):
    choice = self.ui.choice(
        "Cruzamento na área:", ["Cortar de cabeça", "Disputar físico", "Recuar"]
    )

    physical = self.player.attributes["physical"]

    if choice == 3:
        self.ui.show("↩️ Você recua.")
        return

    chance = physical + (10 if choice == 1 else 5)

    if random.randint(0, 100) < chance:
        self.ui.show("🧱 Corte perfeito!")
    else:
        self.ui.show("⚠️ Perdeu no alto!")
        self.score_opponent += 1


def _cb_interception(self):
    iq = self.player.attributes.get("iq", 70)

    if random.randint(0, 100) < iq:
        self.ui.show("🧠 Interceptação inteligente!")
    else:
        self.ui.show("❌ Não conseguiu cortar.")


def _cb_build_up(self):
    choice = self.ui.choice(
        "Saída de bola:", ["Passe seguro", "Passe vertical", "Chutão"]
    )

    passing = self.player.attributes["passing"]

    if choice == 1:
        self.ui.show("✅ Saída tranquila.")
    elif choice == 2:
        if random.randint(0, 100) < passing:
            self.ui.show("🎯 Que passe!")
            assist_attempt(self)
        else:
            self.ui.show("❌ Erro na saída!")
    else:
        self.ui.show("💥 Bola afastada.")
