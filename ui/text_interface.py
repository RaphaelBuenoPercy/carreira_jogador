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