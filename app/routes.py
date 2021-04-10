from flask import render_template, request, url_for, redirect
import random, copy, collections
import pandas as pd

from app import app, db
from app.models import Question, Quiz


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Main quiz page
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def quiz():

	questions = Question.query.all()

	# Get 5 random questions
	quiz_list = random.sample(questions, 5)

	ordered_quiz_list = sorted(quiz_list, key=lambda x: x.id)

	return render_template("main.html", questions=ordered_quiz_list)


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Results page
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

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

		# Get number of total questions and number of correct answers
		num_correct_answers = len(results_table[results_table["Correct Answer"] == results_table["Your Answer"]].Question)
		num_questions = len(results_table.Question)

		return render_template("results.html", results_table_html=results_table_html, num_correct_answers=num_correct_answers, num_questions=num_questions)


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Quiz list
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

@app.route("/show-quizzes", methods=["GET"])
def show_quizzes():

	quizzes = Quiz.query.all()
	return render_template("quiz-list.html", quizzes=quizzes)


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Edit quiz (show all questions and let you remove questions)
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

@app.route("/edit/<quiz_id>", methods=["GET", "POST"])
def edit(quiz_id):

	# Get the appropriate questions that belong to this quiz
	questions = Question.query.filter(Question.quiz_id==quiz_id)

	if request.method == "POST":
		question = request.form["question"]
		answer = request.form["answer"]
		record = Question(question=question, answer=answer, quiz_id=quiz_id)
		db.session.add(record)
		db.session.commit()

		return render_template("edit.html", questions=questions, quiz_id=quiz_id)

	return render_template("edit.html", questions=questions, quiz_id=quiz_id)


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Route to delete question from quiz on /edit/<quiz_id> page
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

@app.route("/delete", methods=["POST"])
def delete():

    question = request.form.get("question")
    quiz_id = request.form.get("quiz_id")
    question_to_delete = Question.query.filter_by(question=question, quiz_id=quiz_id).first()
    db.session.delete(question_to_delete)
    db.session.commit()

    print("quiz_id = {}".format(quiz_id))

    return redirect(url_for("edit", quiz_id=quiz_id))


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Add question to quiz
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

@app.route("/add/<quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):

	quiz_id = quiz_id

	return render_template("add.html", quiz_id=quiz_id)


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Create a new quiz
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
@app.route("/create", methods=["GET", "POST"])
def create():

	if request.form:
		name = request.form["quiz_name"]
		new_quiz = Quiz(name=name)
		db.session.add(new_quiz)
		db.session.commit()

		return redirect(url_for("show_quizzes"))

	return render_template("create.html")


if __name__ == "__main__":
	app.run(debug=True)

