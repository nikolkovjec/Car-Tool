from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter


class JsonPipeline(object):
    def __init__(self):
        self.file = open("file.json", 'wb', buffering=0)
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Don't save item if car was damaged.
        if adapter.get('damaged'):
            raise DropItem(f"Dropping - {item} - damaged was True!")
        # Don't save item if car has more that 1 000 000 KMs of mileage.
        elif adapter.get('mileage') and int(adapter.get('mileage')) > 1000000:
            raise DropItem(f"Dropping - {item} - mileage is over 1 000 000 KMs!")
        else:
            self.exporter.export_item(item)
            self.file.write(b'\n')
            return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
