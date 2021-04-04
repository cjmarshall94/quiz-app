from flask import render_template, request, url_for, redirect
import random, copy, collections
import pandas as pd

from app import app, db
from app.models import Question

# Main quiz page
@app.route("/", methods=["GET"])
def quiz():

	questions = Question.query.all()

	# Get 5 random questions
	quiz_list = random.sample(questions, 5)

	ordered_quiz_list = sorted(quiz_list, key=lambda x: x.id)

	return render_template("main.html", questions=ordered_quiz_list)


# Page to show correct / wrong answers to the quiz
@app.route("/results", methods=["POST"])
def show_result():

	if request.method == "POST":
		
		# Record the user's answers alongside the question that was asked for that answer
		user_answers = {}
		for key, value in request.form.items():
			user_answers[key] = value

		# Converting key ot int so dict is in the correct order for comparison with correct answers
		user_answers = {int(k):v for k,v in user_answers.items()}

		# Order by the question ID
		ordered_answers = [value for key,value in sorted(user_answers.items())]

		# Get the relevant question based on the ID (because want to render out the correct Q/As alongside user's answers)
		question_ids = user_answers.keys()
		ordered_quiz_list = Question.query.filter(Question.id.in_(question_ids)).all()

		# Create the results table
		results_table = pd.DataFrame(data={
										'Question': [question.question for question in ordered_quiz_list], 
										'Correct Answer': [question.answer for question in ordered_quiz_list], 
										'Your Answer': ordered_answers
										})

		# Apply styling to highlight correct / wrong answers
		def identify_correct_answer(row):
			if row["Correct Answer"] == row["Your Answer"]:
				return ['background-color: #D7FFD4']*3
			else:
				return ['background-color: #FFDEDE']*3

		results_table_html = results_table[["Question", "Correct Answer", "Your Answer"]].style.apply(identify_correct_answer, axis=1).hide_index().render()

		return render_template("results.html", results_table_html=results_table_html)


# This page lets you add a question to the quiz
@app.route("/add", methods=["GET", "POST"])
def add_question():

	if request.form:
		question = request.form["question"]
		answer = request.form["answer"]
		record = Question(question=question, answer=answer)
		db.session.add(record)
		db.session.commit()

		return redirect(url_for("edit"))

	return render_template("add.html")


# After successful edit, this page asks if you want to do the quiz or add another question
@app.route("/edit", methods=["GET"])
def edit():

	questions = Question.query.all()
	return render_template("edit.html", questions=questions)


# Ability to remove questions from the quiz
@app.route("/delete", methods=["POST"])
def delete():

    question = request.form.get("question")
    question_to_delete = Question.query.filter_by(question=question).first()
    db.session.delete(question_to_delete)
    db.session.commit()
    return redirect("/edit")


if __name__ == "__main__":
	app.run(debug=True)

