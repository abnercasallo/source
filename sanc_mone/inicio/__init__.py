from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'inicio'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    acepta = models.StringField(choices=['No', 'Sí'], widget=widgets.RadioSelectHorizontal, )
    pass

# PAGES
# PAGES
class Inicio(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.recurso = 2000
        participant.total_contribution= 0

class instrucciones(Page):
    pass

class ResultsWaitPage(WaitPage):
    pass

class ConsentimientoInformado(Page):
    form_model = 'player'
    form_fields = ['acepta']
    pass

class agradecimiento(Page):
    def is_displayed(player: Player):
        return player.acepta == "No"  ####Esto es diferente a la versión 3, donde se suele usar el Self.

class instrucciones_time(Page):
    pass

class info_general(Page):
    pass

class calculo(Page):
    pass

class test(Page):
    pass

page_sequence = [ instrucciones, calculo, instrucciones_time]
