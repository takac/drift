#! /usr/bin/env python

import drift
import re
import datetime

def print_drift(drifter, upstream_branch, local_branch):
    print("Comparing {0} to {1}".format(
        upstream_branch, local_branch))

    in_upstream = drifter.unique_change_ids(upstream_branch)
    print("Unique change ids in {0}: {1}".format(
            upstream_branch, len(in_upstream)))

    in_local = drifter.unique_change_ids(local_branch)
    print("Unique change ids in {0}: {1}".format(
            local_branch, len(in_local)))

    change_id_diff = drifter.drift(upstream_branch, local_branch)
    print("Number of unique change ids in {0} and not in {1}: {2}"
        .format(upstream_branch, local_branch,
            change_id_diff))

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        drifter = drift.Drift(sys.argv[1])
        upstream = drifter.unique_change_ids(sys.argv[2])
        local = drifter.unique_change_ids(sys.argv[3])
        subj = re.compile('([^\n]{0,60})')
        diff = upstream.viewkeys() - local.viewkeys()
        for i in sorted(diff, key=lambda r:upstream.get(r).committed_date, reverse=True):
            commit = upstream[i]
            committed_time = datetime.datetime.fromtimestamp(commit.committed_date).strftime("%d/%m/%Y@%H:%M")
            print("{0} {1} {2} {3}".format(i, commit.hexsha, committed_time, subj.match(commit.message).group(1)))
    else:
        print("Usage: python {0} repo_dir branch_one branch_two".format(sys.argv[0]))
