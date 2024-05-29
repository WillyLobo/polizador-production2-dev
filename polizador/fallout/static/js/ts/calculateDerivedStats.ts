import { IPrimaryStats, IDerivedStats, ITrait, IPerk, PerkNames } from "./models"

/**
 * Calculate the derived stats
 * @param primaryStats primary stats state
 * @param traits traits state
 * @returns derived stats state
 */

export default function calculateDerivedStats(primaryStats: IPrimaryStats, traits: ITrait[], perks: IPerk[]): IDerivedStats {
    let newDerivedStats: IDerivedStats = derivedStatsDefault;

    newDerivedStats.hitPoints = calculateHitPoints(primaryStats);
    newDerivedStats.armorClass = calculateArmorClass(primaryStats, traits);
    newDerivedStats.carryWeight = calculateCarryWeight(primaryStats, traits);
    newDerivedStats.criticalChance = calculateCriticalChance(primaryStats, traits);
    newDerivedStats.healingRate = calculateHealingRate(primaryStats, traits);
    newDerivedStats.meleeDamage = calculateMeleeDamage(primaryStats, traits);
    newDerivedStats.damageResistance = calculateDamageResistance(primaryStats);
    newDerivedStats.poisonResistance = calculatePoisonResistance(primaryStats, traits);
    newDerivedStats.radiationResistance = calculateRadiationResistance(primaryStats, traits);
    newDerivedStats.sequence = calculateSequence(primaryStats, traits);
    newDerivedStats.partyLimit = calculatePartyLimit(primaryStats);
    newDerivedStats.perkRate = calculatePerkRate(primaryStats, traits);
    newDerivedStats.skillRate = calculateSkillRate(primaryStats, traits);
    newDerivedStats.actionPoints = calculateActionPoints(primaryStats, traits);
    newDerivedStats.enemyDamageResistanceModifier = calculateEnemyDamageResistance(traits);
    newDerivedStats.criticalDamageModifier = calculateCriticalDamageModifier(traits);
    newDerivedStats.chemAddictionChance = calculateChemAddictionChance(traits);
    newDerivedStats.chemDuration = calculateChemDuration(traits);
    newDerivedStats.chemAddictionRecovery = calculateChemAddictionRecovery(traits);
    newDerivedStats.hitPointsPerLevel = calculateHitPointsPerLevel(primaryStats);

    perks.forEach((perk) => {
        switch (perk.name) {
            case PerkNames.actionBoy:
                if (perk.ranks === 2) {
                    newDerivedStats.actionPoints += 2;
                } else if (perk.ranks === 1) {
                    newDerivedStats.actionPoints += 1;
                }
                break;
            case PerkNames.betterCriticals:
                if (perk.ranks === 1) {
                    newDerivedStats.criticalDamageModifier += 20;
                }
                break;
            case PerkNames.dodger:
                if (perk.ranks === 1) {
                    newDerivedStats.armorClass += 5;
                }
                break;
            case PerkNames.earlierSequence:
                if (perk.ranks === 1) {
                    newDerivedStats.sequence += 2;
                } else if (perk.ranks === 2) {
                    newDerivedStats.sequence += 4;
                } else if (perk.ranks === 3) {
                    newDerivedStats.sequence += 6;
                }
                break;
            case PerkNames.educated:
                if (perk.ranks === 1) {
                    newDerivedStats.skillRate += 2;
                } else if (perk.ranks === 2) {
                    newDerivedStats.skillRate += 4;
                } else if (perk.ranks === 3) {
                    newDerivedStats.skillRate += 6;
                }
                break;
            case PerkNames.fasterHealing:
                if (perk.ranks === 1) {
                    newDerivedStats.healingRate += 2;
                } else if (perk.ranks === 2) {
                    newDerivedStats.healingRate += 4;
                } else if (perk.ranks === 3) {
                    newDerivedStats.healingRate += 6;
                }
                break;
            case PerkNames.moreCriticals:
                if (perk.ranks === 1) {
                    newDerivedStats.criticalChance += 5;
                } else if (perk.ranks === 2) {
                    newDerivedStats.criticalChance += 10;
                } else if (perk.ranks === 3) {
                    newDerivedStats.criticalChance += 15;
                }
                break;
            case PerkNames.radResistance:
                if (perk.ranks === 1) {
                    newDerivedStats.radiationResistance += 15;
                } else if (perk.ranks === 2) {
                    newDerivedStats.radiationResistance += 30;
                }
                break;
            case PerkNames.snakeater:
                if (perk.ranks === 1) {
                    newDerivedStats.poisonResistance += 25;
                } else if (perk.ranks === 2) {
                    newDerivedStats.poisonResistance += 50;
                }
                break;
            case PerkNames.toughness:
                if (perk.ranks === 1) {
                    newDerivedStats.damageResistance += 10;
                } else if (perk.ranks === 2) {
                    newDerivedStats.damageResistance += 20;
                } else if (perk.ranks === 3) {
                    newDerivedStats.damageResistance += 30;
                }
                break;
            case PerkNames.packRat:
                if (perk.ranks === 1) {
                    newDerivedStats.carryWeight += 50;
                }
                break;
            case PerkNames.magneticPersonality:
                if (perk.ranks === 1) {
                    newDerivedStats.partyLimit += 1;
                }
                break;
            case PerkNames.lifegiver:
                if (perk.ranks === 1) {
                    newDerivedStats.hitPointsPerLevel += 4;
                } else if (perk.ranks === 2) {
                    newDerivedStats.hitPointsPerLevel += 8;
                }
                break;
            case PerkNames.vaultCityInoculations:
                if (perk.ranks === 1) {
                    newDerivedStats.poisonResistance += 10;
                    newDerivedStats.radiationResistance += 10;
                }

                break;
        }
    });

    return newDerivedStats;
}

