import pytest

from input.git_cli import GitCliInput

# TODO: Use test parametrization and move large inputs to a test_resources directory.


def test_empty_string():
    with pytest.raises(TypeError):
        GitCliInput._parse_git_show('')


def test_invalid_string():
    with pytest.raises(TypeError):
        GitCliInput._parse_git_show('some string')


def test_invalid_list():
    with pytest.raises(ValueError):
        GitCliInput._parse_git_show(['a', 'b'])


def test_empty_list():
    with pytest.raises(ValueError):
        GitCliInput._parse_git_show([])


def test_missing_tree():
    with pytest.raises(KeyError):
        GitCliInput._parse_git_show([
            'sha 77de709c36b83e9ad9444eb35af417e3690236a2',
            'author_name Ricardo Amendoeira',
            'author_email ricardo.amendoeira@ist.utl.pt',
            'author_date Sun Sep 30 23:12:53 2018 +0100',
            'committer_name Ricardo Amendoeira',
            'committer_email ricardo.amendoeira@ist.utl.pt',
            'committer_date Sun Sep 30 23:12:53 2018 +0100',
            'parents 30f4a09c7f86e2aa8adeddf8870c21d812038fea',
            '',
            'Update the README file.',
        ])


def test_valid_inputs():
    GitCliInput._parse_git_show([
        'sha 77de709c36b83e9ad9444eb35af417e3690236a2',
        'tree 2cf6729e1bc27ee9173f82bcc3a86356365ef292',
        'author_name Ricardo Amendoeira',
        'author_email ricardo.amendoeira@ist.utl.pt',
        'author_date Sun Sep 30 23:12:53 2018 +0100',
        'committer_name Ricardo Amendoeira',
        'committer_email ricardo.amendoeira@ist.utl.pt',
        'committer_date Sun Sep 30 23:12:53 2018 +0100',
        'parents 30f4a09c7f86e2aa8adeddf8870c21d812038fea',
        '',
        'Update the README file.',
    ])


