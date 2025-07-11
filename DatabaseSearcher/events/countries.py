# DatabaseSearcher/events/countries.py

from collections import namedtuple

GeoCountry = namedtuple('GeoCountry', ['gid', 'code', 'label', 'continent_gid', 'wiki', 'tags'])
GeoCountry.__annotations__ = {
    'gid': int | None,
    'code': str | None,
    'label': str | None,
    'continent_gid': int | None,
    'wiki': str | None,
    'tags': str | None
}

class CountrySearchRequest:
    def __init__(self, code: str, label: str):
        self._code = code
        self._label = label
    def get_code(self) -> str:
        return self._code
    def get_label(self) -> str:
        return self._label
    def __repr__(self) -> str:
        return f'{type(self).__name__}: code = {repr(self._code)}, label = {repr(self._label)}'

class CountrySearchResult:
    def __init__(self, country: GeoCountry):
        self._country = country
    def get_country(self) -> GeoCountry:
        return self._country
    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'

class CountryLoadRequest:
    def __init__(self, gid: int):
        self._gid = gid
    def get_id(self) -> int:
        return self._gid
    def __repr__(self) -> str:
        return f'{type(self).__name__}: gid = {repr(self._gid)}'

class CountryLoadedNotice:
    def __init__(self, country: GeoCountry):
        self._country = country
    def get_country(self) -> GeoCountry:
        return self._country
    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'

class CountryCreateRequest:
    def __init__(self, country: GeoCountry):
        self._country = country
    def get_country(self) -> GeoCountry:
        return self._country
    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'

class CountryUpdateRequest:
    def __init__(self, country: GeoCountry):
        self._country = country
    def get_country(self) -> GeoCountry:
        return self._country
    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'

class CountrySavedNotice:
    def __init__(self, country: GeoCountry):
        self._country = country
    def get_country(self) -> GeoCountry:
        return self._country
    def __repr__(self) -> str:
        return f'{type(self).__name__}: country = {repr(self._country)}'

class CountrySaveFailedNotice:
    def __init__(self, reason: str):
        self._reason = reason
    def get_reason(self) -> str:
        return self._reason
    def __repr__(self) -> str:
        return f'{type(self).__name__}: reason = {repr(self._reason)}'
