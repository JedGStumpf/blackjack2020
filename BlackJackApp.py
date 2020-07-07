"""
This is the file for the black_jack_app

"""
#import kivy 
import webbrowser
import random
import time
import math

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Rectangle 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown  import DropDown 
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial


# Spinner (class similar to a dropdown) displaying the text from a file of the rules of blackjack 
class RulesPopup(Popup):
    rp = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RulesPopup, self).__init__(**kwargs)

    def redirect_popup(self):
        gotowiki = RedirectPopup(title = 'Leave App to Webpage', size_hint = (0.55, 0.55), title_align = 'center', auto_dismiss = False)
        gotowiki.open()


# Re-directs and opens new page in browser to wiki on blackjack strategy
class RedirectPopup(Popup):
    rdp = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RedirectPopup, self).__init__(**kwargs)
    
    def open_link(self, instance):
        webbrowser.open('https://en.wikipedia.org/wiki/Blackjack#Basic_strategy')


# Initial screen with options to start the game or to read rules and to redirect to wiki page for basic blackjack strategy
class HomeScreen(Screen):
    hs = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(HomeScreen,  self).__init__(**kwargs)

    def rules_popup(self):
        rules = RulesPopup(title = 'Game Rules', size_hint = (0.77, 0.66), title_align = 'center', auto_dismiss = False)
        rules.open()


# Class to initialize the objects containing cards and values of the deck
class DeckOfCards:

    def __init__(self, card = None, value = None):

        self.card = card

        self.value = value

    def __str__(self):
        return f'{self.card}, {self.value}'



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


# Initializing the main list of the deck


ace_list = [ace_diamond.card, ace_heart.card, ace_club.card, ace_spade.card]



# Dropdown menu for player to select a bet amount
class BetDropDown(DropDown):
    bdd = ObjectProperty(None)
    maxbet = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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
    
    # Special propoerties to link objects of the kivy file
    bet_amnt = ObjectProperty(None)
    chp_count = ObjectProperty(None)
    maxbet = ObjectProperty(None)
    notify = ObjectProperty(None)
    dropdown = ListProperty([])
    
    #booleans used in the methods logic
    allow_bet = True
    update_bet = True
    dealt_table = False
    hit_again = False
    #allow_special = True
    bust = False
    blck_jck = False
    dealer_turn = False
    play_turn = False 
    soft_ace = False
    splitting_aces = False
    
    #initiated lists
    deck = []
    player_hands = []
    hand_values = []
    hand_boxes = []
    tbl_crds = [[],[],[],[],[],[]]
    tbl_vals = [[],[],[],[],[],[]]
    ace_as_1 = [[],[],[],[],[],[]]
    
    #count values
    value = 0
    hold_bet = 0
    split_count = 0
    split_deal = 0
    who_deal = 0
    add_split_box_ind = 0

    banner = ''
    
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(*args, **kwargs)

        self.bet_drop = BetDropDown()
        
        self.bet_drop.bind(on_select=lambda instance, x: setattr(self.ids.bet, 'text', 'Bet $'+x))



