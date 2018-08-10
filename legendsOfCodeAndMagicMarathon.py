import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
while True:
    for i in range(2):
        player_health, player_mana, player_deck, player_rune = [int(j) for j in input().split()]
    opponent_hand = int(input())
    card_count = int(input())
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        my_health_change = int(my_health_change)
        opponent_health_change = int(opponent_health_change)
        card_draw = int(card_draw)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    print("PASS")

