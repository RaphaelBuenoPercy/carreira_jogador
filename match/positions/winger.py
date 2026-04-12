import random

# -------------------------
# 🔥 PONTA
# -------------------------


def _winger_moment(self):
    self.ui.show("⚡ Você recebe aberto na ponta!")

    situation = random.choice(["1v1", "correr", "cruzar", "cortar"])

    if situation == "1v1":
        self._winger_1v1()
    elif situation == "correr":
        self._winger_run()
    elif situation == "cruzar":
        self._winger_cross()
    else:
        self._winger_cut_inside()


def _winger_1v1(self):
    choice = self.ui.choice(
        "Você encara o lateral:", ["Drible rápido", "Finta técnica", "Passar"]
    )

    dribble = self.player.attributes["dribbling"]

    if choice == 3:
        self._pass()
        return

    if choice == 1:
        chance = dribble + 5
    else:
        chance = dribble + 10

    if random.randint(0, 100) < chance:
        self.ui.show("🔥 Você deixou o marcador pra trás!")
        self._winger_final_decision()

    else:
        if random.random() < 0.3:
            self._foul_event()
        else:
            self.ui.show("❌ Perdeu a bola.")


def _winger_run(self):
    pace = self.player.attributes["pace"]

    if random.randint(0, 100) < pace:
        self.ui.show("🚀 Você dispara pela ponta!")
        self._winger_final_decision()
    else:
        self.ui.show("❌ Não ganhou na corrida.")


def _winger_cross(self):
    choice = self.ui.choice("Você vai cruzar:", ["Alto", "Rasteiro", "Segundo pau"])

    passing = self.player.attributes["passing"]

    if random.randint(0, 100) < passing + 5:
        self.ui.show("🎯 Cruzamento perigoso!")
        self._assist_attempt()
    else:
        self.ui.show("❌ Cruzamento ruim.")


def _winger_cut_inside(self):
    dribble = self.player.attributes["dribbling"]

    if random.randint(0, 100) < dribble:
        self.ui.show("↪️ Cortou pra dentro!")
        self._finalization()
    else:
        self.ui.show("❌ Travado pela defesa.")


def _winger_final_decision(self):
    choice = self.ui.choice(
        "Você chega em posição perigosa:", ["Chutar", "Passar", "Cruzamento rápido"]
    )

    if choice == 1:
        self._finalization()
    elif choice == 2:
        self._assist_attempt()
    else:
        self._winger_cross()
