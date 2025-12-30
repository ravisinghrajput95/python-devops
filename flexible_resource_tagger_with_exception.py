def manage_tags(existing_tags: dict, *simple_tags, **key_value_tags) -> dict:
    """
    Applies simple and key-value tags to an existing dictionary of tags.
    """

    # Input validation (message must match expected text)
    if not isinstance(existing_tags, dict):
        raise TypeError("existing_tags must be a dictionary")

    new_tags = existing_tags.copy()

    for tag in set(simple_tags):
        new_tags[tag] = "true"

    new_tags = new_tags | key_value_tags

    return new_tags

tags = {"env": "prod"}

result = manage_tags(tags, "billable", owner="platform")
print(result)
