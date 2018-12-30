import re
from dataclasses import dataclass

IMM = 'Immune System'
INF = 'Infection'


@dataclass
class Group:

    id: int
    army: str
    units: int
    hp: int
    ap: int
    weak_to: list
    immune_to: list
    ap_type: str
    initiative: int

    def __hash__(self):
        return hash(id(self))

    @property
    def ep(self):
        return self.units * self.ap

    @property
    def target_rank(self):
        return (self.ep, self.initiative)

    @property
    def alive(self):
        return self.units > 0

    def attacked_by(self, other):
        """
        `other` group attacks this group.
        """
        dam = other.would_damage(self)
        killed = dam // self.hp
        self.units -= killed
        return killed

    def would_damage(self, other):
        """
        How much damage this group would do to the other.
        """
        if self.ap_type in other.weak_to:
            return self.ep * 2
        elif self.ap_type in other.immune_to:
            return 0
        return self.ep


def get_imms(groups):
    return [g for g in groups if g.army == IMM]


def get_infs(groups):
    return [g for g in groups if g.army == INF]


def ended(groups):
    return not (get_imms(groups) and get_infs(groups))


def get_enemies(groups, army):
    return get_imms(groups) if army == INF else get_infs(groups)


def round(groups):
    # target selection
    t_ranked = sorted(groups, key=lambda g: g.target_rank, reverse=True)
    attacking = {}
    while t_ranked:
        top = t_ranked.pop(0)
        attackable = [g for g in get_enemies(groups, top.army)
                      if g not in attacking.values() and
                      top.would_damage(g) > 0]
        a_ranked = list(sorted(
            attackable,
            key=lambda e: (top.would_damage(e), e.ep, e.initiative),
            reverse=True))
        if a_ranked:
            defender = a_ranked[0]
            # if top.would_damage(defender) >= defender.hp:
            attacking[top] = defender

    # attacking
    atk_order = sorted(attacking.keys(),
                       key=lambda a: a.initiative,
                       reverse=True)
    for attacker in atk_order:
        defender = attacking[attacker]
        killed = defender.attacked_by(attacker)
        # print("{} attacks {}, {} units killed".format(
            # attacker.id, defender.id, killed))

    # bring out your dead
    groups = [g for g in groups if g.alive]
    # print(list(sorted([g.units for g in groups])))

    # print("end round")
    return groups


def get_groups(lines):
    groups = []
    army = IMM
    g_id = 1
    while lines:
        line = lines.pop(0)
        if IMM in line:
            continue
        if INF in line:
            g_id = 1
            army = INF
            continue
        if line == '\n':
            continue
        units_match = re.findall('(\d+) units', line)
        units = int(units_match[0])
        hp_match = re.findall('(\d+) hit points', line)
        hp = int(hp_match[0])
        weak_to_match = re.findall('weak to ([\w\s,]+)', line)
        weak_to = []
        if weak_to_match:
            weak_to = [w.strip() for w in weak_to_match[0].split(',')]
        immune_to_match = re.findall('immune to ([\w\s,]+)', line)
        immune_to = []
        if immune_to_match:
            immune_to = [w.strip() for w in immune_to_match[0].split(',')]
        ap_match = re.findall('does (\d+)', line)
        ap = int(ap_match[0])
        ap_type_match = re.findall('(\w+) damage', line)
        ap_type = ap_type_match[0]
        initiative_match = re.findall('initiative (\d+)', line)
        initiative = int(initiative_match[0])
        group = Group("{} {}".format(army, g_id),
                      army,
                      units,
                      hp,
                      ap,
                      weak_to,
                      immune_to,
                      ap_type,
                      initiative,
                      )
        groups.append(group)
        g_id += 1

    return groups


def p1(lines):
    groups = get_groups(lines)
    # for group in groups:
        # print(group)
    # exit()
    while not ended(groups):
        groups = round(groups)
    units = sum([g.units for g in groups])
    print(units)


with open('in.txt', 'r') as f:
    lines = f.readlines()
    p1(lines)
