This repository provides a checklist of things to do, complete, & achieve in
the video game *The Legend of Zelda: Breath of the Wild*.  The checklist data
is stored as JSON in [`checklist.json`](/checklist.json) alongside additional
files for converting it to a printable PDF file.

A copy of the PDF produced from this repository can be downloaded via [the
"Releases" page](https://github.com/jwodder/botw-checklist/releases); select
the `checklist.pdf` asset under the latest release.


Building the PDF
================

Requirements:

- GNU Make
- TeX Live
- Python 3

Run `make` in a clone of this repository to produce a `checklist.pdf` file that
can then be printed and checked-off the old-fashioned way.


Conventions in the PDF Checklist
================================

- Items in *italics* (except for shrine trial names) are either DLC or acquired
  via amiibo.

- Next to the checkbox for each shrine is a treasure chest icon that is
  intended to be checked off when the player has looted all chests in the given
  shrine.

- In the "Hyrule Compendium" section, entries that are present in both normal
  mode and Master Mode have the numbers for each mode listed, with the Master
  Mode number in **bold**.  Entries that are only present in Master Mode have
  only one number listed, with both it and the entry name in **bold**.
