import thumby
import random
import time

DECK_COUNT = 2
FPS = 10
thumby.display.setFPS(FPS)

# Utility function to wait for a specified amount of seconds
def wait(seconds):
    global FPS
    frames = round(seconds * FPS)
    for i in range(frames): thumby.display.update()
    

# Contains the deck
class Deck:
    # Create a new deck and shuffle it on init
    def __init__(self):
        global DECK_COUNT
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4 * DECK_COUNT
        # Use CPU ticks as random seed as time is counted from poweron
        random.seed(time.ticks_cpu())
        # Switch each card with a random other card
        l = len(self.deck)
        for i in range(l):
            j = random.randrange(l)
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
            
    # Pops the first card from the deck
    def popCard(self):
        # Pop card from deck
        card = self.deck.pop()
        # Return the corresponding cards for non-number values
        if card == 10: return "X"
        elif card == 11: return "J"
        elif card == 12: return "Q"
        elif card == 13: return "K"
        elif card == 14: return "A"
        else: return card
            

# General class for participants
class Usr:
    # BITMAP: width: 9, height: 11
    bmp_card = bytearray([254,3,1,1,1,1,1,3,254, 3,6,4,4,4,4,4,6,3])
    bmp_card_hidden = bytearray([254,171,85,171,85,171,85,171,254, 3,6,5,6,5,6,5,6,3])
    
    # Setup
    def __init__(self):
        self.cards = []
        self.points = 0
    
    # Appends a card from the deck to the cards list
    def appendCard(self, card):
        self.cards.append(card)
        self.calculatePoints()
        
    # Pop n cards from the deck and append them to the list
    def appendCards(self, deck, n):
        for i in range(n):
            self.cards.append(deck.popCard())
        self.calculatePoints()
        
    # Calculates the point sum
    def calculatePoints(self):
        points = 0
        aces = 0
        for card in self.cards:
            if card == "X" or card == "J" or card == "Q" or card == "K":
                points += 10
            elif card == "A":
                points += 11
                aces += 1
            else:
                points += card
        for a in range(aces):
            if (points > 21): points -= 10
        self.points = points
    
    # Draws current cards to half of the screen
    # Maximum fully visible matrix size is 4x5
    def drawCards(self, x, y, max_cards = 7, hidden = False):
        columns = 3
        
        for index, card in enumerate(self.cards[::-1][:max_cards]):
            hiddenNotFirst = False if index == 0 else hidden
            # Draw card value if not hidden
            if not hiddenNotFirst: thumby.display.drawText(
                str(card), 
                x + int(index % columns * 10) + 2, 
                y + int((index - index % columns) / columns * 12) + 2, 
                1
            )
            # Draw card bitmap
            thumby.display.drawSprite(
                thumby.Sprite(9, 11,
                    self.bmp_card if not hiddenNotFirst else self.bmp_card_hidden,
                    x + int(index % columns * 10), 
                    y + int((index - index % columns) / columns * 12),
                    0
            ))
        
        # Draw +x cards indicator
        if len(self.cards) > max_cards:
            thumby.display.drawText(
                f"+ {len(self.cards) - max_cards}", 
                x + int(max_cards % columns * 10) + 2, 
                y + int((max_cards - max_cards % columns) / columns * 12) + 2, 
                1
            )


# Player
class PlayerUsr(Usr):
    # 32x32 for 10 frames
    anim_cardpick = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,170,85,171,85,171,85,171,85,170,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,42,85,106,85,106,85,106,85,42,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,86,170,86,170,86,170,86,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,53,42,53,42,53,42,53,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,170,85,171,85,171,85,171,85,170,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,42,85,106,85,106,85,106,85,42,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,254,147,109,73,182,37,219,166,108,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,100,219,146,237,73,118,52,27,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,205,50,205,54,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,127,204,179,76,51,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,171,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,106,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,96,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,248,6,161,224,1,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,48,67,128,192,127,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,248,4,2,129,33,32,224,0,1,254,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,16,32,67,66,128,129,128,64,63,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,2,1,1,1,1,1,1,1,2,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,32,64,64,64,64,64,64,64,32,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    # Pick 2 cards on init
    def __init__(self, deck):
        Usr.__init__(self)
        self.appendCards(deck, 2)
    
    # Picks a card while showing a sprite animation
    def pickCard(self, deck):
        # Pick a card and append it to the list
        card = deck.popCard()
        self.appendCard(card)
        
        # Draw animation for 10 frames
        sprite = thumby.Sprite(32, 32, self.anim_cardpick, 20, 4)
        for i in range(10):
            thumby.display.fill(0) 
            thumby.display.drawSprite(sprite)
            sprite.setFrame(sprite.currentFrame+1)
            # Draw the card value on the last frame
            if (i == 9): thumby.display.drawText(str(card), 34, 16, 1)
            thumby.display.update()
    
        wait(1.5)
        thumby.display.fill(0)
        thumby.display.update()
        
        # Reset A and B buttons to prevent invoking them twice
        thumby.buttonA.justPressed()
        thumby.buttonB.justPressed()


