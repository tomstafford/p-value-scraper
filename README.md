# p-value-scraper
extracts p values from .pdf .doc or .docx files in a folder/subfolder

1. Put make_pcurve.py in a folder

2. In a subfolder / subfolders place document files containing reports of p values (these can be .doc .docx or .pdf files)

3. Install python 3 and python-docx and textract

See:
https://python-docx.readthedocs.io/en/latest/user/install.html
 http://textract.readthedocs.io/en/stable/installation.html
 
 if you are using pip then 
 
<code> pip3 install python-docx
<code> pip3 install textract
 
 should work
 
 4. run make_pcurve.py
 
 e.g. from the command line

<code> python3 make_pcurve.py
 
 5. Enjoy the output and hopefully the data will be saved in a CSV file pvalues.csv