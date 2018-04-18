import pandas as pd
import numpy as np
import argparse
import os


def align(file, droptime):
    if not os.path.isfile(file):
        print("File not found.")
        return

    try:
        data = pd.read_csv(file, header=1)
    except:
        print("Wrong file type. Try again with a .csv file.")
        return

    try:
        data = data.drop(0)
        if (droptime):
            data = data.drop(["Time", "Stress.5", "Strain.5"], axis=1)
        else:
            data = data.drop(["Stress.5", "Strain.5"], axis=1)

        data = data.fillna(0)
        data = data.astype(float)

        maxes = []
        for col in data:
            if col.startswith('Stress'):
                print(data[col].idxmax())
                print(data[col].max())
                maxes.append(data[col].idxmax())

        output = data.copy(deep=True)

        for idx, col in enumerate(data):
            if col.startswith('Stress'):
                d = pd.DataFrame(np.zeros((max(maxes) - maxes[idx//2], )))
                print(d.shape)
                output[col] = pd.concat([d, output[col]], ignore_index=True)
            elif col.startswith('Strain'):
                output[col] = pd.concat([d, output[col]], ignore_index=True)

        output.to_csv("aligned.csv", encoding='utf-8', index=False)

    except:
        raise

    print("Finished aligning. See aligned.csv for results.")

def main():
    parser = argparse.ArgumentParser(description='Aligns data by max value and adds zero padding as necessary.')
    parser.add_argument('--file', help='CSV file to be aligned.')
    parser.add_argument("--timecol", help="If the first col is time.",
                    action="store_true")
    args = parser.parse_args()
    align(file=args.file, droptime=args.timecol)

if __name__ == '__main__':
    main()
