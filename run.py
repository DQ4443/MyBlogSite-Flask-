from myblog import create_app

app = create_app() # can pass in a config parameter to test different configs

if __name__ == '__main__':
    app.run(debug=True)