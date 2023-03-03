import sys
import zipfile

from lxml import etree

from utils.file import File


class Export:
    def __init__(self, export_file_path: str):
        self.export_root: etree._Element = self._load_file(export_file_path)  # TODO: is it actually str or lxml

    def _load_file(self, file_path: str) -> etree._Element:  # TODO: is this static?
        # TODO:
        #  TEST if is zip
        #    unzip file into tmp
        #  load file as xml
        #    delete file from tmp is was zip
        #  return xml file contents
        # TODO: error handling (is file xml or zip?) failed to load = die?
        # TODO: load into sqlite? and work with db instead of .. welp, this..
        tree: etree._ElementTree = File(file_path).get_as_xml()
        return tree.getroot()

    def get_product_count(self) -> int:  # TODO: test file is loaded?
        return len(self.export_root.xpath("items/item"))

    def get_next_product(self) -> str:  # TODO: str? should return lxml object
        for item in self.export_root.xpath("items/item"):
            yield item

    def get_spare_parts_for_product(self, product: etree._Element) -> etree._Element:  # TODO: IN lxml product object OUT lxml list
        if len(product.xpath("parts/part[@categoryId=1]")):
            for item in product.xpath("parts/part[@categoryId=1]/item"):
                yield item

    def item_to_string(self, item: etree._Element) -> str:
        tmp_code = item.xpath("@code")[0]
        tmp_name = item.xpath("@name")[0]
        if len(tmp_name) and len(tmp_code):
            return f"{tmp_code}: {tmp_name}"
        sys.exit(-1)  # TODO: error handling if no name

    def full_flow(self):  # TODO: yeah
        print(f"Amount of Products: {self.get_product_count()}")
        for product in self.get_next_product():
            print(f"Product: {self.item_to_string(product)}")
            for spare_part in self.get_spare_parts_for_product(product):
                print(f"Spare part: {self.item_to_string(spare_part)}")
            print("-"*10)


if __name__ == '__main__':
    export: Export = Export("tmp/export_full.xml")  # TODO: load name based on command line argument
    export.full_flow()

