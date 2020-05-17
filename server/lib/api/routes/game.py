from .. import routing, JSON
from tornado.web import authenticated, RequestHandler
from sqlite3 import IntegrityError

from lib.questions import SQLMethod as questionsSQLMethod
from lib.auth import SQLMethod as authSQLMethod
from lib.site import SSE_messages


@routing.POST("/questions/questions.json")
@authenticated
def questions(self: RequestHandler, args: dict):
    self.finish(JSON.data(questionsSQLMethod.questions.getQuestions()))


@routing.POST("/questions/categories.json")
@authenticated
def categories(self: RequestHandler, args: dict):
    self.finish(JSON.data(questionsSQLMethod.categories.getCategories()))


@routing.POST("/questions/leaderboard.json")
def leaderboard(self: RequestHandler, args: dict):
    questionsSQL = questionsSQLMethod.questions.getQuestions()
    solvesSQL = questionsSQLMethod.questions.getSolves()
    usersSQL = authSQLMethod.getUsers()

    points = {}
    for question in questionsSQL:
        points[question[0]] = question[3]

    board = {}
    for user in usersSQL:
        board[user[0]] = dict(name=user[1], points=0, solves=0)

    for solve in solvesSQL:
        board[solve[0]]["points"] += points[solve[1]]
        board[solve[0]]["solves"] += 1
    
    return self.finish(JSON.data(board))


@routing.POST("/questions/adminSolves.json")
@authenticated
def adminSolves(self: RequestHandler, args: dict):
    return self.finish(JSON.data(questionsSQLMethod.questions.getSolves()))


@routing.POST("/questions/userSolves.json")
@authenticated
def userSolves(self: RequestHandler, args: dict):
    return self.finish(JSON.data(questionsSQLMethod.questions.getSolves(user=self.current_user.id)))


@routing.POST("/questions/questionSolves.json")
@authenticated
def questionSolves(self: RequestHandler, args: dict):
    return self.finish(JSON.data(len(questionsSQLMethod.questions.getSolves(question=args["question"]))))


@routing.POST("/questions/userPoints.json")
def userPoints(self: RequestHandler, args: dict):
    questionsSQL = questionsSQLMethod.questions.getQuestions()
    solvesSQL = questionsSQLMethod.questions.getSolves(user=self.current_user.id)

    pointsMap = {}
    for question in questionsSQL:
        pointsMap[question[0]] = question[3]

    points = 0
    for solve in solvesSQL:
        points += pointsMap[solve[1]]
    
    return self.finish(JSON.data(points))


@routing.POST("/questions/solve")
@authenticated
def trySolve(self: RequestHandler, args: dict):
    if args["answer"].lower() == questionsSQLMethod.questions.getAnswer(args["question"]):
        try:
            questionsSQLMethod.questions.solveQuestion(self.current_user.id, args["question"])
            SSE_messages.addMessage(self.current_user.username + " has found an answer!")
        except IntegrityError:
            pass
        return self.finish(JSON.YES())
    return self.finish(JSON.NO())

@routing.POST("/questions/special/solve")
@authenticated
def submitSpecial(self: RequestHandler, args: dict):
    result = questionsSQLMethod.questions.addUnapproved(self.current_user.id, args["question"], args["answer"])
    if result:
        SSE_messages.addMessage(self.current_user.username + " has found an answer!")
        return self.finish(JSON.YES())
    return self.finish(JSON.NO())
