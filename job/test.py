import pandas as pd

plate = pd.read_csv('../object/plate.csv')
plate_new = plate[plate['enable'] != 'n']
print(plate_new)
