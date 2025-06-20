How to use:
The script defaults to running the box-cox normalization on the provided "GWAS_Ionomics_Phenotype.txt" data.
Other data and types of normalization can be supplied using this format in the command line:

(program name) (data file name) (test type)

Example Usage:

transformApp/script.py GWAS_Ionomics_Phenotype.txt sqrt

Types of test available:
- Box-Cox
- Square Root
- Logarithmic

Output: 
The program will output a tsv file with the name of the transformation performed. Two histograms will be generated for each trait, showing before and after the transformation. These are stored in subfolders named for each trait in the plots folder.