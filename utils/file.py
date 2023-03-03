from lxml import etree


class File:
    def __init__(self, filename: str):
        self.filename: str = filename

    def get_as_xml(self) -> etree._ElementTree:  # TODO: protected
        parser: etree.XMLParser = etree.XMLParser(ns_clean=True, recover=True)  # TODO: don't create everytime?
        return etree.parse(self.filename, parser)
