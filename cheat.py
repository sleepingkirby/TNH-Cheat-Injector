import re

v = "2.93"
tab = " " * 4
newline = "\n"

#=============  ./interfaces/main_menu.rpy =========
def main_menu():
    fn="./interfaces/main.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'    text "\[config.version\]" anchor \(1.0, 0.5\) pos \(0.157, 0.96\):\n        size 25'
    repl=r'    text "[config.version]" anchor (1.0, 0.5) pos (0.157, 0.96):\n        size 25\n    frame:\n        xalign .5\n        yalign 0\n        text("Cheats enabled!")'


    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

main_menu()

#=============  ./interfaces/base.rpy =========
def quick_menu():
    fn="./interfaces/base.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'(?P<t1> +)textbutton _\("Q.Load"\) action QuickLoad\(\) text_size quick_size'
    repl=r'\g<t1>textbutton _("Q.Load") action QuickLoad() text_size quick_size\n\n\g<t1>textbutton _("CheatV' + v + r'"):\n\g<t1>    action NullAction()'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

quick_menu()

#============= config.rpy =========
def console():
    fn="../renpy/common/00console.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    fc = fc.replace('config.console = False', 'config.console = True')

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

console()

#=========== ./core/utilities/utilities.rpy
def utilities():
    fn="./core/utilities/utilities.rpy"
    with open(fn, "r") as file:
        fc = file.read()
    patt=r'(?P<tabs> *)init -1:'
    repl=r'init python:\n    def removeCheating(C) -> None:\n        C.remove_trait("cheated_on_flirting")\n        C.remove_trait("cheated_on_flirting_in_public")\n        C.remove_trait("cheated_on_date")\n        C.remove_trait("cheated_on_relationship")\n        C.History.remove("cheated_on_flirting")\n        C.History.remove("cheated_on_flirting_in_public")\n        C.History.remove("cheated_on_date")\n        C.History.remove("cheated_on_relationship")\n        if "permanent" in C.History.trackers and "cheated_on_flirting_in_public" in C.History.trackers["permanent"]:\n            del C.History.trackers["permanent"]["cheated_on_flirting_in_public"]\n        if "permanent" in C.History.trackers and "cheated_on_date" in C.History.trackers["permanent"]:\n            del C.History.trackers["permanent"]["cheated_on_date"]\n        if "permanent" in C.History.trackers and "cheated_on_relationship" in C.History.trackers["permanent"]:\n            del C.History.trackers["permanent"]["cheated_on_relationship"]\n\n        for other_C in GameState.ALL_COMPANIONS:\n            if hasattr(other_C, "tag"):\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public")\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_date")\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_relationship")\n                if "permanent" in Player.History.trackers and f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public" in Player.History.trackers["permanent"]:\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public"]\n                if "permanent" in Player.History.trackers and f"cheated_on_{C.tag}_with_{other_C.tag}_date" in Player.History.trackers["permanent"]:\n                   del Player.History.trackers["permanent"][f"cheated_on_{C.tag}_with_{other_C.tag}_date"]\n                if "permanent" in Player.History.trackers and f"cheated_on_{C.tag}_with_{other_C.tag}_relationship" in Player.History.trackers["permanent"]:\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_relationship"]\n        return\n\n\g<tabs>init -1:'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

utilities()

#=========== ./interfaces/Player_menu/inventory.rpy =========
def inventory():
    fn='./interfaces/menu/inventory.rpy'

    with open(fn, "r") as file:
        fc = file.read()

    #turns text cash number into textbutton
    patt=r'    text "\$\[Player\.cash\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        size (?P<size>[0-9]+)'
    repl=r'    textbutton "{size=\g<size>}" + "$[Player.cash]" \g<pos>:\r\n        action SetVariable("Player.cash", int(Player.cash) + int(50000))'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file: 
        file.write(fc)

    print(f"{fn} patched")

inventory()

#============= ./interfaces/menu/skills.rpy =========
def player_skills():
    fn='./interfaces/menu/skills.rpy'

    with open(fn, "r") as file:
        fc = file.read()

    #turns text for ability points into text button
    patt=r'    text "\[Player.skill_points\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\n]+        font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \n]+        size (?P<size>[0-9]+)'
    repl=r'    textbutton "{size=\g<size>}{font=\g<font>}" + "[Player.skill_points]" \g<pos>:\n        action Function(Player.History.update, "bought_skill_point")'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #allows for draggable player xp bar
    patt=r'value \(Player\.XP - Player\.XP_goal / 1\.75\) range \(Player\.XP_goal - Player\.XP_goal / 1\.75\)'
    repl=r'value FieldValue(Player, "XP", Player.XP_goal) range (Player.XP_goal)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #allows for draggable player xp bar for level 1
    patt=r'value Player\.XP range Player\.XP_goal'
    repl=r'value FieldValue(Player, "XP", Player.XP_goal) range(Player.XP_goal)'
    fc = re.sub(patt, repl, fc, flags=re.M)


    #Points will add "studied" or "trained" to player history
    patt=r'    text "Points" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)) size (?P<size>[0-9]+)'
    repl=r'    textbutton "{size=\g<size>}" + "Points" \g<pos>:\n        action Function(Player.History.update, "trained" if leaderboard == "combat" else "cognitive")'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

