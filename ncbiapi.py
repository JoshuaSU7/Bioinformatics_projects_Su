import requests
import pandas as pd
import time
from collections import OrderedDict
import json

api_url_example = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=XXX&id=XXXXXX&rettype=XXXXX'

api_key = '151f13fc99980906479f7830b615184ccb08'

'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=6103&format=json' #first link that was used to find chromosome info about RGPR gene (or any gene ID)



print('separate all words with an underscore.\n')
time.sleep(0.5)

term = input("enter condition here: ")
retmax = int(input("number of genes to compare (integer value): "))
print(retmax)


getGeneIds = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term='+term+'&sort=relevance&retmax='+str(retmax)+'&format=json&api_key=151f13fc99980906479f7830b615184ccb08').json()

geneIdListRaw = getGeneIds['esearchresult']['idlist']
print(geneIdListRaw)
global df
global chromloc
chromloc = []
df = pd.DataFrame() #first dataframe

def geneIdInformation(): 
    for i in range(retmax):
        gene_information = geneIdListRaw[i] #raw ID of each gene
        getGeneInformation = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id='+gene_information+'&format=json&api_key=151f13fc99980906479f7830b615184ccb08').json()
        gene_name = getGeneInformation['result'][gene_information]['name'] #name of gene
        gene_chromosome = getGeneInformation['result'][gene_information]['chromosome'] #chromosome gene is located on
        gene_mapLoc = getGeneInformation['result'][gene_information]['maplocation'] #chromosome gene is located on
        #format data

        try:
            gene_nucStart = getGeneInformation['result'][gene_information]['genomicinfo'][0]['chrstart'] #where nucleotides start for the gene on the chromosome
            gene_nucStop = getGeneInformation['result'][gene_information]['genomicinfo'][0]['chrstop'] #where nucleotides stop for the gene on the chromosome
            gene_exonCount = getGeneInformation['result'][gene_information]['genomicinfo'][0]['exoncount'] #exon count
        except:
            gene_nucStart = -1
            gene_nucStop = -1
            gene_exonCount = -1
        else:
            gene_nucStart = getGeneInformation['result'][gene_information]['genomicinfo'][0]['chrstart'] 
            gene_nucStop = getGeneInformation['result'][gene_information]['genomicinfo'][0]['chrstop']
            gene_exonCount = getGeneInformation['result'][gene_information]['genomicinfo'][0]['exoncount'] 
        #gene_nucLength = gene_nucStart - gene_nucStop
        chromloc.append(gene_chromosome)
        df.at[i, 'Gene_Name'] = gene_name
        df.at[i, 'ChromosomeLocation'] = gene_chromosome
        df.at[i, 'Gene_ID'] = gene_information
        df.at[i, 'Gene_Map_Location'] = gene_mapLoc
        df.at[i, 'Nucleotides_Start_At'] = gene_nucStart
        df.at[i, 'Nucleotides_Stop_At'] = gene_nucStop
        #df.at[i, 'Nucleotide length'] = gene_nucLength
        df.at[i, 'Exon Count'] = gene_exonCount

        #df.at[i, 'Nucleotides Start'] = gene_nucStart
        #df.at[i, 'Nucleotides Stop'] = gene_nucStop
        time.sleep(0.25)

geneIdInformation()


def dataSort(df):
    df_filtered = df[(df['ChromosomeLocation'] != '') & (df['Gene_Map_Location'] != '')] # can add more conditions later
    print(df_filtered)
    print(df_filtered.ChromosomeLocation.value_counts())
    return df_filtered
dataSort(df)



#12/24: sorted chromosome locations
#need to get corresponding data back from all the genes in a certain subset of the chromosome locations - get ID of all genes in the subset to perform analysis.
#maybe separate getgeneinformation() into two methods, one for api call, other for df
#then can call getgeneinformation() again, and make it return chromosome location and name
#set if statement to if chromosome location == one in subset, add that gene id to a new list. 
#focus on only one subset tomorrow if extra time, work on performing lines 54-56 for all subsets of data.

#Machine learning possibilities: 
#identify existing genes, but not yet associated to the disease, that could impact the disease in some way, based on function, location, other factors
#possibly do genotype to phenotype predictions

#12/24: added more information to the table as well as try/catch block to stop errors. Will email ms bliss about project and if identifying existing genes at similar loci makes sense


        