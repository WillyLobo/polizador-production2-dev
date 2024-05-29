import React, { ReactNode, MouseEventHandler } from "react";
import { IPerk, IPlayerSkills, IPrimaryStats } from "../models";
import PlayersPerks from "./playersPerks";
import setAvailablePerks from "../setAvailablePerks";
import { calculateFinalSkills } from "../calculateFinalSkills";

interface IPerksProps {
    children?: ReactNode,
    playersPerks: IPerk[],
    availablePerks: IPerk[],
    perkPoints: number,
    playerLevel: number,
    primaryStats: IPrimaryStats,
    baseSkills: IPlayerSkills,
    raisedSkills: IPlayerSkills,
    handlePlayersPerkClick: MouseEventHandler<HTMLDivElement>,
    handleAvailablePerkClick: MouseEventHandler<HTMLDivElement>
}

export default function Perks({ playersPerks, availablePerks, perkPoints, playerLevel, primaryStats, baseSkills, raisedSkills, handlePlayersPerkClick, handleAvailablePerkClick }: IPerksProps): JSX.Element {
    const finalSkills = calculateFinalSkills(baseSkills, raisedSkills);

    const offeredPerks = setAvailablePerks(availablePerks, primaryStats, finalSkills, playerLevel);

    return (
        <div className="perks">
            <PlayersPerks playersPerks={playersPerks} handlePlayerPerkClick={handlePlayersPerkClick}></PlayersPerks>
            <div className="available-perks">
                <div className="available-perks-heading">
                    <h3>Available perks</h3>
                    <span className="perk-points-heading">Perk points</span>
                    <span className="perk-points">{perkPoints.toString()}</span>
                </div>
                <div className="available-perks-list">
                {
                    offeredPerks.map((perk, index) => {
                        let jsx;

                        // Only render perks with ranks left.

                        (perk.ranks > 0) ?

                            // Render perks where requirements are not met dark green.

                            perk.requirementsMet ?
                                jsx = <div key={index} onClick={handleAvailablePerkClick} data-perk-name={perk.name} data-requirements-met={"true"}>{perk.name} {perk.ranks}</div>
                                :
                                jsx = <div key={index} className="unavailable-perk" onClick={handleAvailablePerkClick} data-perk-name={perk.name} data-requirements-met={"false"}>{perk.name} {perk.ranks}</div>
                            :
                            jsx = null;

                        return jsx;
                    })
                }
                </div>
            </div>

            
        </div>
    )
}