

**Contributing to eacopenlist.org**
===============================


**Thank you for thinking of helping us**. We need your support at the points referenced at this document. The project is at early phase but we are not asking for help for every point waiting to be developed. In spite of that we would like to focus your efforts to the following points to take ordered steps. So, please, read the current document always before to start any task and choose whatever you like. Every support is welcome and kindly appreciated

**Web crawling**
------------

 1. Completing the spiders already created with all the products categories:
	 - Cells
	 - Tablets
	 - Laptops
	 - Desktops
	 - Digital_Photo
	 - Digital_Video
 2. Creating more spiders for e-commerce and vendors web sites

If you don't know ***scrapy*** we suggest you to start with this [tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html). 

All the spiders should: 

 - Be included at *eacopenlist/eacopenlistbot/eacopenlistbot/spiders*
 - Follow the *0_template.py* estructure 
 - Generate the output csv file with the fields
	 - Product: It use to be the page title
	 - Vendor
	 - Default: the features table or text field

In case of modifications in the scrapy settings file take care of **crawling responsibly**.

 - Respect robots.txt
 - Identify eacopenlist.org at the user-agent field
 - Use polite delay between HTTP GET's in order to not to convert the spider in a DOS attack


**Information retrieval process**
-----------------------------

***[NLTK](http://www.nltk.org/)*** is the python tool we are using to perform an information retrieval process to take from the scraped sites information of vendor, product and features. For this process we are developing a [conll](http://ifarm.nl/signll/conll/) based corpus. 

We need you to add pos and iob tags to the  file eacopenlist/chunker/conlleac/trainer_default. You will see the different tags at eacopenlist/chunker/conlleac/readme.

You can find the IR source code at eacopenlist/chunker/chunker_rel_extractor.py.

You can evaluate your trainer_default file dividing its content between files trainer_default_test and trainer_default_train and using eacopenlist/chunker/chunker_evaluation.py.

**How to patch eacopenlist.org**
----------------------------
Please refer to [this procedure](https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project)  to know how to contribute to eacopenlist.org project

Tools and dependencies:

 - Scrapy
 - NLTK
	 - Punkt Tokenizer Model
	 - maxent_treebank_pos_tagger
	 - maxent_ne_chunker
 - Beautifulsoup


**Suggestions and Mailing List**
----------------------------

Mailing list and other resources pending hosting at ourproject.org