# Dealer
class DealerUsr(Usr):
    # Pick 2 cards on init
    def __init__(self, deck):
        Usr.__init__(self)
        self.appendCards(deck, 2)
    
    # Pick a card only if current points < 17
    def pickCard(self, deck):
        if self.points < 17:
            self.appendCard(deck.popCard())
    
    # Pick remaining cards until points are >= 17
    def pickRemainingCards(self, deck, game):
        while self.points < 17:
            self.appendCard(deck.popCard())
            game.draw()
            wait(0.5)


# Game class
class Game:
    # Init with new deck and players
    def __init__(self):
        self.deck = Deck()
        self.player = PlayerUsr(self.deck)
        self.dealer = DealerUsr(self.deck)
        self.dealerHidden = True
        
    # Draw player and dealer cards
    def draw(self):
        thumby.display.fill(0)
        thumby.display.drawLine(35, 1, 35, 38, 1)
        self.player.drawCards(1, 1)
        self.dealer.drawCards(42, 1, hidden = self.dealerHidden)
        thumby.display.update()
    
    # Handle inputs during the game
    def handleInputs(self):
        if thumby.buttonA.justPressed():
            self.player.pickCard(self.deck)
            self.dealer.pickCard(self.deck)
            # End the game if player is bust
            if self.player.points > 21: self.endGame()
        elif thumby.buttonB.justPressed():
            self.endGame()
            
    # Let the dealer pick more cards and evaluate the game
    def endGame(self):
        self.dealer.pickRemainingCards(self.deck, self)
        self.dealerHidden = False
        self.draw()
        wait(1.5)
        self.drawEvaluation()
    
    # Show the game evaluation screen
    def drawEvaluation(self):
        global FPS
        
        # Evaluate who won
        text = ""
        player = self.player.points
        dealer = self.dealer.points
        if player == 21 and dealer != 21:
            text = "Got 21!"
        elif player <= 21 and dealer > 21:
            text = "Won!"
        elif player <= 21 and player > dealer:
            text = "You won!"
        elif player > 21 and dealer > 21 or player == dealer:
            text = "Draw!"
        elif player > 21:
            text = "Bust!"
        elif player < dealer:
            text = "Lost!"
        
        thumby.display.setFPS(30)
        self.drawEvaluationAnimation(text, player, dealer, -40, 5)
        thumby.display.setFPS(FPS)
        
        # Wait until A button is pressed and lifted
        while not thumby.buttonA.pressed(): True
        while thumby.buttonA.pressed(): True
        
        # Reset game for another round
        resetGame()
  
    def drawEvaluationAnimation(self, text, playerPoints, dealerPoints, yOffset, step):
        # Draw win or loose and points
        thumby.display.drawFilledRectangle(0, yOffset, 71, 39, 0)
        thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
        thumby.display.drawText(text, 1, yOffset + 1, 1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText(f"You:  {playerPoints}", 1, yOffset + 11, 1)
        thumby.display.drawText(f"Them: {dealerPoints}", 1, yOffset + 20, 1)
        thumby.display.update()
        
        if yOffset != 0: self.drawEvaluationAnimation(text, playerPoints, dealerPoints, yOffset + step, step)
        
    
# Game setup
game = object
def resetGame():
    global game
    game = Game()
resetGame()


# Game loop
while True:
    game.handleInputs()
    game.draw()


    