
#import sample file
import pandas as pd
import numpy as np
from boxcox import run_boxcox 
import numpy as np
import csv



df = pd.read_csv("GWAS_Ionomics_Phenotype.txt", delimiter= "\t")
#print(df.loc[:,"Mo98"])
cols = list((df.columns))[1:]
print(cols)

def run_boxcox(trait_list):
    print(df.loc[:trait_list])

output_tsv = 'box_cox.tsv'
tsv_header_name = ['id', 'firstname', 'lastname', 'age']
each_row = [
    ['1', 'James', 'Moore', '10'],
]
#with open(output_tsv, 'w') as tsvfile:
    #csv writer to write in tsv file
    tsv_writer = csv.writer(tsvfile, delimiter='\t')
    #write header in tsv file
    tsv_writer.writerow(tsv_header_name)
    #write rows
    tsv_writer.writerows(each_row)
    #close csv file
    tsvfile.close()
    pass




for col in cols:
    run_boxcox(col)
    