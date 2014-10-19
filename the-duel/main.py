#!/usr/bin/env python
# The Duel, by Michael Sarfati
# A small and goofy turn-based dueling game, in which a player must
#   fight against a computer opponent. 

from players import nameGen, Dueler, AI

def forfeit():
    'Quits the game gracefully.'
    print('\n\tYou have forfitted the game.\n\t{} wins.'.format(ENEMY_NAME))
    raise SystemExit

def action(dueler, target, selection):
    'Player action event handler'
    if selection == 1:
        dueler.slash(target)
    elif selection == 2:
        dueler.thrust(target)
    elif selection == 3:
        dueler.heal()
    elif selection == 0:
        forfeit()

def isValid():
    'Validates user input. Asks for user-input once called, and returns validated form.'
    while True:
        try:
            select = int(raw_input(PLAYER_MENU))
        except (EOFError, KeyboardInterrupt):
            forfeit()
        except:
            print "Please choose a number from the menu."
        else:
            if (select in range(0, 4)) == True:
                return select
            print "Invalid selection."

def gameStatus(p, e, TURN_COUNTER):
    'Prints the status of the game to the screen'
    print(\
'''
Turn #{turn}
{player_name} (You)\t\t{enemy_name} (Enemy)
HP: {player_hp} of {player_totalHp}\t\tHP: {enemy_hp} of {enemy_totalHp}
Status: {player_status}\t\tStatus: {enemy_status}\
'''.format(
        turn=TURN_COUNTER,
        player_name=p.name,
        player_hp=p.hp,
        player_totalHp=p.totalHp,
        player_status=p.health()[1].capitalize(),
        enemy_name=e.name,
        enemy_hp=e.hp,
        enemy_totalHp=e.totalHp,
        enemy_status=e.health()[1].capitalize(),
    )
)

def main():
    print("===:: THE DUEL ::===\n\
    Welcome to The Duel, a small, turn-based RPG-style dueling game.")
    global TURN_COUNTER
    global PLAYER_MENU
    global ENEMY_NAME
    TURN_COUNTER = int(1)
    PLAYER_MENU = 'Moves: | (1) Slash | (2) Thrust | (3) Heal | (0) Forfeit |\nSelect:> '

    # p = Dueler(name=nameGen())
    p = Dueler(name=raw_input("What is your name? "))
    e = Dueler(name=nameGen(), isAI=True)
    ai = AI(e)
    ENEMY_NAME = str(e.name)

    while p.hp > 0 and e.hp > 0:
        'Main event thread'
        gameStatus(p, e, TURN_COUNTER)
        pSelect = isValid()
        action(p, e, pSelect) # Player action
        action(e, p, ai.select()) # Enemy action
        if (p.hp < 0) or (e.hp < 0):
            whoWon = lambda a, b: a.name if a.hp > b.hp else b.name
            whoWon = whoWon(p, e)
            print("{} {}wins in {} turns.\nThanks for playing!".format(
                whoWon,
                "(you) " if p.name == whoWon else "(enemy) ",
                TURN_COUNTER))
            raise SystemExit
        TURN_COUNTER += 1

if __name__=='__main__':
    main()