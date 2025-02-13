from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_alerts_vuetify": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_alerts_vuetify/trame_alerts_vuetify.umd.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__trame_alerts_vuetify/trame_alerts_vuetify.css"]

# List of Vue plugins to install/load
vue_use = ["trame_alerts_vuetify"]


# Optional if you want to execute custom initialization at module load
def setup(server, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    assert server.client_type == "vue3"
