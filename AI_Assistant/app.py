# -*- encoding:utf-8 -*-
# main.py

from setting import app
from blueprint import build_blueprint
print("Server ready")

build_blueprint(app)

# Uncomment the code below to initialize the tables and records in the database
# For subsequent runs, comment this line again
# init_database()

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)