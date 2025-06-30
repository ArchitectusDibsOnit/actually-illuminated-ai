# meta_tag_autocomplete.py

from phoneme_and_meta_tag_utils import meta_tags

def get_all_tags_flat():
    tags = []
    for category in meta_tags.values():
        tags.extend(category)
    return tags

def filter_tags(user_input):
    if not user_input.startswith("["):
        return []
    return [tag for tag in get_all_tags_flat() if tag.startswith(user_input)]
