import sys
import getopt
from swtor.gtn_window import GtnWindow
item_price_index = -1
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i::')
except getopt.GetoptError:
    print('capture_gtn_price_images.py -i <item_price_index>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-i':
        item_price_index = int(arg)

GtnWindow().save_all_item_price_images_on_page_raw(item_price_index)