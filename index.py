import argparse
import logging
from swtor.swtor_game import SwtorGame

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s (%(name)s.%(funcName)s) %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
swtor_game = SwtorGame(logger)

def check_lowest_prices():
    # Position the character directly in front of a GTN terminal
    swtor_game.check_inventory_gtn_lowest_price()

def check_gtn():
    # Position the character directly in front of a GTN terminal
    swtor_game.check_inventory_gtn()

def inv_to_cargo():
    # Ensure both Cargo Hold and Inventory windows are already open
    # and that desired Cargo Hold bay is selected
    swtor_game.transfer_inventory_to_cargo_hold()

def cargo_to_inv():
    # Ensure both Cargo Hold and Inventory windows are already open
    # and that desired Cargo Hold bay is selected
    swtor_game.transfer_cargo_hold_to_inventory()

def open_crew_skills_window():
    swtor_game.open_crew_skills_window()

def _add_subparser(subparsers, command_name):
    subparser = subparsers.add_parser(command_name)
    subparser.add_argument('--debug', action = 'store_true')
    return subparser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(func = check_lowest_prices)
    subparsers = parser.add_subparsers()
    parser_check_prices = _add_subparser(subparsers, 'check-lowest-prices')
    parser_check_prices.set_defaults(func = check_lowest_prices)
    parser_check_prices = _add_subparser(subparsers, 'check-gtn')
    parser_check_prices.set_defaults(func = check_gtn)
    parser_inv_to_cargo = _add_subparser(subparsers, 'inv-to-cargo')
    parser_inv_to_cargo.set_defaults(func = inv_to_cargo)
    parser_cargo_to_inv = _add_subparser(subparsers, 'cargo-to-inv')
    parser_cargo_to_inv.set_defaults(func = cargo_to_inv)
    parser_open_crew_skills = _add_subparser(subparsers, 'open-crew-skills')
    parser_open_crew_skills.set_defaults(func = open_crew_skills_window)
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    args.func()





# if __name__ == "__main__":
#     from swtor.google_sheet import GoogleSheet
#     google_sheet = GoogleSheet()
#     GoogleSheet().to_sqlite()

# if __name__ == "__main__":
#     from swtor.gtn_window import GtnWindow
#     GtnWindow().save_all_item_price_images_on_page_raw()

# if __name__ == "__main__":
#     from swtor.gtn_window import GtnWindow
#     print(GtnWindow().location)