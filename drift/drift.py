from collections import defaultdict
from util import memoize
import datetime
import git
import os
import re
import sys


class Drift(object):

    CHANGE_ID_RE = re.compile(r'\nchange-id:\s*(.{41})(\n|$)', re.I)

    def __init__(self, repo_dir):
        self.repo = git.Repo(repo_dir)

    @memoize
    def change_ids(self, branch_name):
        cid_dict = defaultdict(list)
        for commit in self.repo.iter_commits(branch_name):
            cid = self._extract_change_id(commit)
            if cid:
                cid_dict[cid].append(commit)
        return cid_dict

    @staticmethod
    def _extract_change_id(commit):
        match = Drift.CHANGE_ID_RE.search(commit.message)
        if match:
            return match.group(1)
        return None

    def drift(self, branch_one, branch_two):
        return len(self.change_ids(branch_one).viewkeys() -
                   self.change_ids(branch_two).viewkeys())

def main():
    if len(sys.argv) == 3:
        # Repo to analyse
        drifter = Drift(os.getcwd())
        # upstream branch name
        upstream_changes = drifter.change_ids(sys.argv[1])
        # local branch name
        local = drifter.change_ids(sys.argv[2])

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
