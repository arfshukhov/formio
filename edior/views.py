from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import template
from .models import *
from db_ops import *
import json


class Select:
    def __init__(self, unique_token: str, question: str, variants: list):
        self.variants = variants
        self.question = question
        self.unique_token = unique_token
        self.code = "".join(["<div>",
                             f"<h2>{self.question}</h2>",
                             self.compile(),
                             "</div>"])

    def compile(self):
        res = ""
        for elem in self.variants:
            res += f"""
            <input type="radio" id="{elem}" name="{self.unique_token}" value="{elem}"> 
            <label for="{elem}">{elem}</label><br>
            """
        return res


class Input:
    def __init__(self, unique_token: str, question: str):
        self.question = question
        self.unique_token = unique_token
        self.type = "text"
        self.code = "".join(["<div>",
                             f'<h2>{self.question}</h2>'
                             f'<input type="{self.type}", id="{self.question}" name="{self.unique_token}"> ',
                             '</div>'])


class Textarea(Input):
    def __init__(self,unique_token: str, question: str):
        super().__init__(question, unique_token)
        self.type = "textarea"


class Logic:

    @classmethod
    def get_spaces(cls, form_uid):
        return json.load(get_dumps_of_spaces(form_uid))

    @classmethod
    def make_space(cls, unique_token, type, question, **variants: list):
        match type:
            case "input":
                return Input(unique_token=unique_token, question=question).code
            case "textarea":
                return Textarea(unique_token=unique_token, question=question)
            case "select":
                return Select(unique_token=unique_token, question=question, variants=variants)
            case _:
                raise ValueError

    @classmethod
    def prepare_spaces(cls, form_uid):
        data_of_spaces = cls.get_spaces(form_uid)
        spaces: list = []
        for el in data_of_spaces:
            match el["type"]:
                case "input" | "textarea":
                    spaces.append(cls.make_space(
                        unique_token=el["unique_token"],
                        type=el["type"],
                        question=el["question"]))
                case "select":
                    spaces.append(cls.make_space(
                        unique_token=el["unique_token"],
                        type=el["type"],
                        question=el["question"],
                        varicants=el["variants"]))
        return spaces


class Renderer(Logic):
    @classmethod
    def show_invalid_data_exception(cls, request):
        form_uid = request.POST.get("form_uid")
        context = {"form_uid": form_uid}
        render(request, "errorpage.html", context)

    @classmethod
    def redirect_to_error_page(cls, request):
        ...

    @classmethod
    def show_main_window(cls, request, form_uid):
        spaces = cls.prepare_spaces(form_uid)
        content = {'spaces': spaces}






