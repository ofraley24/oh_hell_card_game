# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import random
import math
from itertools import groupby
import os
from enum import Enum, auto


class Suit(Enum): 
    Hearts = auto()
    Diamonds = auto()
    Spades = auto()
    Clubs = auto()
    
    
class Player():
    def __init__(self, name):
        self.name = name
        self.tricks_won = 0
        self.points = 0

        
    def create_hand(self, cards_index):
        card_list = []
        for card in cards_index:
            suit_number = (card-1)*4//52
            suit = SUIT_LIST[suit_number]
            number = card-(suit_number*13)
            card_list.append(Card(suit, number))
            
        self.hand = card_list
    
    def print_hand(self):
        sorted_cards = sorted(self.hand, key=lambda card: card.suit)
        grouped_cards = {key: list(group) for key, group in groupby(sorted_cards, key=lambda card: card.suit)}
        for suit, cards in grouped_cards.items():
            print(f"{suit}: {', '.join(str(card.number) for card in cards)}")
        print('\n')

        
    
    def input_bet(self, bet_amount):
        self.bet = bet_amount
        
    def set_card_played(self, card):
        self.card_played = card
        
    def add_trick_win(self):
        self.tricks_won += 1
        
    def reset_tricks_won(self):
        self.tricks_won = 0
        
    def add_points(self, amount):
        self.points += amount
        
class Card():
    def __init__(self, suit, number):
        self.number = number
        self.suit = suit
        
class OhHellGame():
    
    def __init__(self, number_of_players):
        
        self.number_of_players = number_of_players
        self.round = 1
        self.max_rounds = 52//self.number_of_players
        self.player_list = []
        self.input_player_names()            
        self.dealer = self.player_list[0]
        self.active_player = self.dealer
        self.turn_type = 'betting'
        
    def input_player_names(self):
        
        print("Lets play a game of Oh Hell! \n")
        for i in range(self.number_of_players):
            name = input(f'Player {i+1}, enter your name: ')
            self.player_list.append(Player(name))
        self.clear_terminal()
        
        

    def deal_cards(self):
        
        cards = [x for x in range(1,53)]
        deal_outcome = []
        for _ in range(self.number_of_players):
            players_cards = random.sample(cards, self.round)
            cards = [i for i in cards if i not in players_cards]
            self.active_player.create_hand(players_cards)
            self.change_active_player()

        self.trump = SUIT_LIST[math.floor(random.sample(cards, 1)[0]//52)]


        return deal_outcome
    
    def change_active_player(self):
        
        active_player_index = self.player_list.index(self.active_player)
        if active_player_index == self.number_of_players-1:
            self.active_player = self.player_list[0]
        else:
            self.active_player = self.player_list[active_player_index+1]
            
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def bet_placing_round(self):
        
        for _ in range(len(self.player_list)):
            print(f'{self.active_player.name}, your turn to bet \n')
            print(f'Trumps are {self.trump}\n')
            self.active_player.print_hand()
            valid_bet = False
            while not valid_bet:
                try:
                    bet = int(input('Enter your bet: '))
                    if (0 <= bet <= self.round):
                        valid_bet = True
                        self.clear_terminal()
                        break
                    else:
                        print(f'Your bet must be between between 0 and {self.round}')
                        
                except:
                    print('Bet must be an integer')

            self.active_player.input_bet(bet)
            self.change_active_player()
        self.turn_type = 'playing'
        
    def is_card_in_hand(self, input_card):
        card_in_hand = False
        for card in self.active_player.hand:
            if card.suit == input_card.suit and card.number == input_card.number:
                card_in_hand == True
                break
            else: continue
        return card_in_hand
        
    def have_you_followed_suit(self, input_card):
        has_led_suit = False
        followed_suit = False
        for card in self.active_player.hand:
            if card.suit == self.suit_led:
                has_led_suit == True
                break
            else:
                continue
        if (has_led_suit):
            if input_card.suit == self.suit_led:
                followed_suit == True
        return followed_suit
    
    def card_playing_round(self):
        
        for i in range(self.number_of_players):
            print(f'{self.active_player.name}, these are your cards: ')
            self.active_player.print_hand()
            valid_input = False
            while not valid_input:
                try: 
                    input_str = input('Enter suit then number, e.g. (Diamonds,3): ')
                    suit, number_str = input_str.split(',')
                    number = int(number_str)
                    input_card = Card(suit, number)
                    if (self.is_card_in_hand(input_card)):
                        if i == 0:
                            self.suit_led = suit
                        else:
                            if (self.have_you_followed_suit(input_card)):
                                valid_input = True
                                self.active_player.set_card_played(input_card)
                                self.active_player.card_list.remove(input_card)  
                            else:
                                print('You have not followed suit!')
                    else: print('Card not in hand')
    
                except ValueError:
                    print("Invalid Input")
            self.change_active_player()
        self.determine_trick_winner()
            
    def determine_trick_winner(self):
        current_winner = self.active_player
        winning_card = current_winner.card_played
        for _ in range(self.number_of_players):
            current_card = self.active_player.card_played
            if (current_card.suit == self.trump) and (winning_card.suit != self.trump):
                winning_card = current_card
                current_winner = self.active_player
            elif (current_card.suit == winning_card.suit) and (current_card.number > winning_card.number):
                winning_card = current_card
                current_winner = self.active_player
            else:
                continue
            self.change_active_player()
        
        print(f'{current_winner.name} won the trick')
        current_winner.add_trick_win()
        
    
    def scoring_calculator(self):
        
        for _ in range(self.number_of_players):
            tricks_won = self.active_player.tricks_won
            bet = self.active_player.bet
            difference = abs(tricks_won - bet)
            print(self.active_player.name)
                  
            print(tricks_won)
            print(bet)
            if difference == 0:
                points_added = 10 + (5*bet)
            else:
                points_added = (-5*difference)
                
            self.active_player.add_points(points_added)
            self.change_active_player()
            
        
    def display_scoreboard(self):
        
        self.scoring_calculator()
        sorted_players = sorted(self.player_list, key=lambda player: player.points, reverse=True)

        print("\nScoreboard:")
        print("{:<15} {:<10}".format("Name", "Score"))
        print("-" * 25)
    
        for player in sorted_players:
            print("{:<15} {:<10}".format(player.name, player.points))
        self.round += 1
            


        
    def play_a_round(self):
        
        for _ in range(self.max_rounds):
            self.deal_cards()
            self.bet_placing_round()
            for _ in range(self.round):
                self.card_playing_round()
            self.display_scoreboard()


            
def main():
    game = OhHellGame(2)
    game.play_a_round()
    
main()
            

    
