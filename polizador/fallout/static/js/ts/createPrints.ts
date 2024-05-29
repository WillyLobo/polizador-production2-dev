import { IPrimaryStats, ITrait, IPerk } from "./models";

export function getPrintablePrimaryStats(primaryStats: IPrimaryStats): string {
    let printablePrimaryStats: string = "PRIMARY STATS\n\n";

    printablePrimaryStats = printablePrimaryStats + "Strength " + primaryStats.strength.toString() + "\n";
    printablePrimaryStats = printablePrimaryStats + "Perception " + primaryStats.perception.toString() + "\n";
    printablePrimaryStats = printablePrimaryStats + "Endurance " + primaryStats.endurance.toString() + "\n";
    printablePrimaryStats = printablePrimaryStats + "Charisma " + primaryStats.charisma.toString() + "\n";
    printablePrimaryStats = printablePrimaryStats + "Intelligence " + primaryStats.intelligence.toString() + "\n";
    printablePrimaryStats = printablePrimaryStats + "Agility " + primaryStats.agility.toString() + "\n";
    printablePrimaryStats = printablePrimaryStats + "Luck " + primaryStats.luck.toString() + "\n\n\n";

    return printablePrimaryStats;
}

export function getPrintableTraits(traits: ITrait[]): string {
    let printableTraits: string = "TRAITS\n\n";

    if (traits.length > 0) {
        printableTraits = printableTraits + traits.map((trait) => { return trait.name}).join("\n");
    }
    else {
        printableTraits = printableTraits + "None"
    }

    printableTraits = printableTraits + "\n\n\n"

    return printableTraits;
}

export function getPrintablePerks(perks: IPerk[]): string {
    let printablePerks = "PERKS\n\n";

    const selectedPerks: IPerk[] = perks.filter(perk => perk.levelSelected.length > 0);

    if (selectedPerks.length === 0) {
        return printablePerks + "None\n\n";
    }

    selectedPerks.forEach((perk) => {
        perk.levelSelected.forEach(level => printablePerks = printablePerks + "Level " + level.toString() + "\n");

        printablePerks = printablePerks + "\n" + perk.name + "\n\n";
    });

    return printablePerks;
}