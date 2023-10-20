import flask_site

app = flask_site.create_app()

if __name__ == '__main__':
    # import os
    # ssl_context = (os.path.join(os.path.dirname(__file__), 'certs', 'cert.pem'), os.path.join(os.path.dirname(__file__), 'certs', 'key.pem'))
    # app.run(debug=True, host='0.0.0.0', port=443, ssl_context=ssl_context)
    app.run(debug=True, host='0.0.0.0', port=80)