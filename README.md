## Structure

    ├── README.md
    ├── email
    │   └── user_email.list
    ├── flask
    ├── papers
    │   └── 2016-01-05
    │       └── cs.cv
    └── spider

 - [x] email folder include the scripts of send emails to users
 - [x] flask folder include the scripts of our web interface
 - [x] papers folder include the paper we get from arxiv.com, named by data-time, and the subfolder in the folder of date-time is the research area such as cs.cv
 - [x] spider include the scripts to scrawl the papers from arxiv.

### The link with the research area

[https://arxiv.org/list/cs.CV/pastweek?skip=0&show=1000](https://arxiv.org/list/cs.CV/pastweek?skip=0&show=1000)


### Sqite Data (no support now)

| user_id | user_nickname | user_email | subject |
| ------| ------ | ------ | ------|
| 1 | hello | hello@hello.com | cs_cv |
| 2 | hello | hello@hello.com | cs_kl |
| 3 | hello2| hello2@hello.com| cs_cv |


### TODO
 - [x] extract the information of the pdf
 - [x] add the support of multi thread to download pdfs
 - [x] add the config of the url including research area
 - [x] add the module to write the all paper info to a file in the pdf folder 'summary.csv'
    - [] add the support of filter the download failed files in the summary.csv
 - [x] add the email to format the area email to the users
 - [x] add the flask module including add the user email
 - [x] add the module that python read the pdf files, detailed in [Python读取PDF内容](https://zhuanlan.zhihu.com/p/20910680)
 - [] replace the write file to sqite data
    - [] replace write_file with write_sqite_file
    - [] replace the run() in deploy_email and deploy_download_pdfs.py to be sqite version
 - [] add the module of the paper recommendation


### How to deploy

 - `deploy_download_pdfs.py`: Scrapy the pdfs each week according the user_info.csv
 - `deploy_email.py`: Send the emails





 