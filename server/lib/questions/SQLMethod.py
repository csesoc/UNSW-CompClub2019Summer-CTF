from .SQLQuery import SQLQuery
from .. import database


class SQLMethod:
    class questions:
        # User Functions
        @staticmethod
        def solveQuestion(user: int, question: int):
            return database.insert(SQLQuery.solves.add, (user, question))

        @staticmethod
        def addUnapproved(user: int, question: int, answer: str):
            return database.insert(SQLQuery.solves.addUnapproved, (user, question, answer))
        
        @staticmethod
        def getQuestionsBoth():
            return database.fetchAll(SQLQuery.questions.getAllBoth)

        @staticmethod
        def deleteSpecific(user: int, question: int):
            return database.update(SQLQuery.solves.deleteSpecific, (user, question))

        # Admin functions
        @staticmethod
        def deleteSolve(solve: int):
            return database.update(SQLQuery.solves.deleteSpecificAdmin, (solve,))

        @staticmethod
        def createQuestion(title: str, description: str, answer: str, value: int, category: int):
            return database.insert(SQLQuery.questions.add, (title, description, answer, value, category))

        @staticmethod
        def editQuestion(question: int, title: str, description: str, value: int, category: int):
            return database.update(SQLQuery.questions.edit, (title, description, value, category, question))

        @staticmethod
        def editQuestionAnswer(question: int, answer: str):
            return database.update(SQLQuery.questions.editAnswer, (answer, question))

        @staticmethod
        def deleteQuestion(question: int):
            # Delete solves
            result = []
            result.append(database.update(
                SQLQuery.questions.deleteQuestionSolves, (question,), commit=False))
            result.append(database.update(
                SQLQuery.questions.deleteQuestion, (question,), commit=False))

            return database.assertSQLResult(result)

        @staticmethod
        def deleteUser(user: int):
            return database.update(SQLQuery.solves.deleteUser, (user,))
        
        @staticmethod
        def approveSolve(solve: int):
            return database.update(SQLQuery.solves.approve, (solve,))

        @staticmethod
        def unapproveSolve(solve: int):
            return database.update(SQLQuery.solves.unapprove, (solve,))

        @staticmethod
        def getQuestionsSpecial(question: int):
            return database.fetchAll(SQLQuery.solves.getSolvesSpecial, (question,))
        
        @staticmethod
        def addSpecial(title: str, description: str, value: int, category: int):
            return database.insert(SQLQuery.questions.addSpecial, (title, description, value, category))
        
        @staticmethod
        def editSpecial(title: str, description: str, value: int, category: int, question: int):
            return database.update(SQLQuery.questions.editSpecial, (title, description, value, category, question))

        @staticmethod
        def genAllSpecial():
            return database.fetchAll(SQLQuery.questions.genAllSpecial)
        
        @staticmethod
        def genOneSpecial(question: int):
            return database.fetchOne(SQLQuery.questions.genOneSpecial, (question,))


        # Helper functions
        @staticmethod
        def getAnswer(question: int):
            return database.fetchOne(SQLQuery.questions.getAnswer, (question,))[0]

        @staticmethod
        def getSolves(*, user: int = None, question: int = None):
            if user:
                return list(map(lambda result: result[0], database.fetchAll(SQLQuery.solves.getUser, (user,))))
            elif question:
                return list(map(lambda result: result[0], database.fetchAll(SQLQuery.solves.getQuestion, (question,))))
            else:
                return database.fetchAll(SQLQuery.solves.getAll)

        @staticmethod
        def getPending(*, user: int = None, question: int = None):
            if user:
                return list(map(lambda result: result[0], database.fetchAll(SQLQuery.solves.getUserPending, (user,))))
            elif question:
                return list(map(lambda result: result[0], database.fetchAll(SQLQuery.solves.getQuestionPending, (question,))))
            else:
                return database.fetchAll(SQLQuery.solves.getAllPending)

        @staticmethod
        def getQuestions(*, question: int = None, answer: bool = False):
            if question:
                if answer:
                    return database.fetchOne(SQLQuery.questions.getOneWithAnswer, (question,))
                else:
                    return database.fetchOne(SQLQuery.questions.getOne, (question,))
            else:  # get all
                if answer:
                    return database.fetchAll(SQLQuery.questions.getAllWithAnswer)
                else:
                    return database.fetchAll(SQLQuery.questions.getAll)


    class categories:
        @staticmethod
        def getCategories():
            return database.fetchAll(SQLQuery.categories.getAll)

        @staticmethod
        def createCategory(category: str):
            return database.insert(SQLQuery.categories.add, (category,))

        @staticmethod
        def editCategory(catId: int, category: str):
            return database.update(SQLQuery.categories.edit, (category, catId))

        @staticmethod
        def deleteCategory(catId: int):
            # Delete questions and solves
            result = []
            result.append(database.update(
                SQLQuery.categories.deleteCategorySolves, (catId,), commit=False))
            result.append(database.update(
                SQLQuery.categories.deleteCategoryQuestions, (catId,), commit=False))
            result.append(database.update(
                SQLQuery.categories.deleteCategory, (catId,), commit=False))
            return database.assertSQLResult(result)

    class users:
        @staticmethod
        def getAllUsers():
            users = database.fetchAll(SQLQuery.users.getAllUsers)
            for i, user in enumerate(users):
                questionsSQL = SQLMethod.questions.getQuestionsBoth()
                solvesSQL = SQLMethod.questions.getSolves(user=user[0])

                pointsMap = {}
                for question in questionsSQL:
                    pointsMap[question[0]] = question[3]
                
                points = 0
                solves = 0
                for solve in solvesSQL:
                    points += pointsMap[solve]
                    solves += 1

                users[i] = (user[0], user[1], points, solves)
            return users
        
        @staticmethod
        def deleteUser(userId: int):
            result = []
            result.append(database.update(
                SQLQuery.users.deleteUserSolves, (userId,), commit=False))
            result.append(database.update(
                SQLQuery.users.deleteUser, (userId,), commit=False))

            return database.assertSQLResult(result)
