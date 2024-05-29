import { IPlayerSkills, IPrimaryStats, ITrait, PlayerSkillNames, getDefaultPlayerSkills, IPerk, PerkNames, TraitNames, Difficulty } from "./models";

/**
 * Calculates base skills from primary stats, traits, perks and tagged skills.
 * @param primaryStats primary stats for calculation.
 * @param traits traits used in the calculation.
 * @param taggedSkills tagged skills.
 * @param playersPerks perks used in the calculation.
 * @returns calculated base skills.
 */

export default function calculateBaseSkills(primaryStats: IPrimaryStats, traits: ITrait[], taggedSkills: string[], playersPerks: IPerk[], difficulty: string): IPlayerSkills {
    let newBaseSkills: IPlayerSkills = getDefaultPlayerSkills();

    // Modifier applied to all skills.

    let modifier: number = 0;

    // Gifted trait.

    const gifted = traits.find(trait => trait.name === TraitNames.gifted);

    if (gifted) { modifier -= 10; }

    switch (difficulty) {
        case Difficulty.easy:
            modifier += 20;
            break;
        case Difficulty.hard:
            modifier -= 10;
            break;
    }

    newBaseSkills.smallGuns = calculateSmallGuns(primaryStats, taggedSkills) + modifier;
    newBaseSkills.bigGuns = calculateBigGuns(primaryStats, taggedSkills) + modifier;
    newBaseSkills.energyWeapons = calculateEnergyWeapons(primaryStats, taggedSkills) + modifier;
    newBaseSkills.unarmed = calculateUnarmed(primaryStats, taggedSkills) + modifier;
    newBaseSkills.meleeWeapons = calculateMeleeWeapons(primaryStats, taggedSkills) + modifier;
    newBaseSkills.throwing = calculateThrowing(primaryStats, taggedSkills) + modifier;
    newBaseSkills.firstAid = calculateFirstAid(primaryStats, taggedSkills) + modifier;
    newBaseSkills.doctor = calculateDoctor(primaryStats, taggedSkills) + modifier;
    newBaseSkills.sneak = calculateSneak(primaryStats, taggedSkills) + modifier;
    newBaseSkills.lockpick = calculateLockpick(primaryStats, taggedSkills) + modifier;
    newBaseSkills.steal = calculateSteal(primaryStats, taggedSkills) + modifier;
    newBaseSkills.traps = calculateTraps(primaryStats, taggedSkills) + modifier;
    newBaseSkills.science = calculateScience(primaryStats, taggedSkills) + modifier;
    newBaseSkills.repair = calculateRepair(primaryStats, taggedSkills) + modifier;
    newBaseSkills.speech = calculateSpeech(primaryStats, taggedSkills) + modifier;
    newBaseSkills.barter = calculateBarter(primaryStats, taggedSkills) + modifier;
    newBaseSkills.gambling = calculateGambling(primaryStats, taggedSkills) + modifier;
    newBaseSkills.outdoorsman = calculateOutdoorsman(primaryStats, taggedSkills) + modifier;

    // Good natured trait.

    const goodNatured = traits.find(trait => trait.name === TraitNames.goodNatured);

    if (goodNatured) {  
        newBaseSkills = calculateGoodNatured(newBaseSkills);
    }

    // Perks affecting base skills.

    playersPerks.forEach((perk) => {
        switch (perk.name) {
            case PerkNames.gambler:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, gambling: newBaseSkills.gambling + 20 };
                }
                break;
            case PerkNames.ghost:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, sneak: newBaseSkills.sneak + 20 };
                }
                break;
            case PerkNames.harmless:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, steal: newBaseSkills.steal + 20 };
                }
                break;
            case PerkNames.livingAnatomy:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, doctor: newBaseSkills.doctor + 10 };
                }
                break;
            case PerkNames.masterThief:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, steal: newBaseSkills.steal + 15, lockpick: newBaseSkills.lockpick + 15 };
                }
                break;
            case PerkNames.medic:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, firstAid: newBaseSkills.firstAid + 10, doctor: newBaseSkills.doctor + 10 };
                }
                break;
            case PerkNames.mrFixit:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, science: newBaseSkills.science + 10, repair: newBaseSkills.repair + 10 };
                }
                break;
            case PerkNames.negotiator:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, speech: newBaseSkills.speech + 10, barter: newBaseSkills.barter + 10 };
                }
                break;
            case PerkNames.ranger:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, outdoorsman: newBaseSkills.outdoorsman + 15 };
                }
                break;
            case PerkNames.salesman:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, barter: newBaseSkills.barter + 20 };
                }
                break;
            case PerkNames.speaker:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, speech: newBaseSkills.speech + 20 };
                }
                break;
            case PerkNames.survivalist:
                if (perk.ranks > 0) {
                    newBaseSkills = { ...newBaseSkills, outdoorsman: newBaseSkills.outdoorsman + 25 };
                }
                break;
            case PerkNames.thief:
                if (perk.ranks > 0) {
                    newBaseSkills = {
                        ...newBaseSkills,
                        sneak: newBaseSkills.sneak + 10,
                        lockpick: newBaseSkills.lockpick + 10,
                        steal: newBaseSkills.steal + 10,
                        traps: newBaseSkills.traps + 10
                    };
                }
                break;
                case PerkNames.vaultCityTraining:
                    if (perk.ranks > 0) {
                        newBaseSkills = {
                            ...newBaseSkills,
                            firstAid: newBaseSkills.firstAid + 5,
                            doctor: newBaseSkills.doctor + 5
                        };
                    }
                    break;
        }
    });

    return newBaseSkills;
}

