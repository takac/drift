import git
import re
from util import memoize
from collections import defaultdict


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
