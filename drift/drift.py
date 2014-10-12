import git
import re
from util import memoize

class Drift(object):

    CHANGE_ID_RE = re.compile(r'\nchange-id: ?(.{41})$', re.I)

    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.repo = git.Repo(repo_dir)
        self.branch_dict = {}

    @memoize
    def unique_change_ids(self, branch_name):
        self.branch_dict[branch_name] = {}
        for commit in self.repo.iter_commits(branch_name):
            match = self.CHANGE_ID_RE.search(commit.message)
            if match:
                self.branch_dict[branch_name][match.group(1)] = commit
        return self.branch_dict[branch_name]

    def drift(self, branch_one, branch_two):
        return len(self.unique_change_ids(branch_one).viewkeys() -
                self.unique_change_ids(branch_two).viewkeys())
