import { getDefaultPlayerSkills, IPlayerSkills } from "./models";

/**
 * Calculates the final skills
 */

export function calculateFinalSkills(baseSkills: IPlayerSkills, raisedSkills: IPlayerSkills) : IPlayerSkills {
    let newFinalSkills: IPlayerSkills = getDefaultPlayerSkills();

    newFinalSkills.smallGuns = baseSkills.smallGuns + raisedSkills.smallGuns;
    newFinalSkills.bigGuns = baseSkills.bigGuns + raisedSkills.bigGuns;
    newFinalSkills.energyWeapons = baseSkills.energyWeapons + raisedSkills.energyWeapons;
    newFinalSkills.unarmed = baseSkills.unarmed + raisedSkills.unarmed;
    newFinalSkills.meleeWeapons = baseSkills.meleeWeapons + raisedSkills.meleeWeapons;
    newFinalSkills.throwing = baseSkills.throwing + raisedSkills.throwing;
    newFinalSkills.firstAid = baseSkills.firstAid + raisedSkills.firstAid;
    newFinalSkills.doctor = baseSkills.doctor + raisedSkills.doctor;
    newFinalSkills.sneak = baseSkills.sneak + raisedSkills.sneak;
    newFinalSkills.lockpick = baseSkills.lockpick + raisedSkills.lockpick;
    newFinalSkills.steal = baseSkills.steal + raisedSkills.steal;
    newFinalSkills.traps = baseSkills.traps + raisedSkills.traps;
    newFinalSkills.repair = baseSkills.repair + raisedSkills.repair;
    newFinalSkills.science = baseSkills.science + raisedSkills.science;
    newFinalSkills.speech = baseSkills.speech + raisedSkills.speech;
    newFinalSkills.barter = baseSkills.barter + raisedSkills.barter;
    newFinalSkills.gambling = baseSkills.gambling + raisedSkills.gambling;
    newFinalSkills.outdoorsman = baseSkills.outdoorsman + raisedSkills.outdoorsman;

    return newFinalSkills;
}