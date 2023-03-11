import xml.etree.cElementTree as et


class Episode:
    def __init__(self):
        self.title = ""
        self.link = ""
        self.schwurbel = ""


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

            if child.tag == '{http://purl.org/rss/1.0/modules/content/}encoded' and "Schwurbel" in child.text:
                episode.schwurbel = extract_schwurbel(child.text)

        if episode.schwurbel:
            episodes.append(episode)

    return episodes


def extract_schwurbel(text):
    for line in text.splitlines():
        if 'Schwurbel der Woche:' in line.strip():
            return line + '\n'


def main():
    print('<!DOCTYPE html>')
    print('<html lang="en">')
    print('<head>')
    print('<meta charset="UTF-8">')
    print('<title>Schwurbel</title>')
    print('</head>')
    print('<body>')
    print('<h1>Schwurbel</h1>')

    episodes = parse_feed('./feed.xml')
    episodes.reverse()
    for episode in episodes:
        print(f'<h2><a href="{episode.link}">{episode.title}</a></h2>')
        print(f"{episode.schwurbel}")

    print('</body>')
    print('</html>')


if __name__ == "__main__":
    main()
