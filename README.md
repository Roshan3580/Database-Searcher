# DatabaseSearcher

DatabaseSearcher is a desktop application for searching, viewing, and editing geographical data (continents, countries, and regions) stored in an SQLite database. It features a graphical user interface (GUI) built with Tkinter and a modular event-driven architecture.

## Features
- Open and close SQLite database files
- Search, view, add, and edit continents, countries, and regions
- Modular, event-driven design for easy extension
- User-friendly interface with menus and dialogs

## Project Structure
```
DatabaseSearcher/
├── engine/         # Core application logic (CoreProcessor)
├── events/         # Event definitions and event bus (EventDispatcher)
├── views/          # GUI components (AppMainWindow, views for continents, countries, regions)
├── __init__.py     # Package initialization
main.py             # Application entry point
schema.sql          # Example database schema
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
python main.py
```

## Usage
- Use the menu to open an SQLite database file (see `schema.sql` for the expected schema).
- Search, add, or edit continents, countries, and regions using the provided views.
- Save changes directly to the database.

## Architecture Overview
- **CoreProcessor**: Handles all database operations and event processing.
- **EventDispatcher**: Routes events between the GUI and the engine.
- **AppMainWindow**: The main Tkinter window and event handler.
- **Views**: Separate views for continents, countries, and regions.

## License
MIT License

---
*This project was refactored from a school assignment to serve as a general-purpose database search and edit tool.* 