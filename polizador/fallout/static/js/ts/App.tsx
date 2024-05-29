import React, { useReducer, useState, MouseEvent, useEffect } from "react";
import "./App.css";
import PrimaryStats from "./components/primaryStats";
import PlayerSkills from "./components/playerSkills";
import DerivedStats from "./components/derivedStats";
import { IPrimaryStats, IPlayerSkills, ITrait, TRAITS, getEmptyPlayerSkills, getDefaultPlayerSkills, PlayerSkillNames, IPerk, PERKS, PerkNames, TOOLTIPS, TraitNames, Difficulty } from "./models";
import calculateBaseSkills from "./calculateBaseSkills";
import calculateDerivedStats, { derivedStatsDefault } from "./calculateDerivedStats";
import { calculateFinalSkills } from "./calculateFinalSkills";
import Traits from "./components/traits";
import Perks from "./components/perks";
import { getPrintablePrimaryStats, getPrintableTraits, getPrintablePerks } from "./createPrints";
import Footer from "./components/footer";

/**
 * Returns supplied perks with ranks set to 0.
 * @param perks supplied perks.
 * @returns perks with ranks set to 0.
 */

function getDefaultPlayerPerks(perks: IPerk[]): IPerk[] {
    // Set all perk ranks to 0.

    const defaultPlayerPerks: IPerk[] = perks.map(perk => { return { ...perk, ranks: 0 } });

    return defaultPlayerPerks;
}

interface IPlayersPerksAction {
    type: string,
    perkName: string,
    playerLevel: number,
    primaryStats: IPrimaryStats
}

function playersPerksReducer(state: IPerk[], action: IPlayersPerksAction): IPerk[] {
    let newPlayersPerks: IPerk[] = [...state];

    // Find the index of the perk to mutate.

    const index = newPlayersPerks.findIndex((perk) => perk.name === action.perkName);

    // Perk not found.

    if (index === -1 && action.type !== "reset") { return newPlayersPerks; }

    let rank: number;

    switch (action.type) {
        case "add":
            // Prevent ranks over the max rank.

            const maxRanks = newPlayersPerks[index].maxRanks;

            rank = newPlayersPerks[index].ranks;

            if (rank + 1 > maxRanks) {
                return newPlayersPerks;
            }

            // Add rank to the perk.

            newPlayersPerks[index].ranks += 1;

            // Save the current luck value to the zeta scan perk.

            if (newPlayersPerks[index].name === PerkNames.zetaScan) {

                newPlayersPerks[index].baseValue = action.primaryStats.luck;
            }

            newPlayersPerks[index].levelSelected.push(action.playerLevel);

            break;
        case "remove":
            // Prevent perk ranks below 0.

            rank = newPlayersPerks[index].ranks;

            if (rank < 0) { return newPlayersPerks; }

            // Remove a rank from the perk.

            newPlayersPerks[index].ranks -= 1;

            // Remove the latest level selected.

            newPlayersPerks[index].levelSelected.pop();

            break;
        case "reset":
            newPlayersPerks = getDefaultPlayerPerks(PERKS);

            break;
    }

    return newPlayersPerks;
}

interface IAvailablePerksAction {
    type: string,
    perkName: string
}

function availablePerksReducer(state: IPerk[], action: IAvailablePerksAction): IPerk[] {
    let newAvailablePerks = [...state];

    // Find the index of the perk to mutate.

    const index = state.findIndex((perk) => perk.name === action.perkName);

    // Perk not found.

    if (index === -1) { return newAvailablePerks; }

    let rank: number;

    switch (action.type) {
        case "add":

            // Prevent adding the here and now perk.

            if (newAvailablePerks[index].name === PerkNames.hereAndNow) {
                return newAvailablePerks;
            }

            // Prevent perk ranks over the max rank.

            const maxRanks = newAvailablePerks[index].maxRanks;

            rank = newAvailablePerks[index].ranks;

            if (rank + 1 > maxRanks) {
                return newAvailablePerks;
            }

            // Add rank to the perk.

            newAvailablePerks[index].ranks += 1;

            break;
        case "remove":
            // Prevent perk ranks below 0.

            rank = newAvailablePerks[index].ranks;

            if (rank < 0) {
                return newAvailablePerks;
            }

            // Remove a rank from the perk.

            newAvailablePerks[index].ranks -= 1;

            break;
        case "reset":
            newAvailablePerks = [...PERKS];

            break;
    }

    return newAvailablePerks;
}

function raisedSkillsReducer(state: IPlayerSkills, action: IRaisedSkillsAction): IPlayerSkills {
    let newState: IPlayerSkills = Object.assign({}, state);

    switch (action.type) {
        case "increase":
            newState = increaseRaisedSkill(action.skillName, action.amount, newState);
            break;
        case "decrease":
            newState = decreaseRaisedSkill(action.skillName, action.amount, newState);
            break;
        case "reset":
            newState = getEmptyPlayerSkills();
            break;
        default:
    }

    return newState;
}

