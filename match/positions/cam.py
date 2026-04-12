import random


# -------------------------
# ⚙️ MEIA AVANÇADO
# -------------------------
def _cam_moment(self):
    self.ui.show("🎯 Você recebe entre as linhas!")

    situation = random.choice(
        ["criacao", "finalizacao", "infiltracao", "decisao_rapida"]
    )

    if situation == "criacao":
        self._cam_creation()
    elif situation == "finalizacao":
        self._cam_shot()
    elif situation == "infiltracao":
        self._cam_run()
    else:
        self._cam_quick_decision()


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
        self._assist_attempt()
    else:
        self.ui.show("❌ Passe não funcionou.")


def _cam_shot(self):
    finishing = self.player.attributes["finishing"]

    if random.randint(0, 100) < finishing:
        self.score_player_team += 1
        self.ui.show("⚽ GOLAÇO!")
        self.player.record_match(8, goals=1)
    else:
        self.ui.show("❌ Chute pra fora!")


def _cam_run(self):
    dribble = self.player.attributes["dribbling"]

    if random.randint(0, 100) < dribble:
        self.ui.show("🔥 Você invade a área!")
        self._cam_shot()
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
        self._cam_shot()
    elif choice == 2:
        self._cam_creation()
    else:
        self.ui.show("⏳ Você segura a posse.")
