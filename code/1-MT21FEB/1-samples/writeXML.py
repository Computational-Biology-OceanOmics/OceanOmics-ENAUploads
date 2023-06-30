
from datetime import datetime
from glob import glob
import pandas as pd
import os

#checklist https://www.ebi.ac.uk/ena/browser/view/ERC000011
for l in glob('/data/analysed_data/OceanOmics/amplicon/new_demux_runs/MT21FEB_amplicon_analysis/06-report/*rds'):
    # in this case, the csv files are identical - parse only the first one
     os.popen(f'Rscript -e \'library("phyloseq"); write.csv(as.data.frame(sample_data(readRDS("{l}"))@.Data, col.names=sample_data(readRDS("{l}"))@names, row.names=sample_data(readRDS("{l}"))@row.names), "{os.path.basename(l)}.csv")\'').read()
     break


print('<?xml version="1.0" encoding="UTF-8"?>')
print('<SAMPLE_SET>')


# now parse the CSVs and write the right XML
for l in glob('*csv'):
    with open(l) as fh:
        for line in fh:

            ll = line.rstrip().split(',')
            ll = [x.replace('"','') for x in ll]
            if ll[0] == '':
                header = ll
                continue
            
            #"","Sites","Atoll","Environment","Replicate.ID","Latitude","Longitude","Year","Month"
            #"DAY1_BC",NA,"Thevenard","Day1","BC",NA,NA,2021,"February"

            # should become 
            # *sample_name  sample_title    bioproject_accession    *organism   host    isolation_source    *collection_date    *geo_loc_name   *lat_lon    ref_biomaterial rel_to_oxygen   samp_collect_device samp_mat_process    samp_size   source_material_id  description site_depth  control_sample  replicate_id    collection_time sample_depth    sample_temperature  filtration_device   pumping_device
            #RS1_ME_S1_1         marine metagenome       Ocean water sample  7-Aug-21    Australia: Indian Ocean, Rowley Shoals, Mermaid 17.0657084754 S 119.649665671 E     aerobe  Niskin sampler, manual      1l          5   FALSE   1   11:02   4   25  0.45 micron filter  Grover pump


            sample_name = ll[0]
            bioproject_accession = 'PRJEB63551'
            organism = 'marine metagenome'
            isolation_source = 'Ocean water sample'
            organism_id = '408172'
            thissite = ll[1]
            geo_loc_name = f'Australia: Indian Ocean, Montebello Islands, {ll[2]}'
            location = 'Indian Ocean'
            replicate_id = ll[4]

            collection_time = 'NA'
            if 'NA' in ll[-1]:
                collection_date = 'missing: control sample'
            else:
                month = datetime.strptime(ll[-1], '%B').month
                if month < 10:
                    month = f'0{month}'
                else:
                    month = f'{month}'
                collection_date = f'{ll[-2]}-{month}-01'
            latitude = ll[5]
            longitude = ll[6]
            rel_to_oxygen = 'aerobe'
            samp_collect_device = 'Niskin sampler, manual'
            samp_size = '1l'
            site_depth = 'NA'
            control_sample = 'FALSE'
            if latitude == 'NA':
                control_sample = 'TRUE'
            collection_time = 'NA'
            sample_depth = 'NA'
            sample_temperature = 'NA'
            filtration_device = 'Grover pump'

            print(f'\t<SAMPLE alias="{sample_name}" center_name="Minderoo Foundation">')
            print('\t<TITLE>Metagenome or environmental sample from marine metagenome</TITLE>')
            print('\t<SAMPLE_NAME>')
            print('\t\t<TAXON_ID>408172</TAXON_ID>')
            print('\t\t<SCIENTIFIC_NAME>marine metagenome</SCIENTIFIC_NAME>')
            print('\t\t<COMMON_NAME></COMMON_NAME>')
            print('\t</SAMPLE_NAME>')
            print(f'\t<DESCRIPTION>{ll[1]}</DESCRIPTION>')

            print('\t<SAMPLE_ATTRIBUTES>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>collection date</TAG>')
            print(f'\t\t\t<VALUE>{collection_date}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>filtration_device</TAG>')
            print(f'\t\t\t<VALUE>{filtration_device}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')


            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>environmental package</TAG>')
            print(f'\t\t\t<VALUE>water</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>rel_to_oxygen</TAG>')
            print(f'\t\t\t<VALUE>aerobe</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>replicate_id</TAG>')
            print(f'\t\t\t<VALUE>{replicate_id}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>organism</TAG>')
            print(f'\t\t\t<VALUE>marine metagenome</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>geographic location (country and/or sea)</TAG>')
            print(f'\t\t\t<VALUE>{location}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>geo_loc_name</TAG>')
            print(f'\t\t\t<VALUE>{geo_loc_name}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>control_sample</TAG>')
            print(f'\t\t\t<VALUE>{control_sample}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>isolation_source</TAG>')
            print(f'\t\t\t<VALUE>Ocean water sample</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>geographic location (latitude)</TAG>')
            print(f'\t\t\t<VALUE>{latitude}</VALUE>')
            print('\t\t\t<UNITS>DD</UNITS>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>geographic location (longitude)</TAG>')
            print(f'\t\t\t<VALUE>{longitude}</VALUE>')
            print('\t\t\t<UNITS>DD</UNITS>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>environment (biome)</TAG>')
            print(f'\t\t\t<VALUE>{ll[3]}</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t\t<SAMPLE_ATTRIBUTE>')
            print('\t\t\t<TAG>ENA-CHECKLIST</TAG>')
            print('\t\t\t<VALUE>ERC000011</VALUE>')
            print('\t\t</SAMPLE_ATTRIBUTE>')

            print('\t</SAMPLE_ATTRIBUTES>')
            print('\t</SAMPLE>')


print('</SAMPLE_SET>')
