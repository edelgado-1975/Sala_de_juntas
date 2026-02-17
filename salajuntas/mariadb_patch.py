# Monkey patch to disable MySQL version check for MariaDB compatibility
import django.db.backends.mysql.base as mysql_base

# Store original function
original_check_database_version_supported = mysql_base.DatabaseWrapper.check_database_version_supported

# Create patched function that does nothing
def patched_check_database_version_supported(self):
    pass

# Apply patch
mysql_base.DatabaseWrapper.check_database_version_supported = patched_check_database_version_supported
