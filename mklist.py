#!/usr/bin/env python3
from   collections import defaultdict
from   contextlib  import redirect_stdout
from   itertools   import groupby
import json
from   operator    import itemgetter
import re

WEAPON_SPACE_START = 9
WEAPON_SPACE_MAX   = WEAPON_SPACE_START + 11
BOW_SPACE_START    = 5
BOW_SPACE_MAX      = BOW_SPACE_START + 8
SHIELD_SPACE_START = 4
SHIELD_SPACE_MAX   = SHIELD_SPACE_START + 16

with open('checklist.json') as fp:
    data = json.load(fp)

def classify(iterable, field):
    classed = defaultdict(list)
    for obj in iterable:
        classed[obj[field]].append(obj)
    return classed

shrines_by_region = classify(data["shrines"], 'region')
for v in shrines_by_region.values():
    v.sort(key=itemgetter("name"))

quests_by_region = classify(data["side_quests"], 'region')
for v in quests_by_region.values():
    v.sort(key=itemgetter("name"))

with open('checklist.tex', 'w') as fp, redirect_stdout(fp):
    print(r'''
\documentclass[10pt]{article}
\usepackage{amssymb}
\usepackage{bbding}
\usepackage{enumitem}
\usepackage[margin=1in]{geometry}
\usepackage{longtable}
\usepackage{multicol}
\usepackage{tikz}
\newcommand{\dlc}{\emph}
\newcommand{\amiibo}{\emph}
\newsavebox\ltmcbox
\raggedcolumns
\makeatletter
\newlength{\chest@width}
\setlength{\chest@width}{1em}
\newlength{\chest@height}
\setlength{\chest@height}{\dimexpr\chest@width*618/1000\relax}
\newlength{\chest@roundness}
\setlength{\chest@roundness}{\dimexpr\chest@width/5\relax}
\newlength{\chest@latchsize}
\setlength{\chest@latchsize}{\dimexpr\chest@width/5\relax}
\newlength{\chest@latchHeight}
\setlength{\chest@latchHeight}{\dimexpr\chest@height/2\relax}
\newcommand{\chest}{
    \tikz{
        \draw (0,0)
            [rounded corners=\chest@roundness]
                -- (0, \chest@height)
                -- (\chest@width, \chest@height)
            [sharp corners]
                -- (\chest@width, 0)
                -- (0,0);
        \node (latch) at (\dimexpr\chest@width/2, \chest@latchHeight)
            [circle,minimum width=\chest@latchsize,inner sep=0,draw] {};
        \draw (           0, \chest@latchHeight) -- (latch.west);
        \draw (\chest@width, \chest@latchHeight) -- (latch.east);
    }
}
\makeatother
\begin{document}
''')

    print(r'\begin{multicols}{2}')

    print(r'\section*{Main Quests}')
    print(r'\begin{itemize}[label=$\square$]')
    for quest in data["main_quests"]:
        print(r'\item', quest)
    for quest in data["dlc_main_quests"]:
        print(r'\item \dlc{', quest, '}', sep='')
    print(r'\end{itemize}')

    print(r'\columnbreak')
    print(r'\section*{Recovered Memories}')
    print(r'\begin{itemize}[label=$\square$]')
    for i, mem in enumerate(data["memories"], start=1):
        print(r'\item ', i, '. ', mem, sep='')
    print(r'\end{itemize}')

    print(r'\end{multicols}')

    for region in data["regions"]:
        print(r'\section*{' + region["tower"] + ' Region}')

        print(r'\begin{itemize}[label=$\square$]')
        print(r'\item Activate', region["tower"])
        print(r'\end{itemize}')

        if quests_by_region[region["name"]]:
            print(r'\begin{multicols}{2}')
            print(r'\subsection*{Shrines}')
        else:
            print(r'\begin{multicols}{2}[\subsection*{Shrines}]')
        print(r'\begin{itemize}[label=$\square$\thinspace\protect\chest]')
        for shrine in shrines_by_region[region["name"]]:
            if not shrine["dlc"]:
                print(r'\item {name} \emph{{({trial})}}'.format(**shrine))
                if shrine["quest"] is not None:
                    print(r'\begin{itemize}[label=$\square$]')
                    print(r'\item Shrine Quest:', shrine["quest"])
                    print(r'\end{itemize}')
        print(r'\end{itemize}')

        if quests_by_region[region["name"]]:
            print(r'\columnbreak')
            print(r'\subsection*{Side Quests}')
            print(r'\begin{itemize}[label=$\square$]')
            for quest in quests_by_region[region["name"]]:
                print(r'\item', quest["name"])
            print(r'\end{itemize}')

        print(r'\end{multicols}')

    assert all((quest["region"] is None) == quest.get("dlc", False)
               for quest in data["side_quests"])
    print(r'\section*{DLC Side Quests}')
    print(r'\begin{itemize}[label=$\square$]')
    for quest in quests_by_region[None]:
        print(r'\item \dlc{', quest["name"], '}', sep='')
    print(r'\end{itemize}')

    print(r'\newpage')
    print(r'\begin{multicols}{2}[\section*{Enhance Armor}]')
    # <https://tex.stackexchange.com/a/46001/7280>
    print(r'\setbox\ltmcbox\vbox{\makeatletter\col@number\@ne')
    print(r'\begin{longtable}{r|ccccc}')
    boxes = r' & $\square$' + r' & \FiveStarOpen' * 4 + r'\\'
    armor_sets = classify(data["enhanceable_armor"], 'set')
    ### TODO: Sort by headgear name instead of set name:
    for aset in sorted(k for k in armor_sets.keys() if k is not None):
        chest,head,legs = sorted(armor_sets[aset], key=itemgetter("body_part"))
        if chest["amiibo"]:
            pre, post = r'\amiibo{', '}'
        else:
            pre, post = '', ''
        print(pre, head["name"], post, boxes, sep='')
        print(pre, chest["name"], post, boxes, sep='')
        print(pre, legs["name"], post, boxes, sep='')
        print(r'\hline')
    for armor in sorted(armor_sets[None], key=itemgetter("name")):
        if armor["amiibo"]:
            print(r'\amiibo{', armor["name"], '}', boxes, sep='')
        else:
            print(armor["name"], boxes, sep='')
    print(r'\end{longtable}')
    print(r'\unskip\unpenalty\unpenalty}\unvbox\ltmcbox')
    print(r'\end{multicols}')

    max_spaces = max(WEAPON_SPACE_MAX, BOW_SPACE_MAX, SHIELD_SPACE_MAX)
    print(r'\section*{Expand Inventory}')
    print(r'\begin{tabular}{r|', r'@{\enskip}'.join('c' * max_spaces), '}',
          sep='')
    for i in range(1, max_spaces+1):
        print('&', i, end='')
    print(r'\\ \hline')
    for label, start, maxxed in [
        ('Weapons', WEAPON_SPACE_START, WEAPON_SPACE_MAX),
        ('Bows', BOW_SPACE_START, BOW_SPACE_MAX),
        ('Shields', SHIELD_SPACE_START, SHIELD_SPACE_MAX),
    ]:
        print(label, '& --' * start, r'& $\square$' * (maxxed - start),
              '& ' * (max_spaces - maxxed), r'\\')
    print(r'\end{tabular}')

    print(r'\section*{Overworld Mini-bosses}')
    for sg, pl, key, species in [
        ('Hinox', 'Hinoxes', 'hinoxes', 'Hinox'),
        ('Talus', 'Taluses', 'taluses', 'Stone Talus'),
        ('Molduga', 'Moldugas', 'moldugas', 'Molduga'),
    ]:
        print(r'\subsection*{', pl, '}', sep='')
        print(r'\begin{itemize}[label=$\square$]')
        for boss in data[key]:  ### TODO: Sort
            print(r'\item', boss["region"], '---', boss["display_location"])
            if boss["species"] != species:
                m = re.fullmatch(
                    r'{} \((.+)\)'.format(re.escape(species)),
                    boss["species"],
                )
                if m:
                    print('(', m.group(1), ')', sep='')
                else:
                    print('(', boss["species"], ')', sep='')
        print(r'\item Get Medal of Honor:', sg, 'from Kilton')
        print(r'\end{itemize}')

    print(r'\section*{Other}')
    print(r'\begin{itemize}[label=$\square$]')
    for other in data["other"]:
        print(r'\item', other["name"])
    print(r"\item Find dogs' buried treasures:")
    print(r'\begin{itemize}[label=$\square$]')
    for dog in data["dogs"]:
        print(r'\item', dog["location"])
        if dog.get("item_qty"):
            print(r'({item} $\times {item_qty}$)'.format_map(dog))
        else:
            print(r'({item})'.format_map(dog))
    print(r'\end{itemize}')
    print(r'\end{itemize}')

    print(r'\newpage')
    print(r'\section*{Hyrule Compendium}')
    print(r'\begin{multicols}{2}')
    for section, entries in groupby(data["compendium"], itemgetter("section")):
        print(r'\subsection*{', section, '}', sep='')
        print(r'\begin{itemize}[label=$\square$]')
        for e in entries:
            number = e["dlc_number"]
            master = e["dlc_master_number"]
            name   = e["name"]
            if number is None:
                number = '---'
                name = r'\textbf{' + e["name"] + '}'
            else:
                number = str(number).rjust(3, '~')
                if e["number"] is None:
                    name = r'\dlc{' + e["name"] + '}'
            print(r'\item ', number, r'/\textbf{', master, '}. ', name, sep='')
        print(r'\end{itemize}')
    print(r'\end{multicols}')

    ### TODO: DLC shrines

    print(r'\end{document}')
