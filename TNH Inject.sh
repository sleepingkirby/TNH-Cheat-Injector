#!/bin/bash
v='1.5'
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

  if [[ -f ./scripts/interface/main_menu.rpy.orig || -f ./scripts/interface/phone.rpy.orig ]]
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


  if [[ ! -f ./scripts/interface/main_menu.rpy || ! -f ./scripts/interface/phone.rpy ]]
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
perl -i -pe 's/config.developer = "auto"/config.developer = "auto"\n    config.console = True/' $fn

echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interface/phone.rpy (as of 0.5a, this was moved from the phone to the menu. So this is no longer needed and has been moved to Player_menu.rpy (below)
#fn='./scripts/interface/phone.rpy'
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

#=========== ./scripts/interface/Player_menu.rpy
fn='./scripts/interface/Player_menu.rpy'
cp $fn $fn.orig

#turns text cash number into textbutton
patt='    text f"\$ \{Player\.cash\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        size (?P<size>[0-9]+)'
repl='    textbutton "{size=$+{size}}" + f"\$ {Player.cash}" $+{pos}:\r\n        action SetVariable("Player.cash", Player.cash + 50000)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#turns text for ability points into text button
patt='    text f"\{Player.ability_points\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[\r\n]+        font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+        size (?P<size>[0-9]+)'
repl='    textbutton "{size=$+{size}}{font=$+{font}}" + f"{Player.ability_points}" $+{pos}:\r\n        action SetVariable("Player.ability_points", Player.ability_points + 5)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#allows for draggable player xp bar
patt='value Player.XP'
repl='value FieldValue(Player, "XP", Player.XP_goal)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#turns text for both love and trust into textbuttons
patt='(?P<tabs1> +)text f"\{current_relationships_Entry\.(?P<lt>love|trust)\}"(?P<pos> anchor \([0-9.]+, [0-9.]+\) pos \(0\.[0-9]+, 0\.[0-9]+\)):[ \r\n]+font "(?P<font>[a-zA-Z_]+\.[a-zA-Z]{3,6})"[ \r\n]+size (?P<size>[0-9]+)[ \r\n]+color "[a-z0-9#]+"'
repl='$+{tabs1}textbutton "{size=$+{size}}{font=$+{font}}" + f"{current_relationships_Entry.$+{lt}}"$+{pos}:\r\n$+{tabs1}    action SetVariable("current_relationships_Entry.$+{lt}", current_relationships_Entry.$+{lt} + 100)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#turn emotion icons into buttons to turn off said status
patt='(?P<tabs1> +)add (?P<f>f?)"images\/interface\/Player_menu\/relationships_(?P<status>mad|horny|nympho|\{status\})\.webp" zoom interface_adjustment'
repl='$+{tabs1}imagebutton idle $+{f}"images\/interface\/Player_menu\/relationships_$+{status}.webp" action SetDict(current_relationships_Entry.status, $+{f}"$+{status}", 0)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

#friendship is the best thing ever! (allows for clicking on friendship to increase it by 50)
patt='(?P<tabs> +)add f"images\/interface\/photos\/\{C\}\.webp" align (?<align>\([0-9., ]+\)) zoom (?P<zoom>0\.[0-9]+)'
repl='$+{tabs}imagebutton idle f"images\/interface\/photos\/{C}.webp" align $+{align}:\r\n$+{tabs}    at transform:\r\n$+{tabs}        zoom 0.13\r\n$+{tabs}    action SetDict(current_relationships_Entry.friendship, f"{C}", current_relationships_Entry.friendship[C] + 50)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interface/actions.rpy
fn='./scripts/interface/actions.rpy'
cp $fn $fn.orig

#sets text stamina into textbutton
patt='        text f"\{Player.stamina\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
repl='        textbutton "{size=$+{size}}" + f"{Player.stamina}" $+{pos}:\r\n            action SetVariable("Player.stamina", Player.max_stamina + Player.stamina)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

patt='        text f"\{Character.stamina\}" (?P<pos>anchor \([0-9.]+, [0-9.]+\) pos \([0-9.]+, [0-9.]+\)):[ \r\n]+            size (?P<size>[0-9]+)'
repl='        textbutton "{size=$+{size}}" + f"{Character.stamina}" $+{pos}:\n            action SetVariable("focused_Character.stamina", focused_Character.max_stamina + Character.stamina)'
perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn


#sets player and character desire values into field values, aka, interactable sliding bars
patt='value (?<cp>Player|Character).desire'
repl='value FieldValue($+{cp}, "desire", 100)'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"

#=========== ./scripts/interface/approval.rpy
fn='./scripts/mechanics/approval.rpy'
cp $fn $fn.orig

#breaks approval limit on last season/chapter
patt='[0-9]{3,},'
repl='99999,'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn

patt=', [0-9]{3,}\]'
repl=', 99999]'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"


#=========== ./scripts/interface/quick_menu.rpy 
fn='./scripts/interface/quick_menu.rpy' 
cp $fn $fn.orig

#writes into main menu that cheat is on
patt='        textbutton _\("Q.Load"\):\r\n            action QuickLoad\(\)'
repl='        textbutton _("Q.Load"):\r\n            action QuickLoad()\r\n\r\n        textbutton _("CheatV'$v'"):\r\n            action NullAction()'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"


#=========== ./scripts/interface/main_menu.rpy
fn='./scripts/interface/main_menu.rpy'
cp $fn $fn.orig

#writes into main menu that cheat is on
patt='    text f"\{config.version\}" anchor \(1.0, 0.5\) pos \(0.157, 0.96\):\r\n        size 25'
repl='    text f"{config.version}" anchor (1.0, 0.5) pos (0.157, 0.96):\r\n        size 25\r\n    frame:\r\n        xalign .5\r\n        yalign 0\r\n        text("Cheats enabled!")'

perl -0777 -i -pe 's/'"$patt"'/'"$repl"'/mg' $fn
echo -e "${BGreen}${fn} patched$NC"

IFS=$bkupIFS

echo -e "${BGreen}DONE!$NC"
exit 0
