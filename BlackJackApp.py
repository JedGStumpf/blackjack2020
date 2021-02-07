"""
The code written below and in the corresponding kv file represents my first app.  It was a tremendous learning experience.
I have since packaged this app with Pyinstaller for Windows and Buildozer for Android.
"""

import kivy
kivy.require('1.11.1')  # Replace with version of Kivy
import webbrowser as webbrowser
from random import random as random
from random import shuffle as shuffle
from math import ceil as ceil

# The next 2 lines for Config is used ony for mouse touch instances, uncomment them for that purpose.  For touchscreens delete or leave them commented out.
# from kivy.config import Config
# Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# The Below line is used when packaging for Windows, uncomment if that is your use case.
# from kivy.resources import resource_add_path, resource_find
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Rectangle 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial



class ScreenManagement(ScreenManager):
    pass


class SpinnerOption(ScreenManager):
    pass


class RedirectPopup(Popup):
    rdp = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RedirectPopup, self).__init__(**kwargs)
    
    def open_link(self, instance):
        webbrowser.open('https://en.m.wikipedia.org/wiki/Blackjack')


class RulesPopup(Popup):
    rp = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RulesPopup, self).__init__(**kwargs)


    def redirect_popup(self):
        gotowiki = RedirectPopup(title = 'Leave App to Webpage', size_hint = (0.55, 0.55), title_align = 'center', auto_dismiss = False)
        gotowiki.open()


# Initial screen with options to start the game or to read rules and to redirect to wiki page for basic blackjack strategy
class HomeScreen(Screen):
    hs = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(HomeScreen,  self).__init__(**kwargs)
        


    def rules_popup(self):
        rules = RulesPopup(title = 'Game Rules', size_hint = (0.77, 0.66), title_align = 'center', auto_dismiss = False)
        rules.open()
        


class DeckOfCards:
    """  Class to initialize the objects containing cards and values of the deck
    """
    def __init__(self, card = None, value = None):

        self.card = card

        self.value = value


#Deck of Cardsd objects, each object is an image of a card and the corrisponding value    
two_diamond = DeckOfCards('two_diamond.png', 2)
two_heart = DeckOfCards('two_heart.png', 2)
two_club = DeckOfCards('two_club.png', 2)
two_spade = DeckOfCards('two_spade.png', 2)

three_diamond = DeckOfCards('three_diamond.png', 3)
three_heart = DeckOfCards('three_heart.png', 3)
three_club = DeckOfCards('three_club.png', 3)
three_spade = DeckOfCards('three_spade.png', 3)

four_diamond  = DeckOfCards('four_diamond.png', 4)
four_heart  = DeckOfCards('four_heart.png', 4)
four_club  = DeckOfCards('four_club.png', 4)
four_spade  = DeckOfCards('four_spade.png', 4)

five_diamond = DeckOfCards('five_diamond.png', 5)
five_heart = DeckOfCards('five_heart.png', 5)
five_club = DeckOfCards('five_club.png', 5)
five_spade = DeckOfCards('five_spade.png', 5)

six_diamond = DeckOfCards('six_diamond.png', 6)
six_heart = DeckOfCards('six_heart.png', 6)
six_club = DeckOfCards('six_club.png', 6)
six_spade = DeckOfCards('six_spade.png', 6)

seven_diamond = DeckOfCards('seven_diamond.png', 7)
seven_heart = DeckOfCards('seven_heart.png', 7)
seven_club = DeckOfCards('seven_club.png', 7)
seven_spade = DeckOfCards('seven_spade.png', 7)

eight_diamond = DeckOfCards('eight_diamond.png', 8)
eight_heart = DeckOfCards('eight_heart.png', 8)
eight_club = DeckOfCards('eight_club.png', 8)
eight_spade = DeckOfCards('eight_spade.png', 8)

nine_diamond = DeckOfCards('nine_diamond.png', 9)
nine_heart = DeckOfCards('nine_heart.png', 9)
nine_club = DeckOfCards('nine_club.png', 9)
nine_spade = DeckOfCards('nine_spade.png', 9)

ten_diamond = DeckOfCards('ten_diamond.png', 10)
ten_heart = DeckOfCards('ten_heart.png', 10)
ten_club = DeckOfCards('ten_club.png', 10)
ten_spade = DeckOfCards('ten_spade.png', 10)

jack_diamond = DeckOfCards('jack_diamond.png', 10)
jack_heart = DeckOfCards('jack_heart.png', 10)
jack_club = DeckOfCards('jack_club.png', 10)
jack_spade = DeckOfCards('jack_spade.png', 10)

queen_diamond = DeckOfCards('queen_diamond.png', 10)
queen_heart = DeckOfCards('queen_heart.png', 10)
queen_club = DeckOfCards('queen_club.png', 10)
queen_spade = DeckOfCards('queen_spade.png', 10)

