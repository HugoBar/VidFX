import logging

# Configure logging globally
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Create a global logger instance
logger = logging.getLogger("vidfx")
