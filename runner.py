import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "swa.api.v1.app.main:app",
        port=8080,
        host="127.0.0.1",
        # host="127.0.0.1" if os.getenv('DEBUG', default='false') in ('true',) else '0.0.0.0',
        reload=True
    )