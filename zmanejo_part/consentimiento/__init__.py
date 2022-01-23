from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'consentimiento'
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



class ResultsWaitPage(WaitPage):
    pass

class ConsentimientoInformado(Page):
    form_model = 'player'
    form_fields = ['acepta']
    pass

class agradecimiento(Page):
    def is_displayed(player: Player):
        return player.acepta == "No"  ####Esto es diferente a la versión 3, donde se suele usar el Self.




page_sequence = [ConsentimientoInformado, agradecimiento]
