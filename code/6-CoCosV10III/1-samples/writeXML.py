
from datetime import datetime
from glob import glob
import pandas as pd
import os

#checklist https://www.ebi.ac.uk/ena/browser/view/ERC000011
# CHANGEME
for l in glob('/data/analysed_data/OceanOmics/amplicon/new_demux_runs/CoCosV10III_amplicon_analysis/06-report/*rds'):
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
            
            # ['', 'voyage_id', 'sampling_method...2', 'site_id', 'replicate_id', 'vial_id', 'sampling_date', 'time_start_local', 'time_end_local', 'X_latitude_d', 'X_latitude_m', 'X_longitude_d', 'X_longitude_m', 'latitude_dd', 'longitude_dd', 'site_depth_m', 'sample_depth_m', 'swell_m', 'wind_kt', 'sampling_method...20', 'filtration_device', 'volume_filtered_L', 'sampling_comments', 'sampling_personnel', 'digestion_date', 'digestion_personnel', 'extraction_date', 'extraction_personnel', 'lab_comments', 'water_rinse_control', 'water_DI_control', 'bleach_control', 'extraction_blank', 'no_template_control', 'project', 'eDNA_template_plate', 'qPCR_plate']
            # ['V10_CKI_N_68_3', 'V10_CKI', 'N', '68', '3', 'N_68_3', '7/12/2022', '35460', 'NA', 'NA', 'NA', 'NA', 'NA', '-12.118923', '96.825165', '6.8', '5', '1', '15', 'manual niskin', 'sentino peristaltic', '2', 'Med complexity. Close to island and sand bank.', 'ER/ST', 'NA', 'NA', 'NA', 'NA', 'NA', 'V10_CKI_N_68_WC', 'V10_CKI_N_68_DI', 'V10_CKI_BC_17', 'NA', 'NA', 'NA', 'NA', 'NA']


            sample_name = ll[0]
            if sample_name == 'NTC':
                sample_name = 'RS19_NTC'
            bioproject_accession = 'PRJEB63678' #CHANGEME
            organism = 'marine metagenome'
            isolation_source = 'Ocean water sample'
            organism_id = '408172'
            thissite = ll[1]
            geo_loc_name = f'Australia: Indian Ocean, Rowley Shoals Islands, {ll[2]}'
            location = 'Indian Ocean'
            replicate_id = ll[4]

            collection_time = ll[7]
            if 'NA' in ll[6]:
                collection_date = 'missing: control sample'
            else:
                day, month, year = ll[6].split('/')
                if int(day) < 10:
                    day = f'0{day}'
                collection_date = f'{year}-{month}-{day}'
            #collection_date = 'not collected'
            latitude = ll[13]
            longitude = ll[14]
            rel_to_oxygen = 'aerobe'
            samp_collect_device = 'Niskin sampler, manual'
            samp_size = '1l'
            site_depth = ll[15]
            control_sample = 'FALSE'
            if latitude == 'NA':
                control_sample = 'TRUE'
            collection_time = ll[7]
            sample_depth = ll[16]
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
