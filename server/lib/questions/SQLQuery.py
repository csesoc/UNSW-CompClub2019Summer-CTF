class SQLQuery:
    class solves:
        createTable = """
            CREATE TABLE IF NOT EXISTS solves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER NOT NULL,
                question INTEGER NOT NULL,
                answer TEXT DEFAULT NULL,
                approved INTEGER DEFAULT 1,
                FOREIGN KEY (user) REFERENCES users (id),
                FOREIGN KEY (question) REFERENCES questions (id)
            );
            """

        add = """
            INSERT
            INTO solves (user, question)
            VALUES (?, ?)
            ;
            """

        deleteUser = """
            DELETE FROM solves
            WHERE user = ?
            ;
            """

        deleteSpecific = """
            DELETE FROM solves
            WHERE id = ?
            ;
            """

        getAll = """
            SELECT user, question
            FROM solves
            WHERE approved = 1
            ;
            """

        getUser = """
            SELECT question
            FROM solves
            WHERE user = ? AND approved = 1
            ;
            """

        getQuestion = """
            SELECT user
            FROM solves
            WHERE question = ? AND approved = 1
            ;
            """
        
        approve = """
            UPDATE solves
            SET approved = 1
            WHERE id = ?
            ;
            """
        
        unapprove = """
            UPDATE solves
            SET approved = 0
            WHERE id = ?
            ;
            """
        
        addUnapproved = """
            INSERT
            INTO solves (user, question, answer, approved)
            VALUES (?, ?, ?, 0)
            ;
            """
        
        getSolvesSpecial = """
            SELECT id, user, answer, approved
            FROM solves
            WHERE question = ?
            ;
            """
    
    class questions:
        createTable = """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                answer TEXT DEFAULT NULL,
                value INTEGER NOT NULL,
                category INTEGER NOT NULL,
                type INTEGER DEFAULT 0,
                FOREIGN KEY (category) REFERENCES categories (id)
            );
            """

        add = """
            INSERT
            INTO questions (title, description, answer, value, category)
            VALUES (?, ?, LOWER(?), ?, ?)
            ;
            """
        
        deleteQuestionSolves = """
            DELETE FROM solves
            WHERE question = ?
            ;
            """

        deleteQuestion = """
            DELETE FROM questions
            WHERE id = ?
            ;
            """

        edit = """
            UPDATE questions
            SET title = ?, description = ?, value = ?, category = ?
            WHERE id = ?
            ;
            """
        
        editAnswer = """
            UPDATE questions
            SET answer = LOWER(?)
            WHERE id = ?
            ;
            """

        getAll = """
            SELECT id, title, description, value, category
            FROM questions
            WHERE type = 0
            ;
            """
        
        getOne = """
            SELECT id, title, description, value, category
            FROM questions
            WHERE id = ?
            ;
            """
        
        getAllWithAnswer = """
            SELECT id, title, description, answer, value, category
            FROM questions
            WHERE type = 0
            ;
            """
        
        getOneWithAnswer = """
            SELECT id, title, description, answer, value, category
            FROM questions
            WHERE id = ?
            ;
            """
        
        getAnswer = """
            SELECT answer
            FROM questions
            WHERE id = ?
            ;
            """
        
        addSpecial = """
            INSERT
            INTO questions (title, description, value, category, type)
            VALUES (?, ?, ?, ?, 1)
            ;
            """
        
        editSpecial = """
            UPDATE questions
            SET title = ?, description = ?, value = ?, category = ?
            WHERE id = ?
            ;
            """
        
        genAllSpecial = """
            SELECT id, title, description, value, category
            FROM questions
            WHERE type = 1
            ;
            """
        
        genOneSpecial = """
            SELECT id, title, description, value, category
            FROM questions
            WHERE id = ? AND type = 1
            ;
            """

        getAllBoth = """
            SELECT id, title, description, value, category, type
            FROM questions
            ;
            """

    class categories:
        createTable = """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                UNIQUE (category)
            );
            """
        
        add = """
            INSERT
            INTO categories (category)
            VALUES (LOWER(?))
            ;
            """
        
        deleteCategorySolves = """
            DELETE FROM solves
            WHERE question IN (
                SELECT id
                FROM questions
                WHERE category = ?
            );
            """

        deleteCategoryQuestions = """
            DELETE FROM questions
            WHERE category = ?
            ;
            """

        deleteCategory = """
            DELETE FROM categories
            where id = ?
            ;
            """

        edit = """
            UPDATE categories
            SET category = LOWER(?)
            WHERE id = ?
            ;
            """
        
        getAll = """
            SELECT id, category
            FROM categories
            ;
            """

    
    class users:
        getAllUsers = """
            SELECT id, username
            FROM users
            ;
            """

        deleteUserSolves = """
            DELETE FROM solves
            where user = ?
            ;
            """
            
        deleteUser = """
            DELETE FROM users
            WHERE id = ?
            ;
            """
