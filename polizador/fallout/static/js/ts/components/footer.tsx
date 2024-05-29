import React, { MouseEventHandler } from "react";
import { Difficulty } from "../models";
import Tooltip from "./tooltip";

interface IFooterProps {
    tooltipHeading: string,
    tooltipSubHeading: string,
    tooltipBody: string,
    difficulty: string,
    handlePrintClick: MouseEventHandler<HTMLButtonElement>,
    handleDifficultyClick: MouseEventHandler<SVGElement>,
    handleResetClick: MouseEventHandler<HTMLButtonElement>,
    children?: React.ReactNode
}
/**
 * Component fixed to the bottom of the screen, containing tooltip, difficulty settings and a button to print out the character.
 */

export default function Footer({ tooltipHeading, tooltipSubHeading, tooltipBody, difficulty, handleDifficultyClick, handlePrintClick, handleResetClick }: IFooterProps): JSX.Element {
    return (
        <div id="footer-container">
            <div id="footer">

                <Tooltip tooltipHeading={tooltipHeading} tooltipSubHeading={tooltipSubHeading} tooltipBody={tooltipBody}></Tooltip>

                <div className="utility-container">
                    <div className="difficulty-container">
                        <h4>Difficulty</h4>
                        <div className="difficulty-labels">
                            <span className="difficulty-easy">easy</span>
                            <span className="difficulty-normal">normal</span>
                            <span className="difficulty-hard">hard</span>
                        </div>

                        {
                            difficulty === Difficulty.easy ?
                                <svg id="knob-container" style={{ "transform": "rotate(-45deg)" }} onClick={handleDifficultyClick}>
                                    <circle id="knob" cx="25" cy="25" r="15"></circle>
                                    <line id="knob-line" x1="25" y1="24" x2="25" y2="11"></line>
                                </svg> : null
                        } {
                            difficulty === Difficulty.normal ?
                                <svg id="knob-container" onClick={handleDifficultyClick}>
                                    <circle id="knob" cx="25" cy="25" r="15"></circle>
                                    <line id="knob-line" x1="25" y1="24" x2="25" y2="11"></line>
                                </svg> : null
                        } {
                            difficulty === Difficulty.hard ?
                                <svg id="knob-container" style={{ "transform": "rotate(45deg)" }} onClick={handleDifficultyClick}>
                                    <circle id="knob" cx="25" cy="25" r="15"></circle>
                                    <line id="knob-line" x1="25" y1="24" x2="25" y2="11"></line>
                                </svg> : null
                        }
                    </div>

                    <div className="print-button-container">
                        <button onClick={handlePrintClick}></button>
                        <div>Print</div>
                    </div>

                    <div className="reset-button-container">
                        <div>
                            <div>Reset</div>
                        </div>
                        <button onClick={handleResetClick}></button>
                    </div>
                </div>
            </div>
        </div>
    )
}