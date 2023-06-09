from app_asset_translator import ConfigUtil
from app_asset_translator import Constants


def create_ios_resource_string(key, value):
    if str(value) == "nan":
        pass
    else:
        return f"\"{key}\" = \"{value}\";"


def write_resource_to_file(writer, value):
    if value is not None:
        writer.write(f"{value}\n")


def create_android_resource_string(key, value):
    if str(value) == "nan":
        pass
    else:
        return f"    <string name=\"{key}\">{value}</string>"


def generate_resource_file_for_language(language, given_df):
    locale = language[Constants.KEY_CONFIG_LOCALE]
    string_path = language[Constants.KEY_CONFIG_STRINGS_PATH]
    xml_path = language[Constants.KEY_CONFIG_XML_PATH]

    config = ConfigUtil.get_config()

    if string_path is not None:
        f = open(string_path, "w")

        results = [create_ios_resource_string(x, y) for x, y in
                   zip(given_df[config[Constants.KEY_CONFIG_VARIABLE_NAME]], given_df[locale])]

        [write_resource_to_file(f, x) for x in results]

        f.close()

    if xml_path is not None:
        f = open(xml_path, "w")
        f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        f.write("<resources>\n")

        results = [create_android_resource_string(x, y) for x, y in
                   zip(given_df[config[Constants.KEY_CONFIG_VARIABLE_NAME]], given_df[locale])]
        [write_resource_to_file(f, x) for x in results]

        f.write("</resources>")
