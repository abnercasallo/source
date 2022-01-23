from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'formulario_pagos'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Pagos (Page):
    """def vars_for_template(self):
        return dict(participant_id=self.participant.label)"""
    pass


page_sequence = [Pagos]
