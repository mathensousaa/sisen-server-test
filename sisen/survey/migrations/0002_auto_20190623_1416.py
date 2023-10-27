# Generated by Django 2.1.9 on 2019-06-23 14:16

from django.db import migrations
import json



def get_data_from_file():
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(current_dir, '..', '..', '..', 'documentation', 'dataLoad.txt')
    
    with open(data_file_path, encoding='utf-8') as json_file:
        return json.load(json_file)

def get_model(apps, model, app='survey'):
    return apps.get_model(app, model)

def get_object(apps, model, attrs):
    Model = get_model(apps, model)
    return Model.objects.filter(**attrs)

def institution_load(apps):
    Institution = get_model(apps, 'Institution')
    for i_dict in fixtures.get('institution', []):
        institution = Institution(name=i_dict.get('name'), initials=i_dict.get('initials'))
        institution.save()
        program_load(apps, i_dict, institution)

def program_load(apps, i_dict, institution):
    Program = get_model(apps, 'Program')
    for p_dict in i_dict.get('program', []):
        program = Program(institution=institution, name=p_dict.get('name'))
        program.save()
        class_load(apps, p_dict, program)

def class_load(apps, p_dict, program):
    Class = get_model(apps, 'Class')
    for c_dict in p_dict.get('class', []):
        sclass = Class(program=program,
            code=c_dict.get('code'),
            description=c_dict.get('description'),
            semester=c_dict.get('semester'),
            year=c_dict.get('year'))
        sclass.save()

def answer_load(apps):
    Answer = get_model(apps, 'Answer')
    for s_dict in fixtures.get('study', []):
        for a_dict in s_dict.get('answers', []):
            if not get_object(apps, 'Answer', a_dict):
                answer = Answer(value=a_dict.get('value'),
                    text=a_dict.get('text'))
                answer.save()

def study_load(apps):
    Study = get_model(apps, 'Study')
    for s_dict in fixtures.get('study', []):
        study = Study(acronym=s_dict.get('acronym'),
            description=s_dict.get('description'))
        study.save()
        studyoption_load(apps, s_dict, study)

def studyoption_load(apps, s_dict, study):
    StudyOption = get_model(apps, 'StudyOption')
    for so_dict in s_dict.get('studyoption', []):
        study_option = StudyOption(study=study,
            code=so_dict.get('code'),
            description=so_dict.get('description'))
        study_option.save()
        question_load(apps, so_dict, study_option, s_dict.get('questions', []))

def question_load(apps, so_dict, study_option, questions):
    Question = get_model(apps, 'Question')
    Answer = get_model(apps, 'Answer')
    study_option_question_pos = so_dict.get('questions', [])
    study_option_question_dicts = filter(
        lambda e: e.get('position') in study_option_question_pos, questions)
    for q_dict in study_option_question_dicts:
        question = Question(position=q_dict.get('position'),
            text=q_dict.get('text'),
            study=study_option.study,
            study_option=study_option)
        question.save()
        answers = Answer.objects.filter(value__in=q_dict.get('answers', []))
        for answer in answers:
            answer.questions.add(question)
            answer.save()

def student_load(apps):
    pass

def professor_load(apps):
    pass

def admin_load(apps):
    from django.contrib.auth.models import User
    # User = apps.get_model('auth', 'User')
    for admin_dict in fixtures.get("admin", []):
        user = User.objects.create_user(**admin_dict)
        user.is_superuser = True
        user.is_staff = True
        user.save()

def group_load(apps):
    from django.contrib.auth.models import Group
    # User = apps.get_model('auth', 'Group')
    Group(name='Student').save()
    Group(name='Professor').save()

def initial_data_load(apps, schema_editor):
    admin_load(apps)
    group_load(apps)
    institution_load(apps)
    answer_load(apps)
    study_load(apps)

fixtures = get_data_from_file()

class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_data_load),
    ]
