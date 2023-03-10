import xml.etree.cElementTree as et


def main():
    tree = et.parse('./feed.xml')
    root = tree.getroot()

    for item in root.iter('item'):
        print('-------------------------')
        for child in item:
            if child.text and "Schwurbel" in child.text:
                print(child.text)


if __name__ == "__main__":
    main()
