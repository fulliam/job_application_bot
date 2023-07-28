import requests
from difflib import SequenceMatcher
import webbrowser
from regions import regions
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
import time
import psycopg2
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobSearchBot:
    def __init__(self, resume, vacancies, skip_words, similarity_threshold, table_name):
        self.resume = resume
        self.vacancies = vacancies
        self.skip_words = skip_words
        self.similarity_threshold = similarity_threshold
        self.url = "https://api.hh.ru/vacancies"
        self.table_name = table_name

        self.connection = psycopg2.connect(
            host = DB_HOST,
            port = DB_PORT,
            database = DB_NAME,
            user = DB_USER,
            password = DB_PASS
        )
        self.cursor = self.connection.cursor()
        self.create_table()
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit([self.resume])

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (vacancy_id VARCHAR(255))"
        self.cursor.execute(query)
        self.connection.commit()

    def store_vacancy(self, vacancy_id):
        query = f"INSERT INTO {self.table_name} (vacancy_id) VALUES (%s)"
        values = (vacancy_id,)
        self.cursor.execute(query, values)
        self.connection.commit()

    def check_vacancy_applied(self, vacancy_id):
        query = f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE vacancy_id = %s)"
        values = (vacancy_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()[0]
        return result

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def colored_text(self, text, color, style=None):
        if style:
            colored_text = colored(text, color, style=style)
        else:
            colored_text = colored(text, color)
        print(colored_text)

    def check_skip_words(self, vacancy_name):
        return any(word in vacancy_name.lower() for word in self.skip_words)

    def extract_vacancy_description(self, snippet):
        requirement = snippet.get('requirement')
        responsibility = snippet.get('responsibility')
        if requirement is not None and responsibility is not None:
            return requirement + ' ' + responsibility
        elif requirement is not None:
            return requirement
        elif responsibility is not None:
            return responsibility
        else:
            return ""

    def search_vacancies(self):
        resume_vector = self.vectorizer.transform([self.resume])
        for vacancy in self.vacancies:
            for region in regions:
                params = {
                    "text": vacancy,
                    "area": region['id'],
                    "per_page": 100
                }
                try:
                    response = requests.get(self.url, params=params).json()

                    if 'items' in response:
                        for vacancy_item in response['items']:
                            if self.check_vacancy_applied(vacancy_item['id']):
                                continue

                            if self.check_skip_words(vacancy_item['name']):
                                continue

                            vacancy_description = self.extract_vacancy_description(vacancy_item['snippet'])

                            if self.check_skip_words(vacancy_description):
                                continue
                            
                            vacancy_vector = self.vectorizer.transform([vacancy_description])
                            similarity_vector = cosine_similarity(resume_vector, vacancy_vector)[0][0]
                            similarity_sequence = SequenceMatcher(None, vacancy_description, self.resume).ratio()
                            similarity = (similarity_vector + similarity_sequence)/2

                            self.colored_text("Совпадение: " + str(similarity), 'red')
                            if similarity > self.similarity_threshold:
                                apply_url = vacancy_item['apply_alternate_url']
                                self.colored_text("Найдена подходящая вакансия!", 'green')
                                self.colored_text("Вакансия:" + vacancy_item['name'], 'white')
                                self.colored_text("Регион:" + region['name'], 'white')
                                self.colored_text("Ссылка на вакансию:" + apply_url, 'blue')
                                self.store_vacancy(vacancy_item['id'])
                                webbrowser.open(apply_url)
                                time.sleep(7)
                    else:
                        continue
                except requests.exceptions.RequestException:
                    print("Ошибка при запросе к API")
                    continue

    def run_search(self, pause_duration):
        try:
            while True:
                self.search_vacancies()
                time.sleep(pause_duration)
        except psycopg2.Error as e:
            print("Ошибка при работе с базой данных:", e)
        finally:
            self.close_connection()