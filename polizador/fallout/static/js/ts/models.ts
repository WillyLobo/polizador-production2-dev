/**
 * Primary stats are strength, perception, endurance, charisma, intelligence, agility and luck.
 * Unspent stat points are also included.
 * 
 * Primary stats are used to calculate derived stats such as action points and the base level for skills like small guns.
 * 
 * Some perks also have primary stat requirements.
 */

export interface IPrimaryStats {
    strength: number,
    perception: number,
    endurance: number,
    charisma: number,
    intelligence: number,
    agility: number,
    luck: number,
    unspentPoints: number
}

/**
 * Defines names for player skills.
 */

export enum PlayerSkillNames {
    SmallGuns = "Small guns",
    BigGuns = "Big guns",
    EnergyWeapons = "Energy weapons",
    Unarmed = "Unarmed",
    MeleeWeapons = "Melee weapons",
    Throwing = "Throwing",
    FirstAid = "First aid",
    Doctor = "Doctor",
    Sneak = "Sneak",
    Lockpick = "Lockpick",
    Steal = "Steal",
    Traps = "Traps",
    Science = "Science",
    Repair = "Repair",
    Speech = "Speech",
    Barter = "Barter",
    Gambling = "Gambling",
    Outdoorsman = "Outdoorsman"
}

/**
 * Holds the values of skills, such as small guns.
 */

export interface IPlayerSkills {
    smallGuns: number,
    bigGuns: number,
    energyWeapons: number,
    unarmed: number,
    meleeWeapons: number,
    throwing: number,
    firstAid: number,
    doctor: number,
    sneak: number,
    lockpick: number,
    steal: number,
    traps: number,
    science: number,
    repair: number,
    speech: number,
    barter: number,
    gambling: number,
    outdoorsman: number
}

/**
 * Stats derived from primary stats, traits and perks.
 */

export interface IDerivedStats {
    hitPoints: number,
    armorClass: number,
    actionPoints: number,
    carryWeight: number,
    meleeDamage: number,
    damageResistance: number,
    poisonResistance: number,
    radiationResistance: number,
    sequence: number,
    healingRate: number,
    criticalChance: number,
    partyLimit: number,
    perkRate: number,
    skillRate: number,
    criticalDamageModifier: number,
    enemyDamageResistanceModifier: number,
    chemAddictionChance: number,
    chemDuration: number,
    chemAddictionRecovery: number,
    hitPointsPerLevel: number
}

/**
 * Represents a character trait.
 */

export interface ITrait {
    name: string
}

/**
 * Defines the names for the traits.
 */

export enum TraitNames {
    bloodyMess = "Bloody mess",
    bruiser = "Bruiser",
    chemReliant = "Chem reliant",
    chemResistant = "Chem resistant",
    fastMetabolism = "Fast metabolism",
    fastShot = "Fast shot",
    finesse = "Finesse",
    gifted = "Gifted",
    goodNatured = "Good natured",
    heavyHanded = "Heavy handed",
    jinxed = "Jinxed",
    kamikaze = "Kamikaze",
    oneHander = "One hander",
    sexAppeal = "Sex appeal",
    skilled = "Skilled",
    smallFrame = "Small frame"
}

/**
 * Holds all the available traits.
 */

export const TRAITS: Array<ITrait> = [
    { name: TraitNames.bloodyMess },
    { name: TraitNames.bruiser },
    { name: TraitNames.chemReliant },
    { name: TraitNames.chemResistant },
    { name: TraitNames.fastMetabolism },
    { name: TraitNames.fastShot },
    { name: TraitNames.finesse },
    { name: TraitNames.gifted },
    { name: TraitNames.goodNatured },
    { name: TraitNames.heavyHanded },
    { name: TraitNames.jinxed },
    { name: TraitNames.kamikaze },
    { name: TraitNames.oneHander },
    { name: TraitNames.sexAppeal },
    { name: TraitNames.skilled },
    { name: TraitNames.smallFrame }
];

/**
 * Returns player skills with 0 values.
 */

export function getEmptyPlayerSkills(): IPlayerSkills {
    const emptyPlayerSkills: IPlayerSkills = {
        smallGuns: 0,
        bigGuns: 0,
        energyWeapons: 0,
        unarmed: 0,
        meleeWeapons: 0,
        throwing: 0,
        firstAid: 0,
        doctor: 0,
        sneak: 0,
        lockpick: 0,
        steal: 0,
        traps: 0,
        science: 0,
        repair: 0,
        speech: 0,
        barter: 0,
        gambling: 0,
        outdoorsman: 0
    }

    return emptyPlayerSkills;
}

/**
 * Returns the base skills calculated with 5-5-5-5-5-5-5 primary stats.
 */

export function getDefaultPlayerSkills() : IPlayerSkills {
    const defaultPlayerSkills: IPlayerSkills = {
        smallGuns: 25,
        bigGuns: 10,
        energyWeapons: 15,
        unarmed: 50,
        meleeWeapons: 40,
        throwing: 20,
        firstAid: 50,
        doctor: 15,
        sneak: 20,
        lockpick: 20,
        steal: 15,
        traps: 20,
        science: 20,
        repair: 15,
        speech: 25,
        barter: 20,
        gambling: 25,
        outdoorsman: 20
    }

    return defaultPlayerSkills;
}

/**
 * Returns skills filled with 0 values.
 */

const emptyPlayerSkills: IPlayerSkills = {
    smallGuns: 0,
    bigGuns: 0,
    energyWeapons: 0,
    unarmed: 0,
    meleeWeapons: 0,
    throwing: 0,
    firstAid: 0,
    doctor: 0,
    sneak: 0,
    lockpick: 0,
    steal: 0,
    traps: 0,
    science: 0,
    repair: 0,
    speech: 0,
    barter: 0,
    gambling: 0,
    outdoorsman: 0
}

/**
 * Returns primary stats filled with 0 values.
 */

const emptyPrimaryStats: IPrimaryStats = {
    strength: 0,
    perception: 0,
    endurance: 0,
    charisma: 0, 
    intelligence: 0, 
    agility: 0, 
    luck: 0, 
    unspentPoints: 0
}

