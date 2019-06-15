import pygame
import sys
import os
import random
import time

EXE = True

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([450, 420])
        pygame.display.set_caption("Guitar Hero Clone")
        self.sprites = []
        self.t = 0
        self.cards = []
        self.hand = []
        self.key = 0
        self.instructions = 0
        self.speed = 1
        self.t2 = 0
        self.bases = []
        self.score = 0
        self.health = 10
        self.font = pygame.font.Font("bankgothic/bankgothic-regulardb.ttf", 40)
        self.font2 = pygame.font.Font("bankgothic/bankgothic-regulardb.ttf", 20)
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        self.pause = False
        while not self.pause:
            for event in pygame.event.get():
                if event.type is pygame.KEYDOWN:
                    self.keyPressed(event.key)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            dt = clock.tick(60)
            self.t += dt/1000
            self.t2 += dt/1000
            self.update(dt)
            pygame.display.flip()
            # pygame.display.update()

    def update(self, dt):
        self.speed = 1+(self.score//5)*0.2
        pygame.draw.rect(self.screen, (0,0,0), (0,0,600,420))
        if self.health <=0:
            self.health = 0
            label = self.font.render("GAME OVER", True, (255,255,255))
            self.screen.blit(label, (100, 170))
        for i in range(4):
            pygame.draw.rect(self.screen, (255,255,255), (i*100+50,350,50,50))
        for base in self.bases:
            if self.health > 0:
                base[1] += self.speed
            self.drawBase(base[0]*100+50, int(base[1]), base[0])
            if base[1] > 350+10:
                self.health -= 1
                self.bases.remove(base)
        if self.t > 1/self.speed:
            self.bases += [[random.randint(0,3), -50]]
            self.t = 0
        score = self.font2.render("score: "+str(self.score), True, (255,255,255))
        health = self.font2.render("health: "+str(self.health), True, (255,255,255))

        self.screen.blit(score, (10,10))
        self.screen.blit(health, (10,30))

    def drawBase(self, x, y, type):
        color = (0,0,0)
        fontcolor = (0,0,0)
        text = ''
        if type==0:
            color = (255,0,0)
            fontcolor = (0,255,0)
            text = 'A'
        elif type==1:
            color = (255,255,0)
            fontcolor = (0,0,255)
            text = 'C'
        elif type==2:
            color = (0,255,0)
            fontcolor = (255,0,0)
            text = 'T'
        elif type==3:
            color = (0,0,255)
            fontcolor = (255,255,0)
            text = 'G'
        pygame.draw.rect(self.screen, color, (x,min(y,350),50,50))
        label = self.font.render(text, True, fontcolor)
        self.screen.blit(label, (x+9,min(y,350)))


    def keyPressed(self, key):
        if self.health <= 0:
            self.bases = []
            self.score = 0
            self.t = 0
            self.health = 10
        base = -1
        if key == pygame.K_a:
            base = 0
        elif key == pygame.K_c:
            base = 1
        elif key == pygame.K_t:
            base = 2
        elif key == pygame.K_g:
            base = 3
        else:
            return
        for b in self.bases:
            if (base+2)%4 == b[0] and abs(b[1]- 350) < 10:
                self.score += 1
                self.bases.remove(b)
                return
        self.health -= 1

    def loadCards(self):
        score = self.score(self.opponentHand)
        while 1:
            deck = self.deck[:]
            for card in self.opponentHand:
                if card in deck:
                    deck.remove((card.suit, card.number))
            random.shuffle(deck)
            for j in range(3):
                for i in range(4):
                    card = deck[0]
                    self.addCard(i, card[0], card[1], delay=j)
                    deck.remove(card)
            n = 0
            for i in self.cards[:4]:
                for j in self.cards[4:8]:
                    for k in self.cards[8:12]:
                        if (self.score([i,j,k]) > score) != (score==100014):
                            n += 1
                            print([i,j,k])
            if n >= 1:
                return
            self.cards = []

    def addCard(self, column, suit, number, delay=0):
        Card(self, column, suit, number)
        self.cards.append(Card(self, column, suit, number, delay))

    def fight(self, opponent):
        self.fighting = True

    def loadImage(self, name, number=1):
        ''' Loads an image or list of images '''
        if not hasattr(self, "images"):
            self.images = {}
        elif name in self.images:
            return self.images[name]
        if EXE:
            path = os.path.join(os.path.dirname(sys.executable), 'images')
        else:
            path = os.path.join(os.path.dirname(__file__), 'images')
        if number==1:
            img = pygame.image.load(os.path.join(path, name))
        else:
            img = []
            for i in range(number):
                key = name[:-4]+str(i)+name[-4:]
                img.append(pygame.image.load(os.path.join(path, key)))
        self.images[name] = img
        return img

    def playSound(self, name):
        ''' Plays the given sound effect ''' 
        if EXE:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        sound = pygame.mixer.Sound(os.path.join(path, name))
        sound.play()

    def playMusic(self, name, n=-1, fade = 0):
        ''' Plays the given background track '''
        if EXE:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        if fade:
            pygame.mixer.music.fadeout(fade)
        else:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(path, name))
        pygame.mixer.music.play(n)
        
    def getOpponentHand(self, difficulty):
        if difficulty == 'A':
            return (Card(self, 0, 2, 11),Card(self, 0, 2, 5),Card(self, 0, 2, 2))
        elif difficulty == 'B':
            return (Card(self, 0, 1, 5),Card(self, 0, 3, 5),Card(self, 0, 0, 5))
        elif difficulty == 'C':
            return (Card(self, 0, 1, 11),Card(self, 0, 2, 12),Card(self, 0, 3, 13))
        elif difficulty == 'D':
            return (Card(self, 0, 1, 2),Card(self, 0, 1, 3),Card(self, 0, 1, 4))
        elif difficulty == 'E':
            return (Card(self, 0, 3, 12),Card(self, 0, 2, 12),Card(self, 0, 0, 12))
        elif difficulty == '!':
            return (Card(self, 0, 1, 12),Card(self, 0, 1, 13),Card(self, 0, 1, 1))

    def score(self, hand):
        score = 1
        vals = [hand[0].number,hand[1].number,hand[2].number]
        for i, v in enumerate(vals):
            if v == 1:
                vals[i] = 14
        vals.sort()
        if vals[0] == vals[1] and vals[1] == vals[2]:
            score = 10000*score + vals[0]
        if hand[0].suit == hand[1].suit and hand[1].suit == hand[2].suit:
            score *= 100
        if vals[2]-vals[1] == vals[1]-vals[0] and abs(vals[1]-vals[0]) == 1:
            score = score * 1000 + max(vals)
            return score
        for i, v in enumerate(vals):
            if v == 14:
                vals[i] = 1
        vals.sort()
        if vals[2]-vals[1] == vals[1]-vals[0] and abs(vals[1]-vals[0]) == 1:
            score = score * 1000 + max(vals)
        return score

        


if __name__ == "__main__":
    g = Game()