import React, { MouseEventHandler } from "react";
import { IDerivedStats, IPerk, ITrait, DerivedStatsNames } from "../models";

interface IDerivedStatsProps {
    derivedStats: IDerivedStats,
    playersPerks: IPerk[],
    children?: React.ReactNode,
    traits: ITrait[],
    onClick: MouseEventHandler<HTMLDivElement>
}

function addTrailingPercentSign(value: number | string): string {
    if (typeof value === "number") {
        return value.toString() + "%";
    }

    if (typeof value === "string") {
        return value + "%";
    }

    return "";
}

export default function DerivedStats({ derivedStats, playersPerks, traits, onClick }: IDerivedStatsProps): JSX.Element {
    return (
        <div className="derived-stats">
            <h3> Defensive stats</h3>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.hitPoints}><span className="derived-stat-name">Hit points</span><span className="derived-stat-value">{derivedStats.hitPoints}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.armorClass}><span className="derived-stat-name">Armor class</span><span className="derived-stat-value">{derivedStats.armorClass}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.damageResistance}><span className="derived-stat-name">Damage resistance</span><span className="derived-stat-value">{addTrailingPercentSign(derivedStats.damageResistance)}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.poisonResistance}><span className="derived-stat-name">Poison resistance</span><span className="derived-stat-value">{addTrailingPercentSign(derivedStats.poisonResistance)}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.radiationResistance}><span className="derived-stat-name">Radiation resistance</span><span className="derived-stat-value">{addTrailingPercentSign(derivedStats.radiationResistance)}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.healingRate}><span className="derived-stat-name">Healing rate</span><span className="derived-stat-value">{derivedStats.healingRate.toFixed(2)}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.hitPointsPerLevel}><span className="derived-stat-name">Hit points per level</span><span className="derived-stat-value">{derivedStats.hitPointsPerLevel}</span></div>
            <h3> Offensive stats</h3>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.actionPoints}><span className="derived-stat-name">Action points</span><span className="derived-stat-value">{derivedStats.actionPoints}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.criticalChance}><span className="derived-stat-name">Critical chance</span><span className="derived-stat-value">{addTrailingPercentSign(derivedStats.criticalChance)}</span></div>
            
            {
                derivedStats.criticalDamageModifier < 0 ?
                    <div onClick={onClick} data-tooltip={DerivedStatsNames.criticalDamageModifier}><span className="derived-stat-name">Critical damage modifier</span><span className="derived-stat-value bad">{addTrailingPercentSign(derivedStats.criticalDamageModifier)}</span></div>
                    :
                    <div onClick={onClick} data-tooltip={DerivedStatsNames.criticalDamageModifier}><span className="derived-stat-name">Critical damage modifier</span><span className="derived-stat-value">{addTrailingPercentSign(derivedStats.criticalDamageModifier)}</span></div>
            }

            {
                derivedStats.enemyDamageResistanceModifier === 0 ?
                    <div onClick={onClick} data-tooltip={DerivedStatsNames.enemyDamageResistanceModifier}><span className="derived-stat-name">Enemy damage resistance modifier</span><span className="derived-stat-value">{addTrailingPercentSign(derivedStats.enemyDamageResistanceModifier)}</span></div>
                    :
                    <div onClick={onClick} data-tooltip={DerivedStatsNames.enemyDamageResistanceModifier}><span className="derived-stat-name">Enemy damage resistance modifier</span><span className="derived-stat-value bad">{"+" + addTrailingPercentSign(derivedStats.enemyDamageResistanceModifier)}</span></div>
            }

            <div onClick={onClick} data-tooltip={DerivedStatsNames.meleeDamage}><span className="derived-stat-name">Melee damage</span><span className="derived-stat-value">{derivedStats.meleeDamage}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.sequence}><span className="derived-stat-name">Sequence</span><span className="derived-stat-value">{derivedStats.sequence}</span></div>
            
            <h3> Miscanellous stats</h3>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.carryWeight}><span className="derived-stat-name">Carry weight</span><span className="derived-stat-value">{derivedStats.carryWeight}</span></div>

            {
                derivedStats.perkRate > 3 ?
                    <div onClick={onClick} data-tooltip={DerivedStatsNames.perkRate}><span className="derived-stat-name">Perk rate</span><span className="derived-stat-value bad">{derivedStats.perkRate}</span></div>
                    :
                    <div onClick={onClick} data-tooltip={DerivedStatsNames.perkRate}><span className="derived-stat-name">Perk rate</span><span className="derived-stat-value">{derivedStats.perkRate}</span></div>
            }

            <div onClick={onClick} data-tooltip={DerivedStatsNames.skillRate}><span className="derived-stat-name">Skill rate</span><span className="derived-stat-value">{derivedStats.skillRate}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.partyLimit}><span className="derived-stat-name">Party limit</span><span className="derived-stat-value">{derivedStats.partyLimit}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.chemAddictionChance}><span className="derived-stat-name">Chem addiction chance</span><span className="derived-stat-value">{derivedStats.chemAddictionChance + "x"}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.chemAddictionRecovery}><span className="derived-stat-name">Chem addiction recovery</span><span className="derived-stat-value">{derivedStats.chemAddictionRecovery + "x"}</span></div>
            <div onClick={onClick} data-tooltip={DerivedStatsNames.chemDuration}><span className="derived-stat-name">Chem duration</span><span className="derived-stat-value">{derivedStats.chemDuration + "x"}</span></div>
        </div>
    );
}