/**
 * Represents a perk.
 * 
 * Perks have different ranks and a maximum rank.
 * 
 * Rank represents how many times the perk has been selected
 * or how many times it can still be selected.
 * 
 * Max rank represents how many times the perk can be selected.
 * 
 * levelSelected holds the player levels the perk was selected.
 * 
 * requirementsMet holds if the requirements for the perks are met.
 * 
 * baseValue can be used to hold the snapshot of the values they're modifying before they were picked,
 * such as luck before zeta scan perk.
 */

 export interface IPerk {
    name: string,
    requirements: IPerkRequirements,
    ranks: number,
    maxRanks: number,
    levelSelected: number[],
    requirementsMet: boolean,
    baseValue?: number
}

/**
 * Represents perk requirements.
 * 
 * Perks can require different levels, primary stats and skills.
 */

export interface IPerkRequirements {
    level: number,
    primaryStats: IPrimaryStats,
    playerSkills: IPlayerSkills,
}

/**
 * Defines all the perk names.
 */

export enum PerkNames {
    awareness = "Awareness",
    bonusHthDamage = "Bonus hth damage",
    cautiousNature = "Cautious nature", 
    comprehension = "Comprehension",
    earlierSequence = "Earlier sequence",
    fasterHealing = "Faster healing",
    healer = "Healer",
    hereAndNow = "Here and now",
    kamaSutraMaster = "Kama sutra master",
    nightVision = "Night vision",
    presence = "Presence",
    quickPockets = "Quick pockets",
    scout = "Scout",
    smoothTalker = "Smooth talker",
    stonewall = "Stonewall",
    strongBack = "Strong back",
    survivalist = "Survivalist",
    swiftLearner = "Swift learner",
    thief = "Thief",
    toughness = "Toughness",
    adrenalineRush = "Adrenaline rush",
    bonusMove = "Bonus move",
    bonusRangedDamage = "Bonus ranged damage",
    educated = "Educated",
    empathy = "Empathy",
    fortuneFinder = "Fortune finder",
    gambler = "Gambler",
    ghost = "Ghost",
    harmless = "Harmless",
    heaveHo = "Heave Ho!",
    magneticPersonality = "Magnetic personality",
    moreCriticals = "More criticals",
    negotiator = "Negotiator",
    packRat = "Pack rat",
    pathfinder = "Pathfinder",
    quickRecovery = "Quick recovery",
    radResistance = "Rad resistance",
    ranger = "Ranger",
    salesman = "Salesman",
    silentRunning = "Silent running",
    snakeater = "Snakeater",
    betterCriticals = "Better criticals",
    demolitionExpert = "Demolition expert",
    dodger = "Dodger",
    explorer = "Explorer",
    karmaBeacon = "Karma beacon",
    lightStep = "Light step",
    mutate = "Mutate!",
    mysteriousStranger = "Mysterious stranger",
    pyromaniac = "Pyromaniac",
    scrounger = "Scrounger",
    sharpshooter = "Sharpshooter",
    speaker = "Speaker",
    actionBoy = "Action boy",
    cultOfPersonality = "Cult of personality",
    hthEvade = "Hth evade",
    lifegiver = "Lifegiver",
    livingAnatomy = "Living anatomy",
    masterThief = "Master thief",
    masterTrader = "Master trader",
    mrFixit = "Mr. Fixit",
    tag = "Tag!",
    weaponHandling = "Weapon handling",
    bonusHthAttacks = "Bonus hth attacks",
    bonusRateOfFire = "Bonus rate of fire",
    pickpocket = "Pickpocket",
    silentDeath = "Silent death",
    slayer = "Slayer",
    gainStrength = "Gain strength",
    gainPerception = "Gain perception",
    gainEndurance = "Gain endurance",
    gainCharisma = "Gain charisma",
    gainIntelligence = "Gain intelligence",
    gainAgility = "Gain agility",
    gainLuck = "Gain luck",
    medic = "Medic",
    sniper = "Sniper",
    dermalImpactArmor = "Dermal impact armor",
    dermalImpactAssaultEnhancement = "Dermal impact assault enhancement",
    expertExcrementExpeditor = "Expert excrement expeditor",
    phoenixArmorImplants = "Phoenix armor implants",
    phoenixAssaultEnhancement = "Phoenix assault enhancement",
    vaultCityTraining = "VC training",
    vaultCityInoculations = "VC inoculations",
    zetaScan = "Zeta scan"
}

/**
 * Defines all the derived stat names.
 */

export enum DerivedStatsNames {
    hitPoints = "Hit points",
    armorClass = "Armor class",
    actionPoints = "Action points",
    carryWeight = "Carry weight",
    meleeDamage = "Melee damage",
    damageResistance = "Damage resistance",
    poisonResistance = "Poison resistance",
    radiationResistance = "Radiation resistance",
    healingRate = "Healing rate",
    hitPointsPerLevel = "Hit points per level",
    criticalChance = "Critical chance",
    sequence = "Sequence",
    partyLimit = "Party limit",
    enemyDamageResistanceModifier = "Enemy damage resistance modifier",
    criticalDamageModifier = "Critical damage modifier",
    perkRate = "Perk rate",
    skillRate = "Skill rate",
    chemAddictionChance = "Chem addiction chance",
    chemAddictionRecovery = "Chem addiction recovery",
    chemDuration = "Chem duration"
}

