import random
from ..actions import assist_attempt, finalization

# -------------------------
# ⚙️ MEIA AVANÇADO
# -------------------------


def handle(match):
    _cam_moment(match)


def _cam_moment(self):
    self.ui.show("🎯 Você recebe entre as linhas!")

    situation = random.choice(
        ["criacao", "finalizacao", "infiltracao", "decisao_rapida"]
    )

    if situation == "criacao":
        _cam_creation(self)
    elif situation == "finalizacao":
        _cam_shot(self)
    elif situation == "infiltracao":
        _cam_run(self)
    else:
        _cam_quick_decision(self)


def _cam_creation(self):
    choice = self.ui.choice(
        "Você enxerga opções:",
        ["Passe em profundidade", "Passe curto", "Arriscar jogada genial"],
    )

    passing = self.player.attributes["passing"]

    if choice == 1:
        chance = passing + 5
    elif choice == 2:
        chance = passing + 10
    else:
        chance = passing - 10

    if random.randint(0, 100) < chance:
        self.ui.show("🎯 Passe perfeito!")
        assist_attempt(self)
    else:
        self.ui.show("❌ Passe não funcionou.")


def _cam_shot(self):
    finalization(self)


def _cam_run(self):
    dribble = self.player.attributes["dribbling"]

    if random.randint(0, 100) < dribble:
        self.ui.show("🔥 Você invade a área!")
        finalization(self)
    else:
        if random.random() < 0.3:
            self._foul_event(in_box=True)
        else:
            self.ui.show("❌ Foi parado.")


def _cam_quick_decision(self):
    choice = self.ui.choice(
        "Pressionado!", ["Chutar rápido", "Passe rápido", "Proteger bola"]
    )

    if choice == 1:
        finalization(self)
    elif choice == 2:
        _cam_creation(self)
    else:
        self.ui.show("⏳ Você segura a posse.")
