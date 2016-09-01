# -*- coding: cp1252 -*-
import os
import math
import random
import pdb

class Pokebicho:
    pass

class PokeTipo:
    pass

maxid = 1
poketipos = {}
poketype_relations = {}
        
print("Starting type loading")
with open("types.csv") as rd_input:
        tps = rd_input.readline().split(",")
        index = 0
        poketype_relations["order"] = {}
        # sets the indexation order
        for name in tps:
            poketype_relations["order"][name.strip('\n')] = index
            index += 1
        # for each type, it's attack modifier against another class can be accessed using the "order" key
        for line in rd_input:
            lnl = line.split(",")
            poketype_relations[lnl[0]] = []
            for i in range(1, len(lnl)):
                poketype_relations[lnl[0]].append(float(lnl[i]))
        
print("Starting monster loading")
with open("Pokemon.csv") as rd_input:
        rd_input.readline()
        for line in rd_input:
            lnl = line.split(",")
            pk = Pokebicho()
            pk.id = int(lnl[0])
            pk.name = lnl[1]
            pk.type1 = lnl[2]
            pk.type2 = lnl[3] if lnl[3] != "" else lnl[2]
            pk.total = int(lnl[4])
            pk.hp = int(lnl[5])
            pk.attack = int(lnl[6])
            pk.defense = int(lnl[7])
            pk.sp_attack = int(lnl[8])
            pk.sp_defense = int(lnl[9])
            pk.speed = int(lnl[10])
            if pk.id > maxid:
                maxid = pk.id
            if pk.type1 in poketipos:
                poketipos[pk.type1].append(pk)
            else:
                poketipos[pk.type1] = []
                poketipos[pk.type1].append(pk)
            #if pk.type2 in poketipos:
            #    poketipos[pk.type2].append(pk)
            #elif pk.type2 != "":
            #    poketipos[pk.type2] = []
            #    poketipos[pk.type2].append(pk)

print("Data Loaded")

poketipos_stats = {}

print("Type stats...")
for tipo in poketipos.keys():
    counter = 0
    pkt = PokeTipo()
    pkt.name = tipo
    pkt.names = ""
    pkt.mean_attack = 0
    pkt.mean_sattack = 0
    pkt.mean_defense = 0
    pkt.mean_sdefense = 0
    pkt.mean_hp = 0
    pkt.mean_total = 0
    pkt.mean_speed = 0
    pkt.sd_attack = 0
    pkt.sd_sattack = 0
    pkt.sd_defense = 0
    pkt.sd_sdefense = 0
    pkt.sd_hp = 0
    pkt.sd_speed = 0
    pkt.sd_total = 0
    # means
    for bixo in poketipos[tipo]:
        counter += 1
        pkt.names += bixo.name + " "
        pkt.mean_attack += bixo.attack
        pkt.mean_sattack += bixo.sp_attack
        pkt.mean_defense += bixo.defense
        pkt.mean_sdefense += bixo.sp_defense
        pkt.mean_hp += bixo.hp
        pkt.mean_total += bixo.total
        pkt.mean_speed += bixo.speed
    pkt.mean_attack = pkt.mean_attack/float(counter)
    pkt.mean_sattack = pkt.mean_sattack/float(counter)
    pkt.mean_defense = pkt.mean_defense/float(counter)
    pkt.mean_sdefense = pkt.mean_sdefense/float(counter)
    pkt.mean_hp = pkt.mean_hp/float(counter)
    pkt.mean_total = pkt.mean_total/float(counter)
    pkt.mean_speed = pkt.mean_speed/float(counter)
    # standard deviation
    for bixo in poketipos[tipo]:
        pkt.sd_attack += (bixo.attack - pkt.mean_attack) ** 2
        pkt.sd_sattack += (bixo.sp_attack - pkt.mean_sattack) ** 2
        pkt.sd_defense += (bixo.defense - pkt.mean_defense) ** 2
        pkt.sd_sdefense += (bixo.sp_defense - pkt.mean_sdefense) ** 2
        pkt.sd_hp += (bixo.hp - pkt.mean_hp) ** 2
        pkt.sd_speed += (bixo.speed - pkt.mean_speed) ** 2
        pkt.sd_total += (bixo.total - pkt.mean_total) ** 2
    pkt.sd_attack = math.sqrt(pkt.sd_attack / float(counter - 1))
    pkt.sd_sattack = math.sqrt(pkt.sd_sattack / float(counter - 1))
    pkt.sd_defense = math.sqrt(pkt.sd_defense / float(counter - 1))
    pkt.sd_sdefense = math.sqrt(pkt.sd_sdefense / float(counter - 1))
    pkt.sd_hp = math.sqrt(pkt.sd_hp / float(counter - 1))
    pkt.sd_speed = math.sqrt(pkt.sd_speed / float(counter - 1))
    pkt.sd_total = math.sqrt(pkt.sd_total / float(counter - 1))
    poketipos_stats[tipo] = pkt

