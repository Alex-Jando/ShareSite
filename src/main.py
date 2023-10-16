import flask_site

app = flask_site.create_app()

if __name__ == '__main__':
    # ssl_context='adhoc'
    app.run(debug=True, host='0.0.0.0', port=80)