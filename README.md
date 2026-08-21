# Plant Health Management System Back-end
back-end for a full-stack web project incorporating a Raspberry Pi 5 with integrated sensors

## Overview
Constructs a light-weight SQL database to hold a users plant information and live recordings gained from the linked Raspberry Pi 5. Data is written into the database and later retrieved by parametrized queries to be converted into human-readable graphs which are displayed by the linked HTML webpage in a user friendly format.

## Features
- Lightweight database with all necessary core functionality (Adding/Removing Records, Record Lookup)
- Dynamic, parametrized queries which are injection-safe
- Use of Pandas Data frames for data to be restructured after SQL retrieval
- Use of Matplotlib for retrieved data to be displayed in Line/Bar graph format
- Linked CSV containing common house plants for comparison between recorded / ideal values for common British house plants
- Base64 encoding for data to be returned to the Front-end

## Built With
- SQL (SQLite)
- Python
- Pandas
- Matplotlib
- CSV (For Data Library)
 
 ## How It Works
Select statements operate on two lists, they work by only sorting by fields in which data is input for (Each sortable field has a text box for input in the corresponding HTML Webpage) If input is given the relevant condition is added to the Filters list with the filter itself (Plant name, Recorded value etc) being added to the Values list;  If the text box is empty ie no input was given, that parameter is ignored. In the end the Filters list is recursively looped through, adding it alongside its relevant parameter stored inside Values (as they share an index despite being in separate lists). Update queries operate in a similar way. The "WHERE 1=1" Clause is required as SQL SELECT statements cannot have an empty condition, therefore if the user input no conditional values (to get all possible records in a table) the query would crash.

What I learned
- Refined my SQL Skills and taught me the importance of robust architectural design in order to meet end user expectations
- Learnt the importance of planning in regards to system design and what makes an effective software solution
- Expanded my Python knowledge to several imports
- Leant how to set up interactions between different project compartments (HTML, Rust, The Pi Itself)
- Helped sharpen teamwork skills and uphold communication between member
- Learnt the importance of upholding team wide motivation throughout developmental adversity
