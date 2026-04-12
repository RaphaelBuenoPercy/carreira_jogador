import random


# -------------------------
# 🔥 ATACANTE
# -------------------------
def _striker_moment(self):
    self.ui.show("🎯 Você está na área!")

    situation = random.choice(["finalizacao", "pivo", "corrida", "reacao"])

    if situation == "finalizacao":
        self._st_finish()
    elif situation == "pivo":
        self._st_hold_up()
    elif situation == "corrida":
        self._st_run()
    else:
        self._st_reaction()


def _st_finish(self):
    choice = self.ui.choice(
        "Bola na área!", ["Chute de primeira", "Dominar e bater", "Cabeceio"]
    )

    finishing = self.player.attributes["finishing"]
    physical = self.player.attributes["physical"]

    if choice == 1:
        chance = finishing + 5
    elif choice == 2:
        chance = finishing
    else:
        chance = physical + 5

    if random.randint(0, 100) < chance:
        self.score_player_team += 1
        self.ui.show("⚽ GOL DE CENTROAVANTE!")
        self.player.record_match(8, goals=1)
    else:
        self.ui.show("❌ Perdeu chance clara!")


def _st_hold_up(self):
    choice = self.ui.choice(
        "Você recebe de costas:",
        ["Proteger e tocar", "Girou pra chutar", "Esperar apoio"],
    )

    physical = self.player.attributes["physical"]

    if choice == 1:
        self.ui.show("🧱 Segurou bem a bola!")
        self._assist_attempt()
    elif choice == 2:
        if random.randint(0, 100) < physical:
            self.ui.show("🔥 Girou bonito!")
            self._st_finish()
        else:
            self.ui.show("❌ Desarmado.")
    else:
        self.ui.show("⏳ Espera o time chegar.")


def _st_run(self):
    pace = self.player.attributes["pace"]

    if random.randint(0, 100) < pace:
        self.ui.show("🏃 Você ganha da defesa!")
        self._st_finish()
    else:
        self.ui.show("❌ Zagueiro ganhou.")


def _st_reaction(self):
    finishing = self.player.attributes["finishing"]

    if random.randint(0, 100) < finishing + 10:
        self.score_player_team += 1
        self.ui.show("⚡ Gol oportunista!")
        self.player.record_match(8, goals=1)
    else:
        self.ui.show("❌ Não aproveitou o rebote.")