########    PopUps, Banner Labels, and Drop Downs    #######

    # For BetDropDown, attaches all available chips to bet option    
    def max_bet(self):

        self.new_chip_count = self.ids.chip_count.text

        self.bet_drop.ids.bet_all.text = self.new_chip_count
    
    # For BetDropDown, attaches half of all available chips to bet option
    def half_bet(self):
        self.new_chip_count = math.ceil(int(self.ids.chip_count.text)/2)

        self.bet_drop.ids.bet_half.text = str(self.new_chip_count)

    # Popup if bet amount is more than chip count
    def bet_over_chips(self):
        too_much = BetTooHigh_Pop(title = 'Bet Is Too High', size_hint = (0.66, 0.66), title_align = 'center', auto_dismiss = False)  
        if self.allow_bet == True:
            too_much.open()

    
    def add_display(self, dt = 0):
        self.notify = Label(size_hint = (1,1), text = self.banner, color = [0,0,0.5,1], font_size = self.height/15)
        
        if self.banner == 'Play Your Hand' and self.play_turn == True:
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

        #self.test_deck = [five_club, five_spade, king_diamond, king_heart,king_club, king_spade, ace_diamond, ace_heart, ace_club, ace_spade]*100

        return random.shuffle(self.deck)




    # Function to uppdate chip count after bet placement
    def chips_minus_bet(self):
        self.new_chip_count = float(self.ids.chip_count.text)
        self.minus_bet = float(self.ids.bet.text[5:])

        if self.new_chip_count >= self.minus_bet:
            self.new_chip_count -= self.minus_bet
            self.ids.chip_count.text = str(math.ceil(self.new_chip_count))
            self.allow_bet = False
            self.update_bet = False
                
        # Popup if bet try is more than chip count
        else:
            self.bet_over_chips()
            self.allow_bet = True

    # Pulls card from Deck or subs blank card for dealer 1st card
    def pull_card(self):
        self.card = self.deck.pop(0)
        self.dealt_card = self.card.card
        self.dealt_image = Image(source = self.card.card)

        if len(self.player_hands[5].children) == 0 and self.who_deal == 5:
            self.dealt_image = Image(source = blank_card.card)
        ##  Use below to update dealer hand after players are done
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
        stp = self.animate.stop(self.dealt_image)


    # Deals the 1st 2 cards to every player at the table
    def deal_table(self, hand):
        if self.allow_bet == True:
            return
        if len(self.deck) < 104:
            self.shuffle_deck()
        self.player_hands = [self.ids.cp1_cards, self.ids.cp2_cards, self.ids.player_cards, self.ids.cp3_cards, self.ids.cp4_cards, self.ids.dealer_cards]

        self.hand_values = [self.ids.cp1_value, self.ids.cp2_value, self.ids.player_value, self.ids.cp3_value, self.ids.cp4_value, self.ids.dealer_value]

        self.hand_boxes = [self.ids.cp1_hand_box, self.ids.cp2_hand_box, self.ids.player_hand_box, self.ids.cp3_hand_box, self.ids.cp4_hand_box]

        for count, player in enumerate(self.player_hands*2):

            self.deal_card(player)
            self.stop_anim()
            if count > 5:
                count-=6
            self.update_value(count)

            if count == 2 and self.hand_values[count].text == '21':
                self.banner = 'BLACK JACK!!!'
                self.add_display()
                Clock.schedule_once(self.rem_display, 1.5)
                self.blck_jck = True
                self.hit_again = False
            self.who_deal += 1
     
        #print(f'Dealers Hidden Card {self.hld_dlr_val}, {self.hld_dlr_crd}')
        self.who_deal = 0
        self.wait_to_deal(self.deal_cpu_1)

 
    def wait_to_deal(self, func):
        Clock.schedule_interval(func, 0.7)


    def busted(self):
        if self.value > 21:
            self.bust = True
            self.banner = 'Busted'
        else:
            self.bust = False


    def blackjack(self, hand):
        if len(hand.children) == 2 and self.value == 21:
            self.banner = 'BLACK JACK!!!'
            self.blck_jck = True
        else:
            self.blck_jck = False


    def hit(self):
        if len(self.player_hands[self.who_deal].children) == 1:
            self.split_deal += 1

        self.deal_card(self.player_hands[self.who_deal])
        self.update_value(self.who_deal)


    def set_split_vals(self):
        self.split_count = 0
        self.split_deal = 0
        self.splitting_aces = False
        self.add_split_box_ind += 1       


    def stay(self):
        self.play_turn = True
        self.who_deal += 1

        if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
            self.set_split_vals()
            self.hit_again = False
            self.wait_to_deal(self.deal_cpu_3)



    def deal_player(self, hand):
        self.play_turn = True
        self.hit()

        self.blackjack(hand)
        if self.blck_jck == True:
            self.who_deal += 1
            Clock.schedule_once(self.add_display, 0.2)
            Clock.schedule_once(self.rem_display, 1.7)
        
        self.busted()
        if self.bust == True:
            self.who_deal += 1
            Clock.schedule_once(self.add_display, 0.2)
            Clock.schedule_once(self.rem_display, 1.7)

        if self.who_deal == self.player_hands.index(self.ids.cp3_cards):
            self.set_split_vals()
            self.hit_again = False
            self.wait_to_deal(self.deal_cpu_3)



    def deal_cpu_1(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list[0:4]:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.hit()
                    self.who_deal += 1
                    self.hit()
                    self.who_deal += 1
                    self.set_split_vals()
                    self.wait_to_deal(self.deal_cpu_2)
                    return False
                return True

        if hand_value >= 16 or self.splitting_aces == True:
            if self.splitting_aces == False:
                self.who_deal += 1

            if self.who_deal == self.player_hands.index(self.ids.cp2_cards):
                self.set_split_vals()
                self.wait_to_deal(self.deal_cpu_2)
                return False
        else:
            self.hit()

        


    def deal_cpu_2(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list[0:2]:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.hit()
                    self.who_deal += 1
                    self.hit()
                return True

        if hand_value >= 16 or self.splitting_aces == True:
            self.dealt_table = True
            if self.blck_jck == True:
                self.who_deal += 2
                self.add_split_box_ind += 1
                self.set_split_vals()
                self.wait_to_deal(self.deal_cpu_3)

                return False
            else:
                self.who_deal += 1

        if self.who_deal == self.player_hands.index(self.ids.player_cards):
            self.hit_again = True
            self.dealt_table = True
            self.set_split_vals()

            if self.play_turn == False:
                self.banner = 'Play Your Hand'
                Clock.schedule_once(self.add_display, 3)
            return False
        else:
            self.hit()


    def deal_cpu_3(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list[0:3]:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.hit()
                    self.who_deal += 1
                    self.hit()
                    self.who_deal += 1
                    self.set_split_vals()
                    self.wait_to_deal(self.deal_cpu_4)
                    return False
                return True

        if hand_value >= 17 or self.splitting_aces == True:
            if self.splitting_aces == False:
                self.who_deal += 1

            if self.who_deal == self.player_hands.index(self.ids.cp4_cards):
                self.set_split_vals()
                self.wait_to_deal(self.deal_cpu_4)
                return False
        else:
            self.hit()


    def deal_cpu_4(self, dt):
        hand_value = int(self.hand_values[self.who_deal].text)
        Clock.schedule_once(self.rem_display)

        if self.allow_split(self.who_deal) == True:
            if self.tbl_crds[self.who_deal][0][0:3] in self.split_list:
                self.split(self.who_deal)
                if self.splitting_aces == True:
                    self.hit()
                    self.who_deal += 1
                    self.hit()
                    self.who_deal += 1
                    self.flip_dlr_crd()
                    self.wait_to_deal(self.deal_dealer)
                    return False
                return True

        if hand_value >= 16 or self.splitting_aces == True:
            if self.splitting_aces == False:
                self.who_deal += 1

            if self.who_deal == self.player_hands.index(self.ids.dealer_cards):
                self.flip_dlr_crd()
                self.wait_to_deal(self.deal_dealer)
                return False
        else:
            self.hit()



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
        self.split_hand = BoxLayout(orientation = 'vertical')

        self.split_box = BoxLayout(orientation = 'horizontal', padding = '5.0')
        self.split_cards = BoxLayout(orientation = 'vertical')

        self.split_box.add_widget(self.split_cards)

        self.split_card = self.player_hands[position].children[-1]
        self.player_hands[position].remove_widget(self.split_card)

        self.split_cards.add_widget(self.split_card, -1)

        self.split_value = Label(text = 'test', size_hint = (1, 0.15), text_size = self.size, font_size = self.height/35, color = [0,0,0,1], bold = True, halign = 'center', valign = 'middle')        

        self.split_hand.add_widget(self.split_box)
        self.split_hand.add_widget(self.split_value, -1)

        place = self.split_count + self.split_deal
        self.hand_boxes[self.add_split_box_ind].add_widget(self.split_hand, (-1-place))


    def add_split_items(self, position):

        self.hand_values.insert(position+1, self.split_value)
        self.player_hands.insert(position+1, self.split_cards)

        self.move_card = self.tbl_crds[position].pop(0)
        self.tbl_crds.insert(position+1, [self.move_card])

        self.move_value = self.tbl_vals[position].pop(0)
        self.tbl_vals.insert(position+1, [self.move_value])

        self.ace_as_1.insert(position, [])
        
        self.split_count -=1

    
    def allow_split(self, position):
        self.split_list = ['ace', 'eig', 'two', 'thr', 'sev']

        if len(self.tbl_vals[position]) == 2 and self.splitting_aces == False:
            if self.tbl_vals[position][0] == self.tbl_vals[position][1]:
                if self.tbl_crds[position][0][0:3] == self.tbl_crds[position][1][0:3]:
                    return True
                else:
                    return False
        return False


     
    def split(self, position):

        if self.split_count > -3:
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
                self.deal_player(self.player_hands[self.who_deal])
                if self.blck_jck == False:
                    self.stay()

                self.deal_player(self.player_hands[self.who_deal])
                if self.blck_jck == False:
                    self.stay()

        

#####     End of Round Functionality     #####

    def chips_win(self, position, *largs):
        self.chip_anim += 1
        self.move_chips = Image(source = chip.card, allow_stretch = True, width = 30, size_hint_y = None)

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
            
        before = self.hand_winnings + float(self.ids.bet.text[5:]) + double

        for i, val in enumerate(self.hand_values[start:stop]):
            bet_amt = float(self.ids.bet.text[5:])
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
                paid  = True
            
            elif (dealer_hand > 21 or ((plyr_hand > dealer_hand) and plyr_hand <= 21)) and paid == False:
                bet_amt += bet_amt
            
            #before = self.hand_winnings + float(self.ids.bet.text[5:])
            self.hand_winnings += (bet_amt + (double*2))

        if self.hand_winnings > before:
            Clock.schedule_interval(partial(self.chips_win,self.ids.chip_count), 0.2)

        Clock.schedule_once(self.update_winnnings, 1.5)

    
    def update_winnnings(self, dt):
        self.ids.chip_count.text = str(math.ceil(float(self.hand_winnings)))
        
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

        self.allow_bet = True
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
class BlackJackApp(App):
    blackjack = ObjectProperty(None)
    homescreen = HomeScreen()
    new_deck = DeckOfCards()
    bet_dropdown = BetDropDown()
    game_screen = GameScreen()
    exit_popup = ExitPopup()
    end_screen = EndScreen()


    def __init__(self, *args, **kwargs):
        super(BlackJackApp, self).__init__(*args, **kwargs)

    #creates and returns the class logic of each class and screen
    def build(self, **kwargs):

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name = 'home'))
        self.sm.add_widget(GameScreen(name = 'game'))
        self.sm.add_widget(EndScreen(name = 'end'))
        
        return self.sm

if __name__ == '__main__':
    blck_jck = BlackJackApp
    blck_jck().run()