king_diamond = DeckOfCards('king_diamond.png', 10)
king_heart = DeckOfCards('king_heart.png', 10)
king_club = DeckOfCards('king_club.png', 10)
king_spade = DeckOfCards('king_spade.png', 10)

ace_diamond = DeckOfCards('ace_diamond.png', 11)
ace_heart = DeckOfCards('ace_heart.png', 11)
ace_club = DeckOfCards('ace_club.png', 11)
ace_spade = DeckOfCards('ace_spade.png', 11)

blank_card = DeckOfCards('card.png', 0)

chip = DeckOfCards('chip.png')

ace_list = [ace_diamond.card, ace_heart.card, ace_club.card, ace_spade.card]


# Popup Class, see func bet_over_chips in GameScreen Class
class BetTooHigh_Pop(Popup):
    pass
    
# Popup to give option of exitinng the app
class ExitPopup(Popup):
    pass


# Mainscreen Class where all the logic flow of the game is
class GameScreen(Screen):
    
    # Pull in DeckOfCards attributes
    deck_cards = DeckOfCards()

    scrn_mgr = ScreenManagement()

    
    # Special propoerties to link objects of the kivy file
    bet_amnt = ObjectProperty(None)
    play_buttons = ObjectProperty()
    chp_count = ObjectProperty(None)
    maxbet = ObjectProperty(None)
    notify = ObjectProperty(None)
    
    #booleans used in the methods logic
    update_bet = True
    dealt_table = False
    hit_again = False
    bust = False
    blck_jck = False
    dealer_turn = False
    play_turn = False 
    soft_ace = False
    splitting_aces = False
    bl_split = False
    bl_split2 = False
    bl_split_last = False
    
    #initiated lists
    deck = []
    player_hands = []
    hand_values = []
    hand_boxes = []
    tbl_crds = [[],[],[],[],[],[]]
    tbl_vals = [[],[],[],[],[],[]]
    ace_as_1 = [[],[],[],[],[],[]]
    bet_vals = []
    
    #count values
    value = 0
    hold_bet = 0
    split_count = 0
    split_deal = 0
    who_deal = 0
    add_split_box_ind = 0
    
    # String to display messages
    banner = ''

    
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(*args, **kwargs)

    def max_bet(self, value):
        new_chip_count = value
        return f'Bet\n${new_chip_count}'

    def half_bet(self, value):
        new_chip_count = ceil(int(value)/2)
        return f'Bet\n${str(new_chip_count)}'
    
    # Creates Buttons for Bet Options.  Called on when Player is changing their bet amount or making first bet.
    def add_bet_options(self):
        self.ids.new_deal.disabled = True
        if len(self.ids.All_Boxes.children) > 8:
            return

        self.all_bets = BoxLayout(orientation = 'horizontal', padding = (25,25))
        constants = BoxLayout(orientation = 'vertical')
        var_options = BoxLayout(orientation = 'vertical')
        separate = Label(size_hint = (0.3,1))
        self.all_bets.add_widget(constants)
        self.all_bets.add_widget(separate)
        self.all_bets.add_widget(var_options)
                
        bet_hundo = Button(text = 'Bet\n$100', text_size = self.size, color = [0,0,0,1], bold = True, halign = 'center', valign = 'middle', font_size = self.height/45, background_normal = "", background_color = [0,0.4,0,1], border = (5,5,5,5))
        
        if int(bet_hundo.text[5:]) > int(self.ids.chip_count.text):
            bet_hundo.disabled = True

        hundo_update = partial(self.connect_texts, bet_hundo.text)
        bet_hundo.bind(on_release = hundo_update)
        constants.add_widget(bet_hundo)

        spacer = Label(size_hint = (0,0.3))
        constants.add_widget(spacer)

        bet_fivehundo = Button(text = 'Bet\n$500', color = [0,0,0,1], text_size = self.size, bold = True, halign = 'center', valign = 'middle', font_size = self.height/45, background_normal = "", background_color = [0,0.4,0,1])
        
        if int(bet_fivehundo.text[5:]) > int(self.ids.chip_count.text):
            bet_fivehundo.disabled = True

        fivehundo_update = partial(self.connect_texts, bet_fivehundo.text)
        bet_fivehundo.bind(on_release = fivehundo_update)
        constants.add_widget(bet_fivehundo)

        spacer1 = Label(size_hint = (0,0.3))
        constants.add_widget(spacer1)

        bet_oneK = Button(text = 'Bet\n$1000', color = [0,0,0,1], text_size = self.size, bold = True, halign = 'center', valign = 'middle', font_size = self.height/40, background_normal = "", background_color = [0,0.4,0,1])

        if int(bet_oneK.text[5:]) > int(self.ids.chip_count.text):
            bet_oneK.disabled = True

        oneK_update = partial(self.connect_texts, bet_oneK.text)
        bet_oneK.bind(on_release = oneK_update)
        constants.add_widget(bet_oneK)

        bet_half = Button(text = self.half_bet(self.ids.chip_count.text), color = [0,0,0,1], text_size = self.size, bold = True, halign = 'center', valign = 'middle', font_size = self.height/40, background_normal = "", background_color = [0,0.4,0,1])

        half_update = partial(self.connect_texts, bet_half.text)
        bet_half.bind(on_release = half_update)
        var_options.add_widget(bet_half)

        spacer2 = Label(size_hint = (0,0.3))
        var_options.add_widget(spacer2)

        bet_all = Button(text = self.max_bet(self.ids.chip_count.text), color = [0,0,0,1], text_size = self.size, bold = True, halign = 'center', valign = 'middle', font_size = self.height/40, background_normal = "", background_color = [0,0.4,0,1])
        
        all_update = partial(self.connect_texts, bet_all.text)
        bet_all.bind(on_release = all_update)
        var_options.add_widget(bet_all)

        #checks to see if the bet boxes already exist before adding.
        if len(self.ids.All_Boxes.children) == 8:
            
            self.ids.All_Boxes.add_widget(self.all_bets)
        

    def connect_texts(self, *text):
        self.ids.All_Boxes.remove_widget(self.all_bets)
        self.ids.new_deal.disabled = False

        if self.ids.bet.text == text[0]:
            return

        self.ids.bet.text = text[0]



    def deal_release(self):
        BlackJack2020.allow_bet = False
        self.ids.bet.disabled = True
        self.ids.new_deal.disabled = True
        self.keep_count_record = int(self.ids.chip_count.text)

        if self.update_bet == True and BlackJack2020.allow_bet == False:
            self.chips_minus_bet()
        if self.dealt_table == False:
            self.deal_table()

    
    def stay_command(self):
        if self.banner == 'Your Turn':
            Clock.schedule_once(self.rem_display)
        if self.hit_again == True:
            self.stay()
        but_disable = [self.ids.bet,self.ids.new_deal,self.ids.stay,self.ids.double_down,self.ids.split,self.ids.hit]
        if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
            for but in but_disable:
                but.disabled = True
            return
        # else:
        self.enable_special()

    def double(self):
        if self.banner == 'Your Turn':
            Clock.schedule_once(self.rem_display)

        if self.hit_again  == True and self.special() == True and len(self.player_hands[self.who_deal].children) == 2: 
            self.double_down(self.who_deal)
        if self.who_deal != self.player_hands.index(self.ids.cp3_cards):
            self.enable_special()
        else:
            self.ids.double_down.disabled = True
            self.ids.split.disabled = True
            self.ids.hit.disabled = True
            self.ids.stay.disabled = True

    def split_command(self):
        if self.banner == 'Your Turn': 
            Clock.schedule_once(self.rem_display)

        if self.allow_split(self.who_deal) == True and self.special() == True and self.hit_again == True: 
            self.ids.double_down.disabled = True
            self.split(self.who_deal)

    def split_jacks(self):
        if self.bl_split == True and self.bl_split2 == True:
            self.stay()
            self.stay()
            self.ids.double_down.disabled = True
            self.ids.split.disabled = True
            self.ids.hit.disabled = True
            self.ids.stay.disabled = True
            return
        if self.bl_split == True:
            self.stay()
        


    def stay(self):
        Clock.schedule_once(self.rem_display)
        if self.bl_split_last == True:
            self.play_turn = True
            self.who_deal += 2
        else:
            self.play_turn = True
            self.who_deal += 1

        if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
            self.set_split_vals()
            self.hit_again = False
            self.wait_to_deal(self.deal_cpu_3)
    
    def hit_command(self):
        if self.banner == 'Your Turn':
            Clock.schedule_once(self.rem_display)

        self.deal_player(self.player_hands[self.who_deal])
        self.ids.double_down.disabled = True
        self.enable_special()      

