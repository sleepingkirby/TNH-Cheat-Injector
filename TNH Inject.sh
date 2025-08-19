#!/bin/bash
v='2.1'
rpaurl='https://raw.githubusercontent.com/Shizmob/rpatool/master/rpatool'

clear

NC='\033[0m'
# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan

cols=`tput cols`
line=`printf '#%.0s' $(seq 1 $cols)`

bkupIFS=$IFS
IFS=$'\n'

echo -e $BGreen$line"\n\n"
echo -e "The Null Hypothesis Cheat Injector\n" 
echo -e "   Vesrion: ${v}"
echo -e "   by Sleepingkirby"
echo -e "   Inspired/based on RL Cheat Injector by SLDR @ F95zone.com"
echo -e $line$NC"\n\n"

curpath=`pwd`

  if [[ `basename $curpath` != "game" || `echo $curpath|grep -ic 'nullhypothesis'` -lt 1 ]]
  then
  echo -e "$BRed This script is in the wrong path. Please make sure it's in \"TheNullHypothesis<version>/game/\" folder $NC"
  exit 1
  fi

echo -e "$BGreen Checking if modification has already been done...$NC"

  if [[ -f ./scripts/interfaces/main_menu.rpy.orig || -f ./scripts/interfaces/phone.rpy.orig ]]
  then
  echo -e "${BRed}\n\nBackup files found. This probably means it was already patched. No need to further action. Exitting...$NC"
  exit 1
  fi
echo -e "$BGreen No backup's found. Safe to progress.\n$NC"
echo -e "$BGreen Checking to make sure requirements are met. \n\n$NC"

perlP=`which perl`

  if [[ $perlP == "" ]]
  then
  echo $perlP
  echo -e "$BRed Perl was not found. This script requires perl.$NC"
  exit 1
  fi


  if [[ ! -f ./scripts/interfaces/main_menu.rpy || ! -f ./scripts/interfaces/phone.rpy ]]
  then
  echo -e "${BRed}\n\nFiles to be editted not found. Is it still in the archive.rpa?\n\n$NC"
    if [[ -f ./archive.rpa && ! -f ./rpatool ]]
    then
    echo -e "$BRed Rpatool missing. Downloading$NC"
    wget $rpaurl
    chmod 755 ./rpatool
    fi
  echo -e "$BRed Extracting archive.rpa...$NC"
  ./rpatool -x ./archive.rpa
  wait
  fi


#============= config.rpy =========
fn='./scripts/base/config.rpy'
cp $fn $fn.orig
perl -i -pe 's/config.developer = "auto"/config.developer = "auto"\ndefine config.console = True/' $fn

echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interfaces/phone.rpy (as of 0.5a, this was moved from the phone to the menu. So this is no longer needed and has been moved to Player_menu.rpy (below)
#fn='./scripts/interfaces/phone.rpy'
#cp $fn $fn.orig
#
#
##turns text in phone for both love and trust into textbuttons
#perl -0777 -i -pe 's/ {2,}text f"\{current_phone_Character.(?P<lt>love|trust)\}"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0.[0-9]+, 0.[0-9]+\)):[\n\r]+        size (?P<size>[0-9]+)/    textbutton "\{size=$+{size}\}" \+ f"{current_phone_Character.$+{lt}}" $+{pos}:\r\n        action SetVariable("current_phone_Character.$+{lt}", current_phone_Character.$+{lt} + 100)/mg' $fn
#
##turn emotion icons into buttons to turn off said status
#perl -0777 -i -pe 's/ {2,}add At\("images\/interface\/phone\/humhum_status_angry\.webp", interface\)/        imagebutton idle "images\/interface\/phone\/humhum_status_angry.webp" action SetDict(current_phone_Character.status, "mad", 0)/mg' $fn
#perl -0777 -i -pe 's/ {2,}add At\("images\/interface\/phone\/humhum_status_nympho.webp", interface\)/        imagebutton:\n            idle "images\/interface\/phone\/humhum_status_nympho.webp"\n            action [\n                SetDict(current_phone_Character.status, "nympho", 0),\n                SetDict(current_phone_Character.status, "horny", 0)]/mg' $fn
#perl -0777 -i -pe 's/ {2,}add At\(f"images\/interface\/phone\/humhum_status_\{status\}.webp", interface\)/            imagebutton idle f"images\/interface\/phone\/humhum_status_{status}.webp" action SetDict(current_phone_Character.status, status, 0)/mg' $fn
#
##adding cheatV#.# to top of phone because some people keep insisting they're not using the cheat when they obviously are.
#perl -0777 -i -pe 's/add At\("images\/interface\/phone\/signal\.webp", interface\)/text "{b}Cheat V'$v'{\/b}" anchor (0.5, 0.5) pos (0.3905, 0.07)\n            add At("images\/interface\/phone\/signal.webp", interface)/mg' $fn
#
#echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/mechanics/utilities.rpy
fn='./scripts/mechanics/utilities.rpy'
cp $fn $fn.orig


# setup for removing cheating flags
patt='(?P<tabs> +)def unique\(original\):'
repl='    def removeCheating(C):\r\n        C.History.remove("cheated_on_flirting_in_public")\r\n        C.History.remove("cheated_on_date")\r\n        C.History.remove("cheated_on_relationship")\r\n        if C.History.permanent.get("cheated_on_flirting_in_public"):\r\n            del C.History.permanent["cheated_on_flirting_in_public"]\r\n        if C.History.permanent.get("cheated_on_date"):\r\n            del C.History.permanent["cheated_on_date"]\r\n        if C.History.permanent.get("cheated_on_relationship"):\r\n            del C.History.permanent["cheated_on_relationship"]\r\n\r\n        for other_C in all_Companions:\r\n            if hasattr(other_C, "tag"):\r\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public")\r\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_date")\r\n                Player.History.remove(f"cheated_on_{C.tag}_with_{other_C.tag}_relationship")\r\n                if Player.History.permanent.get(f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public"):\r\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_flirting_in_public"]\r\n                if Player.History.permanent.get(f"cheated_on_{C.tag}_with_{other_C.tag}_date"):\r\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_date"]\r\n                if Player.History.permanent.get(f"cheated_on_{C.tag}_with_{other_C.tag}_relationship"):\r\n                   del Player.History.permanent[f"cheated_on_{C.tag}_with_{other_C.tag}_relationship"]\r\n        return\r\n\r\n$+{tabs}def unique(original):'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


patt='(?P<tabs> +)def unique\(original\):'
repl='$+{tabs}def addAbilityPoints(p):\r\n        if not hasattr(Player, "ability_points"):\r\n            Player.ability_points = 0\r\n        if p > 0:\r\n            Player.ability_points += p\r\n\r\n$+{tabs}def unique(original):'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

echo -e "${BGreen}${fn} patched$NC"


#=========== ./scripts/base/player.rpy 
fn='./scripts/base/player.rpy'
cp $fn $fn.orig

patt='(?P<tabs> +)points -= all_abilities\[ability\]\["cost"\]'
repl='$+{tabs}points -= all_abilities[ability]["cost"]\r\n\r\n            if hasattr(self, "ability_points"):\r\n                points += self.ability_points'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interfaces/Player_menu.rpy
fn='./scripts/interfaces/Player_menu.rpy'
cp $fn $fn.orig

#turns text cash number into textbutton
patt='    text "\$\[Player\.cash\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        size (?P<size>[0-9]+)'
repl='    textbutton "{size=$+{size}}" + "\$[Player.cash]" $+{pos}:\r\n        action SetVariable("Player.cash", Player.cash + 50000)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#if I need to break level cap, it's here
#./scripts/mechanics/progression.rpy
#define max_level = [15, 15, 15, 20, 25, 30]

#turns text for ability points into text button
#note: as of 0.6a, ability_points was renamed to skill_points and how it works has completely changed. skill_points is NOT a variable/value, but a functional calculation of player levels
#chaning the button to call a custom function that checks to make sure ability_points exists, if not create it, then add.
#this also depends on a re-write of the function skill_points in "./scripts/base/player.rpy"
patt='    text "\[Player.skill_points\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+        size (?P<size>[0-9]+)'
repl='    textbutton "{size=$+{size}}{font=$+{font}}" + "[Player.skill_points]" $+{pos}:\r\n        action Function(addAbilityPoints, 5)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#allows for draggable player xp bar
patt='value \(Player\.XP - Player\.XP_goal\/1\.75\) range \(Player\.XP_goal - Player\.XP_goal\/1\.75\)'
repl='value FieldValue(Player, "XP", Player.XP_goal) range (Player.XP_goal)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#turns text for both love and trust into textbuttons
patt='(?P<tabs1> +)text "\[relationships_Entry\.(?P<lt>love|trust)\]"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0\.[0-9]+, 0\.[0-9]+\)):[ \r\n]+font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+size (?P<size>[0-9]+)[ \r\n]+color "[a-z0-9#]+"'
repl='$+{tabs1}textbutton "{size=$+{size}}{font=$+{font}}" + "[relationships_Entry.$+{lt}]"$+{pos}:\r\n$+{tabs1}    action SetField(relationships_Entry, "$+{lt}", relationships_Entry.$+{lt} + 100)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#turn emotion icons into buttons to turn off said status
#this was unified into a single function. Good programming on ronchon's part but might be over.
#patt='(?P<tabs1> +)add (?P<f>f?)"images\/interface\/Player_menu\/relationships_(?P<status>mad|horny|nympho|\[status\])\.webp" zoom high_resolution_interface_adjustment'
#repl='$+{tabs1}imagebutton idle $+{f}"images\/interface\/Player_menu\/relationships_$+{status}.webp":\r\n$+{tabs1}    at transform:\r\n$+{tabs1}        zoom high_resolution_interface_adjustment\r\n$+{tabs1}    action SetDict(relationships_Entry.status, $+{f}"$+{status}", 0)'
#
#perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#adapts the relationships_status() to have character as a parameter for mood changing
patt='screen relationships_status\(status, \*\*properties\):'
repl='screen relationships_status(status, c, **properties):'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#setting the relationships_status() function to insert the text as a text button to turn off mood statuses
patt='(?P<t1> +)text "\[status.upper\(\)\]" anchor \(0\.5, 0\.5\) pos \(0\.5, 0\.85\):[\r\n]+(?P<t2> +)size properties\.get\("text_size", 16\)(?P<br>[\r\n ]+)color properties\.get\("text_color", "#000000"\)'
repl='$+{t1}textbutton "{size=[properties.get(\\"text_size\\", 16)]}{color=[properties.get(\\"text_color\\", \\"#000000\\")]}" + "[status.upper()]" anchor (0.5, 0.5) pos (0.5, 0.85):\r\n$+{t2}action SetDict(c.status, status, 0)'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#adding the character into the relationships_status() call
patt='(?P<t1> {2,})use relationships_status\([\r\n]+(?P<t2> {2,})(?P<status>[a-zA-Z"]+),[\r\n]+'
repl='$+{t1}use relationships_status(\r\n$+{t2}$+{status},\r\n$+{t2}relationships_Entry,\r\n'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn



#adding button that allows for removal of cheating
#        text "RELATIONSHIP STATUS" anchor (0.0, 0.5) pos (0.495, 0.297):
patt='        text "RELATIONSHIP STATUS" anchor \(0\.0, 0\.5\) pos \((?P<posX>[0-9.]+), (?P<posY>[0-9.]+)\):[\r\n]+            font "agency_fb\.ttf"[\r\n]+[\r\n]+            size 28'
repl='        textbutton "{size=28}{font=agency_fb.ttf} RELATIONSHIP STATUS" anchor (0.0, 0.5) pos ($+{posX}, $+{posY}):\r\n            action Function(removeCheating, relationships_Entry)'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


#friendship is the best thing ever! (allows for clicking on friendship to increase it by 50)
#                        add "images/interface/full/photos/[C].webp" align (0.5, 0.5) zoom 0.13
patt='(?P<tabs> +)add "images\/interface\/full\/photos\/\[C\]\.webp" align (?P<align>\([0-9., ]+\)) zoom (?P<zoom>0\.[0-9]+)'
repl='$+{tabs}imagebutton idle f"images\/interface\/full\/photos\/{C}.webp" align $+{align}:\r\n$+{tabs}    at transform:\r\n$+{tabs}        zoom 0.13\r\n$+{tabs}    action SetDict(relationships_Entry.friendship, f"{C}", relationships_Entry.friendship[C] + 50)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interfaces/sex.rpy
fn='./scripts/interfaces/sex.rpy'
cp $fn $fn.orig

#sets text stamina into textbutton
patt='        text "\[Player.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
repl='        textbutton "{size=$+{size}}" + "[Player.stamina]" $+{pos}:\r\n            action SetVariable("Player.stamina", Player.max_stamina + Player.stamina)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


#patt='        text "\[Character.stamina\]" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
#repl='        textbutton "{size=$+{size}}" + "[Character.stamina]" $+{pos}:\n            action SetVariable("focused_Character.stamina", focused_Character.max_stamina + Character.stamina)'
#perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


#sets player desire values into field values, aka, interactable sliding bars
patt='value Player.desire range 1.0'
repl='value FieldValue(Player, "desire", range=1.0, step=0.1)'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
#value Character.desires["orgasm"] range 1.0 

#character desire was redesigned in 0.6b. The bar was split into 2. One at below 1.0 and one at and above 1.0
patt='value Character.desire range 1.0'
repl='value DictValue(Character.desires, "orgasm", range=1.0, step=0.1)'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

patt='value Character\.desires\["orgasm"\] range 1\.0'
repl='value DictValue(Character.desires, "orgasm", range=1.0, step=0.1)'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interfaces/approval.rpy
fn='./scripts/mechanics/approval.rpy'
cp $fn $fn.orig

#define max_stats = (1000, 1000, 1000, 1000)
#breaks approval limit on last season/chapter
patt='[0-9]{3,},'
repl='99999,'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

patt=', [0-9]{3,}\)'
repl=', 99999)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"


#=========== allowing sex in public. Props to RonChon. 2 Checks in place to prevent this.
# Did I do this because darkstel couldn't get over himself? Yep. Is it a bit immature? Yep. Do I feel ashamed? Nope. If you don't want code to change, don't poke a programmer.
#=========== ./scripts/sex/request.rpy
fn='./scripts/sex/request.rpy'
cp $fn $fn.orig

#skips bedroom check for place to have sex
patt='\(Player\.location not in bedrooms and "bg_shower" not in Player\.location\) or len\(Present\) > 1'
repl='False'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

echo -e "${BGreen}${fn} patched$NC"

fn='./scripts/interfaces/interactions.rpy'
cp $fn $fn.orig

#skips bedroom checks and number of people checks for place to have sex GUI
patt='if approval_check\(Character, threshold = "hookup"\) and len\(Present\) == 1 and Player.location in \[Character.home, Player.home\] and not get_Present\(location = Player.location.replace\("_", "_shower_"\)\)\[0\]'
repl='if approval_check(Character, threshold = "hookup") and len(Present) >= 1'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/mechanics/movement.rpy 
fn='./scripts/mechanics/movement.rpy'
cp $fn $fn.orig

#character won't wipe off cum when exiting bed room after wearing cum 10 times
patt='                if temp_Characters\[0\]\.spunk\[location\]'
repl='                if temp_Characters[0].History.check("wear_cum") < 10 and temp_Characters[0].spunk[location]'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interfaces/base.rpy 
fn='./scripts/interfaces/base.rpy' 
cp $fn $fn.orig

#writes into main menu that cheat is on
patt='        textbutton _\("Q.Load"\):\r\n            action QuickLoad\(\)'
repl='        textbutton _("Q.Load"):\r\n            action QuickLoad()\r\n\r\n        textbutton _("CheatV'$v'"):\r\n            action NullAction()'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"


#=========== ./scripts/interfaces/main_menu.rpy
fn='./scripts/interfaces/main_menu.rpy'
cp $fn $fn.orig

#writes into main menu that cheat is on
patt='    text "\[config.version\]" anchor \(1.0, 0.5\) pos \(0.157, 0.96\):\r\n        size 25'
repl='    text "[config.version]" anchor (1.0, 0.5) pos (0.157, 0.96):\r\n        size 25\r\n    frame:\r\n        xalign .5\r\n        yalign 0\r\n        text("Cheats enabled!")'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"

IFS=$bkupIFS

echo -e "${BGreen}DONE!$NC"
exit 0
