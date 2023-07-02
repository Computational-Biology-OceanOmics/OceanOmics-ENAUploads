
from datetime import datetime
from glob import glob
import pandas as pd
import os

#checklist https://www.ebi.ac.uk/ena/browser/view/ERC000011
# CHANGEME
for l in glob('/data/analysed_data/OceanOmics/amplicon/new_demux_runs/RS19_amplicon_analysis/06-report/*rds'):
    # in this case, the csv files are identical - parse only the first one
     os.popen(f'Rscript -e \'library("phyloseq"); write.csv(as.data.frame(sample_data(readRDS("{l}"))@.Data, col.names=sample_data(readRDS("{l}"))@names, row.names=sample_data(readRDS("{l}"))@row.names), "{os.path.basename(l)}.csv")\'').read()
     break


out = open('sample.xml', 'w')
out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
out.write('<SAMPLE_SET>\n')


# now parse the CSVs and write the right XML
for l in glob('*csv'):
    with open(l) as fh:
        for line in fh:

            ll = line.rstrip().split(',')
            ll = [x.replace('"','') for x in ll]
            if ll[0] == '':
                header = ll
                continue
            
            # ['', 'Sites', 'Atoll', 'Environment', 'Replicate.ID', 'Latitude', 'Longitude', 'Year', 'Month']
            # ['C13_A', 'C13 BT', 'Clerke', 'Lagoon', '1', '-17.312342', '119.36798', '2019', 'October']

            # should become 
            # *sample_name  sample_title    bioproject_accession    *organism   host    isolation_source    *collection_date    *geo_loc_name   *lat_lon    ref_biomaterial rel_to_oxygen   samp_collect_device samp_mat_process    samp_size   source_material_id  description site_depth  control_sample  replicate_id    collection_time sample_depth    sample_temperature  filtration_device   pumping_device
            #RS1_ME_S1_1         marine metagenome       Ocean water sample  7-Aug-21    Australia: Indian Ocean, Rowley Shoals, Mermaid 17.0657084754 S 119.649665671 E     aerobe  Niskin sampler, manual      1l          5   FALSE   1   11:02   4   25  0.45 micron filter  Grover pump


            sample_name = ll[0]
            if sample_name == 'NTC':
                sample_name = 'RS19_NTC'
            bioproject_accession = 'PRJEB63677' #CHANGEME
            organism = 'marine metagenome'
            isolation_source = 'Ocean water sample'
            organism_id = '408172'
            thissite = ll[1]
            geo_loc_name = f'Australia: Indian Ocean, Rowley Shoals Islands, {ll[2]}'
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
            #collection_date = 'not collected'
            latitude = ll[5]
            longitude = ll[6]
            rel_to_oxygen = 'aerobe'
            samp_collect_device = 'Niskin sampler, manual'
            samp_size = '1l'
            #site_depth = ll[-1]
            site_depth = 'NA'
            control_sample = 'FALSE'
            if latitude == 'NA':
                control_sample = 'TRUE'
            collection_time = 'NA'
            sample_depth = 'NA'
            sample_temperature = 'NA'
            filtration_device = 'Grover pump'

            out.write(f'\t<SAMPLE alias="{sample_name}" center_name="Minderoo Foundation">\n')
            out.write('\t<TITLE>Metagenome or environmental sample from marine metagenome</TITLE>\n')
            out.write('\t<SAMPLE_NAME>\n')
            out.write('\t\t<TAXON_ID>408172</TAXON_ID>\n')
            out.write('\t\t<SCIENTIFIC_NAME>marine metagenome</SCIENTIFIC_NAME>\n')
            out.write('\t\t<COMMON_NAME></COMMON_NAME>\n')
            out.write('\t</SAMPLE_NAME>\n')
            out.write(f'\t<DESCRIPTION>{ll[1]}</DESCRIPTION>\n')

            out.write('\t<SAMPLE_ATTRIBUTES>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>collection date</TAG>\n')
            out.write(f'\t\t\t<VALUE>{collection_date}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>filtration_device</TAG>\n')
            out.write(f'\t\t\t<VALUE>{filtration_device}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')


            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>environmental package</TAG>\n')
            out.write(f'\t\t\t<VALUE>water</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>rel_to_oxygen</TAG>\n')
            out.write(f'\t\t\t<VALUE>aerobe</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>replicate_id</TAG>\n')
            out.write(f'\t\t\t<VALUE>{replicate_id}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>organism</TAG>\n')
            out.write(f'\t\t\t<VALUE>marine metagenome</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>geographic location (country and/or sea)</TAG>\n')
            out.write(f'\t\t\t<VALUE>{location}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>geo_loc_name</TAG>\n')
            out.write(f'\t\t\t<VALUE>{geo_loc_name}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>control_sample</TAG>\n')
            out.write(f'\t\t\t<VALUE>{control_sample}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>isolation_source</TAG>\n')
            out.write(f'\t\t\t<VALUE>Ocean water sample</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>geographic location (latitude)</TAG>\n')
            out.write(f'\t\t\t<VALUE>{latitude}</VALUE>\n')
            out.write('\t\t\t<UNITS>DD</UNITS>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>geographic location (longitude)</TAG>\n')
            out.write(f'\t\t\t<VALUE>{longitude}</VALUE>\n')
            out.write('\t\t\t<UNITS>DD</UNITS>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>environment (biome)</TAG>\n')
            out.write(f'\t\t\t<VALUE>{ll[3]}</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t\t<SAMPLE_ATTRIBUTE>\n')
            out.write('\t\t\t<TAG>ENA-CHECKLIST</TAG>\n')
            out.write('\t\t\t<VALUE>ERC000011</VALUE>\n')
            out.write('\t\t</SAMPLE_ATTRIBUTE>\n')

            out.write('\t</SAMPLE_ATTRIBUTES>\n')
            out.write('\t</SAMPLE>\n')

out.write('</SAMPLE_SET>\n')

for x in glob('*csv'):
    os.popen(f'rm {x}')
