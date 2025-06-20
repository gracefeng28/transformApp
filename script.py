#import modules
import os
import pandas as pd
from scipy import stats
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import shutil
import sys

#input validation
#should be in the form "[program] [sample file] [type of transformation]"
#if none provided, default to box cox
test_file_name = "GWAS_Ionomics_Phenotype.txt" #default data
normalization_type = "box_cox"
if (len(sys.argv)==3):
    if (os.path.exists(sys.argv[1])):
        test_file_name = sys.argv[1]
    else:
        print("Sorry, please enter a valid input file, or run with default parameters")
        sys.exit()
    if ((sys.argv[2].lower()!= "box_cox" and sys.argv[2].lower()!= "sqrt") and sys.argv[2].lower()!= "log"):
        print("Sorry, please enter a valid transformation type, or run with default parameters")
        sys.exit()
    else:
        normalization_type = sys.argv[2].lower();
if (os.path.isdir("plots/")== False): 
    os.mkdir("plots/")
#uncomment if you want to delete all the plot files
#else: 
    #shutil.rmtree("plots/")
    #os.mkdir("plots/")

#read in sample ionomics data
df = pd.read_csv(test_file_name, delimiter= "\t")
cols = list((df.columns))[1:]

output_tsv = "outputs/" + normalization_type+".tsv"
tsv_header_name = list((df.columns))[0:]
each_row = [df.loc[:,"Genotype ID"]]

def is_continous(filtered_list):
    for elem in filtered_list:
        if (type(elem)== bool):
            return False
        
    return True
def show_plot(old_data,new_data):
    transformed_df = pd.DataFrame({'count':new_data})
    old_df = pd.DataFrame( {'count':old_data})
    sns.displot(old_df)
    sns.displot(transformed_df)
    plt.show()

# save all graphs to folder corresponding with trait
def save_plot(data, data_name,age,transform_type):
    df = pd.DataFrame(data)
    sns.displot(df)
    if (os.path.isdir("plots/"+data_name)!= True):
        os.mkdir("plots/"+data_name)
    plt.savefig("plots/"+data_name + "/" + age+ "_" + data_name+"_" + transform_type +".png")
    plt.close()
    
def run_boxcox(trait):
    data = (list(df.loc[:,str(trait)]))
    #filter out missing values
    filter_nan = [x for x in data if not np.isnan(x)]
    #Box-Cox requires all positive values
    assert(min(filter_nan)>=0)
    #perform box cox transformation
    fitted_data, fitted_lambda = stats.boxcox(filter_nan)
    fitted_data = fitted_data.round(2)
    #show_plot(filter_nan,fitted_data)
    #save plots for old and new
    save_plot(filter_nan, trait,"old","bc")
    save_plot(fitted_data, trait,"new", "bc")
    each_row.append(fitted_data)
    print(f"Lambda value used for Transformation: {fitted_lambda}")


def run_sqrt(trait):
    data = (df.loc[:,str(trait)])
    #filter out missing values
    filter_nan = [x for x in data if not np.isnan(x)]
    #perform square root transformation
    sqrt_output = np.sqrt(filter_nan)
    #show_plot(filter_nan,sqrt_output)
    save_plot(filter_nan, trait,"old", "sqrt")
    save_plot(sqrt_output, trait,"new", "sqrt")
    each_row.append(sqrt_output)

def run_log(trait):
    data = (df.loc[:,str(trait)])
    #filter out missing values
    filter_nan = [x for x in data if not np.isnan(x)]
    #perform square root transformation
    log_output = np.log(filter_nan)
    #show_plot(filter_nan,sqrt_output)
    save_plot(filter_nan, trait,"old", "log")
    save_plot(log_output, trait,"new", "log")
    each_row.append(log_output)
print(f"Performing {normalization_type } transformation on {test_file_name}")
#call transformation for each row
for col in cols:
    #first checks if data is continuous, if not prints to screen
    if (is_continous(col)):
        print("Currently transforming: " +col)
        if (normalization_type == "box_cox"):
            run_boxcox(col)
        elif (normalization_type == "sqrt"):
            run_sqrt(col)
        else:
            run_log(col)
    else:
        print("Could not process the following trait (not continuous): " + col)

#rotate rows to become columns
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

