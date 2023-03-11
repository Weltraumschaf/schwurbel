import os
import shutil
import xml.etree.cElementTree as et
import requests


class Episode:
    def __init__(self):
        self.title = ""
        self.link = ""
        self.schwurbel = ""


def load_rss(url, file):
    response = requests.get(url)

    with open(file, 'wb') as f:
        f.write(response.content)


def parse_feed(file):
    tree = et.parse(file)
    root = tree.getroot()
    episodes = []

    for item in root.iter('item'):
        episode = Episode()

        for child in item:
            if child.tag == 'title':
                episode.title = child.text

            if child.tag == 'link':
                episode.link = child.text

            if child.tag == '{http://purl.org/rss/1.0/modules/content/}encoded':
                episode.schwurbel = extract_schwurbel(child.text)

        if episode.schwurbel:
            episodes.append(episode)

    return episodes


def extract_schwurbel(text):
    for line in text.splitlines():
        if 'Schwurbel der Woche:' in line.strip():
            return line + '\n'


def render_html(episodes):
    html = '<!DOCTYPE html>'
    html += '<html lang="en">'
    html += '<head>'
    html += '<meta charset="UTF-8">'
    html += '<title>Schwurbel</title>'
    html += '</head>'
    html += '<body>'
    html += '<h1>Schwurbel</h1>'

    for episode in episodes:
        html += f'<h2><a href="{episode.link}">{episode.title}</a></h2>'
        html += f"{episode.schwurbel}"

    html += '</body>'
    html += '</html>'
    return html


def main():
    build_dir = './target'
    shutil.rmtree(build_dir)

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    load_rss('https://minkorrekt.podigee.io/feed/mp3', f'{build_dir}/feed.xml')
    episodes = parse_feed(f'{build_dir}/feed.xml')
    episodes.reverse()
    html = render_html(episodes)

    with open(f'{build_dir}/schwurbel.html', 'w') as f:
        f.write(html)


if __name__ == "__main__":
    main()
