import magic


def get_mime_type(filenmae):
    with open(filenmae, 'w') as file:
        return magic.from_buffer(file.read(), mime=True)
