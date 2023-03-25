sample = input('water or soil:')

    
waterSeqFile = open("water_all_2.txt", "r")
waterSeqFile = waterSeqFile.read()
soilSeqFile = open("soil_all_2.txt", "r")
soilSeqFile = soilSeqFile.read()
readID = input('Enter read ID:')
startPos = int(input('Enter Start Position:'))
stopPos = int(input('Enter Stop Position:'))

findWaterReadID = waterSeqFile.find(readID)
seqStartsAt = findWaterReadID + 36
geneStart = seqStartsAt + startPos
geneStop = seqStartsAt + stopPos
water_gene_seq = waterSeqFile[geneStart : geneStop]
soil_gene_seq = soilSeqFile[geneStart : geneStop]
if sample == 'soil': 
  print(soil_gene_seq)
else:
  print(water_gene_seq)