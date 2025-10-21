import re

v = "2.8"
tab = " " * 4
newline = "\n"

#=============  ./interfaces/main_menu.rpy =========
def main_menu():
    fn="./interfaces/main_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'    text "\[config.version\]" anchor \(1.0, 0.5\) pos \(0.157, 0.96\):[\r\n]+ +size 25'
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

    patt=r'        textbutton _\("Q.Load"\):[\r\n]+            action QuickLoad\(\)'
    repl=r'        textbutton _("Q.Load"):\n            action QuickLoad()\n\n        textbutton _("CheatV'+v+'"):\n            action NullAction()'

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

#=============  ./scripts/mechanics/utilities.rpy =========
def utilities():
    fn="./core/mechanics/utilities.rpy"
    with open(fn, "r") as file:
        fc = file.read()
    patt=r'(?P<tabs> +)def unique\(original:'
    repl=r'    def removeCheating(C):\r\n        C.remove_trait("cheated_on_flirting")\r\n        C.remove_trait("cheated_on_flirting_in_public")\r\n        C.remove_trait("cheated_on_date")\r\n        C.remove_trait("cheated_on_relationship")\r\n        C.History.remove("cheated_on_flirting")\r\n        C.History.remove("cheated_on_flirting_in_public")\r\n        C.History.remove("cheated_on_date")\r\n        C.History.remove("cheated_on_relationship")\r\n        if "permanent" in C.History.trackers and "cheated_on_flirting_in_public" in C.History.trackers["permanent"]:\r\n            del C.History.trackers["permanent"]["cheated_on_flirting_in_public"]\r\n        if "permanent" in C.History.trackers and "cheated_on_date" in C.History.trackers["permanent"]:\r\n            del C.History.trackers["permanent"]["cheated_on_date"]\r\n        if "permanent" in C.History.trackers and "cheated_on_relationship" in C.History.trackers["permanent"]:\r\n            del C.History.trackers["permanent"]["cheated_on_relationship"]\r\n\r\n        for other_C in GameState.all_Companions:\r\n            if hasattr(other_C, "tag"):\r\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public")\r\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_date")\r\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_relationship")\r\n                if "permanent" in Player.History.trackers and f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public" in Player.History.trackers["permanent"]:\r\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public"]\r\n                if "permanent" in Player.History.trackers and f"cheated_on_{C.tag}_with_{other_C.tag}_date" in Player.History.trackers["permanent"]:\r\n                   del Player.History.trackers["permanent"][f"cheated_on_{C.tag}_with_{other_C.tag}_date"]\r\n                if "permanent" in Player.History.trackers and f"cheated_on_{C.tag}_with_{other_C.tag}_relationship" in Player.History.trackers["permanent"]:\r\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_relationship"]\r\n        return\r\n\r\n\g<tabs>def unique(original:'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

utilities()