########    PopUps, Banner Labels, and Drop Downs    #######

    
    # Popup if bet amount is more than chip count
    def bet_over_chips(self):
        too_much = BetTooHigh_Pop(title = 'Bet Is Too High', size_hint = (0.66, 0.66), title_align = 'center', auto_dismiss = False)  
        too_much.open()

    
    def add_display(self, dt = 0):
        self.notify = Label(size_hint = (1,1), text = self.banner, color = [0,0,0.5,1], font_size = self.height/15, padding = (5,5), halign = 'center')
        
        if self.banner == 'Your Turn' and self.play_turn == True:
            return
        elif self.banner == 'Busted' and self.add_split_box_ind > self.hand_boxes.index(self.ids.cp3_hand_box):
            return

        if len(self.ids.All_Boxes.children) == 8:
            self.ids.All_Boxes.add_widget(self.notify)
        else:
            pass

    def rem_display(self, dt = 0):
        if len(self.ids.All_Boxes.children) > 8:
            self.ids.All_Boxes.remove_widget(self.ids.All_Boxes.children[0])
        else:
            pass


#####     Game Play Functionality     #####

    # resets the Deck and shuffles it    
    def shuffle_deck(self):
        self.deck = [two_diamond, two_heart, two_club, two_spade, three_diamond, three_heart, three_club, three_spade, four_diamond, four_heart, four_club, four_spade, five_diamond, five_heart, five_club, five_spade, six_diamond, six_heart, six_club, six_spade, seven_diamond, seven_heart, seven_club, seven_spade, eight_diamond, eight_heart, eight_club, eight_spade, nine_diamond,nine_heart, nine_club, nine_spade, ten_diamond, ten_heart, ten_club, ten_spade, jack_diamond, jack_heart, jack_club, jack_spade, queen_diamond, queen_heart, queen_club, queen_spade, king_diamond, king_heart, king_club, king_spade, ace_diamond, ace_heart, ace_club, ace_spade]*6
        
        return shuffle(self.deck)

        # Leaving this comented out testing deck.  Put any cards in the test deck necessary to test what happens.  This is very useful for splits.
        # self.test_deck = [eight_diamond, eight_heart, eight_club, eight_spade, king_club, king_spade, ace_diamond, ace_heart]*100
        # return shuffle(self.test_deck)


    # Function to uppdate chip count after bet placement
    def chips_minus_bet(self):
        
        self.new_chip_count = float(self.ids.chip_count.text)
        self.minus_bet = float(self.ids.bet.text[5:])

        if self.new_chip_count >= self.minus_bet:
            self.new_chip_count -= self.minus_bet
            self.ids.chip_count.text = str(ceil(self.new_chip_count))
            BlackJack2020.allow_bet = False
            self.update_bet = False
            
                
        # Popup if bet try is more than chip count
        else:
            self.bet_over_chips()
            BlackJack2020.allow_bet = True

    # Pulls card from Deck or subs blank card for dealer 1st card
    def pull_card(self):
        # self.card = self.test_deck.pop()  #Again leaving in the commented out code for the test deck.
        self.card = self.deck.pop()
        self.dealt_card = self.card.card
        self.dealt_image = Image(source = self.card.card)

        if len(self.player_hands[5].children) == 0 and self.who_deal == 5:
            self.dealt_image = Image(source = blank_card.card)
        ## Below updates dealer hand after players are done
            self.hld_dlr_val = self.card.value
            self.hld_dlr_crd = self.card.card
            self.dealt_value = blank_card.value
        else:
            self.dealt_value = self.card.value

    # Updates Each Hand Values
    def update_value(self, hand):
        updtd_dlr_val = 0

        for i, val in enumerate(self.hand_values):
            if i == hand:
                if self.hand_values[i].text[-1] == 'd':
                    self.hand_values[i].text = '0'

                self.value = int(self.hand_values[i].text) 
                self.value += self.dealt_value
                
                
                self.tbl_crds[i].append(self.dealt_card)
                self.tbl_vals[i].append(self.dealt_value)

                self.ace_value(i)

                ##  Below updates the "Shown" dealer hand value after all players are done
                if self.dealer_turn == True and updtd_dlr_val == 0:
                    self.hld_dlr_val += self.value

                    updtd_dlr_val += 1
                
                self.hand_values[i].text = str(self.value)



    # If a hand has an ACE and hitting again goes over 21, this drops the ace value to 1
    def ace_value(self, position):
        
        ace_qty = 0
        for card in self.tbl_crds[position]:
            if card in ace_list:
                ace_qty += 1

                if self.ace_as_1[position] in self.tbl_crds[position]:
                    pass
                elif len(self.ace_as_1[position]) >= ace_qty:
                    pass
                else:
                    if self.value > 21:
                        self.value -= 10
                        self.ace_as_1[position].append(card)


    # Deals an individual card to the selecded players position
    def deal_card(self, position):

        self.pull_card()
        self.dealt_image.pos = self.ids.dealer_pic.pos

        self.animate = Animation(pos = position.pos, duration = 0.33)
        self.animate.start(self.dealt_image)
        
        position.add_widget(self.dealt_image)

    def stop_anim(self):
        self.animate.stop(self.dealt_image)


    def enable_special(self):
        if self.special() == True:
            if len(self.tbl_vals[self.who_deal]) == 2:
                self.ids.double_down.disabled = False
            else:
                self.ids.double_down.disabled = True

            if self.allow_split(self.who_deal) == True and self.split_count > -1:
                self.ids.split.disabled = False
            else:
                self.ids.split.disabled = True


    # Deals the 1st 2 cards to every player at the table
    def deal_table(self):
        if BlackJack2020.allow_bet == True:
            return
        if len(self.deck) < 104:
            self.shuffle_deck()

        self.player_hands = [self.ids.cp1_cards, self.ids.cp2_cards, self.ids.player_cards, self.ids.cp3_cards, self.ids.cp4_cards, self.ids.dealer_cards]

        self.hand_values = [self.ids.cp1_value, self.ids.cp2_value, self.ids.player_value, self.ids.cp3_value, self.ids.cp4_value, self.ids.dealer_value]

        self.hand_boxes = [self.ids.cp1_hand_box, self.ids.cp2_hand_box, self.ids.player_hand_box, self.ids.cp3_hand_box, self.ids.cp4_hand_box]
        self.dealt_table = True

        for count, player in enumerate(self.player_hands*2):
            if count > 5:
                count-=6
            self.deal_card(player)
            self.stop_anim()
            self.update_value(count)

            if count == 2 and self.hand_values[count].text == '21':
                self.banner = 'BLACK JACK!!!'
                self.add_display()
                Clock.schedule_once(self.rem_display, 1.5)
                self.blck_jck = True
                self.hit_again = False
            self.who_deal += 1
        self.who_deal = 0

        if self.hld_dlr_val + int(self.ids.dealer_value.text) == 21:
            self.flip_dlr_crd()
            Clock.schedule_once(self.winnings, 2)
            Clock.schedule_once(self.play_again, 5)
            self.banner = 'Dealer 21...'
            Clock.schedule_once(self.add_display,0)
            Clock.schedule_once(self.rem_display,4.9)
        else:
            self.wait_to_deal(self.deal_cpu_1)

 
    def wait_to_deal(self, func):
        Clock.schedule_interval(func, 0.7)


    def busted(self):
        
        if self.value > 21:
            self.bust = True
            self.banner = 'Busted'
            if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
                for but in self.ids.play_buttons.children:
                    but.disabled = True
                    self.ids.chip_count.disabled = False
            
        else:
            self.bust = False


    def blackjack(self, hand):
        if len(hand.children) == 2 and self.value == 21:
            self.banner = 'BLACK JACK!!!'
            Clock.schedule_once(self.add_display, 0.2)
            Clock.schedule_once(self.rem_display, 1.7)
            self.blck_jck = True
        else:
            self.blck_jck = False


    def hit(self):
        self.deal_card(self.player_hands[self.who_deal])
        self.update_value(self.who_deal)


    def set_split_vals(self):
        self.split_count = 0
        self.split_deal = 0
        self.splitting_aces = False
        self.add_split_box_ind += 1       


    def deal_player(self, hand):

        self.play_turn = True
        self.ids.hit.disabled = True
        self.blackjack(hand)
        self.blck_jck = False
        
        self.busted()
        if self.bust == True:
            Clock.schedule_once(self.add_display, 0.2)
            Clock.schedule_once(self.rem_display, 1.7)
            if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
                self.ids.double_down.disabled = True
                self.ids.split.disabled = True
                self.ids.hit.disabled = True
                self.ids.stay.disabled = True
            if self.bl_split_last == True:
                self.who_deal += 2

            else:
                self.who_deal += 1

        if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
            self.set_split_vals()
            self.hit_again = False
            self.ids.double_down.disabled = True
            self.ids.split.disabled = True
            self.ids.hit.disabled = True
            self.ids.stay.disabled = True
            self.wait_to_deal(self.deal_cpu_3)

        else:
            self.enable_special()
            self.ids.hit.disabled = False


    def deal_cpu_1(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)

        if self.who_deal == self.player_hands.index(self.ids.cp2_cards):
            self.set_split_vals()
            self.wait_to_deal(self.deal_cpu_2)
            return False

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list[0:4]:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.who_deal += 2
                    return True
                return True

        if hand_value >= 16:
            self.who_deal += 1
            return True
        else:
            self.hit()
            return True


    def deal_cpu_2(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)

        if self.who_deal == self.player_hands.index(self.ids.player_cards):
            if self.blck_jck == True:
                self.who_deal += 1
                return True
            self.hit_again = True
            self.dealt_table = True
            self.set_split_vals()
            self.enable_special()
            self.ids.stay.disabled = False
            self.ids.hit.disabled = False

            if self.play_turn == False:
                self.banner = 'Your Turn'
                Clock.schedule_once(self.add_display, 3)
            return False

        if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
            self.add_split_box_ind += 1
            self.set_split_vals()
            self.dealt_table = True
            self.wait_to_deal(self.deal_cpu_3)
            return False

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list[0:2]:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.who_deal += 2
                    return True
                return True

        if hand_value >= 16:
            self.who_deal += 1
            return True
        else:
            self.hit()
            return True


    def deal_cpu_3(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)

        if self.who_deal == self.player_hands.index(self.ids.cp4_cards):
            self.set_split_vals()
            self.wait_to_deal(self.deal_cpu_4)
            return False

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list[0:3]:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.who_deal += 2
                    return True
                return True

        if hand_value >= 17:
            self.who_deal += 1
            return True
        else:
            self.hit()
            return True


    def deal_cpu_4(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)
        Clock.schedule_once(self.rem_display)

        if self.who_deal == self.player_hands.index(self.ids.dealer_cards):
            self.flip_dlr_crd()
            self.wait_to_deal(self.deal_dealer)
            return False

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.who_deal += 2
                    return True
                return True

        if hand_value >= 16:
            self.who_deal += 1
            return True
        else:
            self.hit()
            return True


    def flip_dlr_crd(self):
        Clock.schedule_once(self.rem_display)
        if self.hld_dlr_val == 11 and int(self.hand_values[-1].text) == 11:
            self.hld_dlr_val -= 10
            self.ace_as_1[-1].append(self.tbl_crds[-1][0])

        hand_value = int(self.hand_values[-1].text) + self.hld_dlr_val
        self.hand_values[-1].text = str(hand_value)

        flip_card_rem = self.player_hands[-1].children[-1]
        flip_card_add = Image(source = self.hld_dlr_crd)

        self.player_hands[-1].remove_widget(flip_card_rem)
        self.player_hands[-1].add_widget(flip_card_add)


    def deal_dealer(self, dt):
        Clock.schedule_once(self.rem_display)
        
        if self.soft_ace == False:
            for card in self.tbl_crds[-1]:
                
                if card in ace_list and len(self.ace_as_1[-1]) == 0:
                    self.soft_ace = True
        if int(self.hand_values[-1].text) == 17 and self.soft_ace == True:
            self.hit()
            return True


        if int(self.hand_values[-1].text) >= 17:
            Clock.schedule_once(self.winnings, 1.5)
            Clock.schedule_once(self.play_again, 4)
            return False
        else:
            self.hit()


