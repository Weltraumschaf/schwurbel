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
    return text


def main():
    episodes = parse_feed('./feed.xml')

    for episode in episodes:
        print(f"Title: {episode.title}")
        print(f"Link: {episode.link}")
        print(f"Schwurbel: {episode.schwurbel}")
        print('=========================')


if __name__ == "__main__":
    main()
