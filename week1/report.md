Steps:

Firtly, I cloned the repository and ran the program against the data after unzipping it. Next, I created the folder structure as requested and did my inital push to my github repo. However, the workflow had initially failed and I soon realized that there were indentation errors in the given actions.yml file. 

I spent the next few days scratching my head as to why my results weren't the same as the results table in the reference github repo and figured out that we were not actually given a reference genome to compare our results to. After being told to work on the N50 instead, I learnt what an N50 is and coded it up. 

Lastly, I read the documentation of Codon and converted the Python files to a codon compatible one making it as a separate copy. I utilized the help of AI to convert the code as I never worked with Codon before this. Moreover, I worked on creating my evaluate.sh, which is just runs the Python and Codon files against each dataset, calculating its runtime and N50. The N50 was also embedded in the file as per the instructor's request.

Gotchas:

I was stuck on the headlines of the results for a long time, only to realize that the assignment did not give a reference genome and I was also led to the report.pdf when I had initially inquired about it which had no explanation of any sorts.

Datasets, especially data4, takes a long time to run and especially when you've just changed a little bit of your program, waiting for each run to finish is very time consuming.