function calculateHitPoints(primaryStats: IPrimaryStats): number {
    // Formula: hit points base value: 15 + strength + (endurance * 2)

    return 15 + primaryStats.strength + (primaryStats.endurance * 2);

    // level * (primaryStats.endurance / 2) + 2
}

function calculateHitPointsPerLevel(primaryStats: IPrimaryStats): number {
    // hit point increase per level (endurance / 2) + 2, NOT retroactive

    return (primaryStats.endurance / 2) + 2;
}

function calculateArmorClass(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: armor class = agility

    // Look for kamikaze trait
    const found = traits.find((trait) => trait.name === "Kamikaze");

    if (found) {
        return 0;
    }

    return primaryStats.agility;
}

function calculateCarryWeight(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: 25 + (strength * 25)

    // Look for small frame trait
    const found = traits.find((trait) => trait.name === "Small frame");

    if (found) {
        return 25 + 15 * primaryStats.strength;
    }

    return 25 + primaryStats.strength * 25;
}

function calculateCriticalChance(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: critical chance = luck

    // Look for finesse trait
    const found = traits.find((trait) => trait.name === "Finesse");

    if (found) {
        return primaryStats.luck + 10;
    }

    return primaryStats.luck;
}

function calculateDamageResistance(primaryStats: IPrimaryStats): number {
    // 0, increased by perk

    return 0;
}

function calculateHealingRate(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: (1/3) * endurance

    // Look for fast metabolism trait

    const found = traits?.find((trait) => trait.name === "Fast metabolism");

    if (found) {
        return (1 / 3) * primaryStats.endurance + 2;
    }

    const value = (1 / 3) * primaryStats.endurance;

    // Minimum value 1

    return value >= 1 ? value : 1;
}

function calculateActionPoints(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: 5 + agility / 2 rounded down

    // Look for bruiser trait

    const found = traits.find((trait) => trait.name === "Bruiser");

    if (found) {
        return 5 + Math.floor(primaryStats.agility / 2) - 2;
    }

    return 5 + Math.floor(primaryStats.agility / 2);
}

