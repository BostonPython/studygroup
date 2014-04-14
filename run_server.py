import argparse

from studygroup.application import create_app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs a study group site.')
    parser.add_argument('--port', '-p', action='store', default=80, type=int)
    args = parser.parse_args()

    app = create_app(debug=True)
    app.run(debug=True, port=args.port)
