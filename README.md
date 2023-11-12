# Full Stack Management and Booking System for Train services
**Goal of the project:** Produce a desktop app that acts as a management system for employees to use for train services

**Front End** Tkinter Python Module

**Back End** MYSQL and Python

**Brief Outline of Data:** Created Class objects to represent the trains and SQL tables which represent stores all train services, with other SQL tables logging the seating plans for any train from one adjacent stop to another.

**The project should be able to:**
  * Correctly identified which base and shift has submitted their daily sitrep
  * Correctly identify the masked NRIC of those who have not completed their ART SA test
  * Output an accurate report in the form of a text document or string
  * Output the report via Twilio to my whatsapp phone number

**Dependencies:**
  * Serial.txt, acts as a reference for the number in the name of the downloaded data

**Additional features added:**
  * Ability to automatically login in to survey website and mail through the use of Selenium
  * Using MAC OSX and Iphone SMS forwarding feature to acquire SMS otp for login (SQlite3 library used to access message.db in the messages app)
  * Download Data for this morning and tonight through the use of finding elements with Selenium
  * Using Chrontab on macOS, automates python script to run at 1000 everyday