print("Type stats done")

def getTypeMod( at1, at2, df1, df2 ):
    #no idea what to do here
    pt1 = poketype_relations[at1.lower()][poketype_relations["order"][df1.lower()]]
    pt2 = poketype_relations[at2.lower()][poketype_relations["order"][df2.lower()]]
    pt3 = poketype_relations[at1.lower()][poketype_relations["order"][df2.lower()]]
    pt4 = poketype_relations[at2.lower()][poketype_relations["order"][df1.lower()]]
    res = random.choice([pt1, pt2, pt3, pt4])
    return res if res != 0 else 0.25
    
def simpleDamage(attack, defense, at1, at2, df1, df2):
        #http://bulbapedia.bulbagarden.net/wiki/Damage#Damage_formula
        #fixed parameters
        attack_level = 50
        attack_base = 50
        #modifier parameters
        stab = 1.0
        if at1 == df1 or at1 == df2 or at2 == df1 or at2 == df2:
            stab = 1.5
        type_mod = getTypeMod( at1, at2, df1, df2 )
        critical_x_other_x_random = 1
        #damage formula
        return ((2 * (attack_level + 10))/250.0 * attack/float(defense) * (attack_base + 2) * stab * type_mod)
        
def simpleBattle (pka, pkb):
    # returns true if pka wins
    #print("pka: " + pka.name + " " + str(pka.attack) +" "+ str(pka.defense) + " " + pka.type1)
    #print("pkb: " + pkb.name + " " + str(pkb.attack) +" "+ str(pkb.defense) + " " + pkb.type1)
    first = pka if pka.speed > pkb.speed else pkb
    last = pka if pka.speed <= pkb.speed else pkb
    hpf = first.hp
    hpl = last.hp
    turn_damage = 0
    while hpf > 0 and hpl > 0:
        turn_damage = simpleDamage(first.attack, last.defense, first.type1, first.type2, last.type1, last.type2)
        hpl = hpl - turn_damage
        if hpl < 0: 
            return True if pka.name == first.name else False
        turn_damage = simpleDamage(last.attack, first.defense, last.type1, last.type2, first.type1, first.type2)
        hpf = hpf - turn_damage
        if hpf < 0:
            return False if pka.name == first.name else True
    #return True if pkb.hp <= 0 else False

def simulate(total_battles):
    random.seed()
    wins = 0
    counter = 1
    shuffled_arrays = {}
    max_type_index = len(poketipos.keys()) - 1
    while counter < total_battles:
        #pdb.set_trace()
        a_type = random.randint(0, max_type_index - 1)
        b_type = random.randint(0, max_type_index - 1)
        if not(a_type in shuffled_arrays):
            shuffled_arrays[a_type] = poketipos[poketipos.keys()[a_type]]
            random.shuffle(shuffled_arrays[a_type])
        if not(b_type in shuffled_arrays):
            shuffled_arrays[b_type] = poketipos[poketipos.keys()[b_type]]
            random.shuffle(shuffled_arrays[b_type])
        try:
            if simpleBattle (shuffled_arrays[a_type].pop(), shuffled_arrays[b_type].pop()):
                wins += 1
            counter += 1
        except:
            print(str(a_type) + " " + str(b_type) + " continue")
            continue
        print(counter)
    print ("Wins: " + str(wins) + " Total Battles: " + str(total_battles))
    return 