player_skills()


#============= ./interfaces/menu/relationships.rpy =========
def relationships():
    fn='./interfaces/menu/relationships.rpy'

    with open(fn, "r") as file:
        fc = file.read()

    #turns text for both love and trust into textbuttons
    patt=r'(?P<tabs1> +)text "\[Entry\.(?P<lt>love|trust)\]"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0\.[0-9]+, 0\.[0-9]+\)):[ \n]+font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \n]+size (?P<size>[0-9]+)[ \n]+color "[a-z0-9#]+"'
    repl=r'\g<tabs1>textbutton "{size=\g<size>}{font=\g<font>}" + "[Entry.\g<lt>]"\g<pos>:\n\g<tabs1>    action SetField(Entry, "\g<lt>", Entry.\g<lt> + 100)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #adding the character into the relationships_status() call
    patt=r'screen relationships_status\(status, '
    repl=r'screen relationships_status(status, char=None, '
    fc = re.sub(patt, repl, fc, flags=re.M)

    #fixing calls to relationships_status() to include the character as a parameter
    patt=r'(?P<t1> {2,})use relationships_status\([\n]+(?P<t2> {2,})(?P<status>[a-zA-Z"]+),[\n]+'
    repl=r'\g<t1>use relationships_status(\n\g<t2>\g<status>,\n\g<t2>char = Entry,\n'
    fc = re.sub(patt, repl, fc, flags=re.M)
 
    #setting the relationships_status() function to insert the text as a text button to turn off mood statuses
    patt=r'(?P<t1> +)text "\[status.upper\(\)\]" anchor \(0\.5, 0\.5\) pos \(0\.5, 0\.85\):[\n]+(?P<t2> +)size text_size(?P<br>[\n ]+)color text_color'
    repl=r'\g<t1>textbutton "{size=[text_size]}{color=[text_color]}" + "[status.upper()]" anchor (0.5, 0.5) pos (0.5, 0.85):\n\g<t2>action SetDict(char._status, status, 0)'
    fc = re.sub(patt, repl, fc, flags=re.M)
    

    #adding button that allows for removal of cheating
    #        text "RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (0.495, 0.297):
    patt=r'        text "RELATIONSHIP STATUS" anchor \(0\.0, 0\.5\) pos \((?P<posX>[0-9.]+), (?P<posY>[0-9.]+)\):[\n]+            font "agency_fb\.ttf"[\n]+[\n]+            size 28'
    repl=r'        textbutton "{size=28}{font=agency_fb.ttf} RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (\g<posX>, \g<posY>):\n            action Function(removeCheating, Entry)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #friendship is the best thing ever! (allows for clicking on friendship to increase it by 50)
    patt=r'(?P<tabs> +)add "characters/\[C\.tag\]/images/photo\.webp" align (?P<align>\([0-9., ]+\)) zoom (?P<zoom>0\.[0-9]+)'
    repl=r'\g<tabs>imagebutton idle f"characters/{C.tag}/images/photo.webp" align \g<align>:\n\g<tabs>    at transform:\n\g<tabs>        zoom 0.13\n\g<tabs>    action SetField(all_Friendships[_create_friendship_key(Entry, C)], "_score", all_Friendships[_create_friendship_key(Entry, C)]._score + 50)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")



#==== inserting _create_friendship_key() from python into renpy
    fn='./core/friendships/__init__.py'
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'from \.mechanics import \('
    repl=r'from .mechanics import (\n    _create_friendship_key,'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")


    fn='./definitions/core.rpy'
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'(?P<tabs> *)from core\.friendships import \('
    repl=r'\g<tabs>from core.friendships import (\n\g<tabs>    _create_friendship_key,'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")


relationships()



#=============  ./interfaces/sex.rpy =========
def sex():
    fn="./interfaces/sex.rpy"
    with open(fn, "r") as file:
        fc = file.read()
    #sets text stamina into textbutton
    patt=r'        text "\[Player.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \n]+            size (?P<size>[0-9]+)'
    repl=r'        textbutton "{size=\g<size>}" + "[Player.stamina]" \g<pos>:\n            action SetVariable("Player.stamina", Player.max_stamina + Player.stamina)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #as of v0.6b, the love interest has no stamina stat
    #patt='        text "\[Character.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    #repl='        textbutton "{size=\g<size>}" + "[Character.stamina]" \g<pos>:\n            action SetVariable("focused_Character.stamina", focused_Character.max_stamina + Character.stamina)'
    #fc = re.sub(patt, repl, fc, flags=re.M)

    #sets player desire values into field values, aka, interactable sliding bars
    patt=r'value player_desire range 1\.0'
    repl=r'value FieldValue(Player, "desire", range=1.0, step=0.1)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #character desire was redesigned in 0.6b. The bar was split into 2. One at below 1.0 and one at and above 1.0
    #And these two bars are rejoined in 0.9c.
    patt=r'value desire range 1\.0'
    repl=r'value DictValue(Character.desires, "orgasm", range=1.0, step=0.1)'
    fc = re.sub(patt, repl, fc, flags=re.M)


    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

