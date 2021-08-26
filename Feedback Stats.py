import sys
import os
import csv


def main():
    #summary_files = sys.argv[1:]
    summary_files = [r'C:\Users\dan.kemp\Documents\R&D\Feedback Stats\summary.csv']
    # Check input is valid.
    for file in summary_files:
        if os.path.basename(file) != 'summary.csv':
            input('Invalid file detected.\nPlease ensure the input consists '
                  'only of summary.csv files.\n\nPress Enter to quit.')
            return

    # Ask user for event code for use in naming the reports.
    event_code = input('Please enter the event code:\n\n')

    # Extract csv data and return as a list.
    data = extract_csv_data(summary_files)
    if not data:
        input('\nUnexpected CSV format.\nPlease contact technical support.\n\n'
              'Press Enter to quit.')
        return

    # Save a report for each photographer.
    for i in data.keys():
        output_report(event_code, i, data[i])

    input()

def extract_csv_data(files):
    expected_headers = ['Directory', 'Filename', 'BarcodeLocation',
                        'BarcodeCity', 'BarcodeState', 'ProcessRekognition',
                        'Colour', 'Rating', 'Orientation', 'Tags']
    data = {}

    # Iterate over each CSV.
    for file in files:
        print(f'\nReading {os.path.basename(file)}')
        with open(file, 'r', errors='ignore') as f:
            csvreader = csv.reader(f)
            headers = next(csvreader)
            # Check headers are as expected, otherwise return None.
            if headers != expected_headers:
                return
            # Iterate over each row in the CSV.
            for row in csvreader:
                # Using the position of the first Q, retrieve photographer
                # code. If no Q found, or it's in the first 2 indices, ignore.
                q_index = row[1].casefold().find('q')
                if q_index < 2:
                    continue
                photographer = row[1][q_index - 2:q_index + 1]
                # If this is the first instance of this photographer, set up
                # the nested dictionary.
                if not photographer in data:
                    data[photographer] = {
                        'individuals': {
                            'total': 0,
                            'qr_codes': 0,
                            'heads': 0,
                            'blurry': 0,
                            'underexposed': 0
                            },
                        'other': {
                            'total': 0,
                            'blurry': 0,
                            'underexposed': 0
                            }
                        }
                # If this is an inds image, add stats to inds dictionary.
                # Otherwise, add stats to other dictionary.
                if 'i ' in row[1].casefold():
                    data[photographer]['individuals']['total'] += 1
                    if row[6] == 'Green':
                        data[photographer]['individuals']['qr_codes'] += 1
                    elif row[6] == 'Blue':
                        data[photographer]['individuals']['heads'] += 1
                    if 'RekognitionSharpnessFail' in row[9]:
                        data[photographer]['individuals']['blurry'] += 1
                    if 'FilterUnderExposed' in row[9]:
                        data[photographer]['individuals']['underexposed'] += 1
                else:
                    data[photographer]['other']['total'] += 1
                    if 'RekognitionSharpnessFail' in row[9]:
                        data[photographer]['other']['blurry'] += 1
                    if 'FilterUnderExposed' in row[9]:
                        data[photographer]['other']['underexposed'] += 1

    return data

def output_report(event_code, photographer, data):
    print(f'\n{photographer} at {event_code}')
    print('    Individuals:')
    print(f'        Total images: {data["individuals"]["total"]}')
    print(f'        QR code images: {data["individuals"]["qr_codes"]}')
    print(f'        Headshots: {data["individuals"]["heads"]}')
    print(f'        Out of focus images: {data["individuals"]["blurry"]}')
    print(f'        Underexposed images: {data["individuals"]["underexposed"]}')
    print('    Other:')
    print(f'        Total images: {data["individuals"]["total"]}')
    print(f'        Out of focus images: {data["individuals"]["blurry"]}')
    print(f'        Underexposed images: {data["individuals"]["underexposed"]}')
                
if __name__ == '__main__':
    main()

