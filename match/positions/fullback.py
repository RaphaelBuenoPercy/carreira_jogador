import random
from ..actions import assist_attempt, finalization
from ..events import foul, red, yellow, penalty


# -------------------------
# 🛡️ LATERAL
# -------------------------
def handle(match):
    _fb_moment(match)


def _fb_moment(self):
    self.ui.show("🏃‍♂️ Você avança pela lateral!")

    situation = random.choice(["apoio", "defesa", "cruzamento", "transicao"])

    if situation == "apoio":
        _fb_support(self)
    elif situation == "defesa":
        _fb_defense(self)
    elif situation == "cruzamento":
        _fb_cross(self)
    else:
        _fb_transition(self)


def _fb_support(self):
    choice = self.ui.choice(
        "Você tem espaço na lateral:",
        ["Avançar em velocidade", "Tocar e passar", "Segurar"],
    )

    pace = self.player.attributes["pace"]
    dribble = self.player.attributes["dribbling"]

    if choice == 1:
        if random.randint(0, 100) < pace:
            self.ui.show("🚀 Você dispara pela lateral!")
            _fb_cross(self)
        else:
            self.ui.show("❌ Perdeu no pique.")
    elif choice == 2:
        if random.randint(0, 100) < dribble:
            self.ui.show("🔁 Boa tabela!")
            assist_attempt(self)
        else:
            self.ui.show("❌ Passe errado.")
    else:
        self.ui.show("⏳ Você segura a jogada.")


def _fb_defense(self):
    choice = self.ui.choice(
        "Ponta adversário parte pra cima:",
        ["Dar bote", "Conter", "Fazer falta tática"],
    )

    defense = self.player.attributes["defense"]

    if choice == 1:
        chance = defense + 5
        foul_risk = 0.3
    elif choice == 2:
        self.ui.show("👣 Você segura o jogador.")
        return
    else:
        foul(self)
        return

    if random.randint(0, 100) < chance:
        self.ui.show("🛡️ Desarme lateral perfeito!")
    else:
        if random.random() < foul_risk:
            foul(self)
        else:
            self.ui.show("❌ Ele passou!")


def _fb_cross(self):
    choice = self.ui.choice(
        "Você vai cruzar:",
        ["Cruzamento alto", "Cruzamento rasteiro", "Cortar pra dentro"],
    )

    passing = self.player.attributes["passing"]

    if choice == 3:
        self.ui.show("↪️ Você corta pra dentro!")
        self._dribble()
        return

    modifier = 5 if choice == 1 else 10

    if random.randint(0, 100) < passing + modifier:
        self.ui.show("🎯 Cruzamento perfeito!")
        assist_attempt(self)
    else:
        self.ui.show("❌ Cruzamento ruim.")


def _fb_transition(self):
    self.ui.show("⚡ Transição rápida!")

    pace = self.player.attributes["pace"]

    if random.randint(0, 100) < pace:
        self.ui.show("🏃‍♂️ Você recompõe bem!")
    else:
        self.ui.show("⚠️ Chegou atrasado!")
        self.score_b += 1