####     Split and Double Down Functionality     #####


    # called to see if special play is available, ie. Double Down and Split
    def special(self):
        if self.new_chip_count >= self.minus_bet and self.hit_again == True and self.dealt_table == True:
            return True
        return False


    def double_down(self, hand):
        self.play_turn = True

        start = self.hand_values.index(self.ids.player_value)
        stop = self.hand_values.index(self.ids.cp3_value)

        if self.hand_values[hand] in self.hand_values[start : stop]:
            self.chips_minus_bet()

        self.deal_card(self.player_hands[hand])
        self.update_value(hand)

        self.hold_bet += self.minus_bet
        self.tbl_crds[hand].append('double')

        self.busted()
        if self.bust == True:
            self.hold_bet -= self.minus_bet
            Clock.schedule_once(self.add_display, 0.2)
            Clock.schedule_once(self.rem_display, 1.7)

        self.stay()


    # Allows for splitting hands when a pair is dealt in the 1st round or the 1st new dealt card of a split hand 

    def move_card_on_split(self, position):
        self.split_count -=1
        self.split_hand = BoxLayout(orientation = 'vertical')

        self.split_box = BoxLayout(orientation = 'horizontal', padding = '5.0', size_hint = (1,1))
        self.split_cards = BoxLayout(orientation = 'vertical')

        self.split_box.add_widget(self.split_cards)

        self.split_card = self.player_hands[position].children[-1]
        self.player_hands[position].remove_widget(self.split_card)

        self.split_cards.add_widget(self.split_card, -1)

        self.split_value = Label(text = '', size_hint = (1, 0.15), text_size = self.size, font_size = self.height/35, color = [0,0,0,1], bold = True, halign = 'center', valign = 'middle')        

        self.split_hand.add_widget(self.split_box)
        self.split_hand.add_widget(self.split_value, -1)

        self.hand_boxes[self.add_split_box_ind].add_widget(self.split_hand,-1)


    def add_split_items(self, position):

        self.hand_values.insert(position+1, self.split_value)
        self.player_hands.insert(position+1, self.split_cards)

        self.move_card = self.tbl_crds[position].pop(1)
        self.tbl_crds.insert(position+1, [self.move_card])

        self.move_value = self.tbl_vals[position].pop(1)
        self.tbl_vals.insert(position+1, [self.move_value])

        self.ace_as_1.insert(position, [])

    
    def allow_split(self, position):
        self.split_list = ['ace', 'eig', 'two', 'thr', 'sev']

        if len(self.tbl_vals[position]) == 2 and self.splitting_aces == False:
            if self.tbl_vals[position][0] == self.tbl_vals[position][1] and self.split_count > -1:
                if self.tbl_crds[position][0][0:3] == self.tbl_crds[position][1][0:3]:
                    return True

        return False


     
    def split(self, position):
        Clock.schedule_once(self.rem_display)

        if self.split_count > -1:
            if self.add_split_box_ind == self.hand_boxes.index(self.ids.player_hand_box):
                self.play_turn = True
                self.chips_minus_bet()

            self.move_card_on_split(position)
            self.add_split_items(position)

            self.new_val = int(self.hand_values[position].text)
            self.new_val-= self.move_value

            if self.tbl_crds[self.who_deal][0] in ace_list:
                self.new_val += 10
                self.splitting_aces = True

            self.hand_values[position].text = str(self.new_val)
            self.split_value.text = str(self.move_value)

            if self.splitting_aces == True and self.add_split_box_ind == self.hand_boxes.index(self.ids.player_hand_box):
                self.hit()
                self.blackjack(self.player_hands[self.who_deal])
                self.blck_jck = False
                self.stay()

                self.hit()
                self.blackjack(self.player_hands[self.who_deal])
                self.stay()

                self.enable_special()
                self.ids.stay.disabled = True
                self.ids.hit.disabled = True
                self.ids.split.disabled = True
                self.blck_jck = False
                return

            if self.add_split_box_ind == self.hand_boxes.index(self.ids.player_hand_box):

                self.hit()
                self.blackjack(self.player_hands[self.who_deal])
                if self.blck_jck == True:
                    self.blck_jck = False
                    self.bl_split = True
                    

                self.who_deal += 1
                self.hit()
                self.blackjack(self.player_hands[self.who_deal])

                if self.blck_jck == True:
                    self.blck_jck = False
                    self.bl_split2 = True
                self.who_deal -= 1
                self.split_jacks()
                if self.bl_split == False and self.bl_split2 == True:
                    self.bl_split_last = True
                self.enable_special()      

            else:
                self.hit()
                self.who_deal += 1
                self.hit()
                self.who_deal -= 1

            if self.who_deal == self.player_hands.index(self.ids.player_cards):   
                self.enable_special()
        Clock.schedule_once(self.rem_display)


