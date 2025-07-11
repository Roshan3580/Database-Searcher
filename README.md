# DatabaseSearcher

DatabaseSearcher is a desktop application for searching, viewing, and editing geographical data (continents, countries, and regions) stored in an SQLite database. It features a graphical user interface (GUI) built with Tkinter and a modular event-driven architecture.

## Features
- Open and close SQLite database files
- Search, view, add, and edit continents, countries, and regions
- Modular, event-driven design for easy extension
- User-friendly interface with menus and dialogs

## New Project Structure
```
DatabaseSearcher/
├── app.py           # Application entry point
├── backend.py       # All database and event handling logic
├── gui.py           # All Tkinter GUI logic
├── events.py        # All event classes and event bus
├── models.py        # Data models for Continent, Country, Region
├── schema.sql       # Example database schema
├── README.md        # Project documentation
```

## Getting Started
### Prerequisites
- Python 3.8+
- Tkinter (usually included with Python)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/DatabaseSearcher.git
   cd DatabaseSearcher
   ```
2. (Optional) Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies (if any):
   ```
   pip install -r requirements.txt
   ```
   *(No external dependencies required for core functionality)*

### Running the Application
```
python app.py
```

## Usage
- Use the menu to open an SQLite database file (see `schema.sql` for the expected schema).
- Search, add, or edit continents, countries, and regions using the provided views.
- Save changes directly to the database.

## Architecture Overview
- **DataBackend**: Handles all database operations and event processing.
- **EventBus**: Routes events between the GUI and the backend.
- **MainWindow**: The main Tkinter window and event handler.
- **Panels**: Separate panels for continents, countries, and regions.
- **Models**: Data classes for each entity.

## License
MIT License 