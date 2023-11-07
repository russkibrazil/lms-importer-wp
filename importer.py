# PROJECT NOTES
# docker run --name mysql-wp-girassol -e MYSQL_ROOT_PASSWORD=wp-girassol -e MYSQL_DATABASE=wp-girassol -e MYSQL_USER=wp-girassol -e MYSQL_PASSWORD=wp-girassol -p 33006:3306 -d mysql:8-debian

import csv, re
from phpserialize import dumps
import mariadb

# Used for Namaste LMS
def exportToCsv(inputFile):
    outputFile = None
    pathOut = input("Digite o nome do arquivo de saída \n")
    if pathOut == '.':
        pathOut = pathIn #just change the file extension
    try:
        outputFile = open(pathOut,'wt')
    except:
        print("Permissões insuficientes")
        return
    csvWriter = csv.writer(pathOut, quoting=csv.QUOTE_NONNUMERIC)

    csvWriter.writerow(["Question","Answer Type","Is Required?","Answer Explanation","Answer","Is correct?","Points","Answer","Is correct?","Points","Answer","Is correct?","Points","Answer","Is correct?","Points"])

    keepReading = True

    while keepReading:
        # TODO Detectar linhas em branco
        lines = []
        for i in range(7):
            lines.append(inputFile.readline())

        if not lines[0]:
            keepReading = False
            continue

        question = lines[0].lstrip('1234567890.').strip()
        answers = [lines[1].strip(),lines[2].strip(), lines[3].strip(), lines[4].strip()]
        correct = re.match('(?<=Resposta Correta: )[A-F]\)', lines[5]).group(0)
        explanation = lines[6].removeprefix("Explicação: ").strip()

        csvWriter.writerow([question,"radio",1,explanation,
                            answers[0].lstrip("ABCDEF)").strip(), answers[0].startswith(correct), answers[0].startswith(correct),
                            answers[1].lstrip("ABCDEF)").strip(), answers[1].startswith(correct), answers[1].startswith(correct),
                            answers[2].lstrip("ABCDEF)").strip(), answers[2].startswith(correct), answers[2].startswith(correct),
                            answers[3].lstrip("ABCDEF)").strip(), answers[3].startswith(correct), answers[3].startswith(correct),
                            ])
    outputFile.close()
    inputFile.close()
    print("Conversão concluída.")

