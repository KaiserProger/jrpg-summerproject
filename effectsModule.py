class Effect():    #Базовый класс эффектов, имеет кол-во ходов и тип эффекта
    def __init__(self, turns, target, strength):
        self.turns = turns
        self.type = 0
        target.effects.append(self) #Добавляет эффект цели
    def use(self, target, i): #Уменьшает кол-во оставшихся ходов эффекта или удаляет его(ссылку)
        if self.turns > 1:
            print('Turns =' + str(self.turns) + ', name = ' + str(self.type))
            self.turns -= 1
            return True
        else:
            del target.effects[i]
            return False

class  Weakening(Effect):
    def __init__(self, turns, target, strength, type, char):
        Effect.__init__(self, turns, target, strength)
        self.strength = strength
        self.check(target, type)
        self.type = type
        self.char = char
        if self.char >= self.strength:
            self.char -= self.strength
        else:
            self.buffer = self.char
            self.char = 0
    def use(self,target, i):
        if not Effect.use(self, target, i):
            self.char += self.strength
    def check(self, target, type):
                for effect in target.effects:
                    if effect.type == type and effect.turns > 0:
                        effect.turns += self.turns
                        if effect.strength < self.strength:
                            effect.strength = self.strength
                        self.turns = 0

class Armor_weaking(Weakening):
    def __init__(self, turns, target, strength):
        Weakening.__init__(self, turns, target, strength, 6, target.armor)

class Str_weaking(Weakening):
    def __init__(self, turns, target, strength):
        Weakening.__init__(self, turns, target, strength, 7, target.str)

class Int_weaking(Weakening):
    def __init__(self, turns, target, strength):
        Weakening.__init__(self, turns, target, strength, 8, target.int)

class Dex_weaking(Weakening):
    def __init__(self, turns, target, strength):
        Weakening.__init__(self, turns, target, strength, 9, target.dex)


class Stun(Effect):
    def __init__(self, turns, target):
        Effect.__init__(self, turns, target, 0)
    def use(self, target, i):
        if Effect.use(self, target, i):
            target.stop = True #Изменяет переменную стана

class Fire(Effect):
    def __init__(self, turns, target, strength):
        Effect.__init__(self, turns, target, strength)
        self.strength = strength #Сила это кол-во урона в ход
        self.check(target)
        self.type = 1
    def use(self,target, i):
        if Effect.use(self, target, i):
            target.hp -= self.strength
    def check(self,target): #Проверяет есть ли такой же эффект у цели(объединяет) или противоположный(вычитает)
        for effect in target.effects:
            if effect.type == 2 and self.turns > 0:
                buffer = effect.turns
                effect.turns -= self.turns
                self.turns -= buffer
            elif effect.type == 1 and effect.turns > 0:
                effect.turns += self.turns
                if effect.strength < self.strength:
                    effect.strength = self.strength
                self.turns = 0

class Ice(Effect):
    def __init__(self, turns, target):
        Effect.__init__(self, turns, target, 0)
        self.check(target)
        self.type = 2
    def use(self,target, i):
        if Effect.use(self, target, i):
            target.stop = True
    def check(self,target):
        for effect in target.effects:
            if effect.type == 1 and self.turns > 0:
                buffer = effect.turns
                effect.turns -= self.turns
                self.turns -= buffer
            elif effect.type == 2 and effect.turns > 0:
                effect.turns += self.turns
                self.turns = 0

class Poison(Effect):
    def __init__(self, turns, target, strength):
        Effect.__init__(self, turns, target, strength)
        self.strength = strength
        self.check(target)
        self.type = 3
    def use(self, target, i):
        if Effect.use(self, target, i):
            target.hp -= (self.turns+1)*self.strength #Чем больше ходов яда, тем он сильнее
    def check(self, target):
        for effect in target.effects:
            if effect.type == 4 and self.turns > 0:
                buffer = effect.turns
                effect.turns -= self.turns
                self.turns -= buffer
            elif effect.type == 3 and effect.turns > 0:
                effect.turns += self.turns
                if effect.strength < self.strength:
                    effect.strength = self.strength
                self.turns = 0

class Heal(Effect):
    def __init__(self, turns, target, strength):
        Effect.__init__(self, turns, target, strength)
        self.strength = strength #Сила влияет на кол-во хила в ход
        self.check(target)
        self.type = 4
    def use(self, target, i):
        if Effect.use(self, target, i):
            target.hp += (self.turns+1)*self.strength
            if target.hp > target.maxhp:
                target.hp = target.max.hp
    def check(self, target):
        for effect in target.effects:
            if effect.type == 3 and self.turns > 0:
                buffer = effect.turns
                effect.turns -= self.turns
                self.turns -= buffer
            elif effect.type == 4 and effect.turns > 0:
                effect.turns += self.turns
                if effect.strength < self.strength:
                    effect.strength = self.strength
                self.turns = 0