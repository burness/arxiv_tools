## Structure

    ├── README.md
    ├── email
    │   └── user_email.list
    ├── flask
    ├── papers
    │   └── 2016-01-05
    │       └── cs.cv
    └── spider

 - [] email folder include the scripts of send emails to users
 - [] flask folder include the scripts of our web interface
 - [] papers folder include the paper we get from arxiv.com, named by data-time, and the subfolder in the folder of date-time is the research area such as cs.cv
 - [] spider include the scripts to scrawl the papers from arxiv.

### the link with the research area

[https://arxiv.org/list/cs.CV/pastweek?skip=0&show=1000](https://arxiv.org/list/cs.CV/pastweek?skip=0&show=1000)

```
https://arxiv.org/list//pastweek?skip=0&show=1000

```
### Sqite Data

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
 - [] add the module that python read the pdf files [Python读取PDF内容](https://zhuanlan.zhihu.com/p/20910680)
 - [] add the module of the paper recommendation


### How to deploy

 - Scrapy the pdfs each week according the user_info.csv
 - Send the emails

deploy.py





 