function increaseRaisedSkill(skillName: string, amount: number, raisedSkills: IPlayerSkills): IPlayerSkills {
    let newRaisedSkills = raisedSkills;

    switch (skillName) {
        case PlayerSkillNames.SmallGuns:
            newRaisedSkills.smallGuns += amount;
            break;
        case PlayerSkillNames.BigGuns:
            newRaisedSkills.bigGuns += amount;
            break;
        case PlayerSkillNames.EnergyWeapons:
            newRaisedSkills.energyWeapons += amount;
            break;
        case PlayerSkillNames.Unarmed:
            newRaisedSkills.unarmed += amount;
            break;
        case PlayerSkillNames.MeleeWeapons:
            newRaisedSkills.meleeWeapons += amount;
            break;
        case PlayerSkillNames.Throwing:
            newRaisedSkills.throwing += amount;
            break;
        case PlayerSkillNames.FirstAid:
            newRaisedSkills.firstAid += amount;
            break;
        case PlayerSkillNames.Doctor:
            newRaisedSkills.doctor += amount;
            break;
        case PlayerSkillNames.Sneak:
            newRaisedSkills.sneak += amount;
            break;
        case PlayerSkillNames.Lockpick:
            newRaisedSkills.lockpick += amount;
            break;
        case PlayerSkillNames.Steal:
            newRaisedSkills.steal += amount;
            break;
        case PlayerSkillNames.Traps:
            newRaisedSkills.traps += amount;
            break;
        case PlayerSkillNames.Science:
            newRaisedSkills.science += amount;
            break;
        case PlayerSkillNames.Repair:
            newRaisedSkills.repair += amount;
            break;
        case PlayerSkillNames.Speech:
            newRaisedSkills.speech += amount;
            break;
        case PlayerSkillNames.Barter:
            newRaisedSkills.barter += amount;
            break;
        case PlayerSkillNames.Gambling:
            newRaisedSkills.gambling += amount;
            break;
        case PlayerSkillNames.Outdoorsman:
            newRaisedSkills.outdoorsman += amount;
            break;
        default:
    }

    return newRaisedSkills;
}

function decreaseRaisedSkill(skillName: string, amount: number, raisedSkills: IPlayerSkills): IPlayerSkills {
    let newRaisedSkills = Object.assign({}, raisedSkills);

    switch (skillName) {
        case PlayerSkillNames.SmallGuns:
            newRaisedSkills.smallGuns -= amount;
            break;
        case PlayerSkillNames.BigGuns:
            newRaisedSkills.bigGuns -= amount;
            break;
        case PlayerSkillNames.EnergyWeapons:
            newRaisedSkills.energyWeapons -= amount;
            break;
        case PlayerSkillNames.Unarmed:
            newRaisedSkills.unarmed -= amount;
            break;
        case PlayerSkillNames.MeleeWeapons:
            newRaisedSkills.meleeWeapons -= amount;
            break;
        case PlayerSkillNames.Throwing:
            newRaisedSkills.throwing -= amount;
            break;
        case PlayerSkillNames.FirstAid:
            newRaisedSkills.firstAid -= amount;
            break;
        case PlayerSkillNames.Doctor:
            newRaisedSkills.doctor -= amount;
            break;
        case PlayerSkillNames.Sneak:
            newRaisedSkills.sneak -= amount;
            break;
        case PlayerSkillNames.Lockpick:
            newRaisedSkills.lockpick -= amount;
            break;
        case PlayerSkillNames.Steal:
            newRaisedSkills.steal -= amount;
            break;
        case PlayerSkillNames.Traps:
            newRaisedSkills.traps -= amount;
            break;
        case PlayerSkillNames.Science:
            newRaisedSkills.science -= amount;
            break;
        case PlayerSkillNames.Repair:
            newRaisedSkills.repair -= amount;
            break;
        case PlayerSkillNames.Speech:
            newRaisedSkills.speech -= amount;
            break;
        case PlayerSkillNames.Barter:
            newRaisedSkills.barter -= amount;
            break;
        case PlayerSkillNames.Gambling:
            newRaisedSkills.gambling -= amount;
            break;
        case PlayerSkillNames.Outdoorsman:
            newRaisedSkills.outdoorsman -= amount;
            break;
        default:
    }

    return newRaisedSkills;
}

interface IRaisedSkillsAction {
    type: string,
    skillName: string,
    amount: number
}

interface IPrimaryStatsAction {
    type: string,
    payload: string,
    traits: ITrait[],
    gainPrimaryStatPerk?: string,
    zetaScanAmount?: number
}

function primaryStatsReducer(state: IPrimaryStats, action: IPrimaryStatsAction): IPrimaryStats {
    let newState = { ...state };

    switch (action.type) {
        case "increase":
            newState = increasePrimaryStat(newState, action.payload, action.traits);

            break;

        case "decrease":
            newState = decreasePrimaryStat(newState, action.payload, action.traits);

            break;

        case "reset":

            newState = getDefaultPrimaryStats();

            break;

        case "small frame":
            if (action.payload === "add") {
                newState.agility += 1;
            }

            if (action.payload === "remove") {
                newState.agility -= 1;
            }

            break;

        case "gifted":
            if (action.payload === "add") {
                newState = increaseAllPrimaryStats(newState);
            }

            if (action.payload === "remove") {
                newState = decreaseAllPrimaryStats(newState);
            }

            break;

        case "bruiser":
            if (action.payload === "add") {
                newState.strength += 2;
            }

            if (action.payload === "remove") {
                newState.strength -= 2;
            }

            break;

        case "gainPerk":
            if (action.payload === "add") {

                // Check undefined.

                if (action.gainPrimaryStatPerk) {
                    switch (action.gainPrimaryStatPerk) {
                        case PerkNames.gainStrength:
                            newState.strength += 1;
                            break;
                        case PerkNames.gainPerception:
                            newState.perception += 1;
                            break;
                        case PerkNames.gainEndurance:
                            newState.endurance += 1;
                            break;
                        case PerkNames.gainCharisma:
                            newState.charisma += 1;
                            break;
                        case PerkNames.gainIntelligence:
                            newState.intelligence += 1;
                            break;
                        case PerkNames.gainAgility:
                            newState.agility += 1;
                            break;
                        case PerkNames.gainLuck:
                            newState.luck += 1;
                            break;
                    }
                }
            }

            if (action.payload === "remove") {

                // Check undefined

                if (action.gainPrimaryStatPerk) {

                    switch (action.gainPrimaryStatPerk) {
                        case PerkNames.gainStrength:
                            newState.strength -= 1;
                            break;
                        case PerkNames.gainPerception:
                            newState.perception -= 1;
                            break;
                        case PerkNames.gainEndurance:
                            newState.endurance -= 1;
                            break;
                        case PerkNames.gainCharisma:
                            newState.charisma -= 1;
                            break;
                        case PerkNames.gainIntelligence:
                            newState.intelligence -= 1;
                            break;
                        case PerkNames.gainAgility:
                            newState.agility -= 1;
                            break;
                        case PerkNames.gainLuck:
                            newState.luck -= 1;
                            break;
                    }

                }
            }

            break;

        case "zetaScan":
            const amount = action.zetaScanAmount;

            if (!amount) { return newState };

            if (action.payload === "add") {
                switch (amount) {
                    case 1:
                        newState.luck += 1;
                        break;
                    case 2:
                        newState.luck += 2;
                        break;
                }
            }

            else if (action.payload === "remove") {
                switch (amount) {
                    case 1:
                        newState.luck -= 1;
                        break;
                    case 2:
                        newState.luck -= 2;
                        break;
                }
            }

            break;

        default:
    }

    return newState;
}

