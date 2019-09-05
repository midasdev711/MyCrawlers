import sys
import subprocess
import sgvalidator

# force an install/upgrade of the sgvalidator package
subprocess.call([sys.executable, "-m", "pip", "uninstall", "sgvalidator"])
subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade",  "--no-cache-dir", "sgvalidator"])
data_location = None

try:
    data_location = sys.argv[1]
except IndexError:
    print("Please include a data location!")
    exit(0)

debug = len(sys.argv) > 2 and sys.argv[2] == "DEBUG"
sgvalidator.validate(data_location, debug=debug)