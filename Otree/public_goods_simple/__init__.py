from otree.api import *



class Constants(BaseConstants):
    name_in_url = 'public_goods_simple'
    players_per_group = 3
    num_rounds = 2
    endowment = cu(100)
    multiplier = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
   # recurso= models.CurrencyField(initial=30)  #initial=0


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="¿Cuántas unidades desea extraer?"
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.endowment - p.contribution + group.individual_share

# PAGES
class Contribute(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.recurso = 30
    form_model = 'player'
    form_fields = ['contribution']



class ConsentimientoInformado(Page):
    pass

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs



class Results(Page):
    def vars_for_template(self):
        return dict(total_earnings=self.group.total_contribution * Constants.multiplier) #ganancia= (Constants.endowment - self.player.contribution) + self.group.individual_share

    pass


page_sequence = [ Contribute, ResultsWaitPage, Results, ResultsWaitPage,] #ConsentimientoInformado, instrucciones,
