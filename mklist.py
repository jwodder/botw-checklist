#!/usr/bin/env python3
from   collections import defaultdict
from   contextlib  import redirect_stdout
from   itertools   import groupby
import json
from   operator    import itemgetter

with open('checklist.json') as fp:
    data = json.load(fp)

shrines_by_region = defaultdict(list)
for shrine in data["shrines"]:
    shrines_by_region[shrine["region"]].append(shrine)
for v in shrines_by_region.values():
    v.sort(key=itemgetter("name"))

quests_by_region = defaultdict(list)
for quest in data["side_quests"]:
    quests_by_region[quest["region"]].append(quest)
for v in quests_by_region.values():
    v.sort(key=itemgetter("name"))

with open('checklist.tex', 'w') as fp, redirect_stdout(fp):
    print(r'''
\documentclass[10pt]{article}
\usepackage{amssymb}
\usepackage{enumitem}
\usepackage[margin=1in]{geometry}
\usepackage{multicol}
\usepackage{tikz}
\newcommand{\dlc}{\emph}
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
    print(r'\begin{enumerate}[label=$\square$]')
    for quest in data["main_quests"]:
        print(r'\item', quest)
    for quest in data["dlc_main_quests"]:
        print(r'\item \dlc{', quest, '}', sep='')
    print(r'\end{enumerate}')

    print(r'\columnbreak')
    print(r'\section*{Recovered Memories}')
    print(r'\begin{enumerate}[label=$\square$]')
    for i, mem in enumerate(data["memories"], start=1):
        print(r'\item ', i, '. ', mem, sep='')
    print(r'\end{enumerate}')

    print(r'\end{multicols}')

    for region in data["regions"]:
        print(r'\section*{' + region["tower"] + ' Region}')

        print(r'\begin{enumerate}[label=$\square$]')
        print(r'\item Activate', region["tower"])
        print(r'\end{enumerate}')

        if quests_by_region[region["name"]]:
            print(r'\begin{multicols}{2}')
            print(r'\subsection*{Shrines}')
        else:
            print(r'\begin{multicols}{2}[\subsection*{Shrines}]')
        print(r'\begin{enumerate}[label=$\square$\thinspace\protect\chest]')
        for shrine in shrines_by_region[region["name"]]:
            if not shrine["dlc"]:
                print(r'\item {name} \emph{{({trial})}}'.format(**shrine))
                if shrine["quest"] is not None:
                    print(r'\begin{enumerate}[label=$\square$]')
                    print(r'\item Shrine Quest:', shrine["quest"])
                    print(r'\end{enumerate}')
        print(r'\end{enumerate}')

        if quests_by_region[region["name"]]:
            print(r'\columnbreak')
            print(r'\subsection*{Side Quests}')
            print(r'\begin{enumerate}[label=$\square$]')
            for quest in quests_by_region[region["name"]]:
                print(r'\item', quest["name"])
            print(r'\end{enumerate}')

        print(r'\end{multicols}')

    print(r'\section*{Other}')
    print(r'\begin{enumerate}[label=$\square$]')
    for other in data["other"]:
        print(r'\item', other["name"])
    print(r"\item Find dogs' buried treasures:")
    print(r'\begin{enumerate}[label=$\square$]')
    for dog in data["dogs"]:
        print(r'\item', dog["location"])
    print(r'\end{enumerate}')
    print(r'\end{enumerate}')

    print(r'\newpage')
    print(r'\section*{Hyrule Compendium}')
    print(r'\begin{multicols}{2}')
    for section, entries in groupby(data["compendium"], itemgetter("section")):
        print(r'\subsection*{', section, '}', sep='')
        print(r'\begin{enumerate}[label=$\square$]')
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
        print(r'\end{enumerate}')
    print(r'\end{multicols}')

    ### regionless/DLC side quests
    ### DLC shrines

    print(r'\end{document}')
