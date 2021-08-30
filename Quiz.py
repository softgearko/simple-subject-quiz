from flask import Flask, render_template, request
import os
import sys
import random

#reload(sys)
#sys.setdefaultencoding('utf8')

app = Flask(__name__)

quizSet = []
randRange = []

def readQuestion():
    global quizSet

    quizSet = []
    data = None
    my_dir = os.path.dirname(__file__)
    filePath = os.path.join(my_dir, 'quiz.txt')
    with open(filePath, 'r') as inputData:
        data= inputData.read().split('\n')

    questions = {}
    count = 0
    for line in data:
        if (len(line)<=0):
            break
        if count%2 == 0:
            if (len(line)<=1):
                break
            questions = {}
            questions['Q'] = line
        else:
            questions['A'] = line
            quizSet.append(questions)
        count += 1

def getRand(ls):
    return [I for I in range(len(ls))]

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/start',methods=['POST','GET'])
def question():
    global  randRange
    global quizSet

    readQuestion()
    randRange = [i for i in range(len(quizSet))]
    questionNo = random.choice(randRange)
    question = quizSet[questionNo]['Q']
    attempted = 0
    return render_template('display.html',score=0,questionNo=questionNo,status="",question=question,attempted=attempted+1)

@app.route('/question',methods=['POST','GET'])
def nextQuestion():
    global  randRange
    global quizSet

    questionNo = int(request.form['questionNo'])
    score = int(request.form['score'])
    answer = request.form['question']
    attempted = int(request.form['attempted'])
    ques = quizSet[questionNo]
    if answer == ques['A']:
        score +=1
        ok = 'ok'
    else:
        ok = 'no'

    rightanswer = ques['A']
    return render_template('answer.html',score=score,questionNo=questionNo,status="",question=ques['Q'],attempted=attempted,answer= rightanswer, entered=answer, ok=ok)

@app.route('/answer',methods=['POST','GET'])
def nextAnswer():
    global  randRange
    global quizSet

    questionNo = int(request.form['questionNo'])
    score = int(request.form['score'])
    attempted = int(request.form['attempted'])
    ok = request.form['ok']

    attempted += 1
    randRange.remove(questionNo)
    if (ok == 'no'):
        randRange.append(questionNo)
    elif (len(randRange)<=0):
        percent = int(100 * score / (attempted-1)) 
        return render_template('score.html',score=score, attempted = attempted-1, percent=percent)

    questionNo = random.choice(randRange)
    ques = quizSet[questionNo]
    return render_template('display.html',score=score,questionNo=questionNo,status="",question=ques['Q'],attempted=attempted)

@app.route('/edit',methods=['POST','GET'])
def edit():
    global quizSet

    readQuestion()
    textareadata = ""
    for question in quizSet:
        textareadata += question['Q'] + '\n'
        textareadata += question['A'] + '\n'

    return render_template('edit.html', textareadata=textareadata)

@app.route('/editsubmit',methods=['POST','GET'])
def editsubmit():
    textareadata = request.form['textareadata']
    if(len(textareadata)<3):
        return edit()
    
    txtfile = open('quiz.txt', 'w')
    n = txtfile.write(textareadata)
    txtfile.close()

    return render_template('index.html')

if __name__ == '__main__':
    readQuestion()
    app.run(host='0.0.0.0', debug=False)
