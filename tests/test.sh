### Environment Variables ###
# Metabase URL
export MB_HOST="localhost"
export MB_PORT=12345 
export MB_PROTOCOL="http"

# Metabase User
export MB_USER_EMAIL="admin@prevoir.mu"
export MB_USER_PASS="Prevoir@123"
export MB_USER_FNAME="iNSight"
export MB_USER_LNAME="Admin"

# Kubernetes namespace
export MB_NS="test"

# Run base script
/usr/bin/python3 ../src/metabase_initial_config.py