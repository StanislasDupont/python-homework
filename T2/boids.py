"""T2 – Boids : le code de départ (étape 0).

D'après le TP « boids » de Thierry Parmentelat (flotpython), réécrit pour le
cours AP Python et pour arcade 3.

Lancez-le avec :  uv run boids.py
Testez-le avec :  uv run pytest
"""

import math  # noqa: F401 (servira à l'étape 2)
import random  # noqa: F401 (servira à l'étape 4)
from pathlib import Path

import arcade

WIDTH, HEIGHT = 800, 800
BACKGROUND = arcade.color.ALMOND

# Les images, cherchées à côté de ce fichier, d'où qu'on le lance.
HERE = Path(__file__).parent
ARROW = HERE / "media" / "arrow.png"
OBSTACLE = HERE / "media" / "obstacle.png"
SKY = HERE / "media" / "sky.png"  # le décor (étape 9)

SPEED = 100  # pixels par seconde (étape 2)
TURN_SPEED = 180  # degrés par seconde, tant qu'une flèche est enfoncée (étape 5)
NOISE = 3  # écart maximal du cap à chaque mise à jour, en degrés (étape 5)
N_BOIDS = 20  # (étape 4)
GRID = 10  # GRID × GRID obstacles (étape 6)
RADIUS = 30  # rayon de détection des voisins, en pixels (étapes 7 et 8)


# --- les objets du jeu -------------------------------------------------------
# Ces classes et fonctions sont vérifiées par les tests (tests/test_boids.py) :
# gardez leur nom et leurs paramètres.
#
# Chaque `raise NotImplementedError("étape …")` est un trou à remplir. S'il est
# atteint, le programme s'arrête net, avec ce message : il dit à quelle étape
# écrire ce morceau. Quand vous y arrivez, effacez la ligne et écrivez votre code.
# À l'étape 0, la fenêtre n'utilise encore aucune de ces classes : rien ne casse.


class Boid(arcade.Sprite):
    """Un oiseau : une flèche qui avance dans la direction où elle pointe."""

    def __init__(self, x, y, angle, speed=SPEED, others=None,turning=0):
        super().__init__(ARROW, center_x=x, center_y=y, angle=angle)
        self.speed = speed
        self.turning=turning

    def update(self, delta_time=1 / 60, *args, **kwargs):
        """Appelée par arcade (via la SpriteList) à chaque mise à jour."""
        rad = math.radians(self.angle)
        self.center_x += self.speed * delta_time * math.cos(rad)+self.separation( self.neighbours(self.others))[0]
        self.center_y -= self.speed * delta_time * math.sin(rad)-self.separation(self.neighbours(self.others))[1]
        if self.center_x >=WIDTH or self.center_x <0 :
            self.center_x=self.center_x %WIDTH
        if self.center_y >=HEIGHT or self.center_y <0 :
            self.center_y=self.center_y %HEIGHT  
        self.angle += self.turning*TURN_SPEED* delta_time 
        noise=random.uniform(-NOISE,NOISE)
        self.angle +=noise
        if len(self.neighbours(self.others))>0 :
            self.alpha=123
        else : self.alpha=255

    def neighbours(self, others, radius=RADIUS):
        """Les objets de `others` à moins de `radius` pixels, sauf soi-même."""
        proches=[]
        for elem in others :
            if math.dist(self.position,elem.position)<radius :
                proches.append(elem)
        return proches
            
             
    def separation(self, others, radius=RADIUS):
        """Le déplacement (dx, dy) qui écarte le boid de ses voisins."""
        dx=0
        dy=0
        for elem in others :
            d=math.dist(self.position,elem.position)
            dx+=(self.position[0]-elem.position[0])/d*(1-(d/radius))/2
            dy+=(self.position[1]-elem.position[1])/d*(1-(d/radius))/2
        return dx,dy


class Obstacle(arcade.Sprite):
    """Un obstacle immobile."""

    def __init__(self, x, y):
        super().__init__(OBSTACLE, center_x=x, center_y=y)


def random_boids(n, others=None):
    """n boids placés et orientés au hasard, qui évitent tous `others`."""
    boids = arcade.SpriteList()
    for i in range (n) :
        boid = Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT), random.uniform(-180, 180),SPEED, others=others)
        boids.append(boid)
    return boids


def obstacle_grid(n):
    """n × n obstacles régulièrement espacés, au centre de leur carré."""
    positions=arcade.SpriteList()
    d=WIDTH/n
    for i in range (n) :
        for j in range (n) :
            new=Obstacle(d/2+i*d,d/2+j*d)
            positions.append(new)
    return positions
    


# --- la fenêtre ---------------------------------------------------------------


class MyWindow(arcade.Window):
    def __init__(self):
        # d'abord, ce que fait toute fenêtre d'arcade : s'ouvrir, en WIDTH × HEIGHT
        # pixels, avec « Boids » pour titre (super() : on y revient en séance)
        super().__init__(WIDTH, HEIGHT, "Boids")
        self.background_color = BACKGROUND  # la couleur que self.clear() étale
        self.obstacles= obstacle_grid(GRID)
        self.boids = random_boids(20, others=None)
        self.turning=0
        self.others=arcade.SpriteList()
        for elem in self.boids :
            self.others.append(elem)
        for elem in self.obstacles :
            self.others.append(elem)

    def on_update(self, delta_time):
        for i, boid in enumerate(self.boids):
            boid.turning = self.turning
            boid.others =[]
            for elem in self.others[:i] :
                boid.others.append(elem)
            for elem in self.others[i+1:] :
                boid.others.append(elem)
        self.boids.update(delta_time)

    def on_draw(self):
        self.clear()
        self.obstacles.draw()
        self.boids.draw()
     
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT :
            self.turning=-1
        if symbol == arcade.key.RIGHT :
            self.turning=1
       # symbol vaut arcade.key.LEFT, arcade.key.RIGHT, arcade.key.Q…

    def on_key_release(self, symbol, modifiers):
        if symbol ==arcade.key.LEFT or symbol==arcade.key.RIGHT :
            self.turning=0


def main():
    MyWindow()
    arcade.run()


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run boids.py),
# pas quand un autre fichier fait `import boids` (les tests, par ex.).
if __name__ == "__main__":
    main()
