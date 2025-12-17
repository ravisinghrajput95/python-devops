def manage_tags(existing_tags, *simple_tags, **key_value_tags):
    # Start with a COPY to keep immutability
    final_tags = existing_tags.copy()

    # Handle simple tags (*args)
    for tag in simple_tags:
        final_tags[tag] = "true"

    # Handle key-value tags (**kwargs) — highest priority
    for key, value in key_value_tags.items():
        final_tags[key] = value

    return final_tags

existing = {"env": "dev", "owner": "alice"}

result1 = manage_tags(existing, "billable", team="platform")
print(result1)

result2 = manage_tags({}, "billable", "billable", "critical")
print(result2)

existing = {"env": "dev", "owner": "alice"}

result = manage_tags(existing, "billable", env="prod", owner="platform")
print(existing)