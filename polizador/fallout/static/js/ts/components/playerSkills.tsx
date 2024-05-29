import React, { MouseEventHandler, ReactNode } from "react";
import { calculateFinalSkills } from "../calculateFinalSkills";
import { IPlayerSkills, PlayerSkillNames } from "../models";
import PlayerSkill from "./playerSkill";

interface IFinalSkillsProps {
    children?: ReactNode,
    baseSkills: IPlayerSkills,
    raisedSkills: IPlayerSkills,
    handleTagClick: MouseEventHandler<HTMLButtonElement>,
    handleSkillValueClick: MouseEventHandler<HTMLButtonElement>,
    handleTooltipClick: MouseEventHandler<HTMLDivElement>
    playerLevel: number,
    skillPoints: number,
    tagPoints: number,
    taggedSkills: string[]
}

export default function PlayerSkills({ baseSkills, raisedSkills, skillPoints, playerLevel, taggedSkills, tagPoints, handleTagClick, handleSkillValueClick, handleTooltipClick }: IFinalSkillsProps): JSX.Element {

    const finalSkills = calculateFinalSkills(baseSkills, raisedSkills);

    return (
        <div className="skills-container">
            <h3>Skills</h3>

            <div className="skills">

                <div className="tag-buttons">
                    {playerLevel === 1 || taggedSkills.length === 4 || tagPoints > 0 ? // Only render tag button on level 1, 4 tagged skills or tag points over 0
                        Object.values(PlayerSkillNames).map((skillName) =>
                            <div className="tag-button-container" key={skillName}>
                                <button data-name={skillName} onClick={handleTagClick}>-</button>
                            </div>)
                        :
                        <></>}
                </div>

                <div className="skill-values">
                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.SmallGuns}
                        value={finalSkills.smallGuns}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.BigGuns}
                        value={finalSkills.bigGuns}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.EnergyWeapons}
                        value={finalSkills.energyWeapons}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Unarmed}
                        value={finalSkills.unarmed}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.MeleeWeapons}
                        value={finalSkills.meleeWeapons}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Throwing}
                        value={finalSkills.throwing}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.FirstAid}
                        value={finalSkills.firstAid}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Doctor}
                        value={finalSkills.doctor}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Sneak}
                        value={finalSkills.sneak}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Lockpick}
                        value={finalSkills.lockpick}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Steal}
                        value={finalSkills.steal}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Traps}
                        value={finalSkills.traps}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Science}
                        value={finalSkills.science}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Repair}
                        value={finalSkills.repair}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Speech}
                        value={finalSkills.speech}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Barter}
                        value={finalSkills.barter}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Gambling}
                        value={finalSkills.gambling}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <PlayerSkill
                        handleTooltipClick={handleTooltipClick}
                        skillName={PlayerSkillNames.Outdoorsman}
                        value={finalSkills.outdoorsman}
                        taggedSkills={taggedSkills}>
                    </PlayerSkill>

                    <div className="skill skill-points">
                        <span className="skill-points-text">Skill points</span>
                        <span className="skill-points-value">{skillPoints}</span>
                    </div>

                    <div className="skill tag-points">
                        <span className="tag-points-text">Tag points</span>
                        <span className="tag-points-value">{tagPoints}</span>
                    </div>
                </div>
                <div className="skill-buttons">
                    {playerLevel > 1 ? // Only render skill buttons when over level 1
                        Object.values(PlayerSkillNames).map((skillName) =>
                            <div className="skill-button-container" key={skillName}>
                                <button className="skill-button" data-skill-name={skillName} data-action="increase" onClick={handleSkillValueClick}>+</button>
                                <button className="skill-button" data-skill-name={skillName} data-action="decrease" onClick={handleSkillValueClick}>-</button>
                            </div>)
                        :
                        <></>}
                </div>
            </div>
        </div>
    )
}