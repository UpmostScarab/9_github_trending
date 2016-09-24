import requests
import datetime
import json


REPO_COUNT = 20
SEARCH_REPO_API = "https://api.github.com/search/repositories"
ISSUES_API = "https://api.github.com/repos/%s/%s/issues"


def get_trending_repositories(top_size):
    last_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
    last_week_string = datetime.datetime.strftime(last_week, "%Y-%m-%d")
    req = requests.get('%s?q=created:>=%s&sort=stars&order=desc'
                       % (SEARCH_REPO_API, last_week_string))
    parsed = json.loads(req.text)
    for repo in parsed['items'][:20]:
        yield {'name': repo['name'], 'url': repo['html_url'],
               'stars': repo['stargazers_count'],
               'owner': repo['owner']['login']}


def get_open_issues_amount(repo_owner, repo_name):
    req = requests.get(ISSUES_API % (repo_owner, repo_name))
    parsed = json.loads(req.text)
    print("Issues amount: %d" % len(parsed))

if __name__ == '__main__':
    repos = get_trending_repositories(REPO_COUNT)
    for repo in repos:
        print("%s - %s stars" % (repo['url'], repo['stars']))
        get_open_issues_amount(repo['owner'], repo['name'])
