from typing import List, Any

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import template
from .models import *
from db_ops import *
import json


class Space:
    def __init__(self, unique_token: str, question: str):
        self.question = question
        self.unique_token = unique_token

    def compile(self, type, *variants):
        match type:
            case "input" | "textarea":
                return "".join(["<div>",
                                f'<h2>{self.question}</h2>'
                                f'<input type="{type}", id="{self.question}" name="{self.unique_token}"> ',
                                '</div>'])
            case "select":
                res = f"""<div>
                <h2>{self.question}</h2>"""
                for elem in variants:
                    res += f"""
                        <input type="radio" id="{elem}" name="{self.unique_token}" value="{elem}"> 
                        <label for="{elem}">{elem}</label><br>
                        """
                else:
                    res += "</div>"
                return res


class Select(Space):
    def __init__(self, unique_token: str, question: str, variants: list):
        super().__init__(unique_token, question)
        self.variants = variants
        self.code_select = self.compile("select", self.variants)


class Input(Space):
    def __init__(self, unique_token, question):
        super().__init__(unique_token, question)
        self.type = "text"
        self.code = self.compile(self.type)


class Textarea(Space):
    def __init__(self, unique_token: str, question: str):
        super().__init__(question, unique_token)
        self.type = "textarea"
        self.code = self.compile("textarea")


class Logic:
    symbols = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g",
               "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n",
               "O", "o", "P", "p", "Q", "q", "R", " r", "S", "s", "T", "t", "U", "u", "V", "v",
               "W", "w", "X", "x", "Y", "y", "Z", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    @classmethod
    def generate_form_uid(cls):
        form_uid = ""
        for _ in range(64):
            form_uid += random.choice(cls.symbols)

    @classmethod
    def create_unique_token(cls):

        token: str = ""
        for _ in range(32):
            token += random.choice(cls.symbols)
        return token

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
