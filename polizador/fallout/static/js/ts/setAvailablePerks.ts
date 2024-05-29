import { IPerk, IPrimaryStats, IPlayerSkills, PerkNames } from "./models";

function checkPrimaryStats(requiredPrimaryStats: IPrimaryStats, primaryStats: IPrimaryStats): boolean {
    let requirementsMet: boolean = true;

    if (requiredPrimaryStats.strength > primaryStats.strength) {
        requirementsMet = false;
    }

    if (requiredPrimaryStats.perception > primaryStats.perception) {
        requirementsMet = false;
    }

    if (requiredPrimaryStats.endurance > primaryStats.endurance) {
        requirementsMet = false;
    }

    if (requiredPrimaryStats.charisma > primaryStats.charisma) {
        requirementsMet = false;
    }

    if (requiredPrimaryStats.intelligence > primaryStats.intelligence) {
        requirementsMet = false;
    }

    if (requiredPrimaryStats.agility > primaryStats.agility) {
        requirementsMet = false;
    }

    if (requiredPrimaryStats.luck > primaryStats.luck) {
        requirementsMet = false;
    }

    return requirementsMet;
};

function checkPlayerSkills(requiredPlayerSkills: IPlayerSkills, playerSkills: IPlayerSkills): boolean {
    let requirementsMet: boolean = true;

    // Perk skill requirement for no requirement is 0

    // Player's skills can be below 0
    
    // Ignore skill requirements for 0

    if (requiredPlayerSkills.smallGuns > playerSkills.smallGuns && requiredPlayerSkills.smallGuns !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.bigGuns > playerSkills.bigGuns && requiredPlayerSkills.bigGuns !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.energyWeapons > playerSkills.energyWeapons && requiredPlayerSkills.energyWeapons !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.unarmed > playerSkills.unarmed && requiredPlayerSkills.unarmed !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.meleeWeapons > playerSkills.meleeWeapons && requiredPlayerSkills.meleeWeapons !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.throwing > playerSkills.throwing && requiredPlayerSkills.throwing !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.firstAid > playerSkills.firstAid && requiredPlayerSkills.firstAid !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.doctor > playerSkills.doctor && requiredPlayerSkills.doctor !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.sneak > playerSkills.sneak && requiredPlayerSkills.sneak !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.lockpick > playerSkills.lockpick && requiredPlayerSkills.lockpick !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.steal > playerSkills.steal && requiredPlayerSkills.steal !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.traps > playerSkills.traps && requiredPlayerSkills.traps !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.science > playerSkills.science && requiredPlayerSkills.science !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.repair > playerSkills.repair && requiredPlayerSkills.repair !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.speech > playerSkills.speech && requiredPlayerSkills.speech !== 0) {
        requirementsMet = false;
    }

    if (requiredPlayerSkills.barter > playerSkills.barter && requiredPlayerSkills.barter !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.gambling > playerSkills.gambling && requiredPlayerSkills.gambling !== 0) {
        requirementsMet = false;
    }


    if (requiredPlayerSkills.outdoorsman > playerSkills.outdoorsman && requiredPlayerSkills.outdoorsman !== 0) {
        requirementsMet = false;
    }


    return requirementsMet;
};

/**
 * Set requirementsMet to true if perk requirements are met
 * @param perks available perks
 * @param primaryStats primary stats
 * @param playerSkills final player skills
 * @returns modified available perks
 */

export default function setAvailablePerks(perks: IPerk[], primaryStats: IPrimaryStats, playerSkills: IPlayerSkills, playerLevel: number): IPerk[] {
    // Set the requirements met property of all perks to false

    let availablePerks: IPerk[] = perks.map((perk) => {
        perk.requirementsMet = false;

        return perk;
    });

    availablePerks = availablePerks.map((perk) => {
        let requirements = perk.requirements;

        let requiredLevel = requirements.level;

        let requirementsMet = false;

        // Check the required level

        if (requiredLevel > playerLevel) {
            perk.requirementsMet = requirementsMet;

            return perk;
        }

        // Gain primary stat perk requires primary stat < 10

        if (perk.name.includes("Gain")) {
            switch (perk.name) {
                case PerkNames.gainStrength:
                    if (primaryStats.strength < perk.requirements.primaryStats.strength) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;

                case PerkNames.gainPerception:
                    if (primaryStats.perception < perk.requirements.primaryStats.perception) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;

                case PerkNames.gainEndurance:
                    if (primaryStats.endurance < perk.requirements.primaryStats.endurance) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;

                case PerkNames.gainCharisma:
                    if (primaryStats.charisma < perk.requirements.primaryStats.charisma) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;

                case PerkNames.gainIntelligence:
                    if (primaryStats.intelligence < perk.requirements.primaryStats.intelligence) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;

                case PerkNames.gainAgility:
                    if (primaryStats.agility < perk.requirements.primaryStats.agility) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;

                case PerkNames.gainLuck:
                    if (primaryStats.luck < perk.requirements.primaryStats.luck) {
                        requirementsMet = true;
                    }

                    perk.requirementsMet = requirementsMet;

                    return perk;
            }
        }

        let requiredPrimaryStats = requirements.primaryStats;

        // Adrenaline rush requires strength < 10

        if (perk.name === PerkNames.adrenalineRush) {
            if (primaryStats.strength < requiredPrimaryStats.strength) {
                requirementsMet = true;

                perk.requirementsMet = requirementsMet;

                return perk;
            }
        }

        // Magnetic personality requires charisma < 10

        if (perk.name === PerkNames.magneticPersonality) {

            if (primaryStats.charisma < requiredPrimaryStats.charisma) {
                requirementsMet = true;

                perk.requirementsMet = requirementsMet;

                return perk;
            }
            requirementsMet = false;

            perk.requirementsMet = requirementsMet;

            return perk;
        }

        // Weapon handling requires strength < 7

        if (perk.name === PerkNames.weaponHandling) {
            if (primaryStats.strength < requiredPrimaryStats.strength) {

                // Weapon handling also requires agility >= 5

                if (primaryStats.agility >= requiredPrimaryStats.agility) {
                    requirementsMet = true;

                    perk.requirementsMet = requirementsMet;

                    return perk;
                }
                
                perk.requirementsMet = requirementsMet;

                return perk;
            }

            perk.requirementsMet = requirementsMet;

            return perk;
        }

        let requiredPlayerSkills = requirements.playerSkills;

        // Check the primary stats

        let primaryStatsRequirementsMet = checkPrimaryStats(requiredPrimaryStats, primaryStats);

        // Check the players skills

        let playerSkillsRequirementsMet = checkPlayerSkills(requiredPlayerSkills, playerSkills);

        if (primaryStatsRequirementsMet && playerSkillsRequirementsMet) {
            requirementsMet = true;
        }

        perk.requirementsMet = requirementsMet;

        // Vault city inoculations requires vault city training.

        if (perk.name === PerkNames.vaultCityInoculations) {
            const vaultCityTraining = perks.find(perk => perk.name === PerkNames.vaultCityTraining);

            let vaultCityTrainingSelected = false;

            if (vaultCityTraining) {

                if (vaultCityTraining.ranks === 0) {
                    vaultCityTrainingSelected = true;
                }
                
            }
       
            if (!vaultCityTrainingSelected) {
                perk.requirementsMet = false;
            }

            // Both requirements are met.  

            if (requirementsMet && vaultCityTrainingSelected) {
                perk.requirementsMet = true;
            }
        }

        return perk;
    });

    return availablePerks;
}