class ConfigManager:
    def __init__(self, filename="config.txt"):
        self.filename = filename
        self.config = {}

        # Load config from file if it exists
        self.load_config()

    def load_config(self):
        """Load key-value pairs from the config file."""
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    key, value = line.strip().split("=", 1)
                    self.config[key] = value
        except OSError:
            print("Config file not found, creating a new one.")
        except ValueError:
            print("Error parsing config file. Check formatting.")

    def save_config(self):
        """Save key-value pairs to the config file."""
        with open(self.filename, "w") as f:
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")

    def set(self, key, value):
        """Set a configuration value and save the file."""
        self.config[key] = value
        self.save_config()

    def get(self, key, default=None):
        """Get a configuration value, return default if not found."""
        return self.config.get(key, default)

# Example usage
if __name__ == "__main__":
    config = ConfigManager()
    config.set("hostname", "esp32smv2")
    config.set("staticip", "192.168.1.210")

    print("Hostname:", config.get("hostname"))
    print("Static IP:", config.get("staticip"))
