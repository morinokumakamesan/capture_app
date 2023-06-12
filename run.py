from app.api import api
from app.api import socketio

if __name__ == '__main__':
#     api.run(host='0.0.0.0', port=3000)
    socketio.run(api, debug=False)

