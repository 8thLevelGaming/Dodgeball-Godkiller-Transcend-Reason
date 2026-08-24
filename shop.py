import items

# This is the function that rolls random items on each separate shop visit.
# Available items are those in the item pool but not in the player's inventory.
# It runs a for loop for every name in the pool.
def item_roll():
    available = [name for name in item_pool if name not in player.owned_items]
    # There is a bit of protection against rolling less than 3 available items but
    # I made so many that it is impossible to deplete the list in full playthrough.
    count = min(3, len(available))
    return random.sample(available, count)
    
# This is the gym function for the shop below.
# It calculates how much exp the player needs to level up.
# And if the player has money equal to that amount it purchases the exp
# at a ratio of $2 per experience point to level up.
def gym():
    training_cost = gym_price()
    exp_to_buy = training_cost // 2
    if player.money >= training_cost:
        player.money = player.money - training_cost
        player.exp = player.exp + exp_to_buy
        # The flavor text for the gym is randomized.
        gym_flavor_text = random_gym_text()
        print(f"\n{gym_flavor_text}")
        if player.exp >= 100:
            player.level = player.level + 1
            player.exp = player.exp - 100
            full_stats_display()
            level_up()
    else:
        print("You can't afford to go to the gym...")

# Function returns the cost of using the gym.
def gym_price():
    gym_price = (100 - player.exp) * 2
    return gym_price

# Lists and rolls randomized flavor text you can get when going to the gym.
def random_gym_text():
    gym_flavors = [
        "You lift heavy weights and run around for a while!",
        "You obliterate several target dummies with your throws!",
        "You do 100 push-ups, 100 sit-ups, 100 squats, and a 10 km run!"
    ]
    
    chosen_text = random.choice(gym_flavors)
    return chosen_text

# Function that creates a shop the player periodically visits.
# At this shop, the player can buy a meal to fully restore HP and stamina.
# The player can also find three randomized items. Only one of them
# can be bought on each shop visit.
# This function uses getattr and setattr. These help with
# saving object attributes into strings.
# For example, setattr(player, "strength", 15) is the same as
# player.strength = 15. There are cases where this is preferable, such as
# when an attribute is decided at runtime.
def shop():
    available_items = item_roll()
    # We make it so every shop visit the player enters as not having
    # already bought an item, enabling them to buy a new one.
    player_already_bought = False

    # The prices and rarities of the 3 items rolled are collected.
    # Note that we are using list positions for the items, meaning that
    # the first item is at position 0.
    item1_price = item_price(available_items[0])
    item1_rarity = item_pool[available_items[0]]['rarity']
    item2_price = item_price(available_items[1])
    item2_rarity = item_pool[available_items[1]]['rarity']
    item3_price = item_price(available_items[2])
    item3_rarity = item_pool[available_items[2]]['rarity']

    # This is the loop where the player can actually interact with the shop.
    while True:
        slow_print("\nA strange old man offers you mapo tofu and a relic. You can buy only one of the three.")
        stats_display()
        slow_print(f"You currently have ${player.money}")
        print("-" * 40)
        gym_price_display = gym_price()
        
        options = {
        "1": f"Buy {available_items[0]} ({item1_rarity}) for ${item1_price}\n ---> {item_effects_display(available_items[0])}",
        "2": f"Buy {available_items[1]} ({item2_rarity}) for ${item2_price}\n ---> {item_effects_display(available_items[1])}",
        "3": f"Buy {available_items[2]} ({item3_rarity}) for ${item3_price}\n ---> {item_effects_display(available_items[2])}",
        "4": "Eat some extra-spicy mapo tofu for $20.",
        "5": f"Buy a big can of sardines to eat later for $20. You currently have {player.sardine_inventory}.",
        "6": f"Hit the gym and train. It will cost ${gym_price_display}.",
        "7": "View your stats.",
        "8": "Leave the shop."
        }
        for num, text in options.items():
            print(f"{num}) {text}")

        player_buy = input("What will you get? ")
        
        if player_buy in options:
            if player_buy == "1":
                item_name = available_items[0]
                # In this function, the details variable pulls up the rolled item's name and
                # stores it, then if the player can afford the item the details vairable
                # can be used to draw the stats to be modified and the amount to modify by,
                # as defined in the earlier item_pool master list.
                details = item_pool[item_name]
                if player.money >= item1_price:
                    # In addition to checking the player can afford the item we also
                    # confirm that the player has not bought an item yet.
                    if player_already_bought is False:
                        player.money = player.money - item1_price
                        apply_item_effects(item_name)
                        print(f"You bought {item_name}! ({item_effects_display(item_name)})")
                        # After sale, we mark that the player bought an item,
                        # which blocks the other options for this visit.
                        player_already_bought = True
                    else:
                        print("The strange old man only had one relic for sale. Try again next visit.")
                else:
                    print("You can't afford that.")
                    
            elif player_buy == "2":
                item_name = available_items[1]
                details = item_pool[item_name]
                if player.money >= item2_price:
                    if player_already_bought is False:
                        player.money = player.money - item2_price
                        apply_item_effects(item_name)
                        print(f"You bought {item_name}! ({item_effects_display(item_name)})")
                        player_already_bought = True
                    else:
                        print("The strange old man only had one relic for sale. Try again next visit.")
                else:
                    print("You can't afford that.")
                    
            elif player_buy == "3":
                item_name = available_items[2]
                details = item_pool[item_name]
                if player.money >= item3_price:
                     if player_already_bought is False:
                        player.money = player.money - item3_price
                        apply_item_effects(item_name)
                        print(f"You bought {item_name}! ({item_effects_display(item_name)})")
                        player_already_bought = True
                     else:
                        print("The strange old man only had one relic for sale. Try again next visit.")
                else:
                    print("You can't afford that")

            # The remaining options are very simple, restoring the player,
            # increasing their sardine_inventory attribute, calling the
            # gym function, or displaying their stats.
            elif player_buy == "4":
                if player.money >= 20:
                    player.money = player.money - 20
                    slow_print("\nYou greedily devour the mapo tofu! It tastes sinful.")
                    player.hp = player.max_hp()
                    player.stamina = player.max_stamina()
                else:
                    print("You can't even afford that delicious mapo tofu... your martyrdom is truly endless.")
                    
            elif player_buy == "5":
                if player.money >= 20:
                    player.money = player.money - 20
                    player.sardine_inventory = player.sardine_inventory + 1
                    print(f"\nYou buy some sardines. You now have {player.sardine_inventory}")
                else:
                    print("The poor must make do without sardines. How cruel.")
                    
            elif player_buy == "6":
                gym()
                
            elif player_buy == "7":
                full_stats_display()

            # We break the loop only when the player leaves the shop.
            elif player_buy == "8":
                slow_print("You leave the tofu shop.")
                break
        else:
            print("Your options range between 1 and 8!")