import React, { MouseEventHandler } from "react";
import { ITrait, TraitNames } from "../models";

interface ITraitsProps {
    traits: Array<ITrait>,
    handleClick: MouseEventHandler<HTMLDivElement>
}

export default function Traits({ traits, handleClick }: ITraitsProps): JSX.Element {
    return (
        <div className="traits-container">
            <h3>Traits</h3>
            <div className="traits">
                {traits.find((trait) => trait.name === "Bloody mess") ?
                    <div className="trait selected" data-name="Bloody mess" data-tooltip={TraitNames.bloodyMess} onClick={handleClick}>Bloody mess</div> :
                    <div className="trait" data-name="Bloody mess" data-tooltip={TraitNames.bloodyMess} onClick={handleClick}>Bloody mess</div>}

                {traits.find((trait) => trait.name === "Bruiser") ?
                    <div className="trait selected" data-name="Bruiser" data-tooltip={TraitNames.bruiser} onClick={handleClick}>Bruiser</div> :
                    <div className="trait" data-name="Bruiser" data-tooltip={TraitNames.bruiser} onClick={handleClick}>Bruiser</div>}

                {traits.find((trait) => trait.name === "Chem reliant") ?
                    <div className="trait selected" data-name="Chem reliant" data-tooltip={TraitNames.chemReliant} onClick={handleClick}>Chem reliant</div> :
                    <div className="trait" data-name="Chem reliant" data-tooltip={TraitNames.chemReliant} onClick={handleClick}>Chem reliant</div>}

                {traits.find((trait) => trait.name === "Chem resistant") ?
                    <div className="trait selected" data-name="Chem resistant" data-tooltip={TraitNames.chemResistant} onClick={handleClick}>Chem resistant</div> :
                    <div className="trait" data-name="Chem resistant" data-tooltip={TraitNames.chemResistant} onClick={handleClick}>Chem resistant</div>}

                {traits.find((trait) => trait.name === "Fast metabolism") ?
                    <div className="trait selected" data-name="Fast metabolism" data-tooltip={TraitNames.fastMetabolism} onClick={handleClick}>Fast metabolism</div> :
                    <div className="trait" data-name="Fast metabolism" data-tooltip={TraitNames.fastMetabolism} onClick={handleClick}>Fast metabolism</div>}

                {traits.find((trait) => trait.name === "Fast shot") ?
                    <div className="trait selected" data-name="Fast shot" data-tooltip={TraitNames.fastShot} onClick={handleClick}>Fast shot</div> :
                    <div className="trait" data-name="Fast shot" data-tooltip={TraitNames.fastShot} onClick={handleClick}>Fast shot</div>}

                {traits.find((trait) => trait.name === "Finesse") ?
                    <div className="trait selected" data-name="Finesse" data-tooltip={TraitNames.finesse} onClick={handleClick}>Finesse</div> :
                    <div className="trait" data-name="Finesse" data-tooltip={TraitNames.finesse} onClick={handleClick}>Finesse</div>}

                {traits.find((trait) => trait.name === "Gifted") ?
                    <div className="trait selected" data-name="Gifted" data-tooltip={TraitNames.gifted} onClick={handleClick}>Gifted</div> :
                    <div className="trait" data-name="Gifted" data-tooltip={TraitNames.gifted} onClick={handleClick}>Gifted</div>}

                {traits.find((trait) => trait.name === "Good natured") ?
                    <div className="trait selected" data-name={TraitNames.goodNatured} data-tooltip={TraitNames.goodNatured} onClick={handleClick}>Good natured</div> :
                    <div className="trait" data-name={TraitNames.goodNatured} data-tooltip={TraitNames.goodNatured} onClick={handleClick}>Good natured</div>}

                {traits.find((trait) => trait.name === "Heavy handed") ?
                    <div className="trait selected" data-name="Heavy handed" data-tooltip={TraitNames.heavyHanded} onClick={handleClick}>Heavy handed</div> :
                    <div className="trait" data-name="Heavy handed" data-tooltip={TraitNames.heavyHanded} onClick={handleClick}>Heavy handed</div>}

                {traits.find((trait) => trait.name === "Jinxed") ?
                    <div className="trait selected" data-name="Jinxed" data-tooltip={TraitNames.jinxed} onClick={handleClick}>Jinxed</div> :
                    <div className="trait" data-name="Jinxed" data-tooltip={TraitNames.jinxed} onClick={handleClick}>Jinxed</div>}

                {traits.find((trait) => trait.name === "Kamikaze") ?
                    <div className="trait selected" data-name="Kamikaze" data-tooltip={TraitNames.kamikaze} onClick={handleClick}>Kamikaze</div> :
                    <div className="trait" data-name="Kamikaze" data-tooltip={TraitNames.kamikaze} onClick={handleClick}>Kamikaze</div>}

                {traits.find((trait) => trait.name === "One hander") ?
                    <div className="trait selected" data-name="One hander" data-tooltip={TraitNames.oneHander} onClick={handleClick}>One hander</div> :
                    <div className="trait" data-name="One hander" data-tooltip={TraitNames.oneHander} onClick={handleClick}>One hander</div>}

                {traits.find((trait) => trait.name === "Sex appeal") ?
                    <div className="trait selected" data-name="Sex appeal" data-tooltip={TraitNames.sexAppeal} onClick={handleClick}>Sex appeal</div> :
                    <div className="trait" data-name="Sex appeal" data-tooltip={TraitNames.sexAppeal} onClick={handleClick}>Sex appeal</div>}

                {traits.find((trait) => trait.name === "Skilled") ?
                    <div className="trait selected" data-name="Skilled" data-tooltip={TraitNames.skilled} onClick={handleClick}>Skilled</div> :
                    <div className="trait" data-name="Skilled" data-tooltip={TraitNames.skilled} onClick={handleClick}>Skilled</div>}

                {traits.find((trait) => trait.name === "Small frame") ?
                    <div className="trait selected" data-name="Small frame" data-tooltip={TraitNames.smallFrame} onClick={handleClick}>Small frame</div> :
                    <div className="trait" data-name="Small frame" data-tooltip={TraitNames.smallFrame} onClick={handleClick}>Small frame</div>}
            </div>
        </div>
    )
}