/**
 * Increases a primary stat.
 * @param primaryStats character's current primary stats.
 * @param stat primary stat to increase.
 * @returns character's new primary stats.
 */

function increasePrimaryStat(primaryStats: IPrimaryStats, primaryStat: string, traits: ITrait[]): IPrimaryStats {
    let newPrimaryStats = {...primaryStats};

    // Need unspent primary stat points

    if (primaryStats.unspentPoints === 0) {
        return newPrimaryStats;
    }
    
    switch (primaryStat) {
        case "strength":
            if (primaryStats.strength < 10) {
                newPrimaryStats.strength += 1;
                newPrimaryStats.unspentPoints -= 1;
            }

            break;

        case "perception":
            if (primaryStats.perception < 10) {
                newPrimaryStats.perception += 1;
                newPrimaryStats.unspentPoints -= 1;
            }

            break;

        case "endurance":
            if (primaryStats.endurance < 10) {
                newPrimaryStats.endurance += 1;
                newPrimaryStats.unspentPoints -= 1;
            }

            break;

        case "charisma":
            if (primaryStats.charisma < 10) {
                newPrimaryStats.charisma += 1;
                newPrimaryStats.unspentPoints -= 1;
            }

            break;

        case "intelligence":
            if (primaryStats.intelligence < 10) {
                newPrimaryStats.intelligence += 1;
                newPrimaryStats.unspentPoints -= 1;
            }
            break;

        case "agility":
            if (primaryStats.agility < 10) {
                newPrimaryStats.agility += 1;
                newPrimaryStats.unspentPoints -= 1;
            }

            break;

        case "luck":
            if (primaryStats.luck < 10) {
                newPrimaryStats.luck += 1;
                newPrimaryStats.unspentPoints -= 1;
            }

            break;

        // Increase the unspent stat points.

        case "unspentPoint":
            newPrimaryStats.unspentPoints += 1;

            break;

        default:
    }

    return newPrimaryStats;
}

/**
 * Decreases a primary stat.
 * @param primaryStats character's current primary stats.
 * @param stat primary stat to decrease.
 * @param traits character's current traits. Certain traits, such as Gifted, limit the minimum primary stat values.
 * @returns character's new primary stats.
 */

function decreasePrimaryStat(primaryStats: IPrimaryStats, stat: string, traits: ITrait[]): IPrimaryStats {
    // Primary stat minimum value 1

    let minimumValue = 1;

    // Look for gifted trait

    const gifted = traits?.find((trait) => trait.name === TraitNames.gifted);

    if (gifted) {

        // Raise minimum value

        minimumValue = 2;
    }

    let newState: IPrimaryStats = Object.assign({}, primaryStats);

    switch (stat) {
        case "strength":
            // Look for bruiser trait

            const bruiser = traits.find((trait) => trait.name === TraitNames.bruiser);

            if (bruiser) {
                // Raise minimum strength

                minimumValue += 2;
            }

            if (primaryStats.strength > minimumValue) {
                newState.strength -= 1;
                newState.unspentPoints += 1;
            }
            break;

        case "perception":
            if (primaryStats.perception > minimumValue) {
                newState.perception -= 1;
                newState.unspentPoints += 1;
            }
            break;

        case "endurance":
            if (primaryStats.endurance > minimumValue) {
                newState.endurance -= 1;
                newState.unspentPoints += 1;
            }
            break;

        case "charisma":
            if (primaryStats.charisma > minimumValue) {
                newState.charisma -= 1;
                newState.unspentPoints += 1;
            }
            break;

        case "intelligence":
            if (primaryStats.intelligence > minimumValue) {
                newState.intelligence -= 1;
                newState.unspentPoints += 1;
            }
            break;

        case "agility":
            // Look for small frame trait

            const smallFrame = traits.find((trait) => trait.name === "Small frame");

            if (smallFrame) {
                // Raise minimum agility

                minimumValue += 1;
            }

            if (primaryStats.agility > minimumValue) {

                newState.agility -= 1;
                newState.unspentPoints += 1;
            }
            break;

        case "luck":
            if (primaryStats.luck > minimumValue) {
                newState.luck -= 1;
                newState.unspentPoints += 1;
            }
            break;

        // Decrease unspent stat points.

        case "unspentPoint":
            newState.unspentPoints -= 1;

            break;

        default:
    }

    return newState;
}

function increaseAllPrimaryStats(primaryStats: IPrimaryStats): IPrimaryStats {
    let newPrimaryStats = Object.assign({}, primaryStats);

    newPrimaryStats.strength += 1;
    newPrimaryStats.perception += 1;
    newPrimaryStats.endurance += 1;
    newPrimaryStats.charisma += 1;
    newPrimaryStats.intelligence += 1;
    newPrimaryStats.agility += 1;
    newPrimaryStats.luck += 1;

    return newPrimaryStats;
}

