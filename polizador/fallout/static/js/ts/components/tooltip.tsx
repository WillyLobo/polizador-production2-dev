import React from "react";

interface ITooltipProps {
    tooltipHeading: string,
    tooltipSubHeading: string,
    tooltipBody: string,
}

/**
 * Component displaying information about clicked primary stat, trait, derived stat, skill or perk.
 */

export default function Tooltip({ tooltipHeading, tooltipSubHeading, tooltipBody }: ITooltipProps): JSX.Element {
    return (
        <div className="tooltip">
            <div className="tooltip-display">
                <h2>{tooltipHeading}</h2>
                {tooltipSubHeading.length > 0 ? <span>{tooltipSubHeading}</span> : <span>&nbsp;</span>}
                <hr></hr>
                <p>{tooltipBody}</p>
            </div>
        </div>
    )
}