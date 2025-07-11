# models.py
# Data models for DatabaseSearcher

class Continent:
    def __init__(self, gid, code, name):
        self.gid = gid
        self.code = code
        self.name = name

class Country:
    def __init__(self, gid, code, name, continent_id, wiki, keywords):
        self.gid = gid
        self.code = code
        self.name = name
        self.continent_id = continent_id
        self.wiki = wiki
        self.keywords = keywords

class Region:
    def __init__(self, gid, code, local, name, continent_id, country_id, wiki, keywords):
        self.gid = gid
        self.code = code
        self.local = local
        self.name = name
        self.continent_id = continent_id
        self.country_id = country_id
        self.wiki = wiki
        self.keywords = keywords 