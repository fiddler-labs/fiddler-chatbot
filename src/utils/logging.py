import logging
import os
from datetime import datetime

def setup_logging(log_level: str = "INFO"):
    """
    Set up logging with appropriate configuration
    Args: log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Generate timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    # Clear any existing handlers from the root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure the root logger
    log_format = '%(asctime)s - %(levelname)8s - %(lineno)4d - %(name)s - %(module)s - %(funcName)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # Add file handler for application logs
    app_log_file = f"logs/log_{timestamp}.log"
    app_file_handler = logging.FileHandler(app_log_file)
    app_file_handler.setFormatter(formatter)
    app_file_handler.setLevel(numeric_level)
    print(f"Application logs will be written to: {app_log_file}")
    
    # Add console handler for ERROR and above (for stack traces)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)
    
    # Add handlers to the root logger
    root_logger.addHandler(app_file_handler)
    root_logger.addHandler(console_handler)
    
    root_logger.setLevel(numeric_level)

