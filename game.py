import random

# Player Class
class Player:
  def __init__(self, name, role):
    self.name = name
    self.role = role
    self.hp = 100
    self.attack = 10
    self.defense = 5
    self.inventory = ["Health Potion"] # Starting Item for all Characters

  def take_damage(self, damage):
    self.hp -= max(damage - self.defense, 0)
    print(f"{self.name} takes {damage} damage! HP: {self.hp}")

  def attack_enemy(self, enemy):
    damage = random.randint(5, self.attack)
    print(f"{self.name} attacks {enemy.name} for {damage} damage!")
    enemy.take_damage(damage)

# Enemy Class
class Enemy:
  def __init__(self, name, hp, attack):
    self.name = name
    self.hp = hp
    self.attack = attack

  def take_damage(self, damage):
    self.hp -= damage
    print(f"{self.name} takes {damage} damage! HP: {self.hp}")

  def attack_player(self, player):
    damage = random.randint(3, self.attack)
    print(f"{self.name} attacks {player.name} for {damage} damage!")
    player.take_damage(damage)

# Combat
def combat(player, enemy):
    print(f"\nA wild {enemy.name} appears!")
    while player.hp > 0 and enemy.hp > 0:
        print("\nChoose your action:")
        print("1) Attack")
        print("2) Defend")
        print("3) Use Item (if available)")

        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":  # Player attacks
            player.attack_enemy(enemy)
        elif choice == "2":  # Player defends
            print(f"{player.name} raises their defense!")
            player.defense += 5
        elif choice == "3":  # Player uses an item
            if "Health Potion" in player.inventory:
                print(f"{player.name} uses a Health Potion!")
                player.hp += 20
                player.inventory.remove("Health Potion")
                print(f"{player.name}'s HP: {player.hp}")
            else:
                print("You have no items to use!")
        else:
            print("Invalid choice. You lose your turn!")

        # Reset defense after defending
        if choice == "2":
            player.defense -= 5

        # Enemy's turn if it's still alive
        if enemy.hp > 0:
            enemy.attack_player(player)

        # Check for end conditions
        if player.hp <= 0:
            print(f"You have been defeated... Game Over!")
        elif enemy.hp <= 0:
            print(f"You have defeated {enemy.name}!\n")
            loot = random.choice(["Health Potion", None])
            if loot:
              player.inventory.append(loot)
              print(f"{enemy.name} dropped a {loot}!")

def main():
  print("Welcome to the Text-Based RPG Game!")
  name = input("Enter your characters name: ")
  print("Choose your role: 1) Warrior 2) Mage 3) Rogue")
  role_choice = input("Enter 1, 2, or 3: ")

  role = "Warrior"
  if role_choice == "2":
    role = "Mage"
  elif role_choice == "3":
    role = "Rogue"

  player = Player(name, role)
  print(f"\nWelcome {player.name} the {player.role}!")

  # Enemies
  goblin = Enemy("Goblin", 50, 8)
  dragon = Enemy("Dragon", 120, 15)

  # Combat
  combat(player, goblin)
  if player.hp > 0:
      combat(player, dragon)

  print("Thanks for playing!")

if __name__ == "__main__":
    main()

