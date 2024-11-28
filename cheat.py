import re

v = "2.0"
tab = " " * 4
newline = "\n"

#=============  ./scripts/interfaces/main_menu.rpy =========
def main_menu():
    fn="./scripts/interfaces/main_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt='    text "\[config.version\]" anchor \(1.0, 0.5\) pos \(0.157, 0.96\):[\r\n]+ +size 25'
    repl='    text "[config.version]" anchor (1.0, 0.5) pos (0.157, 0.96):\n        size 25\n    frame:\n        xalign .5\n        yalign 0\n        text("Cheats enabled!")'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

main_menu()

#=============  ./scripts/interfaces/quick_menu.rpy =========
def quick_menu():
    fn="./scripts/interfaces/quick_menu.rpy"
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

    fc = fc.replace('config.developer = "auto"', 'config.developer = "auto"\ndefine config.console = True')

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

config()

#=============  ./scripts/mechanics/utilities.rpy =========
def utilities():
    fn="./scripts/mechanics/utilities.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt='(?P<tabs> +)def unique\(original\):'
    repl='    def removeCheating(C):\r\n        C.History.remove("cheated_on_flirting_in_public")\r\n        C.History.remove("cheated_on_date")\r\n        C.History.remove("cheated_on_relationship")\r\n        if C.History.permanent.get("cheated_on_flirting_in_public"):\r\n            del C.History.permanent["cheated_on_flirting_in_public"]\r\n        if C.History.permanent.get("cheated_on_date"):\r\n            del C.History.permanent["cheated_on_date"]\r\n        if C.History.permanent.get("cheated_on_relationship"):\r\n            del C.History.permanent["cheated_on_relationship"]\r\n           \r\n        for other_C in all_Companions:\r\n            Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public")\r\n            Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_date")\r\n            Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_relationship")\r\n            if Player.History.permanent.get(f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public"):\r\n                del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public"]\r\n            if Player.History.permanent.get(f"cheated_on_{C.tag}_with_{other_C.tag}_date"):\r\n                del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_date"]\r\n            if Player.History.permanent.get(f"cheated_on_{C.tag}_with_{other_C.tag}_relationship"):\r\n                del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_relationship"]\r\n        return\r\n\r\n\g<tabs>def unique(original):'
    fc = re.sub(patt, repl, fc, flags=re.M)

    patt='(?P<tabs> +)def unique\(original\):'
    repl='\g<tabs>def addAbilityPoints(p):\r\n        if not hasattr(Player, "ability_points"):\r\n            Player.ability_points = 0\r\n        if p > 0:\r\n            Player.ability_points += p\r\n\r\n\g<tabs>def unique(original):'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

utilities()

#=========== ./scripts/base/player.rpy
def basePlayer():
    fn="./scripts/base/player.rpy"
    with open(fn, "r") as file:
        fc = file.read()
    
    patt='(?P<tabs> +)points -= all_abilities\[ability\]\["cost"\]'
    repl='\g<tabs>points -= all_abilities[ability]["cost"]\r\n\r\n            if hasattr(self, "ability_points"):\r\n                points += self.ability_points'
    
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

basePlayer()


