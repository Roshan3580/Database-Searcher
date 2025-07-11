# DatabaseSearcher/engine/main.py

import sqlite3
from DatabaseSearcher.events.app import *
from DatabaseSearcher.events.database import *
from DatabaseSearcher.events.continents import *
from DatabaseSearcher.events.countries import *
from DatabaseSearcher.events.regions import *


class CoreProcessor:
    def __init__(self):
        self.db_conn = None
        self._event_map = {
            QuitInitiatedEvent: self.process_quit,
            OpenDatabaseEvent: self.process_db_open,
            StartContinentSearchEvent: self.process_continent_search,
            LoadContinentEvent: self.process_continent_load,
            SaveNewContinentEvent: self.process_continent_create,
            SaveContinentEvent: self.process_continent_update,
            StartCountrySearchEvent: self.process_country_search,
            LoadCountryEvent: self.process_country_load,
            SaveNewCountryEvent: self.process_country_create,
            SaveCountryEvent: self.process_country_update,
            StartRegionSearchEvent: self.process_region_search,
            LoadRegionEvent: self.process_region_load,
            SaveNewRegionEvent: self.process_region_create,
            SaveRegionEvent: self.process_region_update,
            CloseDatabaseEvent: self.process_db_close
        }

    def handle_event(self, evt):
        try:
            handler = self._event_map.get(type(evt))
            if handler:
                yield from handler(evt)
        except Exception as exc:
            yield ErrorEvent(f"[Core Error] {exc}")

    @staticmethod
    def process_quit(evt):
        yield EndApplicationEvent()

    def process_db_open(self, evt):
        """Handles OpenDatabaseEvent."""
        try:
            database_path = evt.path()
            if database_path.suffix.lower() in ['.db', '.sqlite', '.mdb', '.accdb']:
                self.db_conn = sqlite3.connect(database_path)
                yield DatabaseOpenedEvent(database_path)

            else:
                raise ValueError("The file you selected is not a supported database file!")

        except Exception as e:
            yield DatabaseOpenFailedEvent(f"Failed to open the database. Sorry! {e}")

    def process_db_close(self, evt):
        """Handles CloseDatabaseEvent."""
        if self.db_conn:
            self.db_conn.close()
            yield DatabaseClosedEvent()
            self.db_conn = None


    def process_continent_search(self, evt):
        """Handles StartContinentSearchEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_continent_code = evt.continent_code()
                search_name = evt.name()

                if search_continent_code and search_name:
                    cursor.execute("SELECT * FROM continent WHERE continent_code = ? AND name = ?",
                                   (search_continent_code, search_name))
                elif search_continent_code:
                    cursor.execute("SELECT * FROM continent WHERE continent_code = ?",
                                   (search_continent_code,))
                elif search_name:
                    cursor.execute("SELECT * FROM continent WHERE name = ?", (search_name,))

                rows = cursor.fetchall()
                for row in rows:
                    continent = Continent(*row)
                    yield ContinentSearchResultEvent(continent)
                if not rows:
                    return
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def process_continent_load(self, evt):
        """Handles LoadContinentEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_continent_id = evt.continent_id()
                cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (search_continent_id,))
                rows = cursor.fetchall()
                for row in rows:
                    continent = Continent(*row)
                    yield ContinentLoadedEvent(continent)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def process_continent_create(self, evt):
        """Handles SaveNewContinentEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                new_continent = evt.continent()
                cursor.execute("INSERT INTO continent (continent_code, name) VALUES (?, ?)",
                               (new_continent.continent_code, new_continent.name))
                self.db_conn.commit()
                yield ContinentSavedEvent(new_continent)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveContinentFailedEvent(f"Failed to save the new continent: {e}")


    def process_continent_update(self, evt):
        """Handles SaveContinentEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                modified_continent = evt.continent()
                cursor.execute(
                    "UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?",
                    (modified_continent.continent_code, modified_continent.name,
                     modified_continent.continent_id))
                self.db_conn.commit()
                yield ContinentSavedEvent(modified_continent)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveContinentFailedEvent(f"Failed to save the continent: {e}")


    def process_country_search(self, evt):
        """Handles StartCountrySearchEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_country_code = evt.country_code()
                search_name = evt.name()

                if search_country_code and search_name:
                    cursor.execute("SELECT * FROM country WHERE country_code = ? AND name = ?",
                                   (search_country_code, search_name))
                elif search_country_code:
                    cursor.execute("SELECT * FROM country WHERE country_code = ?",
                                   (search_country_code,))
                elif search_name:
                    cursor.execute("SELECT * FROM country WHERE name = ?", (search_name,))

                rows = cursor.fetchall()
                for row in rows:
                    country = Country(*row)
                    yield CountrySearchResultEvent(country)

                if not rows:
                    return
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def process_country_load(self, evt):
        """Handles LoadCountryEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                country_id = evt.country_id()
                cursor.execute("SELECT * FROM country WHERE country_id = ?", (country_id,))
                country_row = cursor.fetchone()
                if country_row:
                    country = Country(*country_row)
                    yield CountryLoadedEvent(country)
                else:
                    yield ErrorEvent("Country not found in the database.")
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def process_country_create(self, evt):
        """Handles SaveNewCountryEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                new_country = evt.country()
                cursor.execute(
                    "INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?)",
                    (new_country.country_code, new_country.name, new_country.continent_id,
                     new_country.wikipedia_link, new_country.keywords))
                self.db_conn.commit()
                yield CountrySavedEvent(new_country)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveCountryFailedEvent(f"Failed to save the new country: {e}")


    def process_country_update(self, evt):
        """Handles SaveCountryEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                modified_country = evt.country()
                cursor.execute(
                    "UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?",
                    (modified_country.country_code, modified_country.name,
                     modified_country.continent_id, modified_country.wikipedia_link,
                     modified_country.keywords, modified_country.country_id))
                self.db_conn.commit()
                yield CountrySavedEvent(modified_country)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveCountryFailedEvent(f"Failed to save the country: {e}")


    def process_region_search(self, evt):
        """Handles StartRegionSearchEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_region_code = evt.region_code()
                search_local_code = evt.local_code()
                search_name = evt.name()

                sql_query = "SELECT * FROM region WHERE 1=1"
                params = []

                if search_region_code:
                    sql_query += " AND region_code = ?"
                    params.append(search_region_code)
                if search_local_code:
                    sql_query += " AND local_code = ?"
                    params.append(search_local_code)
                if search_name:
                    sql_query += " AND name = ?"
                    params.append(search_name)

                cursor.execute(sql_query, params)
                rows = cursor.fetchall()

                for row in rows:
                    region = Region(*row)
                    yield RegionSearchResultEvent(region)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def process_region_load(self, evt):
        """Handles LoadRegionEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                search_region_id = evt.region_id()

                cursor.execute("SELECT * FROM region WHERE region_id = ?", (search_region_id,))
                row = cursor.fetchone()

                if row:
                    region = Region(*row)
                    yield RegionLoadedEvent(region)
                else:
                    yield ErrorEvent("Region not found.")
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def process_region_create(self, evt):
        """Handles SaveNewRegionEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                new_region = evt.region()

                cursor.execute(
                    "INSERT INTO region (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (new_region.region_code, new_region.local_code, new_region.name,
                     new_region.continent_id, new_region.country_id, new_region.wikipedia_link,
                     new_region.keywords))

                self.db_conn.commit()
                yield RegionSavedEvent(new_region)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveRegionFailedEvent(f"Failed to save the new region: {e}")


    def process_region_update(self, evt):
        """Handles SaveRegionEvent."""
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                modified_region = evt.region()

                cursor.execute(
                    "UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?",
                    (modified_region.region_code, modified_region.local_code,
                     modified_region.name, modified_region.continent_id,
                     modified_region.country_id, modified_region.wikipedia_link,
                     modified_region.keywords, modified_region.region_id))

                self.db_conn.commit()
                yield RegionSavedEvent(modified_region)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveRegionFailedEvent(f"Failed to save the region: {e}")
