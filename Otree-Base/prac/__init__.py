from otree.api import *



class Constants(BaseConstants):
    name_in_url = 'prac'
    players_per_group = 4
    num_rounds = 3
    endowment = cu(100)
    multiplier = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField(initial=0) #En caso que no se llene nada tendrá 0 y no saldrá error por NaN
    individual_share = models.CurrencyField()
    other_contribution= models.CurrencyField(initial=0)
    recurso= models.CurrencyField(initial=30)


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