/**
 * Contains all the perks.
 * 
 * Requirements for the perks are defined here.
 * 
 * Ranks are set to the default maximum rank.
 * 
 * Array for when the perk has been selected is initialized.
 * 
 * Requirements met are set to false.
 */

 export const PERKS: IPerk[] = [
    {
        name: PerkNames.actionBoy,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, agility: 5 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.adrenalineRush,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, strength: 10 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.awareness,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, perception: 5 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.betterCriticals,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, perception: 6, agility: 4, luck: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.bonusHthAttacks,
        requirements: {
            level: 15,
            primaryStats: { ...emptyPrimaryStats, agility: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.bonusHthDamage,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, strength: 6, agility: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.bonusMove,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, agility: 5 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.bonusRangedDamage,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, agility: 6, luck: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.bonusRateOfFire,
        requirements: {
            level: 15,
            primaryStats: { ...emptyPrimaryStats, perception: 6, intelligence: 6, agility: 7 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.cautiousNature,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, perception: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.comprehension,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, intelligence: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.cultOfPersonality,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, charisma: 10 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.demolitionExpert,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, agility: 4 },
            playerSkills: { ...emptyPlayerSkills, traps: 75 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.dodger,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, agility: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.earlierSequence,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: emptyPlayerSkills
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.educated,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, intelligence: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.empathy,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, perception: 7, intelligence: 5 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.explorer,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.fasterHealing,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, endurance: 6 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.fortuneFinder,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, luck: 8 },
            playerSkills: emptyPlayerSkills
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gambler,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, gambling: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.ghost,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, sneak: 60 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.harmless,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, steal: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.healer,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, perception: 7, intelligence: 5, agility: 6 },
            playerSkills: { ...emptyPlayerSkills, firstAid: 40 }
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.heaveHo,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, strength: 9 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.hereAndNow,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.hthEvade,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, unarmed: 75 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.kamaSutraMaster,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, endurance: 5, agility: 5 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.karmaBeacon,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, charisma: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.lifegiver,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, endurance: 4 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.lightStep,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, agility: 5, luck: 5 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.livingAnatomy,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, doctor: 60 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.magneticPersonality,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, charisma: 10 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.masterThief,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, lockpick: 50, steal: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.masterTrader,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, charisma: 7 },
            playerSkills: { ...emptyPlayerSkills, barter: 75 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.medic,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, firstAid: 40, doctor: 40 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.moreCriticals,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, luck: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.mrFixit,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, science: 40, repair: 40 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.mutate,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.mysteriousStranger,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, luck: 40 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.negotiator,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, barter: 50, speech: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.nightVision,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, perception: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.packRat,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.pathfinder,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, endurance: 6 },
            playerSkills: { ...emptyPlayerSkills, outdoorsman: 40 }
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.pickpocket,
        requirements: {
            level: 15,
            primaryStats: { ...emptyPrimaryStats, agility: 8 },
            playerSkills: { ...emptyPlayerSkills, steal: 80 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.presence,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, charisma: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.pyromaniac,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, bigGuns: 75 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.quickPockets,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, agility: 5 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.quickRecovery,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, agility: 5 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.radResistance,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, endurance: 6, intelligence: 4 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.ranger,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, perception: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.salesman,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, barter: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.scout,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, perception: 7 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.scrounger,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, luck: 8 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.sharpshooter,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats, perception: 7, intelligence: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.silentDeath,
        requirements: {
            level: 18,
            primaryStats: { ...emptyPrimaryStats, agility: 10 },
            playerSkills: { ...emptyPlayerSkills, sneak: 80, unarmed: 80 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.silentRunning,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, agility: 6 },
            playerSkills: { ...emptyPlayerSkills, sneak: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.slayer,
        requirements: {
            level: 24,
            primaryStats: { ...emptyPrimaryStats, strength: 8, agility: 8 },
            playerSkills: { ...emptyPlayerSkills, unarmed: 80 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.smoothTalker,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, intelligence: 4 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.snakeater,
        requirements: {
            level: 6,
            primaryStats: { ...emptyPrimaryStats, endurance: 3 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 2,
        maxRanks: 2,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.sniper,
        requirements: {
            level: 24,
            primaryStats: { ...emptyPrimaryStats, perception: 8, agility: 8 },
            playerSkills: { ...emptyPlayerSkills, smallGuns: 80 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.speaker,
        requirements: {
            level: 9,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, speech: 50 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.stonewall,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, strength: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.strongBack,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, strength: 6, endurance: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.survivalist,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, endurance: 6, intelligence: 6 },
            playerSkills: { ...emptyPlayerSkills, outdoorsman: 40}
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.swiftLearner,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, intelligence: 4 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.tag,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.thief,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.toughness,
        requirements: {
            level: 3,
            primaryStats: { ...emptyPrimaryStats, endurance: 6, luck: 6 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 3,
        maxRanks: 3,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.weaponHandling,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, strength: 7, agility: 5 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainStrength,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, strength: 10},
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainPerception,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, perception: 10},
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainEndurance,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, endurance: 10},
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainCharisma,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, charisma: 10},
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainIntelligence,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, intelligence: 10},
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainAgility,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, agility: 10},
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.gainLuck,
        requirements: {
            level: 12,
            primaryStats: { ...emptyPrimaryStats, luck: 10 },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.zetaScan,
        requirements: {
            level: 2,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false,
        baseValue: 5
    },
    {
        name: PerkNames.vaultCityInoculations,
        requirements: {
            level: 1,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, doctor: 75 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
    {
        name: PerkNames.vaultCityTraining,
        requirements: {
            level: 1,
            primaryStats: { ...emptyPrimaryStats },
            playerSkills: { ...emptyPlayerSkills, doctor: 75 }
        },
        ranks: 1,
        maxRanks: 1,
        levelSelected: [],
        requirementsMet: false
    },
]

/**
 * Defines all the primary stat names.
 */

export enum PrimaryStatNames {
    strength = "Strength",
    perception = "Perception",
    endurance = "Endurance",
    charisma = "Charisma",
    intelligence = "Intelligence",
    agility = "Agility",
    luck = "Luck"
}

/**
 * Represents a tooltip for primary stat, trait, player skill or perk.
 * 
 * Name is used for identification.
 * 
 * Heading contains the heading for the tooltip.
 * 
 * SubHeading contains information like perk requirements.
 * 
 * Body contains the description used in tooltip body.
 */

export interface ITooltip {
    name: string,
    heading: string,
    body: string,
    subHeading: string
}

export const emptyTooltip: ITooltip = {
    name: "",
    heading: "",
    body: "",
    subHeading: ""
}

/**
 * Holds all the tooltips for primary stats, traits, player skills and perks
 */

export const TOOLTIPS: ITooltip[] = [
    {
        name: PrimaryStatNames.strength,
        heading: PrimaryStatNames.strength,
        subHeading: "Modifies: hit points, melee damage and carry weight",
        body: "Raw physical strength. A high strength is good for physical characters."
    },
    {
        name: PrimaryStatNames.perception,
        heading: PrimaryStatNames.perception,
        subHeading: "Modifies: sequence and ranged combat distance modifiers",
        body: "The ability to see, hear, taste and notice unusual things. A high perception is important for a sharpshooter."
    },
    {
        name: PrimaryStatNames.endurance,
        heading: PrimaryStatNames.endurance,
        subHeading: "Modifies: HPs, rad & psn resistances, healing rate and HPs per level",
        body: "Stamina and physical toughness. A character with a high endurance will survive where others may not."
    },
    {
        name: PrimaryStatNames.charisma,
        heading: PrimaryStatNames.charisma,
        subHeading: "Modifies: NPC reactions, prices and party limit",
        body: "A combination of appearance and charm. A high charisma is important for characters that want to influence people with words."
    },
    {
        name: PrimaryStatNames.intelligence,
        heading: PrimaryStatNames.intelligence,
        subHeading: "Modifies: skill rate",
        body: "Knowledge, wisdom and the ability to think quickly. A high intelligence is important for any character."
    },
    {
        name: PrimaryStatNames.agility,
        heading: PrimaryStatNames.agility,
        subHeading: "Modifies: action points and armor class",
        body: "Coordination and the ability to move well. A high agility is important for any active character."
    },
    {
        name: PrimaryStatNames.luck,
        heading: PrimaryStatNames.luck,
        subHeading: "Modifies: critical chance",
        body: "Fate. Karma. An extremely high or low luck will affect the character - somehow. Events and situations will be changed by how lucky (or unlucky) your character is."
    },
    {
        name: TraitNames.bloodyMess,
        heading: "Bloody mess",
        subHeading: "",
        body: "By some strange twist of fate, people around you die violently. You always see the worst way a person can die."
    },
    {
        name: TraitNames.bruiser,
        heading: "Bruiser",
        subHeading: "",
        body: "2+ to strength, -2 action points."
    },
    {
        name: TraitNames.chemReliant,
        heading: "Chem reliant",
        subHeading: "",
        body: "You are more easily addicted to chems. Your chance to become addicted to chems is twice the norm, but you recover faster from their ill effects."
    },
    {
        name: TraitNames.chemResistant,
        heading: "Chem resistant",
        subHeading: "",
        body: "The addiction chance of chems are halved, but so too is the effect duration of the chem."
    },
    {
        name: TraitNames.fastMetabolism,
        heading: "Fast metabolism",
        subHeading: "",
        body: "+2 to healing rate, radiation and poison resistances start at 0%."
    },
    {
        name: TraitNames.fastShot,
        heading: "Fast shot",
        subHeading: "",
        body: "Action point costs for all ranged weapons are reduced by 1 AP. Player cannot make called shots to body parts."
    },
    {
        name: TraitNames.finesse,
        heading: "Finesse",
        subHeading: "",
        body: "+10% to critical change, +30% to enemy damage resistance."
    },
    {
        name: TraitNames.gifted,
        heading: "Gifted",
        subHeading: "",
        body: "+1 to all primary stats, -10% to all skills, -5 skill rate."
    },
    {
        name: TraitNames.goodNatured,
        heading: "Good natured",
        subHeading: "",
        body: "+15% to first aid, doctor, speech and barter, -10% to small guns, big guns, energy weapons, unarmed, melee weapons and throwing."
    },
    {
        name: TraitNames.heavyHanded,
        heading: "Heavy handed",
        subHeading: "",
        body: "+4 damage to unarmed and melee weapon attacks, -30% to critical damage modifier."
    },
    {
        name: TraitNames.jinxed,
        heading: "Jinxed",
        subHeading: "",
        body: "All misses have a 50% chance to become critical misses."
    },
    {
        name: TraitNames.kamikaze,
        heading: "Kamikaze",
        subHeading: "",
        body: "+5 to sequence, base armor class to 0."
    },
    {
        name: TraitNames.oneHander,
        heading: "One hander",
        subHeading: "",
        body: "-40% chance to hit with two-handed weapons, +20% to hit with one handed weapons."
    },
    {
        name: TraitNames.sexAppeal,
        heading: "Sex appeal",
        subHeading: "",
        body: "Opposite sex reacts more favorably. Annoys members of the same sex."
    },
    {
        name: TraitNames.skilled,
        heading: "Skilled",
        subHeading: "",
        body: "+5 to skill rate, perk rate to 4 instead of 3."
    },
    {
        name: TraitNames.smallFrame,
        heading: "Small frame",
        subHeading: "",
        body: "+1 to agility, carry weight is equal to 25 + (15 * Strength) pounds instead of 25 + (25 * strength) pounds."
    },
    {
        name: PlayerSkillNames.SmallGuns,
        heading: PlayerSkillNames.SmallGuns,
        subHeading: "Base: 5% + (4 * AG)",
        body: "The use, care and general knowledge of small firearms - pistols, SMGs and rifles."
    },
    {
        name: PlayerSkillNames.BigGuns,
        heading: PlayerSkillNames.BigGuns,
        subHeading: "Base: 0% + (2 * AG)",
        body: "The operation and maintenance of really big guns - miniguns, rocket launchers, flamethrowers and such."
    },
    {
        name: PlayerSkillNames.EnergyWeapons,
        heading: PlayerSkillNames.EnergyWeapons,
        subHeading: "Base: 0% + (2 * AG)",
        body: "The care and feeding of energy-based weapons. How to arm and operate weapons that use laser or plasma technology."
    },
    {
        name: PlayerSkillNames.Unarmed,
        heading: PlayerSkillNames.Unarmed,
        subHeading: "Base: 30% + (2 * (AG + ST))",
        body: "A combination of martial arts, boxing and other hand-to-hand martial arts. Combat with your hands and feet."
    },
    {
        name: PlayerSkillNames.MeleeWeapons,
        heading: PlayerSkillNames.MeleeWeapons,
        subHeading: "Base: 20 + (2 * (AG + ST))",
        body: "Using non-ranged weapons in hand-to-hand combat - knives, sledgehammers, spears, clubs and so on."
    },
    {
        name: PlayerSkillNames.Throwing,
        heading: PlayerSkillNames.Throwing,
        subHeading: "Base: 0% + (4* AG)",
        body: "The skill of muscle-propelled ranged weapns, such as throwing knives, spears and grenades."
    },
    {
        name: PlayerSkillNames.FirstAid,
        heading: PlayerSkillNames.FirstAid,
        subHeading: "Base: 0% + (2 * (PE + IN))",
        body: "General healing skill. Used to heal small cuts, abrasions and other minor ills. In game terms, the use of first aid can heal more hit points over time than just rest."
    },
    {
        name: PlayerSkillNames.Doctor,
        heading: PlayerSkillNames.Doctor,
        subHeading: "Base: 5% + (PE + IN)",
        body: "The healing of major wounds and crippled limbs. Without this skill, it will take a much longer period of time to restore crippled limbs to use."
    },
    {
        name: PlayerSkillNames.Steal,
        heading: PlayerSkillNames.Steal,
        subHeading: "Base: 0% + (3 * AG)",
        body: "The ability to make the things of others your own. Can be used to steal from people or places."
    },
    {
        name: PlayerSkillNames.Sneak,
        heading: PlayerSkillNames.Sneak,
        subHeading: "Base: 5% + (3 * AG)",
        body: "Quiet movement, and the ability to remain unnoticed. If successful, you will be much harder to locate. You cannot run and sneak at the same time."
    },
    {
        name: PlayerSkillNames.Lockpick,
        heading: PlayerSkillNames.Lockpick,
        subHeading: "Base: 10% + (PE + AG)",
        body: "The skill of opening locks without the proper key. The use of lockpicks or electronic lockpicks will greatly enhance this skill."
    },
    {
        name: PlayerSkillNames.Traps,
        heading: PlayerSkillNames.Traps,
        subHeading: "Base: 10% + (PE + AG)",
        body: "The finding and removal of traps. Also the setting of explosives for demolition purposes."
    },
    {
        name: PlayerSkillNames.Repair,
        heading: PlayerSkillNames.Repair,
        subHeading: "Base: 0% + (3 * IN)",
        body: "The practical application of the Science skill for fixing broken equipment, machinery and electronics."
    },
    {
        name: PlayerSkillNames.Science,
        heading: PlayerSkillNames.Science,
        subHeading: "Base: 0% + (4 * IN)",
        body: "Covers a variety of high technology skills, such as computers, biology, physics and geology."
    },
    {
        name: PlayerSkillNames.Gambling,
        heading: PlayerSkillNames.Gambling,
        subHeading: "Base: 0% + (5 * LK)",
        body: "The knowledge and practical skills related to wagering. The skill at cards, dice and other games."
    },
    {
        name: PlayerSkillNames.Outdoorsman,
        heading: PlayerSkillNames.Outdoorsman,
        subHeading: "Base: 0% + (2 * (EN + IN))",
        body: "Practical knowledge of the outdoors, and the ability to live off the land. The knowledge of plants and animals."
    },
    {
        name: PlayerSkillNames.Speech,
        heading: PlayerSkillNames.Speech,
        subHeading: "Base: 0% + (5 * CH)",
        body: "The ability to communicate in a practical and efficient manner. The skill of convincing others that your position is correct. The ability to lie and not get caught."
    },
    {
        name: PlayerSkillNames.Barter,
        heading: PlayerSkillNames.Barter,
        subHeading: "Base: 0% + (4 * CH)",
        body: "Trading and trade-related tasks. The ability to get better prices for items you sell, and lower prices for the items you boy."
    },
    {
        name: DerivedStatsNames.hitPoints,
        heading: DerivedStatsNames.hitPoints,
        subHeading: "",
        body: "How much damage your character can take before dying. If you reach 0 HP or less, you are dead."
    },
    {
        name: DerivedStatsNames.actionPoints,
        heading: DerivedStatsNames.actionPoints,
        subHeading: "Perks: action boy",
        body: "The number of actions that the character can take during one combat turn."
    },
    {
        name: DerivedStatsNames.armorClass,
        heading: DerivedStatsNames.armorClass,
        subHeading: "Perks: dodger",
        body: "Modifies the chance to hit this particular character."
    },
    {
        name: DerivedStatsNames.carryWeight,
        heading: DerivedStatsNames.carryWeight,
        subHeading: "Perks: pack rat",
        body: "The maximum amount of equipment your character can carry, in pounds."
    },
    {
        name: DerivedStatsNames.meleeDamage,
        heading: DerivedStatsNames.meleeDamage,
        subHeading: "Traits: heavy handed",
        body: "The amount of bonus damage your character does in hand-to-hand combat."
    },
    {
        name: DerivedStatsNames.poisonResistance,
        heading: DerivedStatsNames.poisonResistance,
        subHeading: "Perks: snakeater",
        body: "Reduces poison damage by this amount."
    },
    {
        name: DerivedStatsNames.radiationResistance,
        heading: DerivedStatsNames.radiationResistance,
        subHeading: "Perks: rad resistance",
        body: "The amount of radiation you are exposed to is reduced by this percentage. Radiation resistance can be modified by the type of the armor worn, and anti-radiation drugs."
    },
    {
        name: DerivedStatsNames.sequence,
        heading: DerivedStatsNames.sequence,
        subHeading: "Traits: kamikaze",
        body: "Determines how soon in a combat turn your character can react."
    },
    {
        name: DerivedStatsNames.healingRate,
        heading: DerivedStatsNames.healingRate,
        subHeading: "Traits: fast metabolism. Perks: faster healing",
        body: "At the end of each day, your character will heal 1 HP for each points of healing rate. When you rest, you heal every six hours."
    },
    {
        name: DerivedStatsNames.hitPointsPerLevel,
        heading: DerivedStatsNames.hitPointsPerLevel,
        subHeading: "Perks: lifegiver",
        body: "Maximum hit points gained at level up."
    },
    {
        name: DerivedStatsNames.damageResistance,
        heading: DerivedStatsNames.damageResistance,
        subHeading: "Perks: toughness",
        body: "Any damage taken is reduced by this amount. Damage resistance can be increased by wearing armor."
    },
    {
        name: DerivedStatsNames.criticalChance,
        heading: DerivedStatsNames.criticalChance,
        subHeading: "Traits: finesse. Perks: more criticals, sniper, slayer",
        body: "The chance to cause a critical hit in combat is increased by this amount."
    },
    {
        name: DerivedStatsNames.criticalDamageModifier,
        heading: DerivedStatsNames.criticalDamageModifier,
        subHeading: "Traits: heavy handed. Perks: better criticals.",
        body: "On a critical hit, a random number between 1 and 100 is generated. A creature and body part specific critical hit table is then consulted. This modifier is added to the random number generated. The higher roll is better."
    },
    {
        name: DerivedStatsNames.perkRate,
        heading: DerivedStatsNames.perkRate,
        subHeading: "Traits: skilled",
        body: "Determines the character levels when a perk can be chosen. For example, a perk rate of 3 means that a perk can be chosen every 3rd level, starting from level 3."
    },
    {
        name: DerivedStatsNames.chemAddictionChance,
        heading: DerivedStatsNames.chemAddictionChance,
        subHeading: "Traits: chem reliant, chem resistant",
        body: "Modifies a chance to resist addiction."
    },
    {
        name: DerivedStatsNames.chemAddictionRecovery,
        heading: DerivedStatsNames.chemAddictionRecovery,
        subHeading: "Traits: chem reliant",
        body: "Modifies the length of addiction."
    },
    {
        name: DerivedStatsNames.chemDuration,
        heading: DerivedStatsNames.chemDuration,
        subHeading: "Traits: chem resistant",
        body: "Modifies the length of chem effects."
    },
    {
        name: DerivedStatsNames.partyLimit,
        heading: DerivedStatsNames.partyLimit,
        subHeading: "",
        body: "The maximum number of companions."
    },
    {
        name: DerivedStatsNames.enemyDamageResistanceModifier,
        heading: DerivedStatsNames.enemyDamageResistanceModifier,
        subHeading: "Traits: finesse",
        body: "Modifier added to the enemy damage resistance."
    },
    {
        name: DerivedStatsNames.skillRate,
        heading: DerivedStatsNames.skillRate,
        subHeading: "Traits: gifted, skilled. Perks: educated",
        body: "The number of skill points gained on a level up."
    },
    {
        name: PerkNames.actionBoy,
        heading: PerkNames.actionBoy,
        subHeading: "Requirements: level 12, AG 5",
        body: "+1 action point per rank." 
    },
    {
        name: PerkNames.adrenalineRush,
        heading: PerkNames.adrenalineRush,
        subHeading: "Requirements: level 6, ST < 10",
        body: "+1 to strength when hit points < 50%." 
    },
    {
        name: PerkNames.awareness,
        heading: PerkNames.awareness,
        subHeading: "Requirements: level 3, PE 5",
        body: "Looking at the target shows target's hit points, equipped weapon and ammunition count." 
    },
    {
        name: PerkNames.betterCriticals,
        heading: PerkNames.betterCriticals,
        subHeading: "Requirements: level 9, PE 6, AG 4, LK 6",
        body: "+20% bonus to the critical hit table." 
    },
    {
        name: PerkNames.bonusHthAttacks,
        heading: PerkNames.bonusHthAttacks,
        subHeading: "Requirements: level 15, AG 6",
        body: "Unarmed and melee weapon attacks cost 1 less action point." 
    },
    {
        name: PerkNames.bonusHthDamage,
        heading: PerkNames.bonusHthDamage,
        subHeading: "Requirements: level 3, ST 6, AG 6",
        body: "+2 damage to unarmed and melee weapon attacks per rank." 
    },
    {
        name: PerkNames.bonusMove,
        heading: PerkNames.bonusMove,
        subHeading: "Requirements: level 6, AG 5",
        body: "+2 action points for movement per turn per rank." 
    },
    {
        name: PerkNames.bonusRangedDamage,
        heading: PerkNames.bonusRangedDamage,
        subHeading: "Requirements: level 6, AG 6, LK 6",
        body: "+2 damage to ranged attacks per rank." 
    },
    {
        name: PerkNames.bonusRateOfFire,
        heading: PerkNames.bonusRateOfFire,
        subHeading: "Requirements: level 15, PE 6, IN 6, Ag 7",
        body: "Ranged attacks cost 1 less action point." 
    },
    {
        name: PerkNames.cautiousNature,
        heading: PerkNames.cautiousNature,
        subHeading: "Requirements: level 3, PE 6",
        body: "+3 to perception during random encounters for determining placement." 
    },
    {
        name: PerkNames.comprehension,
        heading: PerkNames.comprehension,
        subHeading: "Requirements: level 3, IN 6",
        body: "+50% more skill points from books." 
    },
    {
        name: PerkNames.cultOfPersonality,
        heading: PerkNames.cultOfPersonality,
        subHeading: "Requirements: level 12, CH 10",
        body: "NPCs will always view the character favorably."
    },
    {
        name: PerkNames.demolitionExpert,
        heading: PerkNames.demolitionExpert,
        subHeading: "Requirements: level 9, AG 4, traps 75%",
        body: "Explosives do more damage and always detonate on time." 
    },
    {
        name: PerkNames.dodger,
        heading: PerkNames.dodger,
        subHeading: "Requirements: level 9, AG 6",
        body: "+5 to armor class." 
    },
    {
        name: PerkNames.earlierSequence,
        heading: PerkNames.earlierSequence,
        subHeading: "Requirements: level 3, PE 6",
        body: "+2 to sequence per rank." 
    },

    {
        name: PerkNames.educated,
        heading: PerkNames.educated,
        subHeading: "Requirements: level 6, IN 6",
        body: "+2 to skill points when leveling per rank." 
    },
    {
        name: PerkNames.empathy,
        heading: PerkNames.empathy,
        subHeading: "Requirements: level 6, PE 7, IN 5",
        body: "In conversation, dialog options are colored by reaction." 
    },
    {
        name: PerkNames.explorer,
        heading: PerkNames.explorer,
        subHeading: "Requirements: level 9",
        body: "Higher chance of special encounters." 
    },
    {
        name: PerkNames.fasterHealing,
        heading: PerkNames.fasterHealing,
        subHeading: "Requirements: level 3, EN 6",
        body: "+2 to healing rate per rank." 
    },
    {
        name: PerkNames.fortuneFinder,
        heading: PerkNames.fortuneFinder,
        subHeading: "Requirements: level 6, LK 8",
        body: "Find additional money in random encounters." 
    },
    {
        name: PerkNames.gainAgility,
        heading: PerkNames.gainAgility,
        subHeading: "Requirements: level 12, AG < 10",
        body: "+1 to agility." 
    },
    {
        name: PerkNames.gainCharisma,
        heading: PerkNames.gainCharisma,
        subHeading: "Requirements: level 12, CH < 10",
        body: "+1 to charisma." 
    },
    {
        name: PerkNames.gainEndurance,
        heading: PerkNames.gainEndurance,
        subHeading: "Requirements: level 12, EN < 10",
        body: "+1 to endurance." 
    },
    {
        name: PerkNames.gainIntelligence,
        heading: PerkNames.gainIntelligence,
        subHeading: "Requirements: level 12, IN < 10",
        body: "+1 to intelligence." 
    },
    {
        name: PerkNames.gainLuck,
        heading: PerkNames.gainLuck,
        subHeading: "Requirements: level 12, LK < 10",
        body: "+1 to luck." 
    },
    {
        name: PerkNames.gainPerception,
        heading: PerkNames.gainPerception,
        subHeading: "Requirements: level 12, PE < 10",
        body: "+1 to perception." 
    },
    {
        name: PerkNames.gainStrength,
        heading: PerkNames.gainStrength,
        subHeading: "Requirements: level 12, ST < 10",
        body: "+1 to strength." 
    },
    {
        name: PerkNames.gambler,
        heading: PerkNames.gambler,
        subHeading: "Requirements: level 6, gambling 50%",
        body: "+20% to gambling." 
    },
    {
        name: PerkNames.ghost,
        heading: PerkNames.ghost,
        subHeading: "Requirements: level 6, sneak 60%",
        body: "+20% to sneak in dark conditions." 
    },
    {
        name: PerkNames.harmless,
        heading: PerkNames.harmless,
        subHeading: "Requirements: level 6, steal 50%, karma > 50",
        body: "+20% to steal." 
    },
    {
        name: PerkNames.healer,
        heading: PerkNames.healer,
        subHeading: "Requirements: level 3, PE 7, IN 5, AG 6, first aid 40%",
        body: "4 to 10 more hit points restored using first aid and doctor skills." 
    },
    {
        name: PerkNames.heaveHo,
        heading: PerkNames.heaveHo,
        subHeading: "Requirements: level 6, ST < 9",
        body: "+2 to strength when determining range of a thrown weapon per rank." 
    },
    {
        name: PerkNames.hereAndNow,
        heading: PerkNames.hereAndNow,
        subHeading: "Requirements: level 3",
        body: "Immediatly gain an extra level." 
    },
    {
        name: PerkNames.hthEvade,
        heading: PerkNames.hthEvade,
        subHeading: "Requirements: level 12, unarmed 75%",
        body: "+2 for each unused action point, plus 1/12 of unarmed skill to armor class at the end of a combat turn." 
    },
    {
        name: PerkNames.kamaSutraMaster,
        heading: PerkNames.kamaSutraMaster,
        subHeading: "Requirements: level 3, EN 5, AG 5",
        body: "Some NPCs are more likely to have sex with the character." 
    },
    {
        name: PerkNames.karmaBeacon,
        heading: PerkNames.karmaBeacon,
        subHeading: "Requirements: level 9, CH 6",
        body: "Karma is doubled for the purposes of dialogue and reactions." 
    },
    {
        name: PerkNames.lifegiver,
        heading: PerkNames.lifegiver,
        subHeading: "Requirements: level 12, EN 4",
        body: "Additional 4 hit points per character level per perk rank. " 
    },
    {
        name: PerkNames.lightStep,
        heading: PerkNames.lightStep,
        subHeading: "Requirements: level 9, AG 5, LK 5",
        body: "Halves the chance to set off a trap." 
    },
    {
        name: PerkNames.livingAnatomy,
        heading: PerkNames.livingAnatomy,
        subHeading: "Requirements: level 12, doctor 60%",
        body: "+10% to doctor and +5 damage to all living creatures per attack." 
    },
    {
        name: PerkNames.magneticPersonality,
        heading: PerkNames.magneticPersonality,
        subHeading: "Requirements: level 6, CH < 10",
        body: "+1 to the party limit." 
    },
    {
        name: PerkNames.masterThief,
        heading: PerkNames.masterThief,
        subHeading: "Requirements: level 12, lockpick 50%, steal 50%",
        body: "+15% to lockpick and steal." 
    },
    {
        name: PerkNames.masterTrader,
        heading: PerkNames.masterTrader,
        subHeading: "Requirements: level 12, CH 7, barter 75%",
        body: "25% discount purchasing from stores and traders." 
    },
    {
        name: PerkNames.medic,
        heading: PerkNames.medic,
        subHeading: "Requirements: level 12, first aid 40% or doctor 40%",
        body: "+10% to first aid and doctor." 
    },
    {
        name: PerkNames.moreCriticals,
        heading: PerkNames.moreCriticals,
        subHeading: "Requirements: level 6, LK 6",
        body: "+5% to critical chance per rank." 
    },
    {
        name: PerkNames.mrFixit,
        heading: PerkNames.mrFixit,
        subHeading: "Requirements: level 12, science 40% or repair 40%",
        body: "+10% to repair and science." 
    },
    {
        name: PerkNames.mutate,
        heading: PerkNames.mutate,
        subHeading: "Requirements: level 9",
        body: "Change one of the character traits." 
    },
    {
        name: PerkNames.mysteriousStranger,
        heading: PerkNames.mysteriousStranger,
        subHeading: "Requirements: level 9, LK 4",
        body: "Change for a temporary ally in random encounters. Change: 30% + 2% * luck." 
    },
    {
        name: PerkNames.negotiator,
        heading: PerkNames.negotiator,
        subHeading: "Requirements: level 6, barter 50%, speech 50%",
        body: "+10% to speech and barter." 
    },
    {
        name: PerkNames.nightVision,
        heading: PerkNames.nightVision,
        subHeading: "Requirements: level 3, PE 6",
        body: "20% reduction in darkness level." 
    },
    {
        name: PerkNames.packRat,
        heading: PerkNames.packRat,
        subHeading: "Requirements: level 6",
        body: "Increase carry weight by 50 pounds." 
    },
    {
        name: PerkNames.pathfinder,
        heading: PerkNames.pathfinder,
        subHeading: "Requirements: level 6, EN 6, outdoorsman 40%",
        body: "25% reduction in travel time on the world map."
    },
    {
        name: PerkNames.pickpocket,
        heading: PerkNames.pickpocket,
        subHeading: "Requirements: level 15, AG 8, steal 80%",
        body: "Size and facing modifiers are ignored when stealing." 
    },
    {
        name: PerkNames.presence,
        heading: PerkNames.presence,
        subHeading: "Requirements: level 3, CH 6",
        body: "+10% to the initial reaction of NPCs per rank." 
    },
    {
        name: PerkNames.pyromaniac,
        heading: PerkNames.pyromaniac,
        subHeading: "Requirements: level 9, big guns 75%",
        body: "+5 damage with fire-based weapons, more violent fire death animations." 
    },
    {
        name: PerkNames.quickPockets,
        heading: PerkNames.quickPockets,
        subHeading: "Requirements: level 3, AG 5",
        body: "Accessing inventory during combat only costs 2 action points." 
    },
    {
        name: PerkNames.quickRecovery,
        heading: PerkNames.quickRecovery,
        subHeading: "Requirements: level 6, AG 5",
        body: "Getting up after getting knocked down only costs 1 action point." 
    },
    {
        name: PerkNames.radResistance,
        heading: PerkNames.radResistance,
        subHeading: "Requirements: level 6, EN 6, IN 4",
        body: "+15% to radiation resistance per rank." 
    },
    {
        name: PerkNames.ranger,
        heading: PerkNames.ranger,
        subHeading: "Requirements: level 6, PE 6",
        body: "+15% to outdoorsman." 
    },
    {
        name: PerkNames.salesman,
        heading: PerkNames.salesman,
        subHeading: "Requirements: level 6, barter 50%",
        body: "+20% to barter." 
    },
    {
        name: PerkNames.scout,
        heading: PerkNames.scout,
        subHeading: "Requirements: level 3, PE 7",
        body: "World map reveal radius increased by 1 tile and find special encounters easier." 
    },
    {
        name: PerkNames.scrounger,
        heading: PerkNames.scrounger,
        subHeading: "Requirements: level 9, LK 8",
        body: "Double the ammunition found in the random encounters." 
    },
    {
        name: PerkNames.sharpshooter,
        heading: PerkNames.sharpshooter,
        subHeading: "Requirements: level 9, PE 7, IN 6",
        body: "+2 to perception when determining range modifiers." 
    },
    {
        name: PerkNames.silentDeath,
        heading: PerkNames.silentDeath,
        subHeading: "Requirements: level 18, sneak 80%, unarmed 80%",
        body: "While sneaking, unarmed and melee weapon attacks from behind do double damage." 
    },
    {
        name: PerkNames.silentRunning,
        heading: PerkNames.silentRunning,
        subHeading: "Requirements: level 6, AG 6, sneak 50%",
        body: "Able to sneak and run at the same time." 
    },
    {
        name: PerkNames.slayer,
        heading: PerkNames.slayer,
        subHeading: "Requirements: level 24, ST 8, AG 8, unarmed 80%",
        body: "All attacks with unarmed and melee weapons are critical hits." 
    },
    {
        name: PerkNames.smoothTalker,
        heading: PerkNames.smoothTalker,
        subHeading: "Requirements: level 3, IN 4",
        body: "+1 to intelligence for the purposes of dialogue." 
    },
    {
        name: PerkNames.snakeater,
        heading: PerkNames.snakeater,
        subHeading: "Requirements: level 6, EN 3",
        body: "+25% to poison resistance per rank." 
    },
    {
        name: PerkNames.sniper,
        heading: PerkNames.sniper,
        subHeading: "Requirements: level 24, PE 8, AG 8, small guns 80%",
        body: "All attacks with ranged weapons are criticals hits on a successfull luck roll." 
    },
    {
        name: PerkNames.speaker,
        heading: PerkNames.speaker,
        subHeading: "Requirements: level 9, speech 50%",
        body: "+20% to speech." 
    },
    {
        name: PerkNames.stonewall,
        heading: PerkNames.stonewall,
        subHeading: "Requirements: level 3, ST 6",
        body: "Reduced chance of getting knocked down in combat." 
    },
    {
        name: PerkNames.strongBack,
        heading: PerkNames.strongBack,
        subHeading: "Requirements: level 3, ST 6, EN 6",
        body: "Increase carry weight by 50 pounds per rank." 
    },
    {
        name: PerkNames.survivalist,
        heading: PerkNames.survivalist,
        subHeading: "Requirements: level 3, EN 6, IN 6, outdoorsman 40%",
        body: "+25% to outdoorsman." 
    },
    {
        name: PerkNames.swiftLearner,
        heading: PerkNames.swiftLearner,
        subHeading: "Requirements: level 3, IN 4",
        body: "+5% experience gained per rank." 
    },
    {
        name: PerkNames.tag,
        heading: PerkNames.tag,
        subHeading: "Requirements: level 12",
        body: "+1 tag point." 
    },
    {
        name: PerkNames.thief,
        heading: PerkNames.thief,
        subHeading: "Requirements: level 3",
        body: "+10% to sneak, lockpick, steal and traps." 
    },
    {
        name: PerkNames.toughness,
        heading: PerkNames.toughness,
        subHeading: "Requirements: level 3, EN 6, LK 6",
        body: "+10% to damage resistance per rank." 
    },
    {
        name: PerkNames.weaponHandling,
        heading: PerkNames.weaponHandling,
        subHeading: "Requirements: level 12, ST < 7, AG 5",
        body: "+3 to strength for weapon requirements." 
    },
    {
        name: PerkNames.zetaScan,
        heading: PerkNames.zetaScan,
        subHeading: "Special perk",
        body: "A hubologist called the Enlightened One in downtown NCR gives a \"zeta scan\", giving either -1, +1 or +2 to luck." 
    },
    {
        name: PerkNames.vaultCityInoculations,
        heading: "Vault city inoculations",
        subHeading: "Special perk. Requirements: doctor 75%, vault city training perk",
        body: "+10% to poison and radiation resistances." 
    },
    {
        name: PerkNames.vaultCityTraining,
        heading: "Vault city training",
        subHeading: "Special perk. Requirements: doctor 75%",
        body: "+5% to first aid and doctor skills." 
    },
]

/**
 * Game difficulty effects base skills.
 */

export enum Difficulty {
    easy = "Easy",
    normal = "Normal",
    hard = "Hard"
}