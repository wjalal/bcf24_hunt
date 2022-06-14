# Reception Treasure Hunt
**Treasure hunt website made for CSE Freshers' Reception.**

##  Project Overview
Core framework: Flask (Python), Database (SQLite)
 1. **Requirements** <br>
 Create a Virtual Environment using python's module **virtualenv**. And install the packages mentioned in the "**requirements.txt**" file.

2. **Activate the environment** <br>
In the app directory, open **cmd** or **terminal** and type in- `Scripts\activate.bat` and hit enter. Your **virtualenv** should activate.

3. **Launching the app**<br>
In the **virtualenv**, type `python app.py` to start the server. After it starts, go to browser and type in "`localhost:5000`" to see the flask app running.

## Project Structure
 - **Database**
 The database file named "**hunt.db**" contains 3 tables. Those are: 
 
	 - **User**
	 This one contains **id**, **username**, **password** (sha256), **last input time**, **levels** they have completed and a special **token**. The token contains the serial of the puzzles of the treasure hunt. i.e: 12346578 means that the serial the puzzles will come in is: 1st, 2nd, 3rd, 4th, 6th, 5th, 7th, 8th

	- **Quiz**
	This one contains **id** and **answer** to the specific puzzle. The id of the puzzle works as the name of the puzzle (image file).

	- **Answers**
	This table holds all the input that the teams (user) gives in each rounds. It contains several fields, such as: **teamname**, **answer**, **puzzle level**.
 
 - **Routes**
The URL routes configured for the app are: 
	 - `"/admin"`
	 Leads to admin panel login for the admins.
	- `"/admin_dashboard"`
Takes to the page of 
	- `"/team_reg"`
	This route takes the admin to the user registration page. Where admins can register new user/team.

	- `"/"`
		Index URl where users will need to log in using username and password.
	- `"/logout"`
	This route logs the user out.
	- `"/leaderboard"`
	Takes the user to the leaderboard page. Where the standings can be seen.
	- `"/puzzle"`
	This route takes the user to the latest puzzle (current level).
