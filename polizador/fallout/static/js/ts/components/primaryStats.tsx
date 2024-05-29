import React, { MouseEventHandler } from "react";
import { IPrimaryStats, PrimaryStatNames } from "../models";

// Primary stats have a matching flavor text.

function getFlavorText(value: number): string {
    let text: string;

    switch (value) {
        case 1:
            text = "Very bad";
            break;
        case 2:
            text = "Bad";
            break;
        case 3:
            text = "Poor";
            break;
        case 4:
            text = "Fair";
            break;
        case 5:
            text = "Average";
            break;
        case 6:
            text = "Good";
            break;
        case 7:
            text = "Very good";
            break;
        case 8:
            text = "Great";
            break;
        case 9:
            text = "Excellent";
            break;
        case 10:
            text = "Heroic";
            break;
        case 11:
            text = "Heroic";
            break;
        case 12:
            text = "Heroic";
            break;
        case 13:
            text = "Heroic";
            break;
        default:
            text = "undefined";
            break;
    }

    return text;
}

// Add a leading zero to displayed value.

function formatPrimaryStat(primaryStat: number) : string {
    let valueToDisplay : string;

    if(primaryStat < 10) {
        valueToDisplay = "0" + primaryStat.toString();
    }
    else {
        valueToDisplay = primaryStat.toString()
    }

    return valueToDisplay;
}

/**
 * Returns experience points required for given level.
 * @param level character level.
 * @returns required experience points.
 */

function requiredExperience(level: number): number {
    let experience: number;

    switch (level) {
        case 0:
            experience = 0;
            break;
        case 1:
            experience = 0;
            break;
        case 2:
            experience = 1000;
            break;
        case 3:
            experience = 3000;
            break;
        case 4:
            experience = 6000;
            break;
        case 5:
            experience = 10000;
            break;
        case 6:
            experience = 15000;
            break;
        case 7:
            experience = 21000;
            break;
        case 8:
            experience = 28000;
            break;
        case 9:
            experience = 36000;
            break;
        case 10:
            experience = 45000;
            break;
        case 11:
            experience = 55000;
            break;
        case 12:
            experience = 66000;
            break;
        case 13:
            experience = 78000;
            break;
        case 14:
            experience = 91000;
            break;
        case 15:
            experience = 105000;
            break;
        case 16:
            experience = 120000;
            break;
        case 17:
            experience = 136000;
            break;
        case 18:
            experience = 153000;
            break;
        case 19:
            experience = 171000;
            break;
        case 20:
            experience = 190000;
            break;
        case 21:
            experience = 210000;
            break;
        default:
            experience = (level * (level - 1) / 2) * 1000;
    }

    return experience;
}

interface IPrimaryStatsProps {
    primaryStats: IPrimaryStats,
    handleClick: MouseEventHandler,
    handleTooltipClick: MouseEventHandler,
    playerLevel: number,
    handlePlayerLevelUpClick: MouseEventHandler
}

function PrimaryStats({primaryStats, playerLevel, handleClick, handleTooltipClick, handlePlayerLevelUpClick}: IPrimaryStatsProps) : JSX.Element {
    return (
        <div className="primary-stats">
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.strength} onClick={handleTooltipClick}>Strength</span>
                {primaryStats.strength > 10 ? // Render primary stats over 10 as red
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.strength)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.strength)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.strength)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="strength" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="strength" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div>
            </div>
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.perception} onClick={handleTooltipClick}>Perception</span>
                {primaryStats.perception > 10 ?
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.perception)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.perception)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.perception)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="perception" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="perception" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div></div>
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.endurance} onClick={handleTooltipClick}>Endurance</span>
                {primaryStats.endurance > 10 ?
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.endurance)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.endurance)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.endurance)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="endurance" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="endurance" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div></div>
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.charisma} onClick={handleTooltipClick}>Charisma</span>
                {primaryStats.charisma > 10 ?
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.charisma)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.charisma)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.charisma)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="charisma" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="charisma" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div></div>
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.intelligence} onClick={handleTooltipClick}>Intelligence</span>
                {primaryStats.intelligence > 10 ?
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.intelligence)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.intelligence)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.intelligence)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="intelligence" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="intelligence" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div></div>
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.agility} onClick={handleTooltipClick}>Agility</span>
                {primaryStats.agility > 10 ?
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.agility)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.agility)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.agility)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="agility" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="agility" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div></div>
            <div className="primary-stat">
                <span className="primary-stat-name" data-tooltip={PrimaryStatNames.luck} onClick={handleTooltipClick}>Luck</span>
                {primaryStats.luck > 10 ?
                    <span className="primary-stat-value invalid">{formatPrimaryStat(primaryStats.luck)}</span>
                    :
                    <span className="primary-stat-value">{formatPrimaryStat(primaryStats.luck)}</span>
                }
                <span className="primary-stat-flavor-text">{getFlavorText(primaryStats.luck)}</span>
                <div className="primary-stats-buttons">
                    <button data-payload="luck" data-type="increase" className="primary-stat-button" onClick={handleClick}>+</button>
                    <button data-payload="luck" data-type="decrease" className="primary-stat-button" onClick={handleClick}>-</button>
                </div></div>
            <div className="primary-stat unspent-stat-points"><span className="primary-stat-name unspent-stat-points">Unspent stat points</span><span className="primary-stat-value unspent-stat-points">{formatPrimaryStat(primaryStats.unspentPoints)}</span></div>
            <div className="level">
                <div className="level-display">
                    <span>Level {playerLevel}</span>
                    <span>Experience {requiredExperience(playerLevel).toLocaleString()}</span>
                </div>
                
                <div className="level-button-container">
                    <button className="level-button" onClick={handlePlayerLevelUpClick}>+</button>
                </div>
            </div>
        </div>
    )
}

export default PrimaryStats;