#=============  ./interfaces/Player_menu.rpy =========
def player_menu():
    fn="./interfaces/Player_menu.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #turns text cash number into textbutton
    patt=r'    text "\$\[Player\.cash\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        size (?P<size>[0-9]+)'
    repl=r'    textbutton "{size=\g<size>}" + "$[Player.cash]" \g<pos>:\r\n        action SetVariable("Player.cash", int(Player.cash) + int(50000))'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #turns text for ability points into text button
    patt=r'    text "\[Player.skill_points\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+        size (?P<size>[0-9]+)'
    repl=r'    textbutton "{size=\g<size>}{font=\g<font>}" + "[Player.skill_points]" \g<pos>:\n        action Function(Player.History.update, "bought_skill_point")' 
    fc = re.sub(patt, repl, fc, flags=re.M)

    #allows for draggable player xp bar
    patt=r'value \(Player\.XP - Player\.XP_goal \/ 1\.75\) range \(Player\.XP_goal - Player\.XP_goal \/ 1\.75\)'
    repl=r'value FieldValue(Player, "XP", Player.XP_goal) range (Player.XP_goal)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #allows for draggable player xp bar for level 1
    patt=r'value Player\.XP range Player\.XP_goal'
    repl=r'value FieldValue(Player, "XP", Player.XP_goal) range (Player.XP_goal)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #turns text for both love and trust into textbuttons
    patt=r'(?P<tabs1> +)text "\[relationships_Entry\.(?P<lt>love|trust)\]"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0\.[0-9]+, 0\.[0-9]+\)):[ \r\n]+font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+size (?P<size>[0-9]+)[ \r\n]+color "[a-z0-9#]+"'
    repl=r'\g<tabs1>textbutton "{size=\g<size>}{font=\g<font>}" + "[relationships_Entry.\g<lt>]"\g<pos>:\r\n\g<tabs1>    action SetField(relationships_Entry, "\g<lt>", relationships_Entry.\g<lt> + 100)'
    fc = re.sub(patt, repl, fc, flags=re.M)
   
    #turn emotion icons into buttons to turn off said status
    #patt='(?P<tabs1> +)add (?P<f>f?)"images/interfaces/Player_menu/relationships_(?P<status>mad|horny|nympho|\[status\])\.webp" zoom high_resolution_interface_adjustment'
    #repl='\g<tabs1>imagebutton idle \g<f>"images/interfaces/Player_menu/relationships_\g<status>.webp" action SetDict(relationships_Entry.status, \g<f>"\g<status>", 0)'
    #repl='\g<tabs1>imagebutton idle \g<f>"images/interfaces/Player_menu/relationships_\g<status>.webp":\r\n\g<tabs1>    at transform:\r\n\g<tabs1>        zoom high_resolution_interface_adjustment\r\n\g<tabs1>    action SetDict(relationships_Entry.status, \g<f>"\g<status>", 0)'
    #fc = re.sub(patt, repl, fc, flags=re.M)

    #setting the relationships_status() function to insert the text as a text button to turn off mood statuses
    patt=r'(?P<t1> +)text "\[status.upper\(\)\]" anchor \(0\.5, 0\.5\) pos \(0\.5, 0\.85\):[\r\n]+(?P<t2> +)size properties\.get\("text_size", 16\)(?P<br>[\r\n ]+)color properties\.get\("text_color", "#000000"\)'
    repl=r'\g<t1>textbutton "{size=[properties.get(\\"text_size\\", 16)]}{color=[properties.get(\\"text_color\\", \\"#000000\\")]}" + "[status.upper()]" anchor (0.5, 0.5) pos (0.5, 0.85):\r\n\g<t2>action SetDict(properties.get("char")._status, status, 0)'
    fc = re.sub(patt, repl, fc, flags=re.M)
    
    #adding the character into the relationships_status() call
    patt=r'(?P<t1> {2,})use relationships_status\([\r\n]+(?P<t2> {2,})(?P<status>[a-zA-Z"]+),[\r\n]+'
    repl=r'\g<t1>use relationships_status(\r\n\g<t2>\g<status>,\r\n\g<t2>char = relationships_Entry,\r\n'
    fc = re.sub(patt, repl, fc, flags=re.M)


    #adding button that allows for removal of cheating
    #        text "RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (0.495, 0.297):
    patt=r'        text "RELATIONSHIP STATUS" anchor \(0\.0, 0\.5\) pos \((?P<posX>[0-9.]+), (?P<posY>[0-9.]+)\):[\r\n]+            font "agency_fb\.ttf"[\r\n]+[\r\n]+            size 28'
    repl=r'        textbutton "{size=28}{font=agency_fb.ttf} RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (\g<posX>, \g<posY>):\r\n            action Function(removeCheating, relationships_Entry)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #friendship is the best thing ever! (allows for clicking on friendship to increase it by 50)
    patt=r'(?P<tabs> +)add "images\/interfaces\/full\/photos\/\[C\]\.webp" align (?P<algn>\([0-9., ]+\)) zoom (?P<zoom>0\.[0-9]+)'
    repl=r'\g<tabs>imagebutton idle f"images/interfaces/full/photos/{C}.webp" align \g<algn>:\r\n\g<tabs>    at transform:\r\n\g<tabs>        zoom 0.13\r\n\g<tabs>    action SetDict(relationships_Entry.friendship, f"{C}", relationships_Entry.friendship[C] + 50)'
    fc = re.sub(patt, repl, fc, flags=re.M)


    #Points will add "studied" or "trained" to player history
    patt=r'    text "Points" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+        size (?P<size>[0-9]+)'
    repl=r'    textbutton "{size=\g<size>}" + "Points" \g<pos>:\r\n        action Function(Player.History.update, "trained" if skills_leaderboard_type == "combat" else "studied")'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

player_menu()


