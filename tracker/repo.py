import os
import re
from collections import OrderedDict
from functools import lru_cache

from github import Github

from tracker.utils import get_local_timestamp


GH_API_KEY = os.environ.get('GH_API_KEY')
github = Github(GH_API_KEY)

# Get the organization by name.
organization = github.get_organization('EAD-GCES')

# Get repo of organizations
repos = organization.get_repos()


@lru_cache  # Recently used entries are most likely to be reused, so cache them.
def get_all_repos():
    ''' Returns a dict of all repos '''

    extracted_repos = OrderedDict()

    # Get all the repos
    for repo in repos:

        repo_data = {}
        # Get the repo name
        repo_name = repo.name
        repo_data['repo_name'] = repo_name

        # Person Name is the first index of repo name split by '_'.
        _person_name = repo_name.split('-')[0]
        # Insert space before capital letters.
        re_outer = re.compile(r'([^A-Z ])([A-Z])')
        re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
        person_name = re_outer.sub(r'\1 \2',
                                   re_inner.sub(r' \1\2', _person_name))

        # Get the person name
        repo_data['name'] = person_name

        # Get the repo description
        repo_description = repo.description
        repo_data['repo_description'] = repo_description

        # Get the repo url
        repo_url = repo.html_url
        repo_data['repo_url'] = repo_url

        # Get the repo language
        repo_language = repo.language
        repo_data['repo_language'] = repo_language

        # Get the repo created at
        repo_created_at = repo.created_at
        repo_data['repo_created_at'] = get_local_timestamp(
            timestamp=repo_created_at)

        # Get the repo pushed at
        repo_pushed_at = repo.pushed_at
        repo_data['repo_pushed_at'] = get_local_timestamp(repo_pushed_at)

        # Get the repo size
        repo_size = repo.size
        repo_data['repo_size'] = repo_size

        # Get the repo stargazers_count
        repo_stargazers_count = repo.stargazers_count
        repo_data['repo_stargazers_count'] = repo_stargazers_count

        # Get the repo watchers_count
        repo_watchers_count = repo.watchers_count
        repo_data['repo_watchers_count'] = repo_watchers_count

        # Get the repo forks_count
        repo_forks_count = repo.forks_count
        repo_data['repo_forks_count'] = repo_forks_count

        # Get the total commit count
        repo_commit_count = repo.get_commits().totalCount
        repo_data['repo_commit_count'] = repo_commit_count

        # Merge into users
        extracted_repos[person_name] = repo_data

    return extracted_repos


def get_repo_by_full_name(full_name: str):
    ''' Returns a dict of repo by full name '''

    all_repos = get_all_repos()
    return all_repos.get(full_name, None)
