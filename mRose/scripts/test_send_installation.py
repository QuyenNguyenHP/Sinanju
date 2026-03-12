try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print("Watchdog is installed and can be imported.")
except ImportError:
    print("Watchdog is not installed.")
