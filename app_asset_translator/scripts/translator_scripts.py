import argparse
import pandas as pd

from app_asset_translator import LanguageUtil
from app_asset_translator import ConfigUtil
from app_asset_translator import Constants
from app_asset_translator.GenerateCsvFromResources import generate_csv_from_resource_files
from app_asset_translator.GenerateResourcesFromCsv import generate_resource_file_for_language


def generate_csv():
    result = LanguageUtil.get_languages()
    generate_csv_from_resource_files(result)
    print('CSV has been generated!')


def generate_resources():
    config = ConfigUtil.get_config()
    dataframe = pd.read_csv(f'{config[Constants.KEY_CONFIG_TRANSLATION_FILE_PATH]}', delimiter=';', doublequote=True)

    languages = LanguageUtil.get_languages()
    [generate_resource_file_for_language(language, dataframe) for language in languages]
    print('Resources have been generated!')


def main():
    # Define the default parser
    parser = argparse.ArgumentParser(description='Use the translation service to generate CSV or Android/iOS Resource '
                                                 'files')
    # Initialize the sub parsers (csv / resource commands)
    subparsers = parser.add_subparsers(dest='operation', help='Choose an operation')

    csv_parser = subparsers.add_parser('csv', help='Generate a CSV based on the pre-defined resources.')
    csv_parser.set_defaults(func=generate_csv)

    resource_parser = subparsers.add_parser('resources', help='Generate resource files (Android/iOS) based on the '
                                                              'pre-defined CSV.')
    resource_parser.set_defaults(func=generate_resources)

    # parser.add_argument('-v', '--verbose', action='store_true', help='increase verbosity')
    args = parser.parse_args()
    # Run the function which has been added to the arguments
    args.func()
