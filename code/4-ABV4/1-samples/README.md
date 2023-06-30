
we need to write the XML for the sample submission


python writeXML.py > sample.xml

weirdly enough, the bioproject is not linked here! we link the bioproject when we upload the reads. why

curl -u 'pbayer@minderoo.org':PASSWORD  -F "SUBMISSION=@submission.xml" -F "SAMPLE=@sample.xml" https://www.ebi.ac.uk/ena/submit/drop-box/submit/ > RESULTS.xml

ok now we need the RESULTS.xml sample IDs to upload the reads and link the samples
