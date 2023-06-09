import csv
import xml.etree.ElementTree as Et
import pandas as pd

from app_asset_translator import ConfigUtil
from app_asset_translator import Constants


def ios_get_key_value_from_line(line):
    # Remove potential whitespaces at the start/end of the string
    modified_string = line.strip()

    # Remove the last character: "Yes" = "Ja"; -> "Yes" = "Ja"
    modified_string = modified_string[:-1]

    # Split the string to key/value: "Yes" = "Ja" -> ['"Yes" ', ' "Ja"']
    modified_string = modified_string.split('=')

    # Remove the first and last values of the key
    key = modified_string[0].strip()

    # The key can not contain '=', thus the value contains a combination of all possible entries
    value = '='.join(modified_string[1:]).strip()

    # Remove the first & last characters ('"'): "Yes" -> Yes & "No" -> No
    key = key[1:-1]
    value = value[1:-1]

    return [[key, value]]


def android_get_key_values_from_xml(xml_path):
    tree = Et.parse(xml_path)
    root = tree.getroot()

    key_value_list = []

    for item in root:
        # E.g: <string name="Yes">Ja</string> -> Key = Yes
        key = item.attrib["name"]

        # E.g: <string name="Yes">Ja</string> -> value = Ja
        value = item.text

        key_value_list += [[key, value]]

    return key_value_list


def generate_csv_from_resource_files(languages):
    key_column_name = ConfigUtil.get_config()[Constants.KEY_CONFIG_VARIABLE_NAME]

    final_pd = pd.DataFrame(data=[], columns=[key_column_name])

    for current_language in languages:
        if current_language[Constants.KEY_CONFIG_STRINGS_PATH] is not None:
            key_list = []

            f = open(current_language[Constants.KEY_CONFIG_STRINGS_PATH], 'r')

            for line in f.readlines():
                key_list += ios_get_key_value_from_line(line)

            # Transform the key/value list to a dataframe, and merge it into the 'main' dataframe
            df = pd.DataFrame(data=key_list, columns=[key_column_name, current_language[Constants.KEY_CONFIG_LOCALE]])
            final_pd = pd.merge(left=final_pd, right=df, how='outer')
        if current_language[Constants.KEY_CONFIG_XML_PATH] is not None:
            key_list = android_get_key_values_from_xml(current_language[Constants.KEY_CONFIG_XML_PATH])

            df = pd.DataFrame(data=key_list, columns=[key_column_name, current_language[Constants.KEY_CONFIG_LOCALE]])
            final_pd = pd.merge(left=final_pd, right=df, how='outer')

    final_pd.to_csv(ConfigUtil.get_config()[Constants.KEY_CONFIG_OUTPUT_PATH], index=False, sep=';', encoding='utf-8',
                    quotechar='"', quoting=csv.QUOTE_ALL)
