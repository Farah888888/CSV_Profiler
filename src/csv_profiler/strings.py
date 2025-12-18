def slugify(text):
    newText = text.replace(" ", "-").casefold()
    return newText