function decreaseAllPrimaryStats(primaryStats: IPrimaryStats): IPrimaryStats {
    let newPrimaryStats = Object.assign({}, primaryStats);

    newPrimaryStats.strength -= 1;
    newPrimaryStats.perception -= 1;
    newPrimaryStats.endurance -= 1;
    newPrimaryStats.charisma -= 1;
    newPrimaryStats.intelligence -= 1;
    newPrimaryStats.agility -= 1;
    newPrimaryStats.luck -= 1;

    return newPrimaryStats;
}

/**
 * Returns primary stats filled with 5's.
 */

function getDefaultPrimaryStats(): IPrimaryStats {
    const defaultPrimaryStats: IPrimaryStats = {
        strength: 5,
        perception: 5,
        endurance: 5,
        charisma: 5,
        intelligence: 5,
        agility: 5,
        luck: 5,
        unspentPoints: 5
    }

    return defaultPrimaryStats;
}

/**
 * Calculates the skill point cost to raise the skill level.
 * @param skillValue the current skill level.
 * @returns the skill point cost.
 */

function getSkillCost(skillValue: number): number {
    let cost: number;

    if (skillValue <= 100) {
        cost = 1;
    } else if (skillValue >= 101 && skillValue <= 125) {
        cost = 2;
    } else if (skillValue >= 126 && skillValue <= 150) {
        cost = 3;
    } else if (skillValue >= 151 && skillValue <= 175) {
        cost = 4;
    } else if (skillValue >= 176 && skillValue <= 200) {
        cost = 5;
    } else {
        cost = 6;
    }

    return cost;
}

