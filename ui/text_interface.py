class TextUI:
    def show(self, text):
        print(text)

    def choice(self, prompt, options):
        print("\n" + prompt)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")

        while True:
            try:
                c = int(input("> "))
                if 1 <= c <= len(options):
                    return c
            except:
                pass

            print("Escolha inválida.")


def show_team_lineup(match, team, highlight_player=None):
    lineup = match.lineups[team.id]

    xi = lineup["xi"]
    bench = lineup["bench"]
    positions = lineup["positions"]

    strength = team.get_team_strength()

    print(f"\n⚙️ Força do time: {strength:.1f}")
    print(f"🎯 Estilo: {team.style}")
    print(f"📈 Moral: {team.morale}")

    print("\n========================================")
    print(f"📋 {team.name} - Escalação ({team.formation})")
    print("========================================\n")

    print("🔵 TITULARES:\n")

    for p in xi:
        pos = positions.get(p.id, p.position)

        marker = "⭐" if highlight_player and p.id == highlight_player.id else ""

        print(
            f"{pos:>3} | {p.name:<20} | OVR: {p.get_rating():.0f} | Forma: {p.form} | Fit: {p.fitness} | {marker}"
        )

    print("\n🪑 BANCO:\n")

    for p in bench:
        pos = positions.get(p.id, p.position)

        print(
            f"{pos:>3} | {p.name:<20} | OVR: {p.get_rating():.0f} | Forma: {p.form} | Fit: {p.fitness}"
        )

    print("\n========================================\n")