sex()

#=========== ./core/mechanics/approval.rpy
def approval():
    fn="./core/characters/approval.py"
    with open(fn, "r") as file:
        fc = file.read()

    ##breaks approval limit
    patt=r'max_stat = MAX_STATS\[store.season\] if store\.persistent\.stat_caps else .+'
    repl=r'max_stat = MAX_STATS[store.season] if store.persistent.stat_caps else 999999'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

approval()


##=========== allowing sex in public. Props to RonChon. 2 Checks in place to prevent this.
## Did I do this because darkstel couldn't get over himself? Yep. Is it a bit immature? Yep. Do I feel ashamed? Nope. If you don't want code to change, don't poke a programmer.
##=========== ./scripts/sex/request.rpy
#=========== ./core/mechanics/sex/request.rpy
#=========== ./core/sex/request.py'
def allowPublicSex():
    fn="./core/mechanics/sex/request.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #skips bedroom check for place to have sex
    patt=r'\(Player\.location not in Bedrooms and "Shower" not in Player\.location\) or get_present_Characters\(Player\.location\) - \{Character\}'
    repl=r'False'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")


    fn="./interfaces/interactions.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #skips bedroom checks and number of people checks for place to have sex GUI
    patt=r'if check_approval\(Character, threshold = "hookup"\) and len\(get_visible_Characters\(Player\.location\)\) == 1 and Player\.location in {Character\.home, Player\.home} and not get_visible_Characters\(Player\.location\.replace\("Room", "Shower"\)\):'
    repl=r'if check_approval(Character, threshold = "hookup") and len(get_visible_Characters(Player.location)) >= 1:'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

#allowPublicSex()

#=========== ./core/mechanics/clothing.rpy
def allowWearCum():
#./core/mechanics/clothing.rpy
  fn='./core/mechanics/clothing.rpy'
  with open(fn, "r") as file:
      fc = file.read()

  # will leave cum on if wore cum 10 or more times
  patt=r'if mess:'
  repl=r'if C.History.check("wear_cum") < 10 and mess:'

  fc = re.sub(patt, repl, fc, flags=re.M)

  with open(fn, "w") as file:
      file.write(fc)

  print(f"{fn} patched")

  
  #                    elif C.destination in public_Locations and not C.check_trait("exhibitionist"):
  # this is fixing a bug with the current code for walking around with cum. The clean_cum() function can crash because it's running an interaction when you're in an interaction
  #=========== core/mechanics/behavior.rpy
  fn='./core/mechanics/behavior.rpy'
  with open(fn, "r") as file:
      fc = file.read()

  # will leave cum on if wore cum 10 or more times
  patt=r'elif C\.destination in public_Locations and not C\.check_trait\("exhibitionist"\)'
  repl=r'elif C.destination in public_Locations and not C.check_trait("exhibitionist") and False'
  
  fc = re.sub(patt, repl, fc, flags=re.M)

  with open(fn, "w") as file:
      file.write(fc)

  print(f"{fn} patched")


#allowWearCum()


#=========== ./definitions/player.rpy
def achievementPoints():
    fn="./definitions/player.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'(?P<tabs> +)self\.call_sign: str = self\.name'
    repl=r'\g<tabs>self.call_sign: str = self.name\r\n\g<tabs>self.achievePoints = 0'

    fc = re.sub(patt, repl, fc, flags=re.M)

    patt=r'(?P<tabs> +)points = 0'
    repl=r'\g<tabs>points = 0 + self.achievePoints'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

    fn="./interfaces/phone/achievements.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'(?P<t1> +)text "\[Player\.achievement_points\]"(?P<anchor> anchor \([0-9,. ]+\))(?P<pos> pos \([0-9,. ]+\)):[\r\n]+(?P<t2> +)size (?P<size>[0-9]+)[\r\n ]+color "(?P<color>#[0-9A-Fa-f]+)"'
    repl=r'\g<t1>textbutton "{size=\g<size>}{color=\g<color>}" + "[Player.achievement_points]"\g<anchor>\g<pos>:\r\n\g<t2>action SetVariable("Player.achievePoints", int(Player.achievePoints) + int(500))'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")



#achievementPoints()



print(f"    Success! Cheats are now enabled!")
