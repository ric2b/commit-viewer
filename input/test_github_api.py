import pytest

from common.commit import Commit, Person
from input.github_api import GitHubInput

# TODO: Use test parametrization and move large inputs to a test_resources directory.


def test_string():
    with pytest.raises(TypeError):
        GitHubInput._parse_page_content('some string')


def test_dict():
    with pytest.raises(TypeError):
        GitHubInput._parse_page_content({})


def test_invalid_list():
    with pytest.raises(TypeError):
        GitHubInput._parse_page_content([1, 2, 3])


def test_empty_list():
    assert {} == GitHubInput._parse_page_content([])


def test_missing_tree():
    with pytest.raises(ValueError):
        GitHubInput._parse_page_content([
            {
                "sha": "fe3d33854a9e46771161fea08f8cce4b5f62c733",
                "node_id": "MDY6Q29tbWl0MTA2MzEwOmZlM2QzMzg1NGE5ZTQ2NzcxMTYxZmVhMDhmOGNjZTRiNWY2MmM3MzM=",
                "commit": {
                    "author": {
                        "name": "David Saff",
                        "email": "saff@google.com",
                        "date": "2012-04-23T18:42:54Z"
                    },
                    "committer": {
                        "name": "David Saff",
                        "email": "saff@google.com",
                        "date": "2012-04-23T18:42:54Z"
                    },
                    "message": "Merge pull request #421 from marcphilipp/fix-mvn-artifacts\n\nRelocate Maven artifact \"junit-dep\" to \"junit\"",
                    "url": "https://api.github.com/repos/junit-team/junit4/git/commits/fe3d33854a9e46771161fea08f8cce4b5f62c733",
                    "comment_count": 0,
                    "verification": {
                        "verified": False,
                        "reason": "unsigned",
                        "signature": None,
                        "payload": None
                    }
                },
                "url": "https://api.github.com/repos/junit-team/junit4/commits/fe3d33854a9e46771161fea08f8cce4b5f62c733",
                "html_url": "https://github.com/junit-team/junit4/commit/fe3d33854a9e46771161fea08f8cce4b5f62c733",
                "comments_url": "https://api.github.com/repos/junit-team/junit4/commits/fe3d33854a9e46771161fea08f8cce4b5f62c733/comments",
                "author": {
                    "login": "dsaff",
                    "id": 46155,
                    "node_id": "MDQ6VXNlcjQ2MTU1",
                    "avatar_url": "https://avatars2.githubusercontent.com/u/46155?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/dsaff",
                    "html_url": "https://github.com/dsaff",
                    "followers_url": "https://api.github.com/users/dsaff/followers",
                    "following_url": "https://api.github.com/users/dsaff/following{/other_user}",
                    "gists_url": "https://api.github.com/users/dsaff/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/dsaff/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/dsaff/subscriptions",
                    "organizations_url": "https://api.github.com/users/dsaff/orgs",
                    "repos_url": "https://api.github.com/users/dsaff/repos",
                    "events_url": "https://api.github.com/users/dsaff/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/dsaff/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "committer": {
                    "login": "dsaff",
                    "id": 46155,
                    "node_id": "MDQ6VXNlcjQ2MTU1",
                    "avatar_url": "https://avatars2.githubusercontent.com/u/46155?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/dsaff",
                    "html_url": "https://github.com/dsaff",
                    "followers_url": "https://api.github.com/users/dsaff/followers",
                    "following_url": "https://api.github.com/users/dsaff/following{/other_user}",
                    "gists_url": "https://api.github.com/users/dsaff/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/dsaff/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/dsaff/subscriptions",
                    "organizations_url": "https://api.github.com/users/dsaff/orgs",
                    "repos_url": "https://api.github.com/users/dsaff/repos",
                    "events_url": "https://api.github.com/users/dsaff/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/dsaff/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "parents": [
                    {
                        "sha": "7439e56cc7c2261d231ec46e048c7ac762e7a8cc",
                        "url": "https://api.github.com/repos/junit-team/junit4/commits/7439e56cc7c2261d231ec46e048c7ac762e7a8cc",
                        "html_url": "https://github.com/junit-team/junit4/commit/7439e56cc7c2261d231ec46e048c7ac762e7a8cc"
                    },
                    {
                        "sha": "834dcd7b89a57436c7aa2cb68dbc041fa03a89e1",
                        "url": "https://api.github.com/repos/junit-team/junit4/commits/834dcd7b89a57436c7aa2cb68dbc041fa03a89e1",
                        "html_url": "https://github.com/junit-team/junit4/commit/834dcd7b89a57436c7aa2cb68dbc041fa03a89e1"
                    }
                ]
            },
        ])