// Calculate invididual base skills.

function calculateSmallGuns(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 5 + 4 * agility

    let value: number = 5 + (4 * primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.SmallGuns);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateBigGuns(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 2 * agility

    let value: number = (2 * primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.BigGuns);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateEnergyWeapons(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 2 + (2 * perception) + ceil(luck / 2)

    let value: number = 2 + (2 * primaryStats.perception) + Math.ceil(primaryStats.luck / 2);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.EnergyWeapons);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateUnarmed(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 30 + 2 * (agility + strength)

    let value: number = 30 + 2 * (primaryStats.strength + primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Unarmed);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateMeleeWeapons(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 20 + 2 * (agility + strength)

    let value: number = 20 + 2 * (primaryStats.strength + primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.MeleeWeapons);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateThrowing(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 4 * agility

    let value: number = 4 * primaryStats.agility;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Throwing);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateFirstAid(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 2 * (perception + intelligence)

    let value: number = 30 + 2 * (primaryStats.strength + primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.FirstAid);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateDoctor(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 5 + (perception + intelligence)

    let value: number = 5 + (primaryStats.perception + primaryStats.intelligence);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Doctor);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateSneak(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 5 + 3 * agility

    let value: number = 5 + 3 * primaryStats.agility;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Sneak);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateLockpick(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 10 + (perception + agility)

    let value: number = 10 + (primaryStats.perception + primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Lockpick);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateSteal(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 3 * agility

    let value: number = 3 * primaryStats.agility;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Steal);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateTraps(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 10 + (perception + agility)

    let value: number = 10 + (primaryStats.perception + primaryStats.agility);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Traps);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateScience(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // Formula 4 * intelligence

    let value: number = 4 * primaryStats.intelligence;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Science);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateRepair(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // 3 * intelligence

    let value: number = 3 * primaryStats.intelligence;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Repair);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateSpeech(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // 5 * charisma

    let value: number = 5 * primaryStats.charisma;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Speech);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateBarter(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // 4 * charisma

    let value: number = 4 * primaryStats.charisma;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Barter);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateGambling(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // 5 * luck

    let value: number = 5 * primaryStats.luck;

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Gambling);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateOutdoorsman(primaryStats: IPrimaryStats, taggedSkills: string[]): number {
    // 2 * (intelligence + endurance) 

    let value: number = 2 * (primaryStats.intelligence + primaryStats.endurance);

    const tagged = taggedSkills.find((taggedSkill) => taggedSkill === PlayerSkillNames.Outdoorsman);

    if (tagged) {
        value += 20;
    }

    return value;
}

function calculateGoodNatured(skills: IPlayerSkills): IPlayerSkills {
    let newSkills: IPlayerSkills = { ...skills };

    newSkills.firstAid += 15;
    newSkills.doctor += 15;
    newSkills.speech += 15;
    newSkills.barter += 15;

    newSkills.smallGuns -= 10;
    newSkills.bigGuns -= 10;
    newSkills.energyWeapons -= 10;
    newSkills.unarmed -= 10;
    newSkills.meleeWeapons -= 10;
    newSkills.throwing -= 10;

    return newSkills;
}