def build_summary(results, name, topic, plural='s') -> str:
    length = len(results)
    if length > 1:
        name += plural
    return f'{length} {name} {topic}'
