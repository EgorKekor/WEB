from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from asker.models import Question, Tag, Answer


def paginator(questions_list, request):
    paginator = Paginator(questions_list, 4)

    page = request.GET.get('page')
    try:
        questions_list = paginator.page(page)
    except PageNotAnInteger:
        questions_list = paginator.page(1)
    except EmptyPage:
        questions_list = paginator.page(paginator.num_pages)
    return questions_list


def tag(request, tag):
    m_tag = Tag.objects.get(title=tag)
    questions_list = Question.objects.filter(tags=m_tag.id)
    questions_list = paginator(questions_list, request)
    return render(request, 'asker/tag.html', {"questions": questions_list})


def hot(request):
    questions_list = Question.objects.get_hot()
    questions_list = paginator(questions_list, request)
    return render(request, 'asker/hot.html', {"questions": questions_list})


def index(request):
    questions_list = Question.objects.get_new()
    questions_list = paginator(questions_list, request)
    return render(request, 'asker/index.html', {"questions": questions_list})


def question(request, id):
    t_question = Question.objects.get(pk=id)
    t_answer = Answer.objects.filter(question=id)
    list = [t_question, t_answer]
    a = {"question": list}
    return render(request, "asker/question.html", {"question": list})


def ask(request):
    return render(request, "asker/ask.html", {})


def registration_page(request):
    return render(request, "asker/registration_page.html", {})


def settings(request):
    return render(request, "asker/settings.html", {})


def login(request):
    return render(request, "asker/login.html", {})
