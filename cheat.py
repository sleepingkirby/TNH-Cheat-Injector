import re

v = "1.6"
tab = " " * 4
newline = "\n"

#=============  ./scripts/interface/main_menu.rpy =========
def main_menu():
    fn="./scripts/interface/main_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt='    text f"\{config.version\}" anchor \(1.0, 0.5\) pos \(0.157, 0.96\):[\r\n]+ +size 25'
    repl='    text f"{config.version}" anchor (1.0, 0.5) pos (0.157, 0.96):\n        size 25\n    frame:\n        xalign .5\n        yalign 0\n        text("Cheats enabled!")'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

main_menu()

#=============  ./scripts/interface/quick_menu.rpy =========
def quick_menu():
    fn="./scripts/interface/quick_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt='        textbutton _\("Q.Load"\):[\r\n]+            action QuickLoad\(\)'
    repl='        textbutton _("Q.Load"):\n            action QuickLoad()\n\n        textbutton _("CheatV'+v+'"):\n            action NullAction()'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

quick_menu()

#============= config.rpy =========
def config():
    fn="./scripts/base/config.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    fc = fc.replace('config.developer = "auto"', 'config.developer = "auto"\n    config.console = True')

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

config()

#=============  ./scripts/interface/Player_menu.rpy =========
def player_menu():
    fn="./scripts/interface/Player_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #turns text cash number into textbutton
    patt='    text f"\$ \{Player\.cash\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        size (?P<size>[0-9]+)'
    repl='    textbutton "{size=\g<size>}" + f"$ {Player.cash}" \g<pos>:\n        action SetVariable("Player.cash", Player.cash + 50000)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #turns text for ability points into text button
    patt='    text f"\{Player.ability_points\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+        size (?P<size>[0-9]+)'
    repl='    textbutton "{size=\g<size>}{font=\g<font>}" + f"{Player.ability_points}" \g<pos>:\n        action SetVariable("Player.ability_points", Player.ability_points + 5)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #allows for draggable player xp bar
    patt='value Player.XP'
    repl='value FieldValue(Player, "XP", Player.XP_goal)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #turns text for both love and trust into textbuttons
    patt='(?P<tabs1> +)text f"\{current_relationships_Entry\.(?P<lt>love|trust)\}"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0\.[0-9]+, 0\.[0-9]+\)):[ \r\n]+font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+size (?P<size>[0-9]+)[ \r\n]+color "[a-z0-9#]+"'
    repl='\g<tabs1>textbutton "{size=\g<size>}{font=\g<font>}" + f"{current_relationships_Entry.\g<lt>}"\g<pos>:\n\g<tabs1>    action SetVariable("current_relationships_Entry.\g<lt>", current_relationships_Entry.\g<lt> + 100)'
    fc = re.sub(patt, repl, fc, flags=re.M)
    
    #turn emotion icons into buttons to turn off said status
    patt='(?P<tabs1> +)add (?P<f>f?)"images/interface/Player_menu/relationships_(?P<status>mad|horny|nympho|\{status\})\.webp" zoom interface_adjustment'
    repl='\g<tabs1>imagebutton idle \g<f>"images/interface/Player_menu/relationships_\g<status>.webp" action SetDict(current_relationships_Entry.status, \g<f>"\g<status>", 0)'
    fc = re.sub(patt, repl, fc, flags=re.M)
    
    #friendship is the best thing ever! (allows for clicking on friendship to increase it by 50)
    patt='(?P<tabs> +)add f"images/interface/photos/\{C\}\.webp" align (?P<algn>\([a-z0-9,. ]+\)) zoom (?P<zoom>0\.[0-9]+)'
    repl='\g<tabs>imagebutton idle f"images/interface/photos/{C}.webp" align \g<algn>:\n\g<tabs>    at transform:\n\g<tabs>        zoom 0.13\r\n\g<tabs>    action SetDict(current_relationships_Entry.friendship, f"{C}", current_relationships_Entry.friendship[C] + 50)'
    fc = re.sub(patt, repl, fc, flags=re.M)


    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

player_menu()


#=============  ./scripts/interface/actions.rpy =========
def actions():
    fn="./scripts/interface/actions.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #sets text stamina into textbutton
    patt='        text f"\{Player.stamina\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    repl='        textbutton "{size=\g<size>}" + f"{Player.stamina}" \g<pos>:\n            action SetVariable("Player.stamina", Player.max_stamina + Player.stamina)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    patt='        text f"\{Character.stamina\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    repl='        textbutton "{size=\g<size>}" + f"{Character.stamina}" \g<pos>:\n            action SetVariable("focused_Character.stamina", focused_Character.max_stamina + Character.stamina)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #sets player and character desire values into field values, aka, interactable sliding bars
    patt='value (?P<cp>Player|Character).desire'
    repl='value FieldValue(\g<cp>, "desire", 100)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

actions()

#=========== ./scripts/mechanics/approval.rpy
def approval():
    fn="./scripts/mechanics/approval.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #breaks approval limit
    patt='[0-9]{3,},'
    repl='99999,'

    fc = re.sub(patt, repl, fc, flags=re.M)

    patt=', [0-9]{3,}\]'
    repl=', 99999]'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

approval()


##=========== allowing sex in public. Props to RonChon. 2 Checks in place to prevent this.
## Did I do this because darkstel couldn't get over himself? Yep. Is it a bit immature? Yep. Do I feel ashamed? Nope. If you don't want code to change, don't poke a programmer.
##=========== ./scripts/sex/request.rpy
#=========== ./scripts/mechanics/approval.rpy
def allowPublicSex():
    fn="./scripts/sex/request.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #breaks approval limit
    patt='elif Player.location not in bedrooms and "bg_shower" not in Player.location'
    repl='elif False and Player.location not in bedrooms and "bg_shower" not in Player.location'

    fc = re.sub(patt, repl, fc, flags=re.M)

    patt='    elif len\(Present\) > 1:'
    repl='    elif False and len(Present) > 1:'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")


    fn="./scripts/interface/interactions.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #breaks approval limit
    patt='if approval_check\(Character, threshold = "hookup"\) and len\(Present\) == 1 and Player.location in \[Character.home, Player.home\] and not get_Present\(location = Player.location.replace\("_", "_shower_"\), include_Party = False\)\[0\]'
    repl='if approval_check(Character, threshold = "hookup") and len(Present) >= 1'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

allowPublicSex()

print(f"    Success! Cheats are now enabled!")
