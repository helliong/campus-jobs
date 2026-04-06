from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vacancies = [
    {
        "id": 1,
        "title": {
            "en": "Teaching Assistant",
            "de": "Lehrassistent",
            "ru": "Ассистент преподавателя"
        },
        "description": {
            "en": "Help a professor with lectures and assignments",
            "de": "Unterstützung eines Professors bei Vorlesungen und Aufgaben",
            "ru": "Помощь преподавателю с лекциями и заданиями"
        }
    },
    {
        "id": 2,
        "title": {
            "en": "Research Intern",
            "de": "Forschungspraktikant",
            "ru": "Стажёр-исследователь"
        },
        "description": {
            "en": "Participate in university research projects",
            "de": "Teilnahme an Forschungsprojekten der Universität",
            "ru": "Участие в исследовательских проектах университета"
        }
    },
    {
        "id": 3,
        "title": {
            "en": "Administrative Assistant",
            "de": "Verwaltungsassistent",
            "ru": "Административный помощник"
        },
        "description": {
            "en": "Support the university office with documents and scheduling",
            "de": "Unterstützung des Universitätsbüros bei Dokumenten und Zeitplanung",
            "ru": "Помощь офису университета с документами и расписанием"
        }
    }
]

applications = []
application_counter = 1


class ApplyRequest(BaseModel):
    vacancy_id: int


def get_language(request: Request):
    lang = request.headers.get("Accept-Language", "en")
    if lang not in ["en", "de", "ru"]:
        lang = "en"
    return lang


def get_messages(lang: str):
    messages = {
        "en": {
            "application_sent": "Application submitted successfully",
            "vacancy_not_found": "Vacancy not found",
            "status_pending": "Pending",
            "my_applications": "My applications"
        },
        "de": {
            "application_sent": "Bewerbung erfolgreich gesendet",
            "vacancy_not_found": "Stelle nicht gefunden",
            "status_pending": "Ausstehend",
            "my_applications": "Meine Bewerbungen"
        },
        "ru": {
            "application_sent": "Заявка успешно отправлена",
            "vacancy_not_found": "Вакансия не найдена",
            "status_pending": "На рассмотрении",
            "my_applications": "Мои заявки"
        }
    }
    return messages[lang]


@app.get("/vacancies")
def get_vacancies(request: Request):
    lang = get_language(request)

    result = []
    for v in vacancies:
        result.append({
            "id": v["id"],
            "title": v["title"][lang],
            "description": v["description"][lang]
        })

    return result


@app.post("/apply")
def apply(data: ApplyRequest, request: Request):
    global application_counter

    lang = get_language(request)
    messages = get_messages(lang)

    vacancy = next((v for v in vacancies if v["id"] == data.vacancy_id), None)
    if not vacancy:
        return {
            "message": messages["vacancy_not_found"]
        }

    application = {
        "id": application_counter,
        "vacancy_id": vacancy["id"],
        "vacancy_title": vacancy["title"][lang],
        "status": "pending",
        "status_label": messages["status_pending"]
    }

    applications.append(application)
    application_counter += 1

    return {
        "message": messages["application_sent"],
        "application": application
    }


@app.get("/applications/my")
def get_my_applications(request: Request):
    lang = get_language(request)
    messages = get_messages(lang)

    localized_applications = []

    for app_item in applications:
        vacancy = next((v for v in vacancies if v["id"] == app_item["vacancy_id"]), None)

        if vacancy:
            localized_applications.append({
                "id": app_item["id"],
                "vacancy_id": app_item["vacancy_id"],
                "vacancy_title": vacancy["title"][lang],
                "status": app_item["status"],
                "status_label": messages["status_pending"]
            })

    return {
        "title": messages["my_applications"],
        "applications": localized_applications
    }