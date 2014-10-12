import git
import re
from util import memoize


class Drift(object):

    CHANGE_ID_RE = re.compile(r'\nchange-id: ?(.{41})$', re.I)

    def __init__(self, repo_dir):
        self.repo = git.Repo(repo_dir)
        self.branch_dict = {}

    @memoize
    def change_ids(self, branch_name):
        self.branch_dict[branch_name] = {}
        return filter(lambda t: t[1],
                      map(self._extract_change_id,
                          self.repo.repo.iter_commits(branch_name)))

    @staticmethod
    def _extract_change_id(commit):
        match = Drift.CHANGE_ID_RE.search(commit.message)
        if match:
            return commit, match.group(1)
        return commit, None

    def drift(self, branch_one, branch_two):
        return len(self.change_ids(branch_one).viewkeys() -
                   self.change_ids(branch_two).viewkeys())
