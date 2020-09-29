from src import create_app

DATABASE = 'database.db'

app = create_app(DATABASE)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1024, debug=True)
