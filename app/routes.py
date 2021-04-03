from flask import render_template, request, url_for, redirect
import random, copy

from app import app, db
from app.models import Question

# Main quiz page
@app.route("/", methods=["GET", "POST"])
def quiz():

	questions = Question.query.all()
	# Get 5 random questions
	quiz_list = random.sample(questions, 5)

	if request.method == "GET":
		return render_template("main.html", questions=quiz_list)

	else:
		user_answers = request.form.getlist("answer-box")
		return render_template("results.html", questions=quiz_list, user_answers=user_answers)


# Page to show correct / wrong answers to the quiz
@app.route("/results", methods=["GET", "POST"])
def show_result():

	if request.method == "GET":
		return render_template("results.html")


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

