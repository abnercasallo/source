from otree.api import *



class Constants(BaseConstants):
    name_in_url = 'prac'
    players_per_group = 4   ###Hará un match automático entre dos jugadores, de tal forma que si uno falta solo afecta a su pareja, pero no a los otros
    num_rounds = 3
    endowment = cu(100)
    multiplier = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField(initial=0)
    individual_share = models.CurrencyField()
    other_contribution= models.CurrencyField(initial=0)
    recurso= models.CurrencyField(initial=30)  #initial=0


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=1, max=10, label="¿Cuántas unidades desea extraer? (entre 1 y 10 unidades)"
    )
    acepta = models.StringField(choices=['No', 'Sí'], widget=widgets.RadioSelectHorizontal, )
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)

    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        group.recurso = group.recurso - group.total_contribution #En inicio ya se definió el valor inicial de recurso

        """if player.round_number>1:
             group.total_contribution=player.in_round(group.total_contribution - 1)"""

        #Se hizo en un app aparte para que no afecte las cantidades de rondas.
        #Sino se reiniciaría el monto cada vez que empieza una ronda nueva


# PAGES


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
    timeout_seconds = 60





class instrucciones(Page):
    pass

class Nivel(Page):
    pass


class Pagos(Page):
    pass



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    def vars_for_template(self):
        return dict(total_earnings=self.group.total_contribution * Constants.multiplier) #ganancia= (Constants.endowment - self.player.contribution) + self.group.individual_share

    pass


page_sequence = [Contribute, ResultsWaitPage, Results] #ConsentimientoInformado, instrucciones,
#Saqué "Nivel" para evitar la confunsión de la ultima ronda dejando el nivel bajo/alto
###Por cada ResultsWaitPage se correrá la función
### Templates: {{ if group.total_contribution <= 20 }} El nivel de Recurso es Alto {{ else }} El nivel de Recurso es Bajo {{ endif }}
