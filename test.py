# This is a sample Test Python script.
from pydriller import Repository, Git
import csv

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def function():
    print(Git('https://github.com/ishepard/pydriller').total_commits())
    #print(git.total_commits())                  # #commit nel repo

    for commit in Repository('https://github.com/ishepard/pydriller').traverse_commits():
        # test demo git pydriller
        print(" " + commit.hash)
        #print(commit.msg)

        print("------------")
        #print(commit.author.name)
        #print(commit.author.email)
        #print(commit.author_date)
        """
        for mod in commit.modifications:
            print(mod.filename + " is changed")

        for file in commit.modified_files:
            print(file.filename + " has changed")
        """
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    function()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/