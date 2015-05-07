# BigApple
Web Search Engine


NYU School of Engineering Computer Science and Engineering CS 6913,spring - 15		                		  		
Searching the Big Apple

Submission Details:
GitHub links: code is maintained in two separate GitHub links, as Front end and backend are deployed on AWS server to allow us to have more ease of access.
Front End: Developed in Android framework. 
			Link: https://github.com/ktv205/bigapplesearch
	Back End: Developed in Python and PHP.
			Link: https://github.com/avk287/BigApple
	Full code is also submitted in zip files through New Classes.

Development Environment: 
•	Front End is developed in Android Framework.
•	Backend – Crawling, indexing files is done using Python.
•	Python Apps are deployed on AWS server (public and live running) using flask API.
•	PHP databases are used to store MTA and Citi Bike travel Details.
•	Restaurant details are queried using Yelp API and also web crawled whenever required. 
•	NYC open data for Restaurant inspection details are indexed to scale performance issues.

 Application Features:  
•	Searching the best restaurant’s based on user’s current location.
•	Searching the restaurants based on its name.
•	Displays yelp rating and violation score (as inspected by NYC Govt). For each of the restaurants.
•	 Displays nearby MTA train and Citi bikes details to commute to restaurant.
•	 Displays type and distance to the restaurant location.

Technical Specification Achieved:
•	Indexing large data sets – NYC restaurant inspection results.
 
•	Android based application as front end - Deployed the Application on AWS server and made available for public.
•	Web crawling to fetch results like Price and rating from yelp.
•	Python app integrated with flask and deployed on AWS server.
•	Location based best restaurant results are showcased.
•	Location based best transportation are showcased.
o	Both Citi bikes and MTA train details.
•	Maps – are also included for better user interface.
•	Dealt with 4 different types of Data – Citi bikes data(API), MTA train Data , NYC open data for restaurants , Yelp – Restaurant Data (API)

•	Nearby - Restaurant Details-showcased 
o	Distance
o	Yelp Rating
o	Violation score
o	Violation codes
o	Yelp link
o	Phone Number
o	Map Based Navigation and direction to respective restaurant

•	Nearby - Citi Bike – Details – showcased – 
o	Service available or not.
o	Distance from current location
o	Map based Navigation and location details
o	Number of bikes
o	Citi bike – customer care website and phone number details

•	Nearby - MTA Train – details – showcased –
o	MTA Station name
o	Distance from current location
o	Trains available
o	Map based Navigation and location details
o	MTA – customer care website and phone number details

•	Database and storage  - Used flat file based for NYC open data(after indexing)
o	PHP – backend and MySQL database used for MTA train data usage.

•	Demonstration of Big Apple - (How to Use) – Video is now available:
https://www.youtube.com/watch?v=dR448ULXHHE


Our Super Cool App - Big Apple is ready to use – wait till Demo Day! 
