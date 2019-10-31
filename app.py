import csv
from flask import Flask
from os.path import isfile, join, getsize

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)


def parse_tube_rack_csv(tube_rack_barcode: str) -> str:
    file_to_find = f'{tube_rack_barcode}.csv'
    full_path_to_find = join(app.config['TUBE_RACK_DIR'], file_to_find)
    print(full_path_to_find)

    if isfile(full_path_to_find) and getsize(full_path_to_find) > 0:
        with open(full_path_to_find) as tube_rack_file:
            tube_rack_csv = csv.reader(tube_rack_file, delimiter=',')
            layout = []
            for row in tube_rack_csv:
                postition_dict = {row[0].strip(): row[1].strip()}
                layout.append(postition_dict)
        return {'rack_barcode': tube_rack_barcode, 'layout': layout}
    else:
        return {'error': f'File ({full_path_to_find}) not found'}, 404


@app.route('/tube_rack/<tube_rack_barcode>')
def get_rack_barcode(tube_rack_barcode):
    print(app.config)
    try:
        return parse_tube_rack_csv(tube_rack_barcode)
    except Exception as e:
        return {'error': f'Server error: {e}'}, 500