function App() {

    const [primaryStats, primaryStatsDispatch] = useReducer(primaryStatsReducer, getDefaultPrimaryStats());

    const [playerLevel, setplayerLevel] = useState(1);

    const [baseSkills, setBaseSkills] = useState(getDefaultPlayerSkills());

    const [raisedSkills, raisedSkillsDispatch] = useReducer(raisedSkillsReducer, getEmptyPlayerSkills());

    const [tagPoints, setTagPoints] = useState(3);

    const emptyTaggedSkills: string[] = [];

    const [taggedSkills, setTaggedSkills] = useState(emptyTaggedSkills);

    const emptyTraits: Array<ITrait> = [];

    // Traits are added or removed from an array.

    const [traits, setTraits] = useState([...emptyTraits]);

    const [derivedStats, setDerivedStats] = useState(derivedStatsDefault);

    const [skillPoints, setSkillPoints] = useState(0);

    // Perks are not added or removed from an array, but invidual perks are changed.

    const [playersPerks, playersPerksDispatch] = useReducer(playersPerksReducer, getDefaultPlayerPerks(PERKS));

    const [perkPoints, setPerkPoints] = useState(0);

    const [availablePerks, availablePerksDispatch] = useReducer(availablePerksReducer, PERKS);

    const [tooltipHeading, setTooltipHeading] = useState(TOOLTIPS[0].heading);

    const [tooltipSubHeading, setTooltipSubHeading] = useState(TOOLTIPS[0].subHeading);

    const [tooltipBody, setTooltipBody] = useState(TOOLTIPS[0].body);

    const [difficulty, setDifficulty] = useState(String(Difficulty.normal));

    // The difficulty knob switches from normal to hard, hard to normal, normal to easy, easy to normal.

    const [difficultyDirection, setDifficultyDirection] = useState(true);

    const [, forceRender] = useState(false);

    const handlePlayerLevelUpClick = (event: MouseEvent<HTMLButtonElement>) => {
        if (primaryStats.unspentPoints > 0) {
            alert("You must use all character points!");

            return;
        }

        if (tagPoints !== 0) {
            alert("You must select all tag skills!");

            return;
        }

        let statCheck: boolean = false;

        // Maximum primary stat 10

        Object.values(primaryStats).forEach((primaryStat) => {
            if (primaryStat > 10) {
                statCheck = true;
            }
        });

        if (statCheck) {
            alert("All stats must be between 1 and 10!");

            return;
        }

        levelUp();
    };

    const levelUp = () => {
        // Max level 99.
        
        if (playerLevel >= 99) { return; }

        // Get the skill rate.

        const skillRate = derivedStats.skillRate;

        // Add skill points.

        setSkillPoints(skillPoints => skillPoints + skillRate);

        // Increase the player level.

        setplayerLevel(playerLevel => playerLevel + 1);

        const perkRate = derivedStats.perkRate;

        // Add a perk point every third or fourth level depending on the perk rate.

        if ((playerLevel + 1) % perkRate === 0) {
            setPerkPoints(perkPoints => perkPoints + 1);
        }
    }

    const handleSkillValueClick = (event: MouseEvent<HTMLButtonElement>) => {
        const skillName = event.currentTarget.getAttribute("data-skill-name")
        const action = event.currentTarget.getAttribute("data-action");

        if (!action || !skillName) { return; }

        let isTagged: string | undefined;

        let skillCost: number;

        if (action === "increase") {

            // Combine base and raised skills to calculate skill cost.

            const finalSkills = calculateFinalSkills(baseSkills, raisedSkills);

            switch (skillName) {
                case PlayerSkillNames.SmallGuns:

                    skillCost = getSkillCost(finalSkills.smallGuns);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.SmallGuns);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.SmallGuns, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.SmallGuns, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.BigGuns:

                    skillCost = getSkillCost(finalSkills.bigGuns);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.BigGuns);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.BigGuns, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.BigGuns, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.EnergyWeapons:

                    skillCost = getSkillCost(finalSkills.energyWeapons);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.EnergyWeapons);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.EnergyWeapons, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.EnergyWeapons, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Unarmed:

                    skillCost = getSkillCost(finalSkills.unarmed);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Unarmed);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Unarmed, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Unarmed, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.MeleeWeapons:

                    skillCost = getSkillCost(finalSkills.meleeWeapons);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.MeleeWeapons);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.MeleeWeapons, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.MeleeWeapons, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Throwing:

                    skillCost = getSkillCost(finalSkills.throwing);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Throwing);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Throwing, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Throwing, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.FirstAid:

                    skillCost = getSkillCost(finalSkills.firstAid);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.FirstAid);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.FirstAid, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.FirstAid, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Doctor:

                    skillCost = getSkillCost(finalSkills.doctor);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Doctor);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Doctor, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Doctor, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Sneak:

                    skillCost = getSkillCost(finalSkills.sneak);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Sneak);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Sneak, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Sneak, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Lockpick:

                    skillCost = getSkillCost(finalSkills.lockpick);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Lockpick);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Lockpick, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Lockpick, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Steal:

                    skillCost = getSkillCost(finalSkills.steal);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Steal);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Steal, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Steal, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Traps:

                    skillCost = getSkillCost(finalSkills.traps);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Traps);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Traps, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Traps, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Science:

                    skillCost = getSkillCost(finalSkills.science);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Science);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Science, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Science, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Repair:

                    skillCost = getSkillCost(finalSkills.repair);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Repair);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Repair, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Repair, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Speech:

                    skillCost = getSkillCost(finalSkills.speech);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Speech);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Speech, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Speech, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Barter:

                    skillCost = getSkillCost(finalSkills.barter);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Barter);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Barter, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Barter, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Gambling:

                    skillCost = getSkillCost(finalSkills.gambling);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Gambling);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Gambling, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Gambling, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;

                case PlayerSkillNames.Outdoorsman:

                    skillCost = getSkillCost(finalSkills.outdoorsman);

                    // Not enough skill points.

                    if (skillPoints - skillCost < 0) {
                        break;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Outdoorsman);

                    if (isTagged) {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Outdoorsman, amount: 2 })
                    } else {
                        raisedSkillsDispatch({ type: "increase", skillName: PlayerSkillNames.Outdoorsman, amount: 1 })
                    }

                    // Deduct skill points.

                    setSkillPoints(skillPoints => skillPoints - skillCost);

                    break;
            }
        }

        if (action === "decrease") {

            // Prevent overfunding of skill points at skill cost breakpoints by avoiding the stale state.

            let skillLevel: number;

            switch (skillName) {

                case PlayerSkillNames.SmallGuns:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.smallGuns <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.SmallGuns);

                    skillLevel = baseSkills.smallGuns + raisedSkills.smallGuns;

                    if (isTagged) {
                        if (raisedSkills.smallGuns <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.SmallGuns, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.SmallGuns, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.BigGuns:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.bigGuns <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.BigGuns);

                    skillLevel = baseSkills.bigGuns + raisedSkills.bigGuns;

                    if (isTagged) {
                        if (raisedSkills.bigGuns <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.BigGuns, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.BigGuns, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.EnergyWeapons:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.energyWeapons <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.EnergyWeapons);

                    skillLevel = baseSkills.energyWeapons + raisedSkills.energyWeapons;

                    if (isTagged) {
                        if (raisedSkills.energyWeapons <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.EnergyWeapons, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.EnergyWeapons, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Unarmed:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.unarmed <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Unarmed);

                    skillLevel = baseSkills.unarmed + raisedSkills.unarmed;

                    if (isTagged) {
                        if (raisedSkills.unarmed <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Unarmed, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Unarmed, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.MeleeWeapons:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.meleeWeapons <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.MeleeWeapons);

                    skillLevel = baseSkills.meleeWeapons + raisedSkills.meleeWeapons;

                    if (isTagged) {
                        if (raisedSkills.meleeWeapons <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.MeleeWeapons, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.MeleeWeapons, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);;

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Throwing:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.throwing <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Throwing);

                    skillLevel = baseSkills.throwing + raisedSkills.throwing;

                    if (isTagged) {
                        if (raisedSkills.throwing <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Throwing, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Throwing, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.FirstAid:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.firstAid <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.FirstAid);

                    skillLevel = baseSkills.firstAid + raisedSkills.firstAid;

                    if (isTagged) {
                        if (raisedSkills.firstAid <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.FirstAid, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.FirstAid, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Doctor:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.doctor <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Doctor);

                    skillLevel = baseSkills.doctor + raisedSkills.doctor;

                    if (isTagged) {
                        if (raisedSkills.doctor <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Doctor, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Doctor, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Sneak:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.sneak <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Sneak);

                    skillLevel = baseSkills.sneak + raisedSkills.sneak;

                    if (isTagged) {
                        if (raisedSkills.sneak <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Sneak, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Sneak, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Lockpick:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.lockpick <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Lockpick);

                    skillLevel = baseSkills.lockpick + raisedSkills.lockpick;

                    if (isTagged) {
                        if (raisedSkills.lockpick <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Lockpick, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Lockpick, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Steal:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.steal <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Steal);

                    skillLevel = baseSkills.steal + raisedSkills.steal;

                    if (isTagged) {
                        if (raisedSkills.steal <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Steal, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Steal, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Traps:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.traps <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Traps);

                    skillLevel = baseSkills.traps + raisedSkills.traps;

                    if (isTagged) {
                        if (raisedSkills.traps <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Traps, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Traps, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Science:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.science <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Science);

                    skillLevel = baseSkills.science + raisedSkills.science;

                    if (isTagged) {
                        if (raisedSkills.science <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Science, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Science, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Repair:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.repair <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Repair);

                    skillLevel = baseSkills.repair + raisedSkills.repair;

                    if (isTagged) {
                        if (raisedSkills.repair <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Repair, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Repair, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Speech:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.speech <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Speech);

                    skillLevel = baseSkills.speech + raisedSkills.speech;

                    if (isTagged) {
                        if (raisedSkills.speech <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Speech, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Speech, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Barter:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.barter <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Barter);

                    skillLevel = baseSkills.barter + raisedSkills.barter;

                    if (isTagged) {
                        if (raisedSkills.barter <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Barter, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Barter, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Gambling:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.gambling <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Gambling);

                    skillLevel = baseSkills.gambling + raisedSkills.gambling;

                    if (isTagged) {
                        if (raisedSkills.gambling <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Gambling, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Gambling, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;

                case PlayerSkillNames.Outdoorsman:

                    // Prevent lowering beyond 0.

                    if (raisedSkills.outdoorsman <= 0) {
                        return;
                    }

                    // Tagged skills grow double.

                    isTagged = taggedSkills.find((tag) => tag === PlayerSkillNames.Outdoorsman);

                    skillLevel = baseSkills.outdoorsman + raisedSkills.outdoorsman;

                    if (isTagged) {
                        if (raisedSkills.outdoorsman <= 1) {
                            return;
                        }

                        skillLevel -= 2;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Outdoorsman, amount: 2 })
                    } else {
                        skillLevel -= 1;

                        raisedSkillsDispatch({ type: "decrease", skillName: PlayerSkillNames.Outdoorsman, amount: 1 })
                    }

                    skillCost = getSkillCost(skillLevel);

                    setSkillPoints(skillPoints => skillPoints + skillCost);

                    break;
            }
        }
    };

    const handleTagClick = (event: MouseEvent<HTMLButtonElement>) => {
        let skillName = event.currentTarget.getAttribute("data-name")!;

        if (!skillName) { return; }

        // Check tagged skills for the skill.

        const index = taggedSkills.findIndex((taggedSkill) => taggedSkill === skillName);

        if (index !== -1) {

            // Prevent already tagged skills being removed with Tag! perk.

            if (taggedSkills.length === 3 && playerLevel > 1) {
                return;
            }

            // Skill is already tagged, remove the tag.

            setTaggedSkills(taggedSkills => [
                ...taggedSkills.slice(0, index),
                ...taggedSkills.slice(index + 1)
            ])

            setBaseSkills(baseSkills => Object.assign({}, calculateBaseSkills(primaryStats, traits, taggedSkills, playersPerks, difficulty)));

            // Refund a tag point.

            setTagPoints(tagPoints => tagPoints + 1);

            return;
        }

        // Max tags 3.

        if (taggedSkills.length >= 3 && playerLevel === 1) {
            return;
        }

        // Add a skill tag.

        setTaggedSkills(taggedSkills => [
            ...taggedSkills, skillName
        ]);

        // Spend a tag point.

        setTagPoints(tagPoints => tagPoints - 1)

        setBaseSkills(baseSkills => Object.assign({}, calculateBaseSkills(primaryStats, traits, taggedSkills, playersPerks, difficulty)));

        forceRender(bool => !bool);
    }

    const handleTraitClick = (event: MouseEvent<HTMLDivElement>) => {
        handleTooltipClick(event);

        // Prevent changing traits after level 1
        // and without the Mutate! perk selected.

        // Get the Mutate! perk

        const mutate = playersPerks.find((perk) => perk.name === PerkNames.mutate);

        if (mutate) {
            // Check the rank of the Mutate! perk.

            if (playerLevel > 1 && mutate.ranks === 0) { return; }
        }

        let traitName = event.currentTarget.getAttribute("data-name");

        // DOM can be manipulated.

        if (!traitName) { return; }

        let selectedTraits: ITrait[] = [];

        // Find the trait to be added to the selected traits from all the traits.

        const trait = TRAITS.find(trait => trait.name === traitName);

        if (!trait) { return; }

        // Check if the trait already exists in the character's traits.

        const found = traits.find(element => trait.name === element.name);

        if (found) {

            // Remove the primary stat effects.

            if (trait.name === TraitNames.smallFrame) {
                primaryStatsDispatch({ type: "small frame", payload: "remove", traits: traits });
            }

            if (trait.name === TraitNames.gifted) {
                primaryStatsDispatch({ type: "gifted", payload: "remove", traits: traits });
            }

            if (trait.name === TraitNames.bruiser) {
                primaryStatsDispatch({ type: "bruiser", payload: "remove", traits: traits });
            }

            // Remove the trait from the character's traits.

            setTraits(traits => traits.filter(trait => trait.name !== traitName));
        }

        if (!found) {
            // Limit the maximum selected traits to 2.

            if (traits.length >= 2) { return; };

            // Combine the selected traits with existing traits to a new array.

            selectedTraits = selectedTraits.concat(traits);

            // Add the new trait into the selected traits.

            selectedTraits.push(trait);

            // Primary stats effects.

            if (trait.name === TraitNames.smallFrame) {
                primaryStatsDispatch({ type: "small frame", payload: "add", traits: selectedTraits });
            }

            if (trait.name === TraitNames.gifted) {
                primaryStatsDispatch({ type: "gifted", payload: "add", traits: traits });
            }

            if (trait.name === TraitNames.bruiser) {
                primaryStatsDispatch({ type: "bruiser", payload: "add", traits: traits });
            }

            setTraits(traits => selectedTraits);
        }
    }

    const handlePrimaryStatClick = (event: MouseEvent) => {
        if (playerLevel > 1) { return };

        const type: string = event.currentTarget.getAttribute("data-type")!;

        const payload: string = event.currentTarget.getAttribute("data-payload")!;

        if (type === undefined || payload === undefined) {
            return;
        }

        const action: IPrimaryStatsAction = { type: type, payload: payload, traits: traits };

        primaryStatsDispatch(action);
    }

    // Called when user clicks an available perk.

    // Try to add a rank to the perk in the character's perks
    // and remove a rank from the perk in the available perks.

    const handleAvailablePerkClick = (event: MouseEvent) => {
        const perkName = event.currentTarget.getAttribute("data-perk-name")!;

        if (!perkName) { return; }

        const requirementsMet = event.currentTarget.getAttribute("data-requirements-met");

        if (!requirementsMet) { return; }

        const tooltip = TOOLTIPS.find(tooltip => tooltip.name === perkName);

        if (tooltip) {
            setTooltipHeading(heading => tooltip.heading);

            setTooltipSubHeading(subHeading => tooltip.subHeading);

            setTooltipBody(body => tooltip.body);
        }

        if (requirementsMet === "false") { return; }

        // No perk points. Some perks such as zeta scan are not gained by leveling up and do not require perk points.

        if (perkPoints <= 0
            && perkName !== PerkNames.zetaScan
            && perkName !== PerkNames.vaultCityTraining
            && perkName !== PerkNames.vaultCityInoculations) {
            return;
        }

        const index = availablePerks.findIndex((availablePerk) => availablePerk.name === perkName);

        if (index === -1) { return; }

        // Remove a rank from the perk in the available perks.

        const removeAction: IAvailablePerksAction = { type: "remove", perkName: perkName }

        availablePerksDispatch(removeAction);

        // Add a rank to the perk in the character's perks.

        const addAction: IPlayersPerksAction = { type: "add", perkName: perkName, primaryStats: primaryStats, playerLevel: playerLevel }

        playersPerksDispatch(addAction);

        // Some perks such as zeta scan are not gained by leveling up and do not require perk points.

        if (perkName !== PerkNames.zetaScan
            && perkName !== PerkNames.vaultCityTraining
            && perkName !== PerkNames.vaultCityInoculations) {
            setPerkPoints(perkPoints => perkPoints - 1);
        }

        // Choosing a here and now perk grants an immediate character level.

        if (perkName === PerkNames.hereAndNow) { levelUp(); }

        // Choosing the Tag! perk grants a tag point.

        if (perkName === PerkNames.tag) {
            setTagPoints(tagPoint => tagPoint + 1);
        }

        // Gain primary stat perks increase a primary stat.

        if (perkName.includes("Gain")) {
            let primaryStatsAction: IPrimaryStatsAction = { type: "gainPerk", payload: "add", gainPrimaryStatPerk: perkName, traits: traits };

            primaryStatsDispatch(primaryStatsAction);
        }

        // Zeta scan effects.

        if (perkName === PerkNames.zetaScan) {

            if (primaryStats.luck < 9) {

                // If luck is under 9, zeta scan increases luck by 2.

                const increaseLuck: IPrimaryStatsAction = { type: "zetaScan", payload: "add", zetaScanAmount: 2, traits: traits };

                primaryStatsDispatch(increaseLuck);
            }
            
            else if (primaryStats.luck === 9) {

                // If luck is 9, increase luck by 1.

                const increaseLuck: IPrimaryStatsAction = { type: "zetaScan", payload: "add", zetaScanAmount: 1, traits: traits };

                primaryStatsDispatch(increaseLuck);
        
            } 

            // If luck is 10, do nothing.
        }

    }

    // Called when user clicks a selected perk.

    const handlePlayersPerkClick = (event: MouseEvent) => {
        const perkName = event.currentTarget.getAttribute("data-perk-name")!;

        if (perkName === undefined) { return; }

        // Prevent certain perks from being removed.

        // Enabling the removing of these perks while maintaining the integrity 
        // of the app would require implementing a lot of logic.

        // Perhaps implement a saving of a "snapshot" of the state of the primary stats, traits, level, skills, tags and perks
        // to return to on perk removal.

        if (perkName === PerkNames.hereAndNow ||
            perkName === PerkNames.tag ||
            perkName === PerkNames.mutate) {
            return;
        }

        // Find the index of the perk in the player's perks.

        const index = playersPerks.findIndex((playersPerk) => playersPerk.name === perkName);

        if (index === -1) { return; }

        // If the perk is zeta scan.

        if (perkName === PerkNames.zetaScan) {
            if (playersPerks[index].baseValue) {

                // Check the base value of luck before the perk was selected.

                if (playersPerks[index].baseValue! < 9) {

                    const decreaseLuck: IPrimaryStatsAction = { type: "zetaScan", payload: "remove", zetaScanAmount: 2, traits: traits };

                    // Decrease luck by 2.

                    primaryStatsDispatch(decreaseLuck);
                }

                else if (playersPerks[index].baseValue! === 9) {

                    // Decrease luck by 1.

                    const decreaseLuck: IPrimaryStatsAction = { type: "zetaScan", payload: "remove", zetaScanAmount: 1, traits: traits };

                    primaryStatsDispatch(decreaseLuck);
                }

                // If the base luck was 10, do nothing.
            }

        }

        // Remove a rank from the perk in the character's perks.

        const removeAction: IPlayersPerksAction = { type: "remove", perkName: perkName, primaryStats: primaryStats, playerLevel: playerLevel }

        playersPerksDispatch(removeAction);

        // Add a rank to the perk in the available perks.

        const addAction: IAvailablePerksAction = { type: "add", perkName: perkName }

        availablePerksDispatch(addAction);

        // Refund a perk point.

        // Some perks such as zeta scan are not gained by leveling up and do not require perk points so do not refund perk points.

        if (perkName !== PerkNames.zetaScan
            && perkName !== PerkNames.vaultCityTraining
            && perkName !== PerkNames.vaultCityInoculations) {
            setPerkPoints(perkPoints => perkPoints + 1);
        }

        // "Gain"-perks, such as Gain strength, increase a primary stat.
        // Removing the "Gain"-perk decreases a primary stat.

        if (perkName.includes("Gain")) {
            let primaryStatsAction: IPrimaryStatsAction = { type: "gainPerk", payload: "remove", gainPrimaryStatPerk: perkName, traits: traits };

            primaryStatsDispatch(primaryStatsAction);
        }
    }

    // Create and download a text file containing character's primary stats, traits and perks.

    const handlePrintClick = () => {
        // Get primary stats, traits and perks in printable form.

        const printablePrimaryStats = getPrintablePrimaryStats(primaryStats);

        const printableTraits = getPrintableTraits(traits);

        const printablePerks = getPrintablePerks(playersPerks);

        // Create downloadable file.

        const blob = new Blob([printablePrimaryStats, printableTraits, printablePerks], { type: "text/plain;charset=utf-8", endings: "native" });

        const fileDownloadUrl = URL.createObjectURL(blob);

        // Create an anchor element used for download.

        let element = document.createElement("a");

        element.setAttribute("href", fileDownloadUrl);

        element.style.display = "none";

        // Use a date in naming the text file.

        const date = new Date();

        const timestamp = date.toDateString();

        let fileName = "fallout_2_character-" + timestamp + ".txt";

        fileName = fileName.toLowerCase().replaceAll(" ", "_");

        element.setAttribute("download", fileName)

        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }

    // Called when user clicks a primary stat, trait, derived stat, perk or skill to provide information.

    // Find the tooltip by name from all the tooltips and update the state.

    const handleTooltipClick = (event: MouseEvent) => {
        const name = event.currentTarget.getAttribute("data-tooltip");

        if (!name) { return; }

        // Find a tooltip for specific item

        const tooltip = TOOLTIPS.find(tooltip => tooltip.name === name);

        if (!tooltip) { return; }

        setTooltipHeading(heading => tooltip.heading);

        setTooltipSubHeading(subHeading => tooltip.subHeading);

        setTooltipBody(body => tooltip.body);
    }

    /**
     * Change the difficulty setting.
     * @param event the mouse event when the user clicks the SVG element.
     */

    const handleDifficultyClick = (event: MouseEvent) => {
        if (difficulty === Difficulty.normal && difficultyDirection) {
            setDifficulty(difficulty => Difficulty.hard);
        }

        if (difficulty === Difficulty.hard) {
            setDifficulty(difficulty => Difficulty.normal);
            setDifficultyDirection(direction => !direction);
        }

        if (difficulty === Difficulty.normal && !difficultyDirection) {
            setDifficulty(difficulty => Difficulty.easy);
        }

        if (difficulty === Difficulty.easy) {
            setDifficulty(difficulty => Difficulty.normal);
            setDifficultyDirection(direction => !direction);
        }
    }

    const handleResetClick = (event: MouseEvent) => {
        setplayerLevel(1);

        setTagPoints(3);

        setTaggedSkills([]);

        setPerkPoints(0);

        // Reset all the character's perks.

        const playersPerksAction: IPlayersPerksAction = { type: "reset", perkName: "", playerLevel: 1, primaryStats: primaryStats };

        playersPerksDispatch(playersPerksAction);

        // Reset all the available perks.

        const availablePerksAction: IAvailablePerksAction = { type: "reset", perkName: "" };

        availablePerksDispatch(availablePerksAction);

        // Remove all traits.

        setTraits([]);

        // Set primary stats to 5. Set primary stat points to 5.

        const primaryStatsAction: IPrimaryStatsAction = { type : "reset", payload: "", traits: traits }

        primaryStatsDispatch(primaryStatsAction);

        // Set raised skills to 0.

        const raisedSkillsAction: IRaisedSkillsAction = { type: "reset", skillName: "", amount: 0 };

        raisedSkillsDispatch(raisedSkillsAction);
    }

    // Base skills and derived stats are calculated from primary stats, traits, perks and tagged skills.

    // Re-calculate on change.

    useEffect(() => {
        setBaseSkills(baseSkills => Object.assign({}, calculateBaseSkills(primaryStats, traits, taggedSkills, playersPerks, difficulty)));

        setDerivedStats(derivedStats => Object.assign({}, calculateDerivedStats(primaryStats, traits, playersPerks)));

        forceRender(bool => !bool);
    }, [primaryStats, traits, playersPerks, taggedSkills, difficulty]);

    return (

        <div className="grid-container" id="App">
            
            <div className="flex-container">
                <PrimaryStats
                    primaryStats={primaryStats}
                    playerLevel={playerLevel}
                    handleClick={handlePrimaryStatClick}
                    handleTooltipClick={handleTooltipClick}
                    handlePlayerLevelUpClick={handlePlayerLevelUpClick}></PrimaryStats>
                <DerivedStats
                    derivedStats={derivedStats}
                    playersPerks={playersPerks}
                    traits={traits}
                    onClick={handleTooltipClick}>
                </DerivedStats>
                <PlayerSkills baseSkills={baseSkills}
                    raisedSkills={raisedSkills}
                    handleTagClick={handleTagClick}
                    handleSkillValueClick={handleSkillValueClick}
                    playerLevel={playerLevel}
                    skillPoints={skillPoints}
                    taggedSkills={taggedSkills}
                    tagPoints={tagPoints}
                    handleTooltipClick={handleTooltipClick}>
                </PlayerSkills>
                <Traits handleClick={handleTraitClick} traits={traits}></Traits>
                <Perks playersPerks={playersPerks}
                    availablePerks={availablePerks}
                    perkPoints={perkPoints}
                    playerLevel={playerLevel}
                    primaryStats={primaryStats}
                    baseSkills={baseSkills}
                    raisedSkills={raisedSkills}
                    handleAvailablePerkClick={handleAvailablePerkClick}
                    handlePlayersPerkClick={handlePlayersPerkClick}>
                </Perks>
            </div>

            <Footer
                difficulty={difficulty}
                tooltipHeading={tooltipHeading}
                tooltipSubHeading={tooltipSubHeading}
                tooltipBody={tooltipBody}
                handleDifficultyClick={handleDifficultyClick}
                handlePrintClick={handlePrintClick}
                handleResetClick={handleResetClick}>
            </Footer>

        </div>

    );
}

export default App;