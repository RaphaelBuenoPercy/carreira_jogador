import random
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
        "Bola na área!", ["Chute de primeira", "Dominar e bater", "Cabeceio"]
    )

    finalization(self)


def _st_hold_up(self):
    choice = self.ui.choice(
        "Você recebe de costas:",
        ["Proteger e tocar", "Girou pra chutar", "Esperar apoio"],
    )

    physical = self.player.attributes["physical"]

    if choice == 1:
        self.ui.show("🧱 Segurou bem a bola!")
        assist_attempt(self)
    elif choice == 2:
        if random.randint(0, 100) < physical:
            self.ui.show("🔥 Girou bonito!")
            _st_finish(self)
        else:
            self.ui.show("❌ Desarmado.")
    else:
        self.ui.show("⏳ Espera o time chegar.")


def _st_run(self):
    pace = self.player.attributes["pace"]

    if random.randint(0, 100) < pace:
        self.ui.show("🏃 Você ganha da defesa!")
        _st_finish(self)
    else:
        self.ui.show("❌ Zagueiro ganhou.")


def _st_reaction(self):
    finalization(self)
