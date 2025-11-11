import uvicorn

from . import get_config
from .api import create_api
from .auth import MSAuthAdapter
from .models import create_db_tables, get_db_engine, set_db_engine

SERVER_PORT = 5000
SERVER = "0.0.0.0"
LOG_LEVEL = "debug"

if __name__ == "__main__":
    config = get_config()
    set_db_engine(config)
    create_db_tables(get_db_engine())
    MSAuthAdapter(config.frontend_client_id, config.tenant_id, config.auth_policy, config.auth_url)
    app = create_api()
    uvicorn.run(app, host=SERVER, port=SERVER_PORT)
