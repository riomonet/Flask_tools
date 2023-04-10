from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import personality_quiz


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretsarecool'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
quiz = personality_quiz
questions = personality_quiz.questions
number_of_questions = len(questions)
x = 0

@app.route('/')
def main():
    return render_template('start.html',title=quiz.title, instruction=quiz.instructions)

@app.route('/reset_data', methods=["POST"])
def reset():
    global x
    session['responses'] = []
    x = 0
    return redirect('/questions/0')


# use form template to display questions and options for answers
@app.route('/questions/<int:q_num>')
def question(q_num):

    if x >= number_of_questions:
        flash("You can only take the survey once, you can't change your answers!!")
        return redirect('/thankyou')
    elif q_num != x:
        flash("Pardon me, you skipped a question, please answer THIS question")
        q_num = x
    return render_template("question.html", q=questions[q_num].question, choices=questions[q_num].choices, item = q_num)


# post answers to responses
@app.route('/answer/<int:q_num>',methods=['POST'])  
def answer(q_num):
    global x    
    q_num += 1
    x += 1
#    responses.append(request.form['ans'])
    res = session['responses']
    res.append(request.form['ans'])
    session['responses'] = res

    if q_num < number_of_questions:
        return redirect(f'/questions/{q_num}')
    else:
        return redirect('/thankyou')


@app.route('/thankyou')
def thankyou():
        return render_template('thankyou.html')
    