#####     End of Round Functionality     #####

    def chips_win(self, position, *largs):
        self.chip_anim += 1
        self.move_chips = Image(source = chip.card, allow_stretch = True, size_hint_y = None)

        self.move_chips.pos = self.ids.dealer_pic.pos

        self.animate = Animation(pos = position.pos, duration = 0.2)
        self.animate.start(self.move_chips)

        position.add_widget(self.move_chips, 0)

        if self.chip_anim >= 4:
            self.chip_anim = 0
            return False

    # Updates chip count if the hand is won
    
    def winnings(self, dt):
        Clock.schedule_once(self.rem_display)
        self.chip_anim = 0

        start = self.hand_values.index(self.ids.player_value)
        stop = self.hand_values.index(self.ids.cp3_value)
        plyr_indx_start = self.player_hands.index(self.ids.player_cards)
        
        dealer_hand = int(self.ids.dealer_value.text)
        self.hand_winnings = float(self.ids.chip_count.text)
        dealer_21 = False

        if dealer_hand == 21 and len(self.ids.dealer_cards.children) == 2:
            dealer_21 = True

        double = self.hold_bet

        for i, val in enumerate(self.hand_values[start:stop]):
            bet_amt = float(self.ids.bet.text[5::])
            
            
            plyr_hand = int(val.text)
            num_of_cards = len(self.player_hands[i + plyr_indx_start].children)

            push_21 = False
            paid = False

            if 'double' not in self.tbl_crds[i + plyr_indx_start]:
                double = 0
            if (plyr_hand > 21) or ((plyr_hand < dealer_hand) and dealer_hand <= 21):
                if double > 0:
                    double -= bet_amt
                    self.hold_bet -= bet_amt
                bet_amt = 0
                paid = True
            
            elif plyr_hand == 21 and num_of_cards == 2 and paid == False:
                if dealer_21 == True:
                    push_21 = True
                else:
                    add_to_bet = bet_amt
                    bet_amt *= 1.5
                    bet_amt += add_to_bet
                paid = True
            
            elif (plyr_hand == dealer_hand and push_21 == False) and paid == False:
                if dealer_21 == True:
                    if double > 0:
                        double -= bet_amt
                        bet_amt = 0
                else:
                    if double > 0:
                        double -= bet_amt
                        bet_amt += bet_amt
                paid  = True
            
            elif (dealer_hand > 21 or ((plyr_hand > dealer_hand) and plyr_hand <= 21)) and paid == False:
                bet_amt += bet_amt

            self.hand_winnings += (bet_amt + (double*2))

        if self.hand_winnings > self.keep_count_record and dealer_21 == False:
            Clock.schedule_interval(partial(self.chips_win,self.ids.chip_count), 0.2)

        Clock.schedule_once(self.update_winnnings, 1.5)

    
    def update_winnnings(self, dt):
        self.ids.chip_count.text = str(ceil(float(self.hand_winnings)))
        
        while len(self.ids.chip_count.children) > 0:
            self.ids.chip_count.remove_widget(self.ids.chip_count.children[-1])


    # Resets the table except for chip count if another bet is placed
    def play_again(self, dt):
        count = len(self.player_hands)
        position = 0

        while count > 0:
            for item in self.player_hands[position].children[::]:
                self.player_hands[position].remove_widget(item)
            position += 1
            count -= 1

        for player in self.hand_boxes:
            while len(player.children) > 1:
                player.remove_widget(player.children[0])

        names = ['Dolly Hand','Mama Hand','Your Hand','K-K Hand','Bubba Hand','Dealer Hand']
        
        self.hand_values = [self.ids.cp1_value, self.ids.cp2_value, self.ids.player_value, self.ids.cp3_value, self.ids.cp4_value, self.ids.dealer_value]
        
        for i, vals in enumerate(self.hand_values):
            vals.text = names[i]
        
        if float(self.ids.chip_count.text) == 0.0:
            self.manager.current = 'end'
            self.ids.chip_count.text = '10000'

        but_disable = [self.ids.bet,self.ids.new_deal,self.ids.stay,self.ids.double_down,self.ids.split,self.ids.hit]
        for but in but_disable:
            but.disabled = True
            if but_disable[1] != 'Bet':
                but_disable[1].disabled = False

        if int(self.ids.bet.text[5:]) > int(self.ids.chip_count.text):
            self.ids.bet.text = 'Bet'
            self.ids.new_deal.disabled = True

        self.set_split_vals()
        self.add_split_box_ind = 0

        BlackJack2020.allow_bet = True
        self.update_bet = True
        self.dealt_table = False
        self.hit_again = False
        self.allow_special = True
        self.bust = False
        self.blck_jck = False
        self.dealer_turn = False
        self.play_turn = False
        self.soft_ace = False
        self.splitting_aces = False
        self.ids.bet.disabled = False
        self.bl_split = False
        self.bl_split2 = False
        self.bl_split_last = False

        
        #initiated lists
        self.player_hands = []
        self.hand_values = []
        self.hand_boxes = []
        self.tbl_crds = [[],[],[],[],[],[]]
        self.tbl_vals = [[],[],[],[],[],[]]
        self.ace_as_1 = [[],[],[],[],[],[]]
        
        #loop zero values
        self.value = 0
        self.hold_bet = 0
        self.split_count = 0
        self.split_deal = 0
        self.who_deal = 0
        self.add_split_box_ind = 0

        self.banner = ''




