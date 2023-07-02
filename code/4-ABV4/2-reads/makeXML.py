import os
from glob import glob

experiment_xml = open('experiment.xml', 'w')
run_xml = open('run.xml', 'w')

experiment_xml.write('<EXPERIMENT_SET>\n')

run_xml.write('<RUN_SET>\n')

# we need to parse out some IDs from the previous results
for line in open('../0-study/RESULTS.xml'):
    if 'PROJECT accession' in line:
        #  <PROJECT accession="PRJEB63551" alias="MT21FEB" status="PUBLIC">
        ll = line.lstrip().split(' ')
        ll = [x.replace('"','') for x in ll]
        study_accession = ll[1].replace('accession=','')
        alias = ll[2].replace('alias=','')

for line in open('../0-study/project.xml'):
    if 'TITLE' in line:
        title = line.lstrip().rstrip()
        break

accessions_aliases = []
for line in open('../1-samples/RESULTS.xml'):
    ll = line.split()
    if '<SAMPLE' in line:
        #['<SAMPLE', 'accession="ERS15947778"', 'alias="TVB_5"', 'status="PRIVATE">']
        accession = ll[1].replace('accession=','').replace('"','')
        alias = ll[2].replace('alias=','').replace('"', '')
        oldalias = alias
        if alias == 'PCV3_NTC':
            alias = 'NTC'

        # get the four files for this alias

        sixteen_f, sixteen_r, mifish_f, mifish_r = False, False, False, False
        for line in open('md5sums.txt'):
            ll = line.split(' ')
            if len(ll) == 1: continue
            MD5 = ll[0]
            filename = ll[-1].rstrip()
            base = os.path.basename(filename)
            if alias in base:
                if 'BadHalf' in base and 'BadHalf' not in alias:
                    continue
                # 6f82dc689f2a3df0306a1d2bd6336b11 DAY1_BC_16S.1.fq.gz
                #b21c9262b861324941cfd89c786f948d DAY1_BC_16S.2.fq.gz
                #1a7cd7bd82dfc99ba71a649035f95983 DAY1_BC_MiFish.1.fq.gz
                #1ae4871f1d9f022d9519b4815d5bfa0b DAY1_BC_MiFish.2.fq.gz
                if '16S.1' in base:
                    sixteen_f = (base, MD5)
                elif '16S.2' in base:
                    sixteen_r = (base, MD5)
                elif 'MiFish.1' in base:
                    mifish_f = (base, MD5)
                elif 'MiFish.2' in base:
                    mifish_r = (base, MD5)
        assert sixteen_f, f'Sixteen F not found for {alias}'
        assert sixteen_r, f'Sixteen R not found for {alias}'

        alias = oldalias


        if mifish_f:
            run_xml.write(f'\t<RUN alias="run_12S_{alias}" center_name="Minderoo Foundation">\n')
            run_xml.write(f'\t\t<EXPERIMENT_REF refname="12S_{alias}"/>\n')
            run_xml.write(f'\t\t<DATA_BLOCK>\n')
            run_xml.write(f'\t\t\t<FILES>\n')
            run_xml.write(f'\t\t\t\t<FILE filename="{mifish_f[0]}" filetype="fastq"\n')
            run_xml.write(f'\t\t\t\t checksum_method="MD5" checksum="{mifish_f[1]}"/>\n')
            run_xml.write(f'\t\t\t\t<FILE filename="{mifish_r[0]}" filetype="fastq"\n')
            run_xml.write(f'\t\t\t\t checksum_method="MD5" checksum="{mifish_r[1]}"/>\n')
            run_xml.write(f'\t\t\t</FILES>\n')
            run_xml.write(f'\t\t</DATA_BLOCK>\n')
            run_xml.write(f'\t</RUN>\n')
        else:
            print(f'MiFish F not found for {alias}')
            print(f'MiFish R not found for {alias}')

        # and now for 16S
        run_xml.write(f'\t<RUN alias="run_16S_{alias}">\n')
        run_xml.write(f'\t\t<EXPERIMENT_REF refname="16S_{alias}"/>\n')
        run_xml.write(f'\t\t<DATA_BLOCK>\n')
        run_xml.write(f'\t\t\t<FILES>\n')
        run_xml.write(f'\t\t\t\t<FILE filename="{sixteen_f[0]}" filetype="fastq"\n')
        run_xml.write(f'\t\t\t\t checksum_method="MD5" checksum="{sixteen_f[1]}"/>\n')
        run_xml.write(f'\t\t\t\t<FILE filename="{sixteen_r[0]}" filetype="fastq"\n')
        run_xml.write(f'\t\t\t\t checksum_method="MD5" checksum="{sixteen_r[1]}"/>\n')
        run_xml.write(f'\t\t\t</FILES>\n')
        run_xml.write(f'\t\t</DATA_BLOCK>\n')
        run_xml.write(f'\t</RUN>\n')


        
        if mifish_f:
            experiment_xml.write(f'\t<EXPERIMENT alias="12S_{alias}">\n')
            experiment_xml.write(f'\t\t{title}\n')
            experiment_xml.write(f'\t\t<STUDY_REF accession="{study_accession}"/>\n')
            experiment_xml.write(f'\t\t\t<DESIGN>\n')
            experiment_xml.write(f'\t\t\t\t<DESIGN_DESCRIPTION>12S MiFish sequencing</DESIGN_DESCRIPTION>\n')
            experiment_xml.write(f'\t\t\t\t\t<SAMPLE_DESCRIPTOR accession="{accession}"/>\n')
            experiment_xml.write(f'\t\t\t\t\t<LIBRARY_DESCRIPTOR>\n')
            experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_NAME/>\n')
            experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_STRATEGY>AMPLICON</LIBRARY_STRATEGY>\n')
            experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_SOURCE>METAGENOMIC</LIBRARY_SOURCE>\n')
            experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_SELECTION>PCR</LIBRARY_SELECTION>\n')
            experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_LAYOUT>\n')
            experiment_xml.write(f'\t\t\t\t\t\t\t<PAIRED/>\n')
            experiment_xml.write(f'\t\t\t\t\t\t</LIBRARY_LAYOUT>\n')
            experiment_xml.write(f'\t\t\t\t\t</LIBRARY_DESCRIPTOR>\n')
            experiment_xml.write(f'\t\t\t</DESIGN>\n')
            experiment_xml.write(f'\t\t\t<PLATFORM>\n')
            experiment_xml.write(f'\t\t\t\t<ILLUMINA>\n')
            experiment_xml.write(f'\t\t\t\t\t<INSTRUMENT_MODEL>NextSeq 2000</INSTRUMENT_MODEL>\n')
            experiment_xml.write(f'\t\t\t\t</ILLUMINA>\n')
            experiment_xml.write(f'\t\t\t</PLATFORM>\n')
            experiment_xml.write(f'\t</EXPERIMENT>\n')

        # and now the 16S
        experiment_xml.write(f'\t<EXPERIMENT alias="16S_{alias}">\n')
        experiment_xml.write(f'\t\t{title}\n')
        experiment_xml.write(f'\t\t<STUDY_REF accession="{study_accession}"/>\n')
        experiment_xml.write(f'\t\t\t<DESIGN>\n')
        experiment_xml.write(f'\t\t\t\t<DESIGN_DESCRIPTION>16S sequencing</DESIGN_DESCRIPTION>\n')
        experiment_xml.write(f'\t\t\t\t\t<SAMPLE_DESCRIPTOR accession="{accession}"/>\n')
        experiment_xml.write(f'\t\t\t\t\t<LIBRARY_DESCRIPTOR>\n')
        experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_NAME/>\n')
        experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_STRATEGY>AMPLICON</LIBRARY_STRATEGY>\n')
        experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_SOURCE>METAGENOMIC</LIBRARY_SOURCE>\n')
        experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_SELECTION>PCR</LIBRARY_SELECTION>\n')
        experiment_xml.write(f'\t\t\t\t\t\t<LIBRARY_LAYOUT>\n')
        experiment_xml.write(f'\t\t\t\t\t\t\t<PAIRED/>\n')
        experiment_xml.write(f'\t\t\t\t\t\t</LIBRARY_LAYOUT>\n')
        experiment_xml.write(f'\t\t\t\t\t</LIBRARY_DESCRIPTOR>\n')
        experiment_xml.write(f'\t\t\t</DESIGN>\n')
        experiment_xml.write(f'\t\t\t<PLATFORM>\n')
        experiment_xml.write(f'\t\t\t\t<ILLUMINA>\n')
        experiment_xml.write(f'\t\t\t\t\t<INSTRUMENT_MODEL>NextSeq 2000</INSTRUMENT_MODEL>\n')
        experiment_xml.write(f'\t\t\t\t</ILLUMINA>\n')
        experiment_xml.write(f'\t\t\t</PLATFORM>\n')
        experiment_xml.write(f'\t</EXPERIMENT>\n')

experiment_xml.write(f'</EXPERIMENT_SET>\n')
run_xml.write('</RUN_SET>\n')
