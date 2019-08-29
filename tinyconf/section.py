import typing

class Section():
    """Sections help to tell the models where config options can be found within INI files.

    Parameters
    ----------
        name: Optional[:class:`str`]:
            The name of the section. Defaults to the attribute name.
        *
            All other attributes should be the fields belonging to the section.

    Example::

        class Config(IniDeserializer):
            token = IntegerField()
            username = Field()

            username_mysql = Field(name='username')
            passwd = Field()
            host = Field()

            client = Field()

            DEFAULT = Section(token, username)
            MYSQL = Section(username_mysql, passwd, host)
            PASSMARK = Section(client)
        
        config = Config(string='''
        [DEFAULT]
        token = 1234
        username = hello

        [MYSQL]
        username = jude
        passwd = 12345
        ;host = j.net

        [PASSMARK]
        client = fred''')

    """
    def __init__(self, *args, name: typing.Optional[str]=None):
        self.name = name
        self.contents = args