# Coffee Payment Scheduler

In this coding challenge, I designed a python program that helps the seven coffee-loving
coworkers in the Bertram Labs office decide who should pay for the coffee bill each
day. The user can add people to the group and then the program will output a
schedule showing who should pay for the bill on what days. The user can make group
sizes of any kind and set the schedule length to any number as well. The program
utilizes a GUI to get user input and displays messages to the user in a text box.
There are several mechanisms in place to stop the user from entering invalid data
or using the program incorrectly (i.e. clicking generate schedule before adding people).
The text box displays error messages to help guide the user to use the program correctly.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Algorithm](#algorithm)
- [Credits](#credits)

## Installation

To run this program, you need Python version 3.0 or later installed. The program
uses Tkinter which should come with the standard Python installation.

## Usage

These are the steps to run this program:
1. Open the command prompt or terminal
2. Navigate to the directory the python file is located in
3. write 'python coffee_scheduler.py' and hit enter
4. A GUI will appear with instructions on how to use the program
5. In the GUI, fill out the fields and click 'Add Person'. Add as many people as you want.
6. Next, adjust the schdule length if you want. The default length is 100 days.
7. Finally, click 'Generate Payment Schedule' and the schedule will appear in the text box.

## Algorithm

In order to be fair to everyone, a person should pay the same amount in the group's bills
over time as they would on themself. To accomplish this, each person has an 'Amount Paid'
variable and a 'Running Difference' variable associated with them. Every time they pay
the coffee bill, the bill amount gets added to their 'Amount Paid.' Every day, each person's
'Running Difference' gets recaculated using the formula:

    Running Difference = (Amount if paid alone) - (Amount paid for the group)

where 'Amount if paid alone' equals the day number times the cost of their coffee and 
'Amount paid for the group' equals their 'Amount Paid' variable. The algorithm selects
the next payer by choosing the person with the highest running difference, because
having a high or positive running difference means you owe the group money. This method
minimizes the differences between any two person's 'Amount Paid' so that at any given
day the amounts that everyone has paid for each other is more balanced.

Note: When the 'Generate Payment Schedule' button is pressed, a table will be printed
to the terminal that shows the running differences for each person for each day. Then,
it will show a comparison between what each person would've paid if they purchased
their coffee alone vs with the group. These stats help understand the effectives of
the algorithm.

## Credits

Developed by Tyson Brown (email: tysonbrown@gatech.edu)
