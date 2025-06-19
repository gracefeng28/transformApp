
#import modules
import pandas as pd
from scipy import stats

import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("GWAS_Ionomics_Phenotype.txt", delimiter= "\t")
print(df.columns)
cols = list((df.columns))[1:]

#print(cols)
output_tsv = 'box_cox.tsv'
tsv_header_name = list((df.columns))[0:]
each_row = [df.loc[:,"Genotype ID"]]
def run_boxcox(trait):
    data = (list(df.loc[:,str(trait)]))
    #filter out missing values
    filter_nan = [x for x in data if not np.isnan(x)]
    #perform box cox transformation
    fitted_data, fitted_lambda = stats.boxcox(filter_nan)
    fitted_data = fitted_data.round(2)
    transformed_df = pd.DataFrame({'count':fitted_data})
    old_df = pd.DataFrame( {'count':filter_nan})
    sns.displot(old_df)
    sns.displot(transformed_df)
    
    
    plt.show()
    each_row.append(fitted_data)
    print(f"Lambda value used for Transformation: {fitted_lambda}")




#with open(output_tsv, 'w') as tsvfile:
    #csv writer to write in tsv file
    #tsv_writer = csv.writer(tsvfile, delimiter='\t')
    #write header in tsv file
    #tsv_writer.writerow(tsv_header_name)
    #write rows
    #tsv_writer.writerows(each_row)
    #close csv file
    #tsvfile.close()
    #pass


for col in cols:
    print(col)
    run_boxcox(col)
each_row_df = pd.DataFrame(each_row)

each_row_df=each_row_df.transpose()

with open(output_tsv, 'w') as tsvfile:
    #csv writer to write in tsv file
    tsv_writer = csv.writer(tsvfile, delimiter='\t')
    #write header in tsv file
    tsv_writer.writerow(tsv_header_name)
    #write rows
    tsv_writer.writerows(each_row_df.values.tolist())
   
    #close csv file
    tsvfile.close()
    pass
