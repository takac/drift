Drift
============

Drift small tool to list the differences between two branches that use Change
Ids to track their changes.

Installation
============

Requires python 2.7

Clone the repo

    git clone https://github.com/takac/drift
    cd drift

Setup a venv

    virtualenv .venv
    . .venv/bin/activate

Install drift

    pip install -e .

Run drift against your repo

    cd ~/git/anchor/
    drift origin/master origin/master~20

This will list the changes which are in the first argument and not in the
second. The command above will typically return around 20 changes, however
this may vary if there are merge commits in the last 20 commits.
