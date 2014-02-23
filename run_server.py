from studygroup.application import create_app


if __name__ == "__main__":
    app = create_app(debug=True)
    app.run(debug=True, port=80)
