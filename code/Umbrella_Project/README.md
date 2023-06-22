copy pasted from https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#create-an-umbrella-study

i removed HoldUntilDates and replaced by RELEASE for immediate release


curl -u   'pbayer@minderoo.org':'PASSWORD'  -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella_project.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/" > RESULTS.xml

Replace PASSWORD by password.
