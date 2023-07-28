from job_searcher import JobSearchBot

# Ключевые слова для сравнения с описанием вакансии
resume = "JavaScript CSS3 HTML5 Vue.js Linux Python PostgreSQL SQLAlchemy FastAPI Nginx Docker Git Django Framework Flask"
# Название вакансий, по которым будет производиться поиск
vacancies = ["fullstack", "frontend", "backend", "python", "vue", "бэкэнд", "фронтенд", "developer", "разработчик", "программист"]
# Исключение слов из названий и описаний вакансий
skip_words = ["php", "laravel", "c#", "c++", "senior", "java", "react", "angular", "node.js", ".net", "ruby"]
# Среднее арифметическое между векторым и последовательным сравнением resume и описанием вакансии
similarity_threshold = 0.20
# Перезапуск поиска через 1200 секунд
pause_duration = 1200
# Название таблицы для этого поиска
table_name = "dev"

try:
    bot = JobSearchBot(resume, vacancies, skip_words, similarity_threshold, table_name)
    bot.run_search(pause_duration)
except KeyboardInterrupt:
    print(" Поиск остановлен")
