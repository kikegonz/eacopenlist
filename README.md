**Electronics & Computers OpenList.org**
====================================

***eacopenlist.org*** is an open source project with the aim of maintain a database of all the electronical stuff like mobile cells, laptops, tablets, etc. and all its features.

The goal is to keep the information open and available in a standard or well-known format to any person or organization. The list could be the cornerstone for all sort of big data applications at the service of the users in order to improve buyers decisions.


**How do we get the information**
-----------------------------
At the end of phase 1 (see below the project plan) we'll take it via web crawling and information retrieval processes from vendors and e-commerce websites. Below you have the processes we follow to take and store the information

 - To Take.
	 - eacopenlistbot. Outfit of ***scrapy*** web spiders searching products sites at the most important vendor or e-commerce sites
		 - Input. product sites
		 - Output. CSV files with thress columns. Vendor, product web site title and product web site body.
 - To Analize.
	 - Informational retrieval process based on ***NLTK*** relation extraction process.
		 - Input. CSV files generated at the "to take" process
		 - Output. CSV file with the columns vendor, product, feature1, feature2 ...
 - To save
	 - PostgreSQL database where we store the information after a validation process based on the CPE  Name Matching Specification processes.
		 - Input. CSV file from the "To analize" process
		 - Output. Information saved at a relation database in PostgreSQL.

At the end of phase 2 (below) everyone would be expected to be able to add or edit product information  through a web platform and a collaborative framework.

**Project Plan**
---------------

 - Phase 1. Background bots and database processes
	 - End expected at earlier 2017
	 - Goals:
		 - Web spiders
		 - Corpus files required to  the machine learning process of information retrieval
		 - Database design
		 - CPE  Name Matching Specification processes to manage the information saved at the database
 - Phase 2. WEB Frontend.
	 - End expected at later 2017
	 - Goals:
		 - Project corporate image
		 - WEB site
		 - Collaborative framework

To know how to participate at the project please read the CONTRIBUTING.md file


**License**
-------

All the source code is under the [GPL GNU](http://www.gnu.org/licenses/gpl.html) license.
The information contained at the database is under the [Open Database License](http://opendatacommons.org/licenses/odbl/1.0/)

