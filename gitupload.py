from git import *
repo = Repo("/Users/mtrier/Development/git-python")
assert repo.bare == False

repo = Repo.init("/var/git/git-python.git", bare=True)
assert repo.bare == True