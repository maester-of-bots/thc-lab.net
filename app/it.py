from dotenv import load_dotenv
from github import Github
import os
from github3 import login

# Load in credentials
load_dotenv()
username = os.getenv('git_username')
token = os.getenv('git_token')

# Make the normal github
normal_github = Github(token)

# Make other github to get private repos
private_github = login(username, token=token)

def get_repos(type='All'):
    """ Pull user's repos, either public or all repos """

    if type == 'All':
        repos = []
        for repo in private_github.repositories():
            full_repo = normal_github.get_repo(str(repo))
            repos.append(full_repo)
    else:
        user = normal_github.get_user(username)
        repos = user.get_repos()

    return repos


def get_all_changes(repo):
    """ Get the text of every change pushed to this repo """

    all_changes = []
    # Get every commit
    commits = repo.get_commits()
    # Add them to an array
    for commit in commits:
        for file in commit.files:
            all_changes.append(file)
    return all_changes

def get_all_files(repo):
    """ Get all files from a repo """

    all_contents = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            try:
                all_contents.append(file_content)
            except Exception as e:
                print(e)
                pass

    return all_contents

def pull_github_content(all_repos):
    """ Grab all the stuff from GitHub repos that we can """
    all_public_changes = []
    all_public_files = []

    for repo in all_repos:

        all_public_changes += get_all_changes(repo)

        all_public_files = get_all_files(repo)

    return all_public_changes, all_public_files


def search_repos(keywords=None, repo_type="Public"):
    """ Main search function """

    # Set a basic default keyword
    if keywords is None:
        keywords = ["password="]

    # Get all the repos for the request
    all_repos = get_repos(repo_type)

    # Grab all the GitHub changes / files
    changes, files = pull_github_content(all_repos)

    # Announce how much we found
    print(f'Found {len(files)} files and {len(changes)} changes')

    # Empty stuff
    found_things = []
    total_checked = 0
    errors = []

    # Iterate through changes and check all text for any of the keywords
    for change in changes:
        if change.patch is not None:
            try:
                for key in keywords:
                    if key in change.patch:
                        found_things.append(change.raw_url)
                        print(f'Found {key} in {change.raw_url}')
                total_checked += 1
            except Exception as e:
                errors.append(change)
                print(e)

    # Iterate through files and check all text for any of the keywords
    for file in files:
        try:
            for key in keywords:
                if key in file.decoded_content.decode():
                    found_things.append(file.url)
                    print(f'Found {key} in {file.url}')
            total_checked += 1
        except Exception as e:
            errors.append(file)
            print(e)

    return total_checked, found_things, errors

def main():

    # Make sure the repo type was entered correctly
    repo_type = False
    while not repo_type:

        temp = input("Search (P)ublic repos or (A)ll repos?\n").capitalize()

        if temp in ['P','Public']:
            repo_type = 'Public'

        elif temp in ['A','All']:
            repo_type = 'All'

    # Get things to look up
    data = input("Please input words / phrases to look for, separated by a semicolon (;)")

    # Turn into a list
    keywords = data.split(";")

    # Search for all the things
    total_checked, found_things, errors = search_repos(keywords=keywords, repo_type=repo_type)

    # Great success
    print(f"Finished searching, I checked {total_checked} in total.  This is what I found.")

    # Dump links
    for thing in found_things:
        print(thing)

    # Great failure
    print(f"And here are there errors, there are {len(errors)} in total:")

    # Dump errors
    for thing in errors:
        print(thing)


main()
