russian = dict(
    testsys="Тестирующая система",
    theory="Теория",
    tasks="Задачи",
    submit="Сдача",
    scoreboard="Таблица результатов",
    submit_sol="Сдать задачу",
    submissions="Посылки",
    logout="Выход",
    select_task="Выберите задачу",
    yours="Мои посылки",
    protocol="Протокол решения №",
    not_finished="Тестирование не завершено. Пожалуйста, подождите.",
    solution="Решение №",
    task="задача",
    back="Назад"
)

english = dict(
    testsys="Testing system",
    theory="Theory",
    tasks="Tasks",
    submit="Submit",
    scoreboard="Scoreboard",
    submit_sol="Submit a solution",
    submissions="Submissions",
    logout="Log out",
    select_task="Select task",
    yours="My submissions",
    protocol="Protocol #",
    not_finished="Testing is not finished yet, please wait...",
    solution="Submission #",
    task="task",
    back="Back"
)

languages = dict(
    russian=russian,
    english=english
)

def get_locale():
    return russian
