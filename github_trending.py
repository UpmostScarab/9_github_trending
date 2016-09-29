import requests
import datetime


def get_trending_repositories(top_size):
    SEARCH_REPO_API = "https://api.github.com/search/repositories"
    last_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
    last_week_string = datetime.datetime.strftime(last_week, "%Y-%m-%d")
    payload = {'q': "created:>=%s" % last_week_string,
               'sort': 'stars',
               'order': 'desc'}
    req = requests.get(SEARCH_REPO_API, params=payload)
    parsed = req.json()
    for repo in parsed['items'][:top_size]:
        yield {'name': repo['name'], 'url': repo['html_url'],
               'stars': repo['stargazers_count'],
               'owner': repo['owner']['login']}


def get_open_issues_amount(repo_owner, repo_name):
    ISSUES_API = "https://api.github.com/repos/%s/%s/issues"
    req = requests.get(ISSUES_API % (repo_owner, repo_name))
    parsed = req.json()
    return len(parsed)

if __name__ == '__main__':
    REPO_COUNT = 20
    repos = get_trending_repositories(REPO_COUNT)
    for repo in repos:
        print("%s - %s stars" % (repo['url'], repo['stars']))
        print("Issues amount: %d" % get_open_issues_amount(repo['owner'],
                                                           repo['name']))
