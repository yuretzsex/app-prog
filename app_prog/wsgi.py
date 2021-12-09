from waitress import server

import main

serve(main.app, host='0.0.0.0', port=5000)