def getSql(query) -> str:
    if query == "posts_question":
        return """
        INSERT INTO `TA2tJr_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES
        (1, NOW(), UTC_TIMESTAMP(), '', {question}, '', 'publish', 'closed', 'closed', '', '', '', NOW(), UTC_TIMESTAMP(), '', 0, 0, 'stm-questions', '', 0);
        """

    if query == "meta_question":
        return """
        INSERT INTO `TA2tJr_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES
        ({post_id}, '_edit_lock', CONCAT(UNIX_TIMESTAMP(NOW()),':1')),
        ({post_id}, '_edit_last', '1'),
        ({post_id}, 'curriculum', ''),
        ({post_id}, 'shareware', ''),
        ({post_id}, 'featured', ''),
        ({post_id}, 'views', ''),
        ({post_id}, 'level', ''),
        ({post_id}, 'current_students', ''),
        ({post_id}, 'duration_info', ''),
        ({post_id}, 'video_duration', ''),
        ({post_id}, 'status', ''),
        ({post_id}, 'status_dates', ''),
        ({post_id}, 'not_single_sale', ''),
        ({post_id}, 'price', ''),
        ({post_id}, 'sale_price', ''),
        ({post_id}, 'sale_price_dates', ''),
        ({post_id}, 'enterprise_price', ''),
        ({post_id}, 'not_membership', ''),
        ({post_id}, 'affiliate_course', ''),
        ({post_id}, 'affiliate_course_text', ''),
        ({post_id}, 'affiliate_course_link', ''),
        ({post_id}, 'points_price', ''),
        ({post_id}, 'expiration_course', ''),
        ({post_id}, 'end_time', ''),
        ({post_id}, 'drip_content', ''),
        ({post_id}, 'prerequisites', ''),
        ({post_id}, 'prerequisite_passing_level', ''),
        ({post_id}, 'announcement', ''),
        ({post_id}, 'faq', ''),
        ({post_id}, 'course_certificate', ''),
        ({post_id}, 'type', 'single_choice'),
        ({post_id}, 'video_type', ''),
        ({post_id}, 'presto_player_idx', ''),
        ({post_id}, 'lesson_video', ''),
        ({post_id}, 'lesson_video_poster', ''),
        ({post_id}, 'lesson_video_width', ''),
        ({post_id}, 'lesson_shortcode', ''),
        ({post_id}, 'lesson_embed_ctx', ''),
        ({post_id}, 'lesson_youtube_url', ''),
        ({post_id}, 'lesson_stream_url', ''),
        ({post_id}, 'lesson_vimeo_url', ''),
        ({post_id}, 'lesson_ext_link_url', ''),
        ({post_id}, 'duration', ''),
        ({post_id}, 'preview', ''),
        ({post_id}, 'lesson_excerpt', ''),
        ({post_id}, 'stream_start_date', ''),
        ({post_id}, 'stream_start_time', ''),
        ({post_id}, 'stream_end_date', ''),
        ({post_id}, 'stream_end_time', ''),
        ({post_id}, 'questions', ''),
        ({post_id}, 'quiz_style', ''),
        ({post_id}, 'duration_measure', ''),
        ({post_id}, 'correct_answer', ''), -- Notice: may be lacking data for bringing automatically the answer to the quizz
        ({post_id}, 'passing_grade', ''),
        ({post_id}, 're_take_cut', ''),
        ({post_id}, 'random_questions', ''),
        ({post_id}, 'answers', {answers_arr}),
        ({post_id}, 'question_explanation', {question_expl}),
        ({post_id}, 'question_view_type', 'list'),
        ({post_id}, 'review_course', ''),
        ({post_id}, 'review_user', ''),
        ({post_id}, 'review_mark', ''),
        ({post_id}, 'order', ''),
        ({post_id}, 'assignment_tries', ''),
        ({post_id}, 'assignment_files', ''),
        ({post_id}, 'editor_comment', ''),
        ({post_id}, 'try_num', ''),
        ({post_id}, 'start_time', ''),
        ({post_id}, 'assignment_id', ''),
        ({post_id}, 'student_id', ''),
        ({post_id}, 'course_id', ''),
        ({post_id}, 'author_id', ''),
        ({post_id}, 'emails', ''),
        ({post_id}, 'image', 'a:0:{{}}'),
        ({post_id}, 'question_hint', '');
    """

    if query == "posts_quiz":
        return """
        INSERT INTO `TA2tJr_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES
        (1, NOW(), UTC_TIMESTAMP(), '', {title}, '', 'publish', 'closed', 'closed', '', '', '', NOW(), UTC_TIMESTAMP(), '', 0, 0, 'stm-quizzes', '', 0);
        """

    if query == "meta_quiz":
        return """
        INSERT INTO `TA2tJr_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES
        ({post_id}, 'correct_answer', ''),
        ({post_id}, 'duration_measure', ''),
        ({post_id}, 'lesson_excerpt', ''),
        ({post_id}, 'random_questions', 'on'),
        ({post_id}, 'quiz_style', 'default'),
        ({post_id}, 'questions', {question_list}),
        ({post_id}, 'duration', '0'),
        ({post_id}, 'passing_grade', '0'),
        ({post_id}, 're_take_cut', '0');
        """

    # set for MariaDb 10
    if query == "setVar":
        return """
        SELECT ID INTO @{var_name}
        FROM TA2tJr_posts
        WHERE `post_title` = {title} AND `post_type` = {post_type}
        LIMIT 1
        """
    # to retrieve data just inserted, use this https://mariadb.com/kb/en/insert/#examples

def prepareSqlQuestion(data) -> str:
    queryPosts = getSql().format(question=data["question"])
    queryVar = getSql().format(var_name='id_question_stm', title=data["question"], post_type='stm-questions')
    queryMeta = getSql().format(post_id='', answers_arr=data["answers"], question_expl=data["explanation"])

def prepareSqlQuiz(data) -> str:
    queryPosts = getSql().format(title='')
    queryVar = getSql().format(var_name='id_quiz_stm', title='', post_type='stm-quizzes')
    queryMeta = getSql().format(post_id='', question_list='')

def exportToSql(inputFile):
    outputFile = None
    pathOut = input("Digite o nome do arquivo de saída \n")
    if pathOut == '.':
        pathOut = pathIn #just change the file extension
    try:
        outputFile = open(pathOut,'wt')
    except:
        print("Permissões insuficientes")
        return
    outputFile.write("BEGIN TRANSACTION\n")

    quizTitle = inputFile.readline()
    insertQuiz = True
    if (quizTitle.startswith("1.") or quizTitle == ''):
        insertQuiz = False
        inputFile.seek(0,0)

    outputFile.write("END TRANSACTION\n")

    outputFile.close()
    inputFile.close()
    print("Conversão concluída.")

