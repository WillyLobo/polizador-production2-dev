import React, { MouseEventHandler } from "react";
import { IPerk } from "../models";

interface IPlayerPerksProps {
    playersPerks: IPerk[],
    handlePlayerPerkClick: MouseEventHandler<HTMLDivElement>
}

export default function PlayersPerks({ playersPerks, handlePlayerPerkClick }: IPlayerPerksProps): JSX.Element {
    // Sort player's perks by the earliest level selected

    const sortedPlayersPerks = playersPerks.sort(function (a, b) { return a.levelSelected[0] ? a.levelSelected[0] - b.levelSelected[0] : 1 });

    return (
        <div className="players-perks">
            <div className="players-perks-heading">
                <h3>Selected perks</h3>
            </div>
            
            <div className="players-perks-list">

                {
                    // Go through the player's perks

                    sortedPlayersPerks.map((perk, perksIndex) => {
                        let jsx: JSX.Element[] | null = null;

                        // Only render selected perks

                        if (perk.ranks > 0) {

                            // Render all the levels of the perk

                            jsx = perk.levelSelected.map((levelSelected, index) => {
                                return <div key={index} className="level-selected">Level {levelSelected.toString()}</div>
                            })

                            jsx.push(<div key={perk.name} onClick={handlePlayerPerkClick} data-perk-name={perk.name}>{perk.name + " " + perk.ranks.toString()}</div>)

                            return <div key={perksIndex}>{jsx}</div>;
                        }

                        return jsx;
                    })
                }

            </div>
        </div>
    )
}