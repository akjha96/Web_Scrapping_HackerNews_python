import requests
from bs4 import BeautifulSoup
import pprint
import sys


def response_and_soup(url_link):
    resp = requests.get(url_link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def get_link(soup):
    return soup.select('.storylink')


def get_subtext(soup):
    return soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_fn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'votes': points, 'link': href})
    return sort_stories_by_votes(hn)


def get_mega_links_and_subtext(urls):
    mega_link = []
    mega_subtext = []
    for url in urls:
        mega_link.extend(get_link(response_and_soup(url)))
        mega_subtext.extend(get_subtext(response_and_soup(url)))
    pprint.pprint(create_custom_fn(mega_link, mega_subtext))
    print("DONE !!!")


def input_urls():
    urls_to_webscrape = []
    url = 'https://' + input('Please enter the url to scrape from: ')
    urls_to_webscrape.append(url)
    while True:
        more = input('Do you have more links? y/n: ').lower()
        if more == 'n':
            break
        elif more == 'y':
            url = 'https://' + input('Please enter the url to scrape from: ')
            urls_to_webscrape.append(url)
        else:
            print('Invalid input! Try again')

    return get_mega_links_and_subtext(urls_to_webscrape)


if __name__ == '__main__':
    sys.exit(input_urls())
