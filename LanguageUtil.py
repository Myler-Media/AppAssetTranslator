import ConfigUtil
import Constants


def remove_none_values(value_list):
    return [i for i in value_list if i is not None]


# This function is used to filter out languages without a defined xml/string path
def get_language_details(language):
    # This part is required, as the language string, f.e 'Dutch-NL' is 1 layer higher than the required data
    current_language_key = list(language.keys())[0]
    language = language[current_language_key]

    string_path = language[Constants.KEY_CONFIG_STRINGS_PATH]
    xml_path = language[Constants.KEY_CONFIG_XML_PATH]

    if xml_path is None and string_path is None:
        pass
    else:
        return language


def get_languages():
    language_list = [get_language_details(x) for x in ConfigUtil.get_config()[Constants.KEY_CONFIG_SUPPORTED_LANGUAGES]]
    return remove_none_values(language_list)
