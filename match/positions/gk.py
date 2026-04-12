import random

# -------------------------
# 🛡️ GOLEIRO
# -------------------------


def _goalkeeper_moment(self):
    self.ui.show("🧤 Situação de perigo! Você é o goleiro!")

    situation = random.choice(["finalizacao", "cruzamento", "1v1", "reposicao"])

    if situation == "finalizacao":
        self._gk_shot_save()
    elif situation == "cruzamento":
        self._gk_cross()
    elif situation == "1v1":
        self._gk_one_on_one()
    else:
        self._gk_distribution()


def _gk_shot_save(self):
    choice = self.ui.choice("Chute vindo!", ["Espalmar", "Segurar", "Reação rápida"])

    reflex = self.player.attributes.get("reflex", 70)
    positioning = self.player.attributes.get("iq", 70)

    base = (reflex + positioning) / 2

    if choice == 1:
        chance = base + 5
    elif choice == 2:
        chance = base
    else:
        chance = base + 10

    if random.randint(0, 100) < chance:
        self.ui.show("🧤 DEFESAÇA!")
    else:
        self.score_opponent += 1
        self.ui.show("⚽ Gol adversário...")


def _gk_cross(self):
    choice = self.ui.choice("Cruzamento na área!", ["Sair do gol", "Ficar no gol"])

    aerial = self.player.attributes.get("physical", 70)

    if choice == 1:
        chance = aerial + 10
        if random.randint(0, 100) < chance:
            self.ui.show("✋ Você corta o cruzamento!")
        else:
            self.ui.show("❌ Saiu mal!")
            self.score_opponent += 1
    else:
        self.ui.show("⚠️ Você permanece no gol.")


def _gk_one_on_one(self):
    choice = self.ui.choice(
        "Atacante cara a cara!", ["Fechar ângulo", "Esperar", "Se jogar nos pés"]
    )

    reflex = self.player.attributes.get("reflex", 70)

    if choice == 1:
        chance = reflex + 10
    elif choice == 2:
        chance = reflex
    else:
        chance = reflex - 5

    if random.randint(0, 100) < chance:
        self.ui.show("🧤 DEFENDEU O 1x1!")
    else:
        self.score_opponent += 1
        self.ui.show("⚽ Gol no mano a mano...")


def _gk_distribution(self):
    choice = self.ui.choice(
        "Reposição de bola:", ["Lançamento longo", "Passe curto", "Chutão"]
    )

    passing = self.player.attributes.get("passing", 60)

    if choice == 1:
        chance = passing
        if random.randint(0, 100) < chance:
            self.ui.show("🎯 Lançamento perfeito!")
            self._assist_attempt()
        else:
            self.ui.show("❌ Entregou a bola!")
    elif choice == 2:
        self.ui.show("✅ Saída segura.")
    else:
        self.ui.show("💥 Bola pra frente.")
