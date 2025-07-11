# DatabaseSearcher/engine/main.py

import sqlite3
from DatabaseSearcher.events.app import *
from DatabaseSearcher.events.database import *
from DatabaseSearcher.events.continents import (
    ContinentSearchRequest, ContinentLoadRequest, ContinentCreateRequest, ContinentUpdateRequest,
    ContinentSavedNotice, ContinentSaveFailedNotice, ContinentLoadedNotice, ContinentSearchResult, GeoContinent
)
from DatabaseSearcher.events.countries import *
from DatabaseSearcher.events.regions import (
    RegionSearchRequest, RegionLoadRequest, RegionCreateRequest, RegionUpdateRequest,
    RegionSavedNotice, RegionSaveFailedNotice, RegionLoadedNotice, RegionSearchResult, GeoRegion
)


class CoreProcessor:
    def __init__(self):
        self.db_conn = None
        self._event_map = {
            AppQuitRequest: self.process_quit,
            DBOpenRequest: self.process_db_open,
            ContinentSearchRequest: self.process_continent_search,
            ContinentLoadRequest: self.process_continent_load,
            ContinentCreateRequest: self.process_continent_create,
            ContinentUpdateRequest: self.process_continent_update,
            CountrySearchRequest: self.process_country_search,
            CountryLoadRequest: self.process_country_load,
            CountryCreateRequest: self.process_country_create,
            CountryUpdateRequest: self.process_country_update,
            RegionSearchRequest: self.process_region_search,
            RegionLoadRequest: self.process_region_load,
            RegionCreateRequest: self.process_region_create,
            RegionUpdateRequest: self.process_region_update,
            DBCloseRequest: self.process_db_close
        }

    def handle_event(self, evt):
        try:
            handler = self._event_map.get(type(evt))
            if handler:
                yield from handler(evt)
        except Exception as exc:
            yield AppErrorEvent(f"[Core Error] {exc}")

    @staticmethod
    def process_quit(evt):
        yield AppShutdownEvent()

    def process_db_open(self, evt):
        """Handles OpenDatabaseEvent."""
        try:
            database_path = evt.get_path()
            if database_path.suffix.lower() in ['.db', '.sqlite', '.mdb', '.accdb']:
                self.db_conn = sqlite3.connect(database_path)
                yield DBOpenedNotice(database_path)

            else:
                raise ValueError("The file you selected is not a supported database file!")

        except Exception as e:
            yield DBOpenFailedNotice(f"Failed to open the database. Sorry! {e}")

    def process_db_close(self, evt):
        """Handles CloseDatabaseEvent."""
        if self.db_conn:
            self.db_conn.close()
            yield DBCloseNotice()
            self.db_conn = None


    def process_continent_search(self, evt):
        """Handles StartContinentSearchEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_code = evt.get_code()
                search_label = evt.get_label()

                if search_code and search_label:
                    cursor.execute("SELECT * FROM continent WHERE continent_code = ? AND name = ?",
                                   (search_code, search_label))
                elif search_code:
                    cursor.execute("SELECT * FROM continent WHERE continent_code = ?",
                                   (search_code,))
                elif search_label:
                    cursor.execute("SELECT * FROM continent WHERE name = ?", (search_label,))

                rows = cursor.fetchall()
                for row in rows:
                    continent = GeoContinent(*row)
                    yield ContinentSearchResult(continent)
                if not rows:
                    return
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield AppErrorEvent(f"Error: {e}")


    def process_continent_load(self, evt):
        """Handles LoadContinentEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_gid = evt.get_id()
                cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (search_gid,))
                rows = cursor.fetchall()
                for row in rows:
                    continent = GeoContinent(*row)
                    yield ContinentLoadedNotice(continent)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield AppErrorEvent(f"Error: {e}")


    def process_continent_create(self, evt):
        """Handles SaveNewContinentEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                new_continent = evt.get_continent()
                cursor.execute("INSERT INTO continent (continent_code, name) VALUES (?, ?)",
                               (new_continent.code, new_continent.label))
                self.db_conn.commit()
                yield ContinentSavedNotice(new_continent)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield ContinentSaveFailedNotice(f"Failed to save the new continent: {e}")


    def process_continent_update(self, evt):
        """Handles SaveContinentEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                modified_continent = evt.get_continent()
                cursor.execute(
                    "UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?",
                    (modified_continent.code, modified_continent.label, modified_continent.gid))
                self.db_conn.commit()
                yield ContinentSavedNotice(modified_continent)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield ContinentSaveFailedNotice(f"Failed to save the continent: {e}")


    def process_country_search(self, evt):
        """Handles StartCountrySearchEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_code = evt.get_code()
                search_label = evt.get_label()

                if search_code and search_label:
                    cursor.execute("SELECT * FROM country WHERE country_code = ? AND name = ?",
                                   (search_code, search_label))
                elif search_code:
                    cursor.execute("SELECT * FROM country WHERE country_code = ?",
                                   (search_code,))
                elif search_label:
                    cursor.execute("SELECT * FROM country WHERE name = ?", (search_label,))

                rows = cursor.fetchall()
                for row in rows:
                    country = GeoCountry(*row)
                    yield CountrySearchResult(country)

                if not rows:
                    return
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield AppErrorEvent(f"Error: {e}")


    def process_country_load(self, evt):
        """Handles LoadCountryEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                gid = evt.get_id()
                cursor.execute("SELECT * FROM country WHERE country_id = ?", (gid,))
                country_row = cursor.fetchone()
                if country_row:
                    country = GeoCountry(*country_row)
                    yield CountryLoadedNotice(country)
                else:
                    yield AppErrorEvent("Country not found in the database.")
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield AppErrorEvent(f"Error: {e}")


    def process_country_create(self, evt):
        """Handles SaveNewCountryEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                new_country = evt.get_country()
                cursor.execute(
                    "INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?)",
                    (new_country.code, new_country.label, new_country.continent_gid,
                     new_country.wiki, new_country.tags))
                self.db_conn.commit()
                yield CountrySavedNotice(new_country)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield CountrySaveFailedNotice(f"Failed to save the new country: {e}")


    def process_country_update(self, evt):
        """Handles SaveCountryEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                modified_country = evt.get_country()
                cursor.execute(
                    "UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?",
                    (modified_country.code, modified_country.label,
                     modified_country.continent_gid, modified_country.wiki,
                     modified_country.tags, modified_country.gid))
                self.db_conn.commit()
                yield CountrySavedNotice(modified_country)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield CountrySaveFailedNotice(f"Failed to save the country: {e}")


    def process_region_search(self, evt):
        """Handles StartRegionSearchEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_code = evt.get_code()
                search_local = evt.get_local()
                search_label = evt.get_label()

                sql_query = "SELECT * FROM region WHERE 1=1"
                params = []

                if search_code:
                    sql_query += " AND region_code = ?"
                    params.append(search_code)
                if search_local:
                    sql_query += " AND local_code = ?"
                    params.append(search_local)
                if search_label:
                    sql_query += " AND name = ?"
                    params.append(search_label)

                cursor.execute(sql_query, params)
                rows = cursor.fetchall()

                for row in rows:
                    region = GeoRegion(*row)
                    yield RegionSearchResult(region)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield AppErrorEvent(f"Error: {e}")


    def process_region_load(self, evt):
        """Handles LoadRegionEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                gid = evt.get_id()

                cursor.execute("SELECT * FROM region WHERE region_id = ?", (gid,))
                row = cursor.fetchone()

                if row:
                    region = GeoRegion(*row)
                    yield RegionLoadedNotice(region)
                else:
                    yield AppErrorEvent("Region not found.")
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield AppErrorEvent(f"Error: {e}")


    def process_region_create(self, evt):
        """Handles SaveNewRegionEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                new_region = evt.get_region()

                cursor.execute(
                    "INSERT INTO region (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (new_region.code, new_region.local, new_region.label,
                     new_region.continent_gid, new_region.country_gid, new_region.wiki,
                     new_region.tags))

                self.db_conn.commit()
                yield RegionSavedNotice(new_region)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield RegionSaveFailedNotice(f"Failed to save the new region: {e}")


    def process_region_update(self, evt):
        """Handles SaveRegionEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                modified_region = evt.get_region()

                cursor.execute(
                    "UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?",
                    (modified_region.code, modified_region.local,
                     modified_region.label, modified_region.continent_gid,
                     modified_region.country_gid, modified_region.wiki,
                     modified_region.tags, modified_region.gid))

                self.db_conn.commit()
                yield RegionSavedNotice(modified_region)
            else:
                yield AppErrorEvent("Open a database first!")
        except Exception as e:
            yield RegionSaveFailedNotice(f"Failed to save the region: {e}")