# Essentially the end of game screen, also where the user will go if they press the exit button on the mainscreen
class EndScreen(Screen):

    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(**kwargs)

    # Opens Popup to exit the game
    def exit_popup(self):
        last_exit = ExitPopup(title = 'Is it time to Color Up?', size_hint = (0.66, 0.66), title_align = 'center', auto_dismiss = False)
        last_exit.open()


#Main Catalog Class of the Game.  Instances of each necessary class are kept here for reference in the kivy file
class BlackJack2020(App):
    blackjack = ObjectProperty(None)
    homescreen = HomeScreen()
    new_deck = DeckOfCards()
    game_screen = GameScreen()
    exit_popup = ExitPopup()
    end_screen = EndScreen()
    allow_bet = True

    def __init__(self, *args, **kwargs):
        super(BlackJack2020, self).__init__(*args, **kwargs)
        self.blackjack = ObjectProperty(None)
        self.homescreen = HomeScreen()
        self.new_deck = DeckOfCards()
        self.game_screen = GameScreen()
        self.exit_popup = ExitPopup()
        self.end_screen = EndScreen()
        self.sm = ScreenManagement()
        
 
    #creates and returns the class logic of each class and screen
    def build(self, **kwargs):

        Builder.load_file("main.kv")
        self.sm = ScreenManagement()
        self.sm.add_widget(HomeScreen(name = 'home'))
        self.sm.add_widget(GameScreen(name = 'game'))
        self.sm.add_widget(EndScreen(name = 'end'))
        self.sm.current = 'home'
        return self.sm


if __name__ == '__main__':
    BlackJack2020().run()









