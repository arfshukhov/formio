import json
import random
from django.shortcuts import render, redirect
from .models import Forms, Spaces

def add_new_form(form_uid, title):
    Forms(form_uid=form_uid, title=title)


def add_new_space(form_uid, type, question, *variants):
    def create_unique_token():
        symbols = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z"]
        token: str = ""
        for _ in range(32):
            token += random.choice(symbols)
        return token
    if type == "select":
        Spaces(form_uid=form_uid, unique_token=create_unique_token(), type=type, question=question, variants=variants)
    elif type in ("input", "textarea"):
        Spaces(form_uid=form_uid, unique_token=create_unique_token(), type=type, question=question)
    else:
        return redirect(f'editor:{form_uid}/')


def get_dumps_of_spaces(form_uid):
    temp = Spaces.objects.filter(form_uid=form_uid)
    json_temp: list = []
    for elem in temp:
        json_temp.append(
            {"form_uid": elem.form_uid,
             "unique_token": elem.unique_token,
             "type": elem.type,
             "question": elem.type,
             "variants": elem.variants})
    return json.dumps(json_temp)
