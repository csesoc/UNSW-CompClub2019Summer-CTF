from .. import routing, JSON
from tornado.web import authenticated, RequestHandler

from lib.questions import SQLMethod as questionsSQLMethod
from lib.auth import SQLMethod as authSQLMethod


@routing.POST("/questions/question/submit")
@authenticated
def questionSubmit(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))
    
    result = questionsSQLMethod.questions.createQuestion(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())

@routing.POST("/questions/question/edit")
@authenticated
def questionEdit(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.questions.editQuestion(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())


@routing.POST("/questions/question/editAnswer")
@authenticated
def questionEditAnswer(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))
    
    result = questionsSQLMethod.questions.editQuestionAnswer(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())


@routing.POST("/questions/question/getAnswer")
@authenticated
def questionGetAnswer(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))
    
    result = questionsSQLMethod.questions.getAnswer(**args)
    if result:
        return self.finish(JSON.data(result))
    return self.finish(JSON.FALSE())


@routing.POST("/questions/question/delete")
@authenticated
def questionDelete(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.questions.deleteQuestion(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())

@routing.POST("/questions/category/submit")
@authenticated
def categorySubmit(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.categories.createCategory(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())


@routing.POST("/questions/category/edit")
@authenticated
def categoryEdit(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.categories.editCategory(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())


@routing.POST("/questions/category/delete")
@authenticated
def categoryDelete(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.categories.deleteCategory(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())


@routing.POST("/questions/users/getAll")
@authenticated
def usersGetAll(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    return self.finish(JSON.data(questionsSQLMethod.users.getAllUsers()))

@routing.POST("/questions/users/delete")
@authenticated
def usersDelete(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.users.deleteUser(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())

@routing.POST("/questions/special/approve")
@authenticated
def questionsSpecialApprove(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.questions.approveSolve(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())

@routing.POST("/questions/special/unapprove")
@authenticated
def questionsSpecialUnapprove(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.questions.unapproveSolve(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())

@routing.POST("/questions/special/delete")
@authenticated
def questionsSpecialDelete(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    result = questionsSQLMethod.questions.deleteSolve(**args)
    if result:
        return self.finish(JSON.OK())
    return self.finish(JSON.FALSE())

@routing.POST("/questions/special/solves")
@authenticated
def questionsSpecial(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    return self.finish(JSON.data(questionsSQLMethod.questions.getQuestionsSpecial(**args)))

@routing.POST("/questions/special/add")
@authenticated
def questionsSpecialAdd(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    return self.finish(JSON.data(questionsSQLMethod.questions.addSpecial(**args)))

@routing.POST("/questions/special/edit")
@authenticated
def questionsSpecialEdit(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    return self.finish(JSON.data(questionsSQLMethod.questions.editSpecial(**args)))

@routing.POST("/questions/special/all")
@authenticated
def questionsSpecialAll(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    return self.finish(JSON.data(questionsSQLMethod.questions.genAllSpecial(**args)))

@routing.POST("/questions/special/one")
@authenticated
def questionsSpecialOne(self: RequestHandler, args: dict):
    if not self.current_user.isAdmin:
        return self.finish(JSON.error("access denied"))

    return self.finish(JSON.data(questionsSQLMethod.questions.genOneSpecial(**args)))
