from base import app

if __name__ == "__main__":
    app.run(threaded=True, debug=True)

# deploy on gunicorn server
# gunicorn --bind 0.0.0.0:port_number app:app

# to kill the port
# fuser -n tcp -k port_number

# python flask orm libs
# pip install flask
# pip install pymysql
# pip install sqlalchemy
# pip install flask-sqlalchemy
# pip install Flask-Migrate

# db migrations command
# flask db init
# flask db migrate -m "migration_one"
# flask db upgrade
# flask db --help