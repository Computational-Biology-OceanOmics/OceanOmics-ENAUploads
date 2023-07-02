https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html

I made a file called md5sums.txt that has all the reads md5sums:
for filename in FOLDER/\*;
do md5sum $filename
done > md5sums.txt

use upload.sh to upload the reads to ENA

use makeXML.py to write the two xml files


curl -u 'pbayer@minderoo.org':'PW' -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@experiment.xml" -F "RUN=@run.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/" > RESULTS.xml
