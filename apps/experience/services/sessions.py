"""Ephemeral, namespaced visitor state in the Django session.

Everything here is JSON-serializable (cookie session backend). The visitor
name lives ONLY in these keys and is cleared on reset/timeout (privacy.md §2).
"""

PREFIX = "experience."

KEYS = [
    "started_at",
    "name",
    "age",
    "gender",
    "qv_id",
    "question_order",
    "answers",
    "assessment_uuid",
]


def _key(name):
    return f"{PREFIX}{name}"


def clear_session(request):
    for name in KEYS:
        request.session.pop(_key(name), None)


def write_start_state(request, version, questions, assessment):
    request.session[_key("qv_id")] = version.id
    request.session[_key("question_order")] = [question.id for question in questions]
    request.session[_key("answers")] = {}
    request.session[_key("assessment_uuid")] = str(assessment.session_uuid)
    request.session[_key("started_at")] = assessment.started_at.isoformat()


def set_profile(request, data):
    request.session[_key("name")] = data["name"]
    request.session[_key("age")] = data["age"]
    request.session[_key("gender")] = data["gender"]


def get_name(request):
    return request.session.get(_key("name"))


def get_age(request):
    return request.session.get(_key("age"))


def get_gender(request):
    return request.session.get(_key("gender"))


def get_qv_id(request):
    return request.session.get(_key("qv_id"))


def get_question_order(request):
    return request.session.get(_key("question_order"), [])


def get_answers(request):
    return request.session.get(_key("answers"), {})


def add_answer(request, question_id, answer_option_id):
    answers = get_answers(request)
    answers[str(question_id)] = answer_option_id
    request.session[_key("answers")] = answers


def get_assessment_uuid(request):
    return request.session.get(_key("assessment_uuid"))
