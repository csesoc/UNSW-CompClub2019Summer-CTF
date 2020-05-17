class SQLQuery:
    class solves:
        createTable = """
            CREATE TABLE IF NOT EXISTS solves (
                user INTEGER NOT NULL,
                question INTEGER NOT NULL,
                approved INTEGER DEFAULT 1,
                answer TEXT DEFAULT NULL,
                FOREIGN KEY (user) REFERENCES users (id),
                FOREIGN KEY (question) REFERENCES questions (id),
                UNIQUE (user, question)
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
            WHERE user = ? AND question = ?
            ;
            """

        getAll = """
            SELECT *
            FROM solves
            WHERE approved = 1
            ;
            """

        getUser = """
            SELECT question
            FROM solves
            WHERE user = ? and approved = 1
            ;
            """

        getQuestion = """
            SELECT user
            FROM solves
            WHERE question = ? and approved = 1
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
                FOREIGN KEY (category) REFERENCES questions (title)
            );
            """

        add = """
            INSERT
            INTO questions (title, description, answer, value, category)
            VALUES (?, ?, LOWER(?), ?, LOWER(?))
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
            SET title = ?, description = ?, value = ?, category = LOWER(?)
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
