#! /usr/bin/env python

import drift
import re
import datetime
import sys


if __name__ == '__main__':
    if len(sys.argv) == 4:
        # Repo to analyse
        drifter = drift.Drift(sys.argv[1])
        # upstream branch name
        upstream_changes = drifter.change_ids(sys.argv[2])
        # local branch name
        local = drifter.change_ids(sys.argv[3])

        subj = re.compile('([^\n]{0,60})')
        diff = upstream_changes.viewkeys() - local.viewkeys()
        # Sort changes from youngest to oldest commit date
        sorted_commits = sorted(
            diff, key=lambda r: upstream_changes.get(r)[0].committed_date,
            reverse=True)
        for i in sorted_commits:
            commit_list = upstream_changes[i]
            commit = commit_list[0]
            committed_time = datetime.datetime.fromtimestamp(
                commit.committed_date).strftime("%d/%m/%Y@%H:%M")
            print("{0} {1} {2} {3}".format(
                i, commit.hexsha, committed_time,
                subj.match(commit.message).group(1)))
    else:
        print("Usage: python {0} repo_dir "
              "branch_one branch_two".format(sys.argv[0]))
