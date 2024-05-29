import React, { MouseEventHandler } from "react";

interface ISkillProps {
    children?: React.ReactNode,
    skillName: string,
    value: number,
    taggedSkills: string[],
    handleTooltipClick:  MouseEventHandler<HTMLDivElement>
}

export default function PlayerSkill({ skillName, value, taggedSkills, handleTooltipClick }: ISkillProps): JSX.Element {
    return (
        <div className="skill" data-tooltip={skillName} onClick={handleTooltipClick}>
            {taggedSkills.find((taggedSkill) => taggedSkill === skillName) ? // Render tagged skill white
                <>
                    <span className="skill-name tagged">{skillName}</span>
                    <span className="skill-value tagged">{value.toString() + "%"}</span>
                </>
                :
                <>
                    <span className="skill-name">{skillName}</span>
                    <span className="skill-value">{value.toString() + "%"}</span>
                </>}
        </div>
    )
}