#! /usr/bin/env python

import drift

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
    drifter = drift.Drift(".")
    print(drifter.drift("master", "master~100"))
    print_drift(drifter, "master", "master~100")
