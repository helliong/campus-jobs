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
messages = []

application_counter = 1
message_counter = 1


class ApplyRequest(BaseModel):
    vacancy_id: int


class MessageRequest(BaseModel):
    sender: str
    text: str


def get_language(request: Request):
    lang = request.headers.get("Accept-Language", "en")
    if lang not in ["en", "de", "ru"]:
        lang = "en"
    return lang


def get_messages(lang: str):
    translations = {
        "en": {
            "application_sent": "Application submitted successfully",
            "vacancy_not_found": "Vacancy not found",
            "status_pending": "Pending",
            "my_applications": "My applications",
            "already_applied": "You have already applied for this position",
            "application_not_found": "Application not found",
            "message_sent": "Message sent successfully",
            "invalid_sender": "Invalid sender. Use 'student' or 'employer'",
            "messages_title": "Messages"
        },
        "de": {
            "application_sent": "Bewerbung erfolgreich gesendet",
            "vacancy_not_found": "Stelle nicht gefunden",
            "status_pending": "Ausstehend",
            "my_applications": "Meine Bewerbungen",
            "already_applied": "Sie haben sich bereits für diese Stelle beworben",
            "application_not_found": "Bewerbung nicht gefunden",
            "message_sent": "Nachricht erfolgreich gesendet",
            "invalid_sender": "Ungültiger Absender. Verwenden Sie 'student' oder 'employer'",
            "messages_title": "Nachrichten"
        },
        "ru": {
            "application_sent": "Заявка успешно отправлена",
            "vacancy_not_found": "Вакансия не найдена",
            "status_pending": "На рассмотрении",
            "my_applications": "Мои заявки",
            "already_applied": "Вы уже откликались на эту вакансию",
            "application_not_found": "Заявка не найдена",
            "message_sent": "Сообщение успешно отправлено",
            "invalid_sender": "Неверный отправитель. Используйте 'student' или 'employer'",
            "messages_title": "Сообщения"
        }
    }
    return translations[lang]


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
    ui_messages = get_messages(lang)

    vacancy = next((v for v in vacancies if v["id"] == data.vacancy_id), None)
    if not vacancy:
        return {
            "message": ui_messages["vacancy_not_found"]
        }

    existing_application = next(
        (app_item for app_item in applications if app_item["vacancy_id"] == data.vacancy_id),
        None
    )

    if existing_application:
        return {
            "message": ui_messages["already_applied"]
        }

    application = {
        "id": application_counter,
        "vacancy_id": vacancy["id"],
        "status": "pending"
    }

    applications.append(application)
    application_counter += 1

    return {
        "message": ui_messages["application_sent"],
        "application": {
            "id": application["id"],
            "vacancy_id": application["vacancy_id"],
            "vacancy_title": vacancy["title"][lang],
            "status": application["status"],
            "status_label": ui_messages["status_pending"]
        }
    }


@app.get("/applications/my")
def get_my_applications(request: Request):
    lang = get_language(request)
    ui_messages = get_messages(lang)

    localized_applications = []

    for app_item in applications:
        vacancy = next((v for v in vacancies if v["id"] == app_item["vacancy_id"]), None)

        if vacancy:
            localized_applications.append({
                "id": app_item["id"],
                "vacancy_id": app_item["vacancy_id"],
                "vacancy_title": vacancy["title"][lang],
                "status": app_item["status"],
                "status_label": ui_messages["status_pending"]
            })

    return {
        "title": ui_messages["my_applications"],
        "applications": localized_applications
    }


@app.get("/applications/{application_id}/messages")
def get_application_messages(application_id: int, request: Request):
    lang = get_language(request)
    ui_messages = get_messages(lang)

    application = next((app_item for app_item in applications if app_item["id"] == application_id), None)
    if not application:
        return {
            "message": ui_messages["application_not_found"],
            "messages": []
        }

    application_messages = [
        msg for msg in messages if msg["application_id"] == application_id
    ]

    return {
        "title": ui_messages["messages_title"],
        "messages": application_messages
    }


@app.post("/applications/{application_id}/messages")
def send_message(application_id: int, data: MessageRequest, request: Request):
    global message_counter

    lang = get_language(request)
    ui_messages = get_messages(lang)

    application = next((app_item for app_item in applications if app_item["id"] == application_id), None)
    if not application:
        return {
            "message": ui_messages["application_not_found"]
        }

    if data.sender not in ["student", "employer"]:
        return {
            "message": ui_messages["invalid_sender"]
        }

    new_message = {
        "id": message_counter,
        "application_id": application_id,
        "sender": data.sender,
        "text": data.text
    }

    messages.append(new_message)
    message_counter += 1

    return {
        "message": ui_messages["message_sent"],
        "data": new_message
    }