def test_valid_inputs():
    assert {
        'fe3d3385': Commit(
            sha="fe3d33854a9e46771161fea08f8cce4b5f62c733",
            tree="b015567d2c4a3ba176159b5c96f9ec2b1a890a56",
            author=Person(
                name="David Saff",
                email="saff@google.com",
                date="2012-04-23T18:42:54Z",
            ),
            committer=Person(
                name="David Saff",
                email="saff@google.com",
                date="2012-04-23T18:42:54Z",
            ),
            message="Merge pull request #421 from marcphilipp/fix-mvn-artifacts\n\nRelocate Maven artifact \"junit-dep\" to \"junit\"",
            parents=["7439e56cc7c2261d231ec46e048c7ac762e7a8cc", "834dcd7b89a57436c7aa2cb68dbc041fa03a89e1"]
        ),
    } == GitHubInput._parse_page_content([
        {
            "sha": "fe3d33854a9e46771161fea08f8cce4b5f62c733",
            "node_id": "MDY6Q29tbWl0MTA2MzEwOmZlM2QzMzg1NGE5ZTQ2NzcxMTYxZmVhMDhmOGNjZTRiNWY2MmM3MzM=",
            "commit": {
                "author": {
                    "name": "David Saff",
                    "email": "saff@google.com",
                    "date": "2012-04-23T18:42:54Z"
                },
                "committer": {
                    "name": "David Saff",
                    "email": "saff@google.com",
                    "date": "2012-04-23T18:42:54Z"
                },
                "message": "Merge pull request #421 from marcphilipp/fix-mvn-artifacts\n\nRelocate Maven artifact \"junit-dep\" to \"junit\"",
                "tree": {
                    "sha": "b015567d2c4a3ba176159b5c96f9ec2b1a890a56",
                    "url": "https://api.github.com/repos/junit-team/junit4/git/trees/b015567d2c4a3ba176159b5c96f9ec2b1a890a56"
                },
                "url": "https://api.github.com/repos/junit-team/junit4/git/commits/fe3d33854a9e46771161fea08f8cce4b5f62c733",
                "comment_count": 0,
                "verification": {
                    "verified": False,
                    "reason": "unsigned",
                    "signature": None,
                    "payload": None
                }
            },
            "url": "https://api.github.com/repos/junit-team/junit4/commits/fe3d33854a9e46771161fea08f8cce4b5f62c733",
            "html_url": "https://github.com/junit-team/junit4/commit/fe3d33854a9e46771161fea08f8cce4b5f62c733",
            "comments_url": "https://api.github.com/repos/junit-team/junit4/commits/fe3d33854a9e46771161fea08f8cce4b5f62c733/comments",
            "author": {
                "login": "dsaff",
                "id": 46155,
                "node_id": "MDQ6VXNlcjQ2MTU1",
                "avatar_url": "https://avatars2.githubusercontent.com/u/46155?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/dsaff",
                "html_url": "https://github.com/dsaff",
                "followers_url": "https://api.github.com/users/dsaff/followers",
                "following_url": "https://api.github.com/users/dsaff/following{/other_user}",
                "gists_url": "https://api.github.com/users/dsaff/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/dsaff/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/dsaff/subscriptions",
                "organizations_url": "https://api.github.com/users/dsaff/orgs",
                "repos_url": "https://api.github.com/users/dsaff/repos",
                "events_url": "https://api.github.com/users/dsaff/events{/privacy}",
                "received_events_url": "https://api.github.com/users/dsaff/received_events",
                "type": "User",
                "site_admin": False
            },
            "committer": {
                "login": "dsaff",
                "id": 46155,
                "node_id": "MDQ6VXNlcjQ2MTU1",
                "avatar_url": "https://avatars2.githubusercontent.com/u/46155?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/dsaff",
                "html_url": "https://github.com/dsaff",
                "followers_url": "https://api.github.com/users/dsaff/followers",
                "following_url": "https://api.github.com/users/dsaff/following{/other_user}",
                "gists_url": "https://api.github.com/users/dsaff/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/dsaff/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/dsaff/subscriptions",
                "organizations_url": "https://api.github.com/users/dsaff/orgs",
                "repos_url": "https://api.github.com/users/dsaff/repos",
                "events_url": "https://api.github.com/users/dsaff/events{/privacy}",
                "received_events_url": "https://api.github.com/users/dsaff/received_events",
                "type": "User",
                "site_admin": False
            },
            "parents": [
                {
                    "sha": "7439e56cc7c2261d231ec46e048c7ac762e7a8cc",
                    "url": "https://api.github.com/repos/junit-team/junit4/commits/7439e56cc7c2261d231ec46e048c7ac762e7a8cc",
                    "html_url": "https://github.com/junit-team/junit4/commit/7439e56cc7c2261d231ec46e048c7ac762e7a8cc"
                },
                {
                    "sha": "834dcd7b89a57436c7aa2cb68dbc041fa03a89e1",
                    "url": "https://api.github.com/repos/junit-team/junit4/commits/834dcd7b89a57436c7aa2cb68dbc041fa03a89e1",
                    "html_url": "https://github.com/junit-team/junit4/commit/834dcd7b89a57436c7aa2cb68dbc041fa03a89e1"
                }
            ]
        },
    ])