function calculateMeleeDamage(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: Strength - 5, minimum 1

    // Look for heavy handed trait
    const found = traits.find((trait) => trait.name === "Heavy handed");

    if (found) {
        return primaryStats.strength - 1;
    }

    let value = primaryStats.strength - 5;

    return value >= 1 ? value : 1;
}

function calculatePartyLimit(primaryStats: IPrimaryStats): number {
    // Formula: Charisma / 2, rounded down

    return Math.floor(primaryStats.charisma / 2);
}

export function calculatePerkRate(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Levels before perk, default 3, 4 by trait

    // Look for skilled trait
    const found = traits.find((trait) => trait.name === "Skilled");

    if (found) {
        return 4;
    }

    return 3;
}

function calculatePoisonResistance(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: Endurance * 5

    // Look for fast metabolism trait
    const found = traits.find((trait) => trait.name === "Fast metabolism");

    if (found) {
        return 0;
    }

    return primaryStats.endurance * 5;
}

function calculateRadiationResistance(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: Endurance * 2

    // Look for fast metabolism trait
    const found = traits.find((trait) => trait.name === "Fast metabolism");

    if (found) {
        return 0;
    }

    return primaryStats.endurance * 2;
}

function calculateSequence(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Formula: Perception * 2

    // Look for kamikaze trait
    const found = traits.find((trait) => trait.name === "Kamikaze");

    if (found) {
        return primaryStats.perception * 2 + 5;
    }

    return primaryStats.perception * 2;
}

export function calculateSkillRate(primaryStats: IPrimaryStats, traits: ITrait[]): number {
    // Skill points per level, formula intelligence * 2 + 5

    let value: number = primaryStats.intelligence * 2 + 5;

    // Look for skilled trait

    const skilled = traits.find((trait) => trait.name === "Skilled");

    if (skilled) {
        value = value + 5;
    }

    // Look for gifted trait

    const gifted = traits.find((trait) => trait.name === "Gifted");

    if (gifted) {
        value = value - 5;
    }

    return value;
}

function calculateEnemyDamageResistance(traits: ITrait[]): number {
    // Look for the finesse trait

    const found = traits?.find((trait) => trait.name === "Finesse");

    if (found) {
        return 30;
    }

    return 0;
}

function calculateCriticalDamageModifier(traits: ITrait[]) {
    // Look for the heavy handed trait

    const found = traits?.find((trait) => trait.name === "Heavy handed");

    if (found) {
        return -30;
    }

    return 0;
}

function calculateChemAddictionChance(traits: ITrait[]) {
    let value: number = 1;

    // Look for chem resistance trait
    const chemResistant = traits?.find((trait) => trait.name === "Chem resistant");

    if (chemResistant) {
        value = 0.5 * value;
    }

    // Look for chem reliant trait

    const chemReliant = traits?.find((trait) => trait.name === "Chem reliant");

    if (chemReliant) {
        value = 2 * value;
    }

    return value;
}

function calculateChemDuration(traits: ITrait[]) {
    // Look for chem resistance trait
    const found = traits?.find((trait) => trait.name === "Chem resistant");

    if (found) {
        return 0.5;
    }

    return 1;
}

function calculateChemAddictionRecovery(traits: ITrait[]) {
    // Look for chem reliant trait
    const found = traits?.find((trait) => trait.name === "Chem reliant");

    if (found) {
        return 2;
    }

    return 1;
}

/**
 * Default object
 */

export const derivedStatsDefault: IDerivedStats = {
    hitPoints: 30,
    armorClass: 5,
    actionPoints: 7,
    carryWeight: 150,
    meleeDamage: 1,
    damageResistance: 0,
    poisonResistance: 25,
    radiationResistance: 10,
    sequence: 10,
    healingRate: (5 / 3),
    criticalChance: 5,
    partyLimit: 2,
    skillRate: 15,
    perkRate: 3,
    enemyDamageResistanceModifier: 0,
    criticalDamageModifier: 0,
    chemAddictionChance: 1,
    chemAddictionRecovery: 1,
    chemDuration: 1,
    hitPointsPerLevel: 4.5
};