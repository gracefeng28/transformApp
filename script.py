
#import sample file
import pandas as pd
df = pd.read_csv("GWAS_Ionomics_Phenotype.txt", delimiter= "\t")
#print(df.loc[:,"Mo98"])
cols = list((df.columns))[1:]
print(cols)

for col in cols:
    output = run_boxcox(col)