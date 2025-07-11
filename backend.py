# backend.py
# Handles all database operations and event processing for DatabaseSearcher

import sqlite3
from pathlib import Path
from models import Continent, Country, Region
from events import (
    AppExit, DBOpen, DBClose, ContinentQuery, ContinentFetch, ContinentAdd, ContinentEdit, ContinentResult, ContinentError,
    CountryQuery, CountryFetch, CountryAdd, CountryEdit, CountryResult, CountryError,
    RegionQuery, RegionFetch, RegionAdd, RegionEdit, RegionResult, RegionError,
    DBOpened, DBCloseNotice, AppError, AppShutdown
)

class DataBackend:
    def __init__(self):
        self.connection = None
        self._handlers = {
            AppExit: self._handle_exit,
            DBOpen: self._handle_db_open,
            DBClose: self._handle_db_close,
            ContinentQuery: self._handle_continent_query,
            ContinentFetch: self._handle_continent_fetch,
            ContinentAdd: self._handle_continent_add,
            ContinentEdit: self._handle_continent_edit,
            CountryQuery: self._handle_country_query,
            CountryFetch: self._handle_country_fetch,
            CountryAdd: self._handle_country_add,
            CountryEdit: self._handle_country_edit,
            RegionQuery: self._handle_region_query,
            RegionFetch: self._handle_region_fetch,
            RegionAdd: self._handle_region_add,
            RegionEdit: self._handle_region_edit,
        }

    def process(self, event):
        handler = self._handlers.get(type(event))
        if handler:
            yield from handler(event)
        else:
            yield AppError(f"No handler for event: {type(event).__name__}")

    def _handle_exit(self, event):
        yield AppShutdown()

    def _handle_db_open(self, event):
        try:
            db_path = event.path
            if Path(db_path).suffix.lower() in ['.db', '.sqlite', '.mdb', '.accdb']:
                self.connection = sqlite3.connect(db_path)
                yield DBOpened(db_path)
            else:
                raise ValueError("Unsupported database file!")
        except Exception as e:
            yield AppError(f"Failed to open database: {e}")

    def _handle_db_close(self, event):
        if self.connection:
            self.connection.close()
            self.connection = None
            yield DBCloseNotice()

    def _handle_continent_query(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                code, name = event.code, event.name
                if code and name:
                    cursor.execute("SELECT * FROM continent WHERE continent_code = ? AND name = ?", (code, name))
                elif code:
                    cursor.execute("SELECT * FROM continent WHERE continent_code = ?", (code,))
                elif name:
                    cursor.execute("SELECT * FROM continent WHERE name = ?", (name,))
                else:
                    cursor.execute("SELECT * FROM continent")
                for row in cursor.fetchall():
                    yield ContinentResult(Continent(*row))
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield ContinentError(str(e))

    def _handle_continent_fetch(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (event.gid,))
                row = cursor.fetchone()
                if row:
                    yield ContinentResult(Continent(*row))
                else:
                    yield AppError("Continent not found.")
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield ContinentError(str(e))

    def _handle_continent_add(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                c = event.continent
                cursor.execute("INSERT INTO continent (continent_code, name) VALUES (?, ?)", (c.code, c.name))
                self.connection.commit()
                yield ContinentResult(c)
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield ContinentError(str(e))

    def _handle_continent_edit(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                c = event.continent
                cursor.execute("UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?", (c.code, c.name, c.gid))
                self.connection.commit()
                yield ContinentResult(c)
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield ContinentError(str(e))

    def _handle_country_query(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                code, name = event.code, event.name
                if code and name:
                    cursor.execute("SELECT * FROM country WHERE country_code = ? AND name = ?", (code, name))
                elif code:
                    cursor.execute("SELECT * FROM country WHERE country_code = ?", (code,))
                elif name:
                    cursor.execute("SELECT * FROM country WHERE name = ?", (name,))
                else:
                    cursor.execute("SELECT * FROM country")
                for row in cursor.fetchall():
                    yield CountryResult(Country(*row))
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield CountryError(str(e))

    def _handle_country_fetch(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM country WHERE country_id = ?", (event.gid,))
                row = cursor.fetchone()
                if row:
                    yield CountryResult(Country(*row))
                else:
                    yield AppError("Country not found.")
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield CountryError(str(e))

    def _handle_country_add(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                c = event.country
                cursor.execute("INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?)", (c.code, c.name, c.continent_id, c.wiki, c.keywords))
                self.connection.commit()
                yield CountryResult(c)
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield CountryError(str(e))

    def _handle_country_edit(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                c = event.country
                cursor.execute("UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?", (c.code, c.name, c.continent_id, c.wiki, c.keywords, c.gid))
                self.connection.commit()
                yield CountryResult(c)
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield CountryError(str(e))

    def _handle_region_query(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                code, local, name = event.code, event.local, event.name
                sql = "SELECT * FROM region WHERE 1=1"
                params = []
                if code:
                    sql += " AND region_code = ?"
                    params.append(code)
                if local:
                    sql += " AND local_code = ?"
                    params.append(local)
                if name:
                    sql += " AND name = ?"
                    params.append(name)
                cursor.execute(sql, params)
                for row in cursor.fetchall():
                    yield RegionResult(Region(*row))
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield RegionError(str(e))

    def _handle_region_fetch(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM region WHERE region_id = ?", (event.gid,))
                row = cursor.fetchone()
                if row:
                    yield RegionResult(Region(*row))
                else:
                    yield AppError("Region not found.")
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield RegionError(str(e))

    def _handle_region_add(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                r = event.region
                cursor.execute("INSERT INTO region (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?)", (r.code, r.local, r.name, r.continent_id, r.country_id, r.wiki, r.keywords))
                self.connection.commit()
                yield RegionResult(r)
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield RegionError(str(e))

    def _handle_region_edit(self, event):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                r = event.region
                cursor.execute("UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?", (r.code, r.local, r.name, r.continent_id, r.country_id, r.wiki, r.keywords, r.gid))
                self.connection.commit()
                yield RegionResult(r)
            else:
                yield AppError("No database open.")
        except Exception as e:
            yield RegionError(str(e)) 