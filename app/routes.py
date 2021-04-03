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

		# Order by the question ID
		ordered_answers = collections.OrderedDict(sorted(user_answers.items()))

		# Get the relevant question based on the ID (because want to render out the correct Q/As alongside user's answers)
		question_ids = ordered_answers.keys()
		ordered_quiz_list = Question.query.filter(Question.id.in_(question_ids)).all()

		# We just need the ordered list of values for the front end
		ordered_answers = ordered_answers.values()

		# Create the results table
		results_table = pd.DataFrame(data={
										'Question': [question.question for question in ordered_quiz_list], 
										'Correct Answer': [question.answer for question in ordered_quiz_list], 
										'Your Answer': ordered_answers
										})

		return render_template("results.html", tables=[results_table.to_html()], titles=results_table.columns.values)


# This page lets you add a question to the quiz
@app.route("/edit", methods=["GET", "POST"])
def edit_quiz():

	if request.form:
		question = request.form["question"]
		answer = request.form["answer"]
		record = Question(question=question, answer=answer)
		db.session.add(record)
		db.session.commit()

		return redirect(url_for("success"))

	return render_template("edit.html")


# After successful edit, this page asks if you want to do the quiz or add another question
@app.route("/success", methods=["GET"])
def success():

	questions = Question.query.all()
	return render_template("success.html", questions=questions)


# Ability to remove questions from the quiz
@app.route("/delete", methods=["POST"])
def delete():

    question = request.form.get("question")
    question_to_delete = Question.query.filter_by(question=question).first()
    db.session.delete(question_to_delete)
    db.session.commit()
    return redirect("/success")


if __name__ == "__main__":
	app.run(debug=True)

