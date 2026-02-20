from gooey import Gooey, GooeyParser
import sys
import yaml
from argparse import Namespace

from helpers import root_path, write_plaintext, boolify, space_to_snake
from config import read_presets, write_presets


# Handle Splash Screen
if getattr(sys, "frozen", False):
    import pyi_splash
    pyi_splash.close()


def create_yaml(args: Namespace) -> str:
    """
    
    Generate a YAML representation of settings from the Gooey parser.
    """

    slot_name = getattr(args, "slot_name")
    if slot_name is None:
        raise ValueError("Error: slot_name is a required field.")
    
    data = {"name": slot_name, "game": "Kingdom Hearts"}
    kh = {}

    rename = {
        "required_lucky_emblems_for_final_rest_door": "required_lucky_emblems_door",
        "required_lucky_emblems_for_end_of_the_world": "required_lucky_emblems_eotw",
        "lucky_emblems_in_item_pool": "lucky_emblems_in_pool",
    }

    for field, value in vars(args).items():
        if field == "slot_name":
            continue
        if value is None:
            raise ValueError("Error: %s is a required field." % field)
        key = rename.get(field, field)
        if key == "exp_multiplier":
            try:
                kh[key] = int(value) * 16
            except Exception:
                kh[key] = value
            continue
        if key == "cups":
            if value == "All Cups":
                kh[key] = "hades_cup"
            elif value == "No Hades Cup":
                kh[key] = "cups"
            else:
                kh[key] = value
            continue
        if key in (
            "final_rest_door_key",
            "end_of_the_world_unlock",
            "randomize_postcards",
            "randomize_ap_costs",
            "death_link",
            "remote_items",
        ):
            kh[key] = space_to_snake(value)
            continue

        kh[key] = boolify(value)

    data["Kingdom Hearts"] = kh
    return yaml.safe_dump(data, sort_keys=False, indent=2)


def output_yaml(yaml_str: str, slot_name: str):
    slot_name = slot_name.replace("{number}", "")
    yaml_path = root_path().joinpath("Settings", slot_name + '.yaml')
    write_plaintext(file_path=yaml_path, data=yaml_str, overwrite=True, create_parents=True)
    print(f"YAML file written to {yaml_path}")


