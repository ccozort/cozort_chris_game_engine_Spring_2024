import random

# modified from CoPilot code
def random_select(students):
    random.shuffle(students)
    return students

students4 = [
    "Colin Ambrose", "Sebastian Beresford", "Riley Boynton", "Miles Crooks",
    "Theodore Do", "Andy Gao", "Milun Kalidindi", "Spencer Maffeo",
    "Harrison Manullang", "Jihoon Moon", "Justin Nguyen", "Kaden Nguyen",
    "Sameer Patel", "Owen Pence", "Harish Purushothaman", "Krithik Sambathkumar",
    "Tomas Santos", "Nik Sehestedt", "Aadi Subba", "Aidan Tighe", "Ruhan UPRETI",
    "Jaden Vinoth", "Jackson Willard", "Tanish Yadlapalli", "Reyn Yamamoto"
]

students6 = [
    "Kai Aberin",
    "Abhiram Bejgam",
    "Alex Chavez",
    "Nate Choi",
    "Chris D'Amico",
    "Rohan Dhameja",
    "Matthew Doan",
    "Russell Hackney",
    "Ayden Jafari",
    "Rameil Khoshaba",
    "Benjamin Leafstrand",
    "Zachary Li",
    "Liam Luinenburg",
    "Brandon Mai",
    "Sandryan Matar",
    "Gavin Mullaly",
    "Ian Na",
    "Anthony Olakangil",
    "Adrian Pham",
    "Khoi Pham",
    "Robbie Raiche",
    "Tyler Reed",
    "Eli Rose",
    "Scott Smith",
    "Tino Solomon",
    "Cael Stout",
    "Ethan Suriaga",
    "James von Ploennies",
    "Myles Zhang"
]
students3 = [
    "Keawe Ainoa",
    "Daniel Barandica",
    "Aidan Boomer",
    "Duncan Burk",
    "Lucas Cabral",
    "Ale Callioni",
    "Miguel Castrillon Ochoa",
    "James Che",
    "Nick Corbett",
    "Grant Curtiss",
    "Jude Hammers",
    "James Hayden",
    "Aaron Ko",
    "Dexter Kunimura",
    "Jason Liau",
    "Tyler Marshall",
    "Yash Midde",
    "Matthieu O'Byrne",
    "AJ Ordonio",
    "Daniel Perez",
    "Ariel Quach",
    "Ishan Routray",
    "Aayush Sharma",
    "Leo Tafoya",
    "Matthew Tran",
    "Damon Trieu",
    "Ivan Verduzco",
    "Daniel Zhu"
]

random_students = random_select(students3)
for student in random_students:
    print(student)