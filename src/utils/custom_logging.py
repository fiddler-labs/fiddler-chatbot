import logging
import os
from datetime import datetime

# Module-level variable for singleton pattern (instead of function attribute)
_logging_configured = False

def setup_logging(log_level: str = "INFO"):
    """
    Set up logging with appropriate configuration (singleton pattern)

    This function can be called multiple times safely - it will only configure
    logging once. The first call determines the configuration.

    Args: log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    global _logging_configured
    # Singleton pattern: return early if already configured
    if _logging_configured:
        return

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

    # Add console handler with same level as file handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)

    # Add handlers to the root logger
    root_logger.addHandler(app_file_handler)
    root_logger.addHandler(console_handler)

    root_logger.setLevel(numeric_level)

    # Mark as configured (singleton pattern)
    _logging_configured = True

    def configure_third_party_logging():
        """
        Configure logging for common third-party libraries to reduce noise.
        """
        # Suppress verbose third-party library logs
        logging.getLogger( 'httpx'     ).setLevel(logging. WARNING )
        logging.getLogger( 'httpcore'  ).setLevel(logging. WARNING )
        logging.getLogger( 'urllib3'   ).setLevel(logging. INFO    )
        logging.getLogger( 'cassandra' ).setLevel(logging. ERROR   )
        logging.getLogger( 'cassio'    ).setLevel(logging. WARNING )
        logging.getLogger( 'openai'    ).setLevel(logging. WARNING )
        logging.getLogger( 'langgraph' ).setLevel(logging. INFO    )
        logging.getLogger( 'watchfiles').setLevel(logging. WARNING )


    configure_third_party_logging()
