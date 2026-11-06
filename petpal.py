"""
PetPal 2.0 - Retro Virtual Pet & Adventure Simulator (Pure Python)
Syllabus: OOP, Random, File I/O, Exceptions, Dictionaries, Conditionals & Loops.
"""
import random
import sys

# Ensure UTF-8 output encoding for cross-platform terminal compatibility (Windows/Linux/macOS)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Dynamic ASCII face art based on pet mood
MOOD_ART = {
    "happy": "( ^ ◡ ^ ) ✨",
    "neutral": "( • _ • )",
    "hungry": "( > ‸ < ) 🍽️",
    "tired": "( - . - ) zZZ",
}


class Pet:
    def __init__(self, name, species, level=1, xp=0, hunger=20, happiness=80, energy=80):
        self.name, self.species = name, species
        self.level, self.xp = level, xp
        self.hunger, self.happiness, self.energy = hunger, happiness, energy

    def gain_xp(self, amount):
        """Grants XP and checks for level-ups."""
        self.xp += amount
        if self.xp >= self.level * 40:
            self.level += 1
            print(f"🌟 LEVEL UP! {self.name} evolved to Level {self.level}! 🎉")

    def get_mood(self):
        """Calculates mood based on priority stats."""
        if self.energy <= 20:
            return "tired"
        if self.hunger >= 70:
            return "hungry"
        return "happy" if self.happiness >= 60 else "neutral"

    def status(self):
        """Displays a retro RPG card with ASCII face and stat bars."""
        mood = self.get_mood()
        print(f"\n┌{'─'*34}┐")
        print(f"│ {self.name} the {self.species:<8} (Lvl {self.level}) │")
        print(f"│ Mood: {MOOD_ART[mood]:<26}│")
        print(f"├{'─'*34}┤")
        for stat, val in [("Hunger ", self.hunger), ("Happy  ", self.happiness), ("Energy ", self.energy)]:
            bar = "■" * (val // 10) + "□" * (10 - val // 10)
            print(f"│ {stat}: [{bar}] {val:>3}/100 │")
        print(f"│ XP    : {self.xp}/{self.level * 40:<3} {' '*18}│")
        print(f"└{'─'*34}┘")

    def feed(self):
        """Interactive food menu with different stat trade-offs."""
        menu = {
            "1": ("🍪 Sweet Cookie", -15, 10),
            "2": ("🥩 Juicy Steak", -35, 15),
            "3": ("🧪 Energy Elixir", -10, 25),
        }
        print("\nPantry: [1] Cookie  [2] Steak  [3] Elixir")
        choice = input("Select treat (1-3): ").strip()
        item, hunger_delta, xp_delta = menu.get(choice, menu["1"])

        self.hunger = max(0, self.hunger + hunger_delta)
        self.happiness = min(100, self.happiness + 10)
        print(f"😋 {self.name} happily devoured the {item}!")
        self.gain_xp(xp_delta)

    def adventure(self):
        """Random RPG exploration encounters with XP and stat changes."""
        if self.energy < 25:
            print(f"⚠️ {self.name} is too exhausted for an adventure! Let them sleep first.")
            return

        encounters = [
            ("discovered a secret chest full of gems! 💎", 25, 30),
            ("outsmarted a wild goblin in the woods! 👺", 15, 25),
            ("found a quiet river and took a refreshing dip! 🌊", 20, 20),
            ("tripped into a muddy puddle... 🌧️", -10, 10),
        ]
        event, hap_effect, xp_gain = random.choice(encounters)
        print(f"\n🗺️ Adventure: {self.name} {event}")

        self.happiness = max(0, min(100, self.happiness + hap_effect))
        self.energy = max(0, self.energy - 25)
        self.hunger = min(100, self.hunger + 20)
        self.gain_xp(xp_gain)

    def sleep(self):
        """Restores full energy."""
        self.energy = 100
        self.hunger = min(100, self.hunger + 15)
        print(f"💤 {self.name} took a power nap! Energy fully recharged to 100%.")

    def save(self, filename="pet_save.txt"):
        """Persists pet state into a file."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{self.name},{self.species},{self.level},{self.xp},{self.hunger},{self.happiness},{self.energy}")
            print(f"💾 Journey saved! See you soon, {self.name}!")
        except IOError as e:
            print(f"Error saving: {e}")


def load_pet(filename="pet_save.txt"):
    """Loads saved pet or starts the adoption process."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            d = f.read().strip().split(",")
            if len(d) == 7:
                return Pet(d[0], d[1], int(d[2]), int(d[3]), int(d[4]), int(d[5]), int(d[6]))
    except (FileNotFoundError, ValueError):
        pass

    print("✨ ADOPT A COMPANION ✨")
    name = input("Pet Name: ").strip() or "Nova"
    species = input("Species (Dragon/Wolf/Cat/Phoenix): ").strip().title() or "Dragon"
    return Pet(name, species)


def main():
    pet = load_pet()
    actions = {"1": pet.status, "2": pet.feed, "3": pet.adventure, "4": pet.sleep}

    while True:
        print("\n[1] Card 📋  [2] Feed 🍗  [3] Adventure 🗺️  [4] Sleep 💤  [5] Save & Exit 🚪")
        c = input("Command: ").strip()
        if c == "5":
            pet.save()
            break
        actions.get(c, lambda: print("❌ Invalid command!"))()


if __name__ == "__main__":
    main()
