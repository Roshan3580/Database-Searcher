
# p2app/engine/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.


import sqlite3
from p2app.events.app import *
from p2app.events.database import *
from p2app.events.continents import *
from p2app.events.countries import *
from p2app.events.regions import *


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = None


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        try:
            if isinstance(event, QuitInitiatedEvent):
                yield from self.handle_quit_event()

            elif isinstance(event, OpenDatabaseEvent):
                yield from self.handle_open_database_event(event)

            elif isinstance(event, StartContinentSearchEvent):
                yield from self.handle_start_continent_search_event(event)

            elif isinstance(event, LoadContinentEvent):
                yield from self.handle_load_continent_event(event)

            elif isinstance(event, SaveNewContinentEvent):
                yield from self.handle_save_new_continent_event(event)

            elif isinstance(event, SaveContinentEvent):
                yield from self.handle_save_continent_event(event)

            elif isinstance(event, StartCountrySearchEvent):
                yield from self.handle_start_country_search_event(event)

            elif isinstance(event, LoadCountryEvent):
                yield from self.handle_load_country_event(event)

            elif isinstance(event, SaveNewCountryEvent):
                yield from self.handle_save_new_country_event(event)

            elif isinstance(event, SaveCountryEvent):
                yield from self.handle_save_country_event(event)

            elif isinstance(event, StartRegionSearchEvent):
                yield from self.handle_start_region_search_event(event)

            elif isinstance(event, LoadRegionEvent):
                yield from self.handle_load_region_event(event)

            elif isinstance(event, SaveNewRegionEvent):
                yield from self.handle_save_new_region_event(event)

            elif isinstance(event, SaveRegionEvent):
                yield from self.handle_save_region_event(event)

            elif isinstance(event, CloseDatabaseEvent):
                yield from self.handle_close_database_event()

        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    @staticmethod
    def handle_quit_event():
        """Handles QuitInitiatedEvent."""
        yield EndApplicationEvent()


    def handle_open_database_event(self, event):
        """Handles OpenDatabaseEvent."""
        try:
            database_path = event.path()
            if database_path.suffix.lower() in ['.db', '.sqlite', '.mdb', '.accdb']:
                self.connection = sqlite3.connect(database_path)
                yield DatabaseOpenedEvent(database_path)

            else:
                raise ValueError("The file you selected is not a supported database file!")

        except Exception as e:
            yield DatabaseOpenFailedEvent(f"Failed to open the database. Sorry! {e}")

    def handle_close_database_event(self):
        """Handles CloseDatabaseEvent."""
        if self.connection:
            self.connection.close()
            yield DatabaseClosedEvent()
            self.connection = None


    def handle_start_continent_search_event(self, event):
        """Handles StartContinentSearchEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                search_continent_code = event.continent_code()
                search_name = event.name()

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


    def handle_load_continent_event(self, event):
        """Handles LoadContinentEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                search_continent_id = event.continent_id()
                cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (search_continent_id,))
                rows = cursor.fetchall()
                for row in rows:
                    continent = Continent(*row)
                    yield ContinentLoadedEvent(continent)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield ErrorEvent(f"Error: {e}")


    def handle_save_new_continent_event(self, event):
        """Handles SaveNewContinentEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                new_continent = event.continent()
                cursor.execute("INSERT INTO continent (continent_code, name) VALUES (?, ?)",
                               (new_continent.continent_code, new_continent.name))
                self.connection.commit()
                yield ContinentSavedEvent(new_continent)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveContinentFailedEvent(f"Failed to save the new continent: {e}")


    def handle_save_continent_event(self, event):
        """Handles SaveContinentEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                modified_continent = event.continent()
                cursor.execute(
                    "UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?",
                    (modified_continent.continent_code, modified_continent.name,
                     modified_continent.continent_id))
                self.connection.commit()
                yield ContinentSavedEvent(modified_continent)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveContinentFailedEvent(f"Failed to save the continent: {e}")


    def handle_start_country_search_event(self, event):
        """Handles StartCountrySearchEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                search_country_code = event.country_code()
                search_name = event.name()

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


    def handle_load_country_event(self, event):
        """Handles LoadCountryEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                country_id = event.country_id()
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


    def handle_save_new_country_event(self, event):
        """Handles SaveNewCountryEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                new_country = event.country()
                cursor.execute(
                    "INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?)",
                    (new_country.country_code, new_country.name, new_country.continent_id,
                     new_country.wikipedia_link, new_country.keywords))
                self.connection.commit()
                yield CountrySavedEvent(new_country)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveCountryFailedEvent(f"Failed to save the new country: {e}")


    def handle_save_country_event(self, event):
        """Handles SaveCountryEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                modified_country = event.country()
                cursor.execute(
                    "UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?",
                    (modified_country.country_code, modified_country.name,
                     modified_country.continent_id, modified_country.wikipedia_link,
                     modified_country.keywords, modified_country.country_id))
                self.connection.commit()
                yield CountrySavedEvent(modified_country)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveCountryFailedEvent(f"Failed to save the country: {e}")


    def handle_start_region_search_event(self, event):
        """Handles StartRegionSearchEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                search_region_code = event.region_code()
                search_local_code = event.local_code()
                search_name = event.name()

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


    def handle_load_region_event(self, event):
        """Handles LoadRegionEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                search_region_id = event.region_id()

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


    def handle_save_new_region_event(self, event):
        """Handles SaveNewRegionEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                new_region = event.region()

                cursor.execute(
                    "INSERT INTO region (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (new_region.region_code, new_region.local_code, new_region.name,
                     new_region.continent_id, new_region.country_id, new_region.wikipedia_link,
                     new_region.keywords))

                self.connection.commit()
                yield RegionSavedEvent(new_region)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveRegionFailedEvent(f"Failed to save the new region: {e}")


    def handle_save_region_event(self, event):
        """Handles SaveRegionEvent."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                modified_region = event.region()

                cursor.execute(
                    "UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?",
                    (modified_region.region_code, modified_region.local_code,
                     modified_region.name, modified_region.continent_id,
                     modified_region.country_id, modified_region.wikipedia_link,
                     modified_region.keywords, modified_region.region_id))

                self.connection.commit()
                yield RegionSavedEvent(modified_region)
            else:
                yield ErrorEvent("Open a database first!")
        except Exception as e:
            yield SaveRegionFailedEvent(f"Failed to save the region: {e}")
