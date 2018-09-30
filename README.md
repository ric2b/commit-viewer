# Commit viewer

This program can be used to view a full list of commits for a given git repo url.

Basic usage: `python3.7 main.py https://github.com/myuser/myrepo`

Complete usage (can be seen with `python3.7 main.py -h`):

```
usage: main.py [-h] [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
               [--timeout TIMEOUT] [--input {github,git}] [--skip_cache]
               url

Fetch a github repo's commit list.

positional arguments:
  url                   the url of the github repo

optional arguments:
  -h, --help            show this help message and exit
  --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        logger level
  --timeout TIMEOUT     request timeout (sec)
  --input {github,git}  force input
  --skip_cache          skips the cache
```

The default behaviour is to first try to get a commit list via the GitHub API, falling back to the git CLI if that fails. 
The git CLI input persists the fetched repo locally so that it is cached for future usage. 

### Dependencies
If you already have `pipenv`, you can run `pipenv sync` from the main directory to get all the dependencies installed. 

Otherwise, this is what you need:
- python 3.7
- the `requests` library, can be installed with `pip3 install requests`
- git

### Inputs supported:
- GitHub API
- git CLI

### Testing

Testing is done with `pytest` (it's included as a dev dependency on the Pipfile).
To run the tests, simply run `pytest` from the project's root directory.
