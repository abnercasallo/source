from otree.api import *
import random



class Constants(BaseConstants):
    name_in_url = 'public_goods_simple'
    players_per_group = 4   ###Hará un match automático entre dos jugadores, de tal forma que si uno falta solo afecta a su pareja, pero no a los otros
    num_rounds = 10
    endowment = cu(100)
    multiplier = 1
    e_h=10
    a_h=8
    b_h=0.6
    alfa_h=2
    n_h=4
    e_l = 10
    a_l = 8
    b_l = 0.6
    alfa_l = 2
    n_l = 4
    sanc_2 = 9.6



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField(initial=0)
    individual_share = models.CurrencyField()
    other_contribution= models.CurrencyField(initial=0)
    random_player_id = models.CurrencyField(initial=0)
    random_num= models.CurrencyField(initial=0)

   # recurso= models.CurrencyField(initial=30)  #initial=0


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=1, max=10, label="¿Cuántas unidades desea extraer? (desde 1 hasta 10 unidades)"
    )
    acepta = models.StringField(choices=['No', 'Sí'], widget=widgets.RadioSelectHorizontal, )
    sanc=models.CurrencyField(initial=0)
    pago_final= models.CurrencyField(initial=0)
    contrib_personal= models.CurrencyField(initial=0)
    exceso = models.StringField(initial='NO')
    control = models.StringField(initial="NO PASA")
    monitor=models.StringField (initial="NO ha sido supervisada")

    pass



# FUNCTIONS


def set_payoffs(group: Group):

    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)

    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    ###Elegimos un Id a azar
    group.random_player_id = random.randint(1, 4)
    group.random_num = random.randint(1, 20)
    ### Elegimos un número al azar del 1 al 80, cada decena tendrá 1/8 de probabilidad


    for p in players:
        group.other_contribution = group.total_contribution - p.contribution
        if group.total_contribution <=20:
            p.payoff =Constants.a_h*p.contribution-0.5*Constants.b_h*p.contribution**2+Constants.alfa_h*Constants.n_h*Constants.e_h-Constants.alfa_h*(+p.contribution+group.other_contribution)
        else:
            p.payoff = Constants.a_l * p.contribution - 0.5 * Constants.b_l * p.contribution** 2 + Constants.alfa_l * Constants.n_l * Constants.e_l - Constants.alfa_l * (
                        +p.contribution + group.other_contribution)
       # p.contrib_personal = p.contribution

       # p.random_num= random.uniform(0,1)

        if p.id_in_group == group.random_player_id:
            p.control = "PASA"   ###EL jugador que pase será podrá ser sancionado con una pro 0.8:
            ###O SEA PUEDE PASAR PERO NO NECESARIAMENTE SE LE APLICARÁ SANCIÓN
            #POR EJEMPLO, PASA, LE SALE 4, PERO ELIGIÓ 1
        if group.random_num<= 10:
            p.monitor="SÍ ha sido supervisada"

#p.id_in_group== group.random_player_id
        if p.id_in_group== group.random_player_id and p.contribution >1 and group.random_num<= 10:
            p.exceso = 'SÍ'
            p.sanc= Constants.sanc_2*(p.contribution-1)
            p.pago_final = p.payoff - p.sanc
        else:
            p.pago_final = p.payoff







        #   participant = p.participant
      #  participant.recurso = participant.recurso - group.total_contribution #En inicio ya se definió el valor inicial de recurso

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


page_sequence = [Contribute, ResultsWaitPage, Results, Nivel, Pagos] #ConsentimientoInformado, instrucciones,

###Por cada ResultsWaitPage se correrá la función
### Templates: {{ if group.total_contribution <= 20 }} El nivel de Recurso es Alto {{ else }} El nivel de Recurso es Bajo {{ endif }}
#En esta ronda usted extrajo {{player.contrib_personal}}. Al 80% de probabilidad de detención,
#  <td>Su puntaje de acuerdo al cuadro es {{player.payoff}} </td>