def autoInsert(inputFile):
    settings = readConf()
    conn = None
    retry = True
    while retry:
        try:
            conn = mariadb.connect(
                user=settings["user"].strip(),
                password=settings["pw"].strip(),
                host=settings["host"].strip(),
                database=settings["db"].strip(),
                port=int(settings["port"].strip()))
            retry = False
        except mariadb.Error as e:
            print("Não foi possível conectar devido ao erro:\n",e)
            option = input("Tentar novamente? S/N ")
            if option.lower() == 's':
                setNewConf()
            else:
                return
    cur = conn.cursor()

    questions = []
    quizTitle = inputFile.readline()
    insertQuiz = True
    if (quizTitle.startswith("1.") or quizTitle == ''):
        insertQuiz = False
        inputFile.seek(0,0)
        print("Título não identificado. Incluindo somente pergutnas")

    keepReading = True
    questionsIncluded = 1

    while keepReading:
        lines = []
        for i in range(7):
            lines.append(inputFile.readline())

        if not lines[0]:
            keepReading = False
            continue

        question = lines[0].lstrip('1234567890.').strip()
        answers = [lines[1].strip(),lines[2].strip(), lines[3].strip(), lines[4].strip()]
        correct = re.search(r'(?<=Resposta Correta: )[A-F]\)', lines[5].strip(),re.IGNORECASE).group(0)
        explanation = lines[6].removeprefix("Explicação: ").strip()

        answersObj = []

        for i in range(4):
            answersObj.append({"text": answers[i].lstrip("ABCDEF)").strip(), "isTrue": answers[i].startswith(correct)})

        questionPost = getSql('posts_question').format(question='?')
        cur.execute(questionPost,(question,))

        questions.append(str(cur.lastrowid))

        questionMetaParameters = []
        for i in range(57):
            questionMetaParameters.append(cur.lastrowid)
        questionMetaParameters.append(dumps(answersObj))
        questionMetaParameters.append(cur.lastrowid)
        questionMetaParameters.append(explanation)
        for i in range(17):
            questionMetaParameters.append(cur.lastrowid)

        questionMeta = getSql('meta_question').format(post_id="?",answers_arr="?",question_expl="?")
        cur.execute(questionMeta,tuple(questionMetaParameters))
        # questionSql = prepareSqlQuestion({"question": question, "answers": dumps(answersObj), "explanation": explanation})
        print("Questão {} processada".format(questionsIncluded))
        questionsIncluded += 1

    if (insertQuiz):
        quizPost = getSql('posts_quiz').format(title='?')
        cur.execute(quizPost,(quizTitle,))
        print("Quiz criado")

        quizMeta = getSql('meta_quiz').format(post_id='?', question_list='?')
        quizMetaParameters = []
        for i in range(6):
            quizMetaParameters.append(cur.lastrowid)
        quizMetaParameters.append(','.join(questions))
        for i in range(3):
            quizMetaParameters.append(cur.lastrowid)
        cur.execute(quizMeta,tuple(quizMetaParameters))
        print(f"Incluídas {questionsIncluded} perguntas ao quiz")

    conn.commit()
    conn.close()
    inputFile.close()
    print("Processo concluído.")

def setNewConf() -> dict:
    host = input("Endereço: ")
    port = input("Porta: ")
    user = input("Usuário: ")
    pw = input("Senha: ")
    db = input("Nome da Base de Dados: ")
    prefix = input("Prefixo de tabela: ")
    confFile = open("./cnv.cfg", 'wt')
    confFile.writelines([
        "{}\n".format(host),
        "{}\n".format(port),
        "{}\n".format(user),
        "{}\n".format(pw),
        "{}\n".format(db),
        "{}\n".format(prefix)
    ])
    # confFile.flush()
    confFile.close()
    return {
        "user": user,
        "pw": pw,
        "db": db,
        "prefix": prefix,
        "host": host,
        "port": port
    }

def readConf() -> dict:
    host = ""
    port = ""
    user = ""
    pw = ""
    db = ""
    prefix = ""

    try:
        confFile = open("./cnv.cfg", 'rt')
        host = confFile.readline()
        port = confFile.readline()
        user = confFile.readline()
        pw = confFile.readline()
        db = confFile.readline()
        prefix = confFile.readline()
        confFile.close()

    except:
        confs = setNewConf()
        host = confs["host"]
        user = confs["user"]
        pw = confs["pw"]
        db = confs["db"]
        prefix = confs["prefix"]
        port = confs["port"]

    return {
        "host": host,
        "user": user,
        "pw": pw,
        "db": db,
        "prefix": prefix,
        "port": port
    }

#main
pathIn = input("Digite o caminho para o arquivo \n")
inputFile = None
try:
    inputFile = open(pathIn,'rt')
except:
    print("Falha ao ler o arquivo")
if inputFile != None:
    option = input("1 - Exportar para arquivo\n2 - Inserir automaticamente\n")
    if option == "1":
        option = input("1 - CSV\n2 - SQL")
        if option == "1":
            exportToCsv(inputFile)
        else:
            exportToSql(inputFile)
    else:
        autoInsert(inputFile)