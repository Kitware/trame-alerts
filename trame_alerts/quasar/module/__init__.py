from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_alerts_quasar": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_alerts_quasar/trame_alerts_quasar.umd.js"]

# List of Vue plugins to install/load
vue_use = ["trame_alerts_quasar"]


# Optional if you want to execute custom initialization at module load
def setup(server, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    assert server.client_type == "vue3"