@Gooey(
    program_name="KH1 Randomizer Settings Generator",
    image_dir=str(root_path().joinpath("Images")),
    tabbed_groups=True,
    default_size=(720, 480),
    header_bg_color="#444034",
)
def main():
    presets = read_presets("settings")
    parser = GooeyParser()
    goal_group = parser.add_argument_group(
        "Goal", "Customize how the player can win the game."
    )
    locations_group = parser.add_argument_group(
        "Locations", "Customize which locations can contain non filler items."
    )
    levels_group = parser.add_argument_group(
        "Levels", "Customize what can be found on level ups."
    )
    keyblades_group = parser.add_argument_group(
        "Keyblades", "Customize keyblade stats."
    )
    synth_group = parser.add_argument_group("Synth", "Customize synthesis materials.")
    ap_costs_group = parser.add_argument_group("AP Costs", "Customize AP Costs.")
    misc_group = parser.add_argument_group("Misc", "Customize other misc settings.")

    misc_group.add_argument(
        "--slot_name",
        action="store",
        default=presets["slot_name"],
        metavar="Slot Name",
        help="Defines what the slot name should be for hosting the game on Archipelago.  You can ignore this if you plan to play offline.",
    )
    goal_group.add_argument(
        "--final_rest_door_key",
        choices=[
            "Lucky Emblems",
            "Puppies",
            "Postcards",
            "Final Rest",
            "Sephiroth",
            "Unknown",
        ],
        default=presets["final_rest_door_key"],
        metavar="Final Rest Door Key",
        help="Determines where the key is which manifests the door in Final Rest.",
    )
    goal_group.add_argument(
        "--end_of_the_world_unlock",
        choices=["Item", "Lucky Emblems"],
        default=presets["end_of_the_world_unlock"],
        metavar="End of the World Unlock",
        help="Determines how End of the World unlocks.",
    )
    goal_group.add_argument(
        "--required_lucky_emblems_for_end_of_the_world",
        widget="Slider",
        gooey_options={"min": 1, "max": 13, "increment": 1},
        default=int(presets["required_lucky_emblems_for_end_of_the_world"]),
        metavar="Required Lucky Emblems for End of the World",
        help="If End of the World Unlock is set to Lucky Emblems, determines how many Lucky Emblems are required.",
    )
    goal_group.add_argument(
        "--required_lucky_emblems_for_final_rest_door",
        widget="Slider",
        gooey_options={"min": 1, "max": 13, "increment": 1},
        default=int(presets["required_lucky_emblems_for_final_rest_door"]),
        metavar="Required Lucky Emblems for the Final Rest Door",
        help="If Final Rest Door Key is set to Lucky Emblems, detmermines how many Lucky Emblems are required.",
    )
    goal_group.add_argument(
        "-lucky_emblems_in_item_pool",
        widget="Slider",
        gooey_options={"min": 1, "max": 13, "increment": 1},
        default=int(presets["lucky_emblems_in_item_pool"]),
        metavar="Lucky Emblems in the item pool",
        help="If either the Final Rest Door Key or End of the World Unlock are set to Lucky Emblems, determines how many Lucky Emblems are in the pool.",
    )
    goal_group.add_argument(
        "--required_postcards",
        widget="Slider",
        gooey_options={"min": 1, "max": 10, "increment": 1},
        default=int(presets["required_postcards"]),
        metavar="Required Postcards",
        help="If Final Rest Door Key is set to Postcards, determines how many Postcards are required.",
    )
    goal_group.add_argument(
        "--required_puppies",
        choices=["10", "20", "30", "40", "50", "60", "70", "80", "90", "99"],
        default=presets["required_puppies"],
        metavar="Required Puppies",
        help="If Final Rest Door Key is set to Puppies, determines how many Puppies are required.",
    )
    goal_group.add_argument(
        "--destiny_islands",
        choices=["Yes", "No"],
        default=presets["destiny_islands"],
        metavar="Destiny Islands",
        help='If on, Adds a Destiny Islands item and a number of Raft Materials items to the pool. When "Destiny Islands" is found, Traverse Town will have an additional place to land - Seashore.  "Raft Materials" allow progress into Day 2 and to Homecoming.  The amount is defined in Day 2 Materials and Homecoming Materials.',
    )
    goal_group.add_argument(
        "--day_2_materials",
        widget="Slider",
        gooey_options={"min": 0, "max": 20, "increment": 1},
        default=int(presets["day_2_materials"]),
        metavar="Day 2 Materials",
        help="The number of Raft Materials required to access Day 2.",
    )
    goal_group.add_argument(
        "--homecoming_materials",
        widget="Slider",
        gooey_options={"min": 0, "max": 20, "increment": 1},
        default=int(presets["homecoming_materials"]),
        metavar="Homecoming Materials",
        help="The number of Raft Materials required to access Homecoming.",
    )
    goal_group.add_argument(
        "--materials_in_pool",
        widget="Slider",
        gooey_options={"min": 0, "max": 20, "increment": 1},
        default=int(presets["materials_in_pool"]),
        metavar="Materials in Pool",
        help="Total number of Raft Materials in the item pool.",
    )
    locations_group.add_argument(
        "--super_bosses",
        choices=["Yes", "No"],
        default=presets["super_bosses"],
        metavar="Super Bosses",
        help="Determines if important items can be behind Super Bosses.",
    )
    locations_group.add_argument(
        "--atlantica",
        choices=["Yes", "No"],
        default=presets["atlantica"],
        metavar="Atlantica",
        help="Determines if important items can be in Atlantica.",
    )
    locations_group.add_argument(
        "--cups",
        choices=["Off", "No Hades Cup", "All Cups"],
        default=presets["cups"],
        metavar="Cups",
        help="Determines which, if any, Olympus Coliseum cups hold important items.",
    )
    locations_group.add_argument(
        "--hundred_acre_wood",
        choices=["Yes", "No"],
        default=presets["hundred_acre_wood"],
        metavar="100 Acre Wood",
        help="Determines if important items can be found in the 100 Acre Wood.",
    )
    locations_group.add_argument(
        "--jungle_slider",
        choices=["Yes", "No"],
        default=presets["jungle_slider"],
        metavar="Jungle Slider",
        help="Determines if important items can be found in the Jungle Slider minigame.",
    )
    locations_group.add_argument(
        "--randomize_emblem_pieces",
        choices=["Yes", "No"],
        default=presets["randomize_emblem_pieces"],
        metavar="Randomize Emblem Pieces",
        help="Determines whether the Emblem Piece checks in Hollow Bastion are randomized.",
    )
    locations_group.add_argument(
        "--randomize_postcards",
        choices=["All", "Chests", "None"],
        default=presets["randomize_postcards"],
        metavar="Randomize Postcards",
        help="Determines if Postcards should be in their vanilla locations, all randomized, or if only the postcard that would appear in chests should be randomized.",
    )
    levels_group.add_argument(
        "--exp_multiplier",
        widget="Slider",
        gooey_options={"min": 1, "max": 8, "increment": 1},
        default=int(presets["exp_multiplier"]),
        metavar="EXP Multiplier",
        help="Determines the amount of experience party members need to level up.",
    )
    levels_group.add_argument(
        "--level_checks",
        widget="Slider",
        gooey_options={"min": 0, "max": 99, "increment": 1},
        default=int(presets["level_checks"]),
        metavar="Level Checks",
        help="Determines the latest level for which rewards can be found.",
    )
    levels_group.add_argument(
        "--slot_2_level_checks",
        widget="Slider",
        gooey_options={"min": 0, "max": 33, "increment": 1},
        default=int(presets["slot_2_level_checks"]),
        metavar="Slot 2 Level Checks",
        help="Determines the amount of secondary bonuses are found on levels.",
    )
    levels_group.add_argument(
        "--max_level_for_slot_2_level_checks",
        widget="Slider",
        gooey_options={"min": 2, "max": 100, "increment": 1},
        default=int(presets["max_level_for_slot_2_level_checks"]),
        metavar="Max Level for Slot 2 Level Checks",
        help="Determines the maximum level which can yield a secondary bonus.",
    )
    levels_group.add_argument(
        "--force_stats_on_levels",
        widget="Slider",
        gooey_options={"min": 2, "max": 101, "increment": 1},
        default=int(presets["force_stats_on_levels"]),
        metavar="Force Stats on Levels Starting at Level",
        help="Determines at which level can only stat increases can be found.",
    )
    levels_group.add_argument(
        "--strength_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 100, "increment": 1},
        default=int(presets["strength_increases"]),
        metavar="Strength Increases",
        help="Determines how many strength increases are in the item pool.",
    )
    levels_group.add_argument(
        "--defense_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 100, "increment": 1},
        default=int(presets["defense_increases"]),
        metavar="Defense Increases",
        help="Determines how many defense increases are in the item pool.",
    )
    levels_group.add_argument(
        "--hp_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 100, "increment": 1},
        default=int(presets["hp_increases"]),
        metavar="HP Increases",
        help="Determines how many HP increases are in the item pool.",
    )
    levels_group.add_argument(
        "--ap_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 100, "increment": 1},
        default=int(presets["ap_increases"]),
        metavar="AP Increases",
        help="Determines how many AP increases are in the item pool.",
    )
    levels_group.add_argument(
        "--mp_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 20, "increment": 1},
        default=int(presets["mp_increases"]),
        metavar="MP Increases",
        help="Determines how many MP increases are in the item pool.",
    )
    levels_group.add_argument(
        "--accessory_slot_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 6, "increment": 1},
        default=int(presets["accessory_slot_increases"]),
        metavar="Accessory Slot Increases",
        help="Determines how many accessory slot increases are in the item pool.",
    )
    levels_group.add_argument(
        "--item_slot_increases",
        widget="Slider",
        gooey_options={"min": 0, "max": 5, "increment": 1},
        default=int(presets["item_slot_increases"]),
        metavar="Item Slot Increases",
        help="Determines how many item slot increases are in the item pool.",
    )
    keyblades_group.add_argument(
        "--keyblades_unlock_chests",
        choices=["Yes", "No"],
        default=presets["keyblades_unlock_chests"],
        metavar="Keyblades Unlock Chests",
        help="Determines if chests in worlds can only be opened if you have that world's corresponding keyblade.",
    )
    keyblades_group.add_argument(
        "--keyblade_stats",
        choices=["Vanilla", "Randomize", "Shuffle"],
        default=presets["keyblade_stats"],
        metavar="Keyblade Stats",
        help="Determines if keyblade stats be shuffled, randomized, or remain vanilla.",
    )
    keyblades_group.add_argument(
        "--bad_starting_weapons",
        choices=["Yes", "No"],
        default=presets["bad_starting_weapons"],
        metavar="Bad Starting Weapons",
        help="Determines if the Kingdom Key and Dream weapons should have vanilla stats.",
    )
    keyblades_group.add_argument(
        "--keyblade_max_strength",
        widget="Slider",
        gooey_options={"min": 0, "max": 20, "increment": 1},
        default=int(presets["keyblade_max_strength"]),
        metavar="Keyblade Max STR",
        help="If keyblade stats are randomized, determines the max strength increase a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_min_strength",
        widget="Slider",
        gooey_options={"min": 0, "max": 20, "increment": 1},
        default=int(presets["keyblade_min_strength"]),
        metavar="Keyblade Min STR",
        help="If keyblade stats are randomized, determines the min strength increase a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_max_crit_rate",
        widget="Slider",
        gooey_options={"min": 0, "max": 200, "increment": 1},
        default=int(presets["keyblade_max_crit_rate"]),
        metavar="Keyblade Crit Rate",
        help="If keyblade stats are randomized, determines the max crit rate a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_min_crit_rate",
        widget="Slider",
        gooey_options={"min": 0, "max": 200, "increment": 1},
        default=int(presets["keyblade_min_crit_rate"]),
        metavar="Keyblade Min Crit Rate",
        help="If keyblade stats are randomized, determines the min crit rate a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_max_crit_bonus",
        widget="Slider",
        gooey_options={"min": 0, "max": 16, "increment": 1},
        default=int(presets["keyblade_max_crit_bonus"]),
        metavar="Keyblade Max Crit Bonus",
        help="If keyblade stats are randomized, determines the max crit bonus a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_min_crit_bonus",
        widget="Slider",
        gooey_options={"min": 0, "max": 16, "increment": 1},
        default=int(presets["keyblade_min_crit_bonus"]),
        metavar="Keyblade Min Crit Bonus",
        help="If keyblade stats are randomized, determines the min crit bonus a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_max_recoil",
        widget="Slider",
        gooey_options={"min": 1, "max": 90, "increment": 1},
        default=int(presets["keyblade_max_recoil"]),
        metavar="Keyblade Max Recoil",
        help="If keyblade stats are randomized, determines the max recoil a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_min_recoil",
        widget="Slider",
        gooey_options={"min": 1, "max": 90, "increment": 1},
        default=int(presets["keyblade_min_recoil"]),
        metavar="Keyblade Min Recoil",
        help="If keyblade stats are randomized, determines the min recoil a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_max_mp",
        widget="Slider",
        gooey_options={"min": -2, "max": 5, "increment": 1},
        default=int(presets["keyblade_max_mp"]),
        metavar="Keyblade Max MP",
        help="If keyblade stats are randomized, determines the max MP bonus a keyblade can yield.",
    )
    keyblades_group.add_argument(
        "--keyblade_min_mp",
        widget="Slider",
        gooey_options={"min": -2, "max": 5, "increment": 1},
        default=int(presets["keyblade_min_mp"]),
        metavar="Keyblade Min MP",
        help="If keyblade stats are randomized, determines the min MP bonus a keyblade can yield.",
    )
    misc_group.add_argument(
        "--starting_worlds",
        widget="Slider",
        gooey_options={"min": 0, "max": 10, "increment": 1},
        default=int(presets["starting_worlds"]),
        metavar="Starting Worlds",
        help="Determines the amount of worlds the player starts with in addition to Traverse Town.  These are given by the server, and are received after connection.",
    )
    misc_group.add_argument(
        "--starting_tools",
        choices=["Yes", "No"],
        default=presets["starting_tools"],
        metavar="Starting Tools",
        help="Determines if Sora starts with Scan and Dodge Roll.  These are given by the server, and are received after connection.",
    )
    locations_group.add_argument(
        "--randomize_puppies",
        choices=["Yes", "No"],
        default=presets["randomize_puppies"],
        metavar="Randomize Puppies",
        help="Determines if puppies are randomized.",
    )
    locations_group.add_argument(
        "--puppy_value",
        widget="Slider",
        gooey_options={"min": 1, "max": 99, "increment": 1},
        default=int(presets["puppy_value"]),
        metavar="Puppy Value",
        help='If puppies are randomized, determines how many puppies each "Puppy" item is worth.',
    )
    misc_group.add_argument(
        "--interact_in_battle",
        choices=["Yes", "No"],
        default=presets["interact_in_battle"],
        metavar="Interact in Battle",
        help="Determines if Sora can interact in battle.",
    )
    misc_group.add_argument(
        "--advanced_logic",
        choices=["Yes", "No"],
        default=presets["advanced_logic"],
        metavar="Advanced Logic",
        help="Determines if the player is expected to do advanced tricks to reach certain locations.",
    )
    misc_group.add_argument(
        "--extra_shared_abilities",
        choices=["Yes", "No"],
        default=presets["extra_shared_abilities"],
        metavar="Extra Shared Abilities",
        help="Determines if the item pool contains additional shared abilities, which stack.  For example, more High Jumps make you jump higher, more Glides make you glide faster.",
    )
    misc_group.add_argument(
        "--exp_zero_in_pool",
        choices=["Yes", "No"],
        default=presets["exp_zero_in_pool"],
        metavar="EXP Zero in Pool",
        help="Determines if EXP Zero should be shuffled into the item pool.",
    )
    misc_group.add_argument(
        "--randomize_party_member_starting_accessories",
        choices=["Yes", "No"],
        default=presets["randomize_party_member_starting_accessories"],
        metavar="Randomize Party Member Starting Accessories",
        help="Determines if the 10 starting accessories (normally given to Aladdin, Ariel, Jack, Peter Pan, and Beast) are randomized and distributed amongst all party members randomly.",
    )
    misc_group.add_argument(
        "--death_link",
        choices=["Off", "Toggle", "On"],
        default=presets["death_link"],
        metavar="Death Link",
        help="If another player is KO'ed, so is Sora.  The opposite is also true.",
    )
    misc_group.add_argument(
        "--donald_death_link",
        choices=["Yes", "No"],
        default=presets["donald_death_link"],
        metavar="Donald Death Link",
        help="If Donald is KO'ed, so is Sora.",
    )
    misc_group.add_argument(
        "--goofy_death_link",
        choices=["Yes", "No"],
        default=presets["goofy_death_link"],
        metavar="Goofy Death Link",
        help="If Goofy is KO'ed, so is Sora.",
    )
    misc_group.add_argument(
        "--remote_items",
        choices=["Off", "Allow", "Full"],
        default=presets["remote_items"],
        metavar="Remote Items",
        help="Determines if items can be placed on locations in your own world in such a way that will force them to be remote items.\n"
        + "Off: When your items are placed in your world, they can only be placed in locations that they can be acquired without server connection (stats on levels, items in chests, etc).\n"
        + "Allow: When your items are placed in your world, items that normally can't be placed in a location in-game are simply made remote (stats in chests, abilities on static events, etc).\n"
        + "Full: All items are remote.  Use this when doing something like a co-op seed.",
    )
    misc_group.add_argument(
        "--shorten_go_mode",
        choices=["Yes", "No"],
        default=presets["shorten_go_mode"],
        metavar="Shorten Go Mode",
        help="Determines if the player should be warped to the final cutscene after defeating Ansem 1 > Darkside > Ansem 2.",
    )
    synth_group.add_argument(
        "--mythril_price",
        widget="Slider",
        gooey_options={"min": 100, "max": 5000, "increment": 1},
        default=int(presets["mythril_price"]),
        metavar="Mythril Price",
        help="Cost of mythril in shops",
    )
    synth_group.add_argument(
        "--mythril_in_pool",
        widget="Slider",
        gooey_options={"min": 16, "max": 30, "increment": 1},
        default=int(presets["mythril_in_pool"]),
        metavar="Mythril In Pool",
        help="Number of mythril in the item pool",
    )
    synth_group.add_argument(
        "--orichalcum_price",
        widget="Slider",
        gooey_options={"min": 100, "max": 5000, "increment": 1},
        default=int(presets["orichalcum_price"]),
        metavar="Orichalcum Price",
        help="Cost of orichalcum in shops",
    )
    synth_group.add_argument(
        "--orichalcum_in_pool",
        widget="Slider",
        gooey_options={"min": 17, "max": 30, "increment": 1},
        default=int(presets["orichalcum_in_pool"]),
        metavar="Orichalcum In Pool",
        help="Number of orichalcum in the item pool",
    )
    misc_group.add_argument(
        "--one_hp",
        choices=["Yes", "No"],
        default=presets["one_hp"],
        metavar="One HP",
        help="If on, forces Sora's max HP to 1 and removes the low health warning sound.",
    )
    misc_group.add_argument(
        "--four_by_three",
        choices=["Yes", "No"],
        default=presets["four_by_three"],
        metavar="4by3",
        help="If on, changes the aspect ratio to 4 by 3.",
    )
    misc_group.add_argument(
        "--beep_hack",
        choices=["Yes", "No"],
        default=presets["beep_hack"],
        metavar="Beep Hack",
        help="If on, removes low health warning sound.  Works up to max health of 41.",
    )
    misc_group.add_argument(
        "--consistent_finishers",
        choices=["Yes", "No"],
        default=presets["consistent_finishers"],
        metavar="Consistent Finishers",
        help="If on, 30% chance finishers are now 100% chance.",
    )
    misc_group.add_argument(
        "--early_skip",
        choices=["Yes", "No"],
        default=presets["early_skip"],
        metavar="Early Skip",
        help="If on, allows skipping cutscenes without waiting for them.",
    )
    misc_group.add_argument(
        "--fast_camera",
        choices=["Yes", "No"],
        default=presets["fast_camera"],
        metavar="Fast Camera",
        help="If on, speeds up camera movement and camera centering.",
    )
    misc_group.add_argument(
        "--faster_animations",
        choices=["Yes", "No"],
        default=presets["faster_animations"],
        metavar="Faster Animations",
        help="If on, speeds up animations during which you can't play.",
    )
    misc_group.add_argument(
        "--unlock_0_volume",
        choices=["Yes", "No"],
        default=presets["unlock_0_volume"],
        metavar="Unlock 0 Volume",
        help="If on, volume 1 mutes the audio channel.",
    )
    misc_group.add_argument(
        "--unskippable",
        choices=["Yes", "No"],
        default=presets["unskippable"],
        metavar="Unskippable",
        help="If on, makes unskippable cutscenes skippable.",
    )
    misc_group.add_argument(
        "--auto_save",
        choices=["Yes", "No"],
        default=presets["auto_save"],
        metavar="Auto Save",
        help="If on, enables auto saving.\nPress L1+L2+R1+R2+D-Pad Left to instantly load continue state.\nPress L1+L2+R1+R2+D-Pad Right to instantly load autosave.",
    )
    misc_group.add_argument(
        "--warp_anywhere",
        choices=["Yes", "No"],
        default=presets["warp_anywhere"],
        metavar="Warp Anywhere",
        help="If on, enables the player to warp at any time, even when not at a save point.\nPress L1+L2+R2+Select to open the Save/Warp menu at any time.",
    )
    ap_costs_group.add_argument(
        "--randomize_ap_costs",
        choices=["Off", "Randomize", "Distribute"],
        default=presets["randomize_ap_costs"],
        metavar="Randomize AP Costs",
        help="Off: No randomization\nShuffle: Ability AP Costs will be shuffled amongst themselves.\nRandomize: Ability AP Costs will be randomized to the specified max and min.\nDistribute: Ability AP Costs will totalled and re-distributed randomly between the specified max and min.",
    )
    ap_costs_group.add_argument(
        "--max_ap_cost",
        widget="Slider",
        gooey_options={"min": 4, "max": 9, "increment": 1},
        default=int(presets["max_ap_cost"]),
        metavar="Max AP Cost",
        help="If Randomize AP Costs is set to Randomize or Distribute, this defined the max AP cost an ability can have.",
    )
    ap_costs_group.add_argument(
        "--min_ap_cost",
        widget="Slider",
        gooey_options={"min": 0, "max": 2, "increment": 1},
        default=int(presets["min_ap_cost"]),
        metavar="Min AP Cost",
        help="If Randomize AP Costs is set to Randomize or Distribute, this defined the minimum AP cost an ability can have.",
    )

    args = parser.parse_args()
    write_presets("settings", args)
    result = create_yaml(args)
    slot_name = getattr(args, "slot_name")
    if slot_name is None:
        raise ValueError("Error: slot_name is a required field.")
    
    output_yaml(result, slot_name=slot_name)


if __name__ == "__main__":
    main()
