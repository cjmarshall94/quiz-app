from flask import render_template, request, url_for, redirect
import random, copy

from app import app 

original_questions_answers = {
    'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona':'Phoenix', 'Arkansas':'Little Rock',
    'California': 'Sacramento', 'Colorado':'Denver', 'Connecticut':'Hartford', 'Delaware':'Dover',
    'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
    'Illinios': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Monies', 'Kansas': 'Topeka',
    'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis',
    'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'St. Paul', 'Mississippi': 'Jackson',
    'Missouri': 'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City',
    'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany',
    'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
    'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia',
    'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City',
    'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston',
    'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'
}

# get a list of the answers
questions_answers = copy.deepcopy(original_questions_answers)

# build the list of the correct answers to compare (in global scope)
correct_answers = []
user_answers = []

# initialising the score variable
score = []

@app.route("/", methods=["GET", "POST"])
def quiz():

	if request.method == "GET":

		# load up a random selection of 5 dictionary keys each time
		randomiser = random.sample(range(1, len(questions_answers)), 5)
		print(randomiser)

		correct_answers.clear()

		for num in randomiser:
			correct_answers.append(list(questions_answers.values())[num])
		print(correct_answers)

		# render html page
		return render_template("main.html", q=list(questions_answers.keys()), a=list(questions_answers.values()), rand=randomiser)

	# logic for after form submitted (POST request)
	else:

		# get the data from the form
		req = request.form

		# clear user answers from previous attempt
		user_answers.clear()

		# push the data into a format that I can use to compare with correct answers
		for i in list(req.values()):
			user_answers.append(i)
		print(user_answers)

		# count the score
		list_matching_answers = [i for i, j in zip(user_answers, correct_answers) if i == j]

		# clear score from previous attempt
		score.clear()

		for i in list_matching_answers:
			score.append(i)

		# give the user an alert saying what they scored
		print(f"You scored {len(score)} out of 5!")

		# redirect to the route page after alert and form submission
		return redirect(url_for("show_result"))
		

@app.route("/results", methods=["GET", "POST"])
def show_result():

	if request.method == "GET":
		return render_template("results.html", score=score, correct_answers=correct_answers, user_answers=user_answers, original_questions_answers=original_questions_answers)
	return redirect(url_for("quiz"))


if __name__ == "__main__":
	app.run(debug=True)

