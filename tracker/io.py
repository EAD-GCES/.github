import csv
import os

import humanize

from tracker.utils import get_local_timestamp

from .repo import get_repo_by_full_name
from .students import STUDENTS_LIST

# Initialize the field header.
field_header = {
    'roll': 'Roll',
    'name': 'Student Name',
    'repo_url': 'URL',
    'repo_created_at': 'Start',
    'repo_pushed_at': 'Last Update',
    'repo_commit_count': 'Commits',
    'repo_description': 'Description',
}


def _write_to_csv():
    ''' Writes the data to a csv file '''
    with open('student_data.csv', 'w') as csv_p:

        write = csv.writer(csv_p)
        write.writerow(field_header.values())

        for student in STUDENTS_LIST:
            repo = get_repo_by_full_name(student['name'])
            if repo:
                write.writerow([
                    student['roll'],
                    student['name'],
                    repo['repo_name'],
                    repo['repo_url'],
                    repo['repo_language'],
                    humanize.naturalday(repo['repo_created_at']),
                    humanize.naturalday(repo['repo_pushed_at']),
                    repo['repo_stargazers_count'],
                    repo['repo_watchers_count'],
                    repo['repo_forks_count'],
                    repo['repo_description'],
                ])
            else:
                write.writerow([
                    student['roll'],
                    student['name'],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                ])

        csv_p.flush()
        csv_p.close()


def get_md_string(include_updated_at=True,
                  include_unreported=True,
                  include_action_badge=True):
    ''' Returns a string of markdown formatted data '''

    md_string = ''

    if include_updated_at:
        updated_at = get_local_timestamp()
        md_string += '# Student Data\n\nLast updated at: {}\n\n'.format(
            updated_at)
    else:
        md_string += '# Student Data\n\n'

    if include_action_badge:
        md_string += '[![Student Report Cron](https://github.com/EAD-GCES/.github/actions/workflows/cron.yml/badge.svg)](https://github.com/EAD-GCES/.github/actions/workflows/cron.yml)'
        md_string += '\n\n'

    md_string += ' | '
    for f_header in field_header.values():
        md_string += f_header + ' | '

    md_string += '\n |'
    for _ in range(len(field_header)):
        md_string += ' --- |'

    md_string += '\n'
    # Keep the track of students with no repo.
    unreported_students = []
    for student in STUDENTS_LIST:
        repo = get_repo_by_full_name(student['name'])
        md_string += ' | '
        if repo:
            for f_header in field_header.keys():
                if f_header == 'roll':
                    md_string += student[f_header] + ' | '
                elif f_header == 'repo_url':
                    md_string += f'[Link]({repo[f_header]}) | '
                else:
                    md_string += f'{repo.get(f_header)} | '
            md_string += '\n'
        else:
            unreported_students.append(student['name'])
            for f_header in field_header.keys():
                if f_header in ('roll', 'name'):
                    md_string += student[f_header] + ' | '
                else:
                    md_string += ' | '
            md_string += '\n'

    if include_unreported:
        if len(unreported_students) > 0:
            md_string += '\n## Unreported Students\n\n'
            for student in unreported_students:
                md_string += f'* {student}\n'
            md_string += '\n'

    return md_string


def _write_to_md(md_string):
    ''' Writes the markdown string to a file '''
    # Create a directory named profile.
    os.makedirs('profile', exist_ok=True)

    with open('profile/README.md', 'w') as md_p:
        md_p.write(md_string)
        md_p.flush()
        md_p.close()


def write_to_md():
    ''' Writes the data to a markdown file '''
    md_string = get_md_string()
    _write_to_md(md_string)