#=============  ./interfaces/sex.rpy =========
def sex():
    fn="./interfaces/sex.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #sets text stamina into textbutton
    patt=r'        text "\[Player.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    repl=r'        textbutton "{size=\g<size>}" + "[Player.stamina]" \g<pos>:\n            action SetVariable("Player.stamina", Player.max_stamina + Player.stamina)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #as of v0.6b, the love interest has no stamina stat
    #patt='        text "\[Character.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
    #repl='        textbutton "{size=\g<size>}" + "[Character.stamina]" \g<pos>:\n            action SetVariable("focused_Character.stamina", focused_Character.max_stamina + Character.stamina)'
    #fc = re.sub(patt, repl, fc, flags=re.M)

    #sets player desire values into field values, aka, interactable sliding bars
    patt=r'value Player.desire'
    repl=r'value FieldValue(Player, "desire", range=1.0, step=0.1)'
    fc = re.sub(patt, repl, fc, flags=re.M)

    #character desire was redesigned in 0.6b. The bar was split into 2. One at below 1.0 and one at and above 1.0
    patt=r'value Character.desire range 1.0'
    repl=r'value DictValue(Character.desires, "orgasm", range=1.0, step=0.1)'
    fc = re.sub(patt, repl, fc, flags=re.M)
    
    patt=r'value Character\.desires\["orgasm"\] range 1\.0'
    repl=r'value DictValue(Character.desires, "orgasm", range=1.0, step=0.1)'
    fc = re.sub(patt, repl, fc, flags=re.M)


    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

sex()

#=========== ./core/mechanics/approval.rpy
def approval():
    fn="./core/mechanics/approval.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    ##breaks approval limit
    patt=r'max_stat = max_stats\[season - 1\] if persistent\.stat_caps else 1000'
    repl=r'max_stat = max_stats[season - 1] if persistent.stat_caps else 99999'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

approval()


##=========== allowing sex in public. Props to RonChon. 2 Checks in place to prevent this.
## Did I do this because darkstel couldn't get over himself? Yep. Is it a bit immature? Yep. Do I feel ashamed? Nope. If you don't want code to change, don't poke a programmer.
##=========== ./scripts/sex/request.rpy
#=========== ./core/mechanics/sex/request.rpy
def allowPublicSex():
    fn="./core/mechanics/sex/request.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #skips bedroom check for place to have sex
    patt=r'\(Player\.location not in Bedrooms and "bg_shower" not in Player\.location\) or Present - \{Character\}'
    repl=r'False'
    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")


    fn="./interfaces/interactions.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    #skips bedroom checks and number of people checks for place to have sex GUI
    patt=r'if check_approval\(Character, threshold = "hookup"\) and len\(Present\) == 1 and Player.location in \{Character.home, Player.home\} and not get_Present\(location = Player.location.replace\("_", "_shower_"\)\)\[0\]'
    repl=r'if check_approval(Character, threshold = "hookup") and len(Present) >= 1'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")

allowPublicSex()

#=========== ./core/mechanics/clothing.rpy
def allowWearCum():
#./core/mechanics/clothing.rpy
  fn='./core/mechanics/clothing.rpy'
  with open(fn, "r") as file:
      fc = file.read()

  # will leave cum on if wore cum 10 or more times
  patt=r'if spunk:'
  repl=r'if C.History.check("wear_cum") < 10 and spunk:'

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


allowWearCum()


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

    fn="./interfaces/phone.rpy"
    with open(fn, "r") as file:
        fc = file.read()

    patt=r'(?P<t1> +)text "\[Player\.achievement_points\]"(?P<anchor> anchor \([0-9,. ]+\))(?P<pos> pos \([0-9,. ]+\)):[\r\n]+(?P<t2> +)size (?P<size>[0-9]+)[\r\n ]+color "(?P<color>#[0-9A-Fa-f]+)"'
    repl=r'\g<t1>textbutton "{size=\g<size>}{color=\g<color>}" + "[Player.achievement_points]"\g<anchor>\g<pos>:\r\n\g<t2>action SetVariable("Player.achievePoints", int(Player.achievePoints) + int(500))'

    fc = re.sub(patt, repl, fc, flags=re.M)

    with open(fn, "w") as file:
        file.write(fc)

    print(f"{fn} patched")



achievementPoints()



print(f"    Success! Cheats are now enabled!")