#=============  ./scripts/interfaces/Player_menu.rpy =========
def player_menu():
    fn="./scripts/interfaces/Player_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #turns text cash number into textbutton
    patt='    text "\$\[Player\.cash\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        size (?P<size>[0-9]+)'
    repl='    textbutton "{size=\g<size>}" + "$[Player.cash]" \g<pos>:\r\n        action SetVariable("Player.cash", Player.cash + 50000)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #turns text for ability points into text button
    patt='    text "\[Player.skill_points\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+        size (?P<size>[0-9]+)'
    repl='    textbutton "{size=\g<size>}{font=\g<font>}" + "[Player.skill_points]" \g<pos>:\n        action Function(addAbilityPoints, 5)' 
    fc = re.sub(patt, repl, fc, flags=re.M)

    #allows for draggable player xp bar
    patt='value \(Player\.XP - Player\.XP_goal\/1\.75\) range \(Player\.XP_goal - Player\.XP_goal\/1\.75\)'
    repl='value FieldValue(Player, "XP", Player.XP_goal) range (Player.XP_goal)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #turns text for both love and trust into textbuttons
    patt='(?P<tabs1> +)text "\[relationships_Entry\.(?P<lt>love|trust)\]"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0\.[0-9]+, 0\.[0-9]+\)):[ \r\n]+font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+size (?P<size>[0-9]+)[ \r\n]+color "[a-z0-9#]+"'
    repl='\g<tabs1>textbutton "{size=\g<size>}{font=\g<font>}" + "[relationships_Entry.\g<lt>]"\g<pos>:\n\g<tabs1>    action SetVariable("relationships_Entry.\g<lt>", relationships_Entry.\g<lt> + 100)'
    fc = re.sub(patt, repl, fc, flags=re.M)
   
    #turn emotion icons into buttons to turn off said status
    #patt='(?P<tabs1> +)add (?P<f>f?)"images/interfaces/Player_menu/relationships_(?P<status>mad|horny|nympho|\[status\])\.webp" zoom high_resolution_interface_adjustment'
    #repl='\g<tabs1>imagebutton idle \g<f>"images/interfaces/Player_menu/relationships_\g<status>.webp" action SetDict(relationships_Entry.status, \g<f>"\g<status>", 0)'
    #repl='\g<tabs1>imagebutton idle \g<f>"images/interfaces/Player_menu/relationships_\g<status>.webp":\r\n\g<tabs1>    at transform:\r\n\g<tabs1>        zoom high_resolution_interface_adjustment\r\n\g<tabs1>    action SetDict(relationships_Entry.status, \g<f>"\g<status>", 0)'
    #fc = re.sub(patt, repl, fc, flags=re.M)

    #adapts the relationships_status() to have character as a parameter for mood changing
    patt='screen relationships_status\(status, \*\*properties\):'
    repl='screen relationships_status(status, c, **properties):'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #setting the relationships_status() function to insert the text as a text button to turn off mood statuses
    patt='(?P<t1> +)text "\[status.upper\(\)\]" anchor \(0\.5, 0\.5\) pos \(0\.5, 0\.85\):[\r\n]+(?P<t2> +)size properties\.get\("text_size", 16\)(?P<br>[\r\n ]+)color properties\.get\("text_color", "#000000"\)'
    repl='\g<t1>textbutton "{size=[properties.get(\\"text_size\\", 16)]}{color=[properties.get(\\"text_color\\", \\"#000000\\")]}" + "[status.upper()]" anchor (0.5, 0.5) pos (0.5, 0.85):\r\n$+{t2}action SetDict(c.status, status, 0)'
    fc = re.sub(patt, repl, fc, flags=re.M)
    
    #adding the character into the relationships_status() call
    patt='(?P<t1> {2,})use relationships_status\([\r\n]+(?P<t2> {2,})(?P<status>[a-zA-Z"]+),[\r\n]+'
    repl='\g<t1>use relationships_status(\r\n\g<t2>\g<status>,\r\n\g<t2>relationships_Entry,\r\n'
    fc = re.sub(patt, repl, fc, flags=re.M)


    #adding button that allows for removal of cheating
    #        text "RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (0.495, 0.297):
    patt='        text "RELATIONSHIP STATUS" anchor \(0\.0, 0\.5\) pos \((?P<posX>[0-9.]+), (?P<posY>[0-9.]+)\):[\r\n]+            font "agency_fb\.ttf"[\r\n]+[\r\n]+            size 28'
    repl='        textbutton "{size=28}{font=agency_fb.ttf} RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (\g<posX>, \g<posY>):\r\n            action Function(removeCheating, relationships_Entry)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #friendship is the best thing ever! (allows for clicking on friendship to increase it by 50)
    patt='(?P<tabs> +)add "images/interfaces/photos/\[C\]\.webp" align (?P<algn>\([a-z0-9,. ]+\)) zoom (?P<zoom>0\.[0-9]+)'
    repl='\g<tabs>imagebutton idle f"images/interfaces/photos/{C}.webp" align \g<algn>:\n\g<tabs>    at transform:\n\g<tabs>        zoom 0.13\r\n\g<tabs>    action SetDict(relationships_Entry.friendship, f"{C}", relationships_Entry.friendship[C] + 50)'
    fc = re.sub(patt, repl, fc, flags=re.M)


    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

player_menu()


#=============  ./scripts/interfaces/sex.rpy =========
def sex():
    fn="./scripts/interfaces/sex.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #sets text stamina into textbutton
    patt='        text "\[Player.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    repl='        textbutton "{size=\g<size>}" + "[Player.stamina]" \g<pos>:\n            action SetVariable("Player.stamina", Player.max_stamina + Player.stamina)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #as of v0.6b, the love interest has no stamina stat
    #patt='        text "\[Character.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    #repl='        textbutton "{size=\g<size>}" + "[Character.stamina]" \g<pos>:\n            action SetVariable("focused_Character.stamina", focused_Character.max_stamina + Character.stamina)'
    #fc = re.sub(patt, repl, fc, flags=re.M)

    #sets player desire values into field values, aka, interactable sliding bars
    patt='value Player.desire'
    repl='value FieldValue(Player, "desire", 100)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

sex()

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

    #skips bedroom check for place to have sex
    patt='elif Player.location not in bedrooms and "bg_shower" not in Player.location'
    repl='elif False and Player.location not in bedrooms and "bg_shower" not in Player.location'

    fc = re.sub(patt, repl, fc, flags=re.M)


    #skips people around check
    patt='    elif len\(Present\) > 1:'
    repl='    elif False and len(Present) > 1:'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")


    fn="./scripts/interfaces/interactions.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #skips bedroom checks and number of people checks for place to have sex GUI
    patt='if approval_check\(Character, threshold = "hookup"\) and len\(Present\) == 1 and Player.location in \[Character.home, Player.home\] and not get_Present\(location = Player.location.replace\("_", "_shower_"\)\)\[0\]'
    repl='if approval_check(Character, threshold = "hookup") and len(Present) >= 1'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

allowPublicSex()


#=========== ./scripts/mechanics/movement.rpy
def movement():
    fn="./scripts/mechanics/movement.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #character won't wipe off cum when exiting bed room after wearing cum 10 times
    patt='                if temp_Characters\[0\]\.spunk\[location\]'
    repl='                if temp_Characters[0].History.check("wear_cum") < 10 and temp_Characters[0].spunk[location]'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

movement()



print(f"    Success! Cheats are now enabled!")
