import generate_post_data
import requests as req
import base64
from struct import unpack
import json, re
from decimal import Decimal

from google.protobuf.json_format import MessageToJson, MessageToDict

from protobuf_inspector_master.main import run as protobuf_decoder

from collections import OrderedDict


eggs = [  # name, value
    ("Edible", 0.25),
    ("Superfood", 1.25),
    ("Medical", 6.25),
    ("Rocket Fuel", 30),
    ("Super Material", 150),
    ("Fusion", 700),
    ("Quantum", 3000),
    ("Immortality", 12500),
    ("Tachyon", 50000),
    ("Graviton", 175000),
    ("Dilithium", 525000),
    ("Prodigy", 1500000),
    ("Terraform", 10000000),
    ("Antimatter", 1000000000),
    ("Dark Matter", 100000000000),
    ("AI", 1000000000000),
    ("Nebula", 15000000000000),
    ("Universe", 100000000000000),
    ("Enlightenment", 0.000000001)
    ]
boosts_dictionary = {  # name
    "quantum_bulb": "Quantum Warming Bulb",
    "jimbos_blue": "Jimbo's Excellent Bird Feed",
    "jimbos_blue_big": "Jimbo's Excellent Bird Feed (Large)",
    "jimbos_purple": "Jimbo's Premium Bird Feed",
    "jimbos_purple_big": "Jimbo's Premium Bird Feed (Large)",
    "jimbos_orange": "Jimbo's Best Bird Feed",
    "jimbos_orange_big": "Jimbo's Best Bird Feed (Large)",
    "tachyon_prism_blue": "Tachyon Prism",
    "tachyon_prism_blue_big": "Large Tachyon Prism",
    "tachyon_prism_purple": "Powerful Tachyon Prism",
    "tachyon_prism_purple_big": "Epic Tachyon Prism",
    "tachyon_prism_orange": "Legendary Tachyon Prism",
    "tachyon_prism_orange_big": "Supreme Tachyon Prism",
    "boost_beacon_blue": "Boost Beacon",
    "boost_beacon_purple": "Epic Boost Beacon",
    "boost_beacon_blue_big": "Large Boost Beacon",
    "boost_beacon_orange": "Legendary Boost Beacon",
    "soul_beacon_blue": "Soul Beacon",
    "soul_beacon_purple": "Epic Soul Beacon",
    "soul_beacon_orange": "Legendary Soul Beacon",
    "subsidy_application": "Subsidy Application",
    "blank_check": "Blank Check",
    "money_printer": "Money Printer",
    "soul_mirror_blue": "Soul Mirror",
    "soul_mirror_purple": "Epic Soul Mirror",
    "soul_mirror_orange": "Legendary Soul Mirror"}

research_dictionary = {  # name, tier, max
    "comfy_nests": ("Comfortable Nests", 1, 50),
    "nutritional_sup": ("Nutritional Supplements", 1, 40),
    "better_incubators": ("Better Incubators", 1, 15),
    "excitable_chickens": ("Excitable Chickens", 1, 25),
    "hab_capacity1": ("Hen House Remodel", 2, 8),
    "internal_hatchery1": ("Internal Hatcheries", 2, 10),
    "padded_packaging": ("Padded Packaging", 2, 30),
    "hatchery_expansion": ("Hatchery Expansion", 2, 10),
    "bigger_eggs": ("Bigger Eggs", 2, 1),
    "internal_hatchery2": ("Internal Hatchery Upgrades", 3, 10),
    "leafsprings": ("Improved Leafsprings", 3, 30),
    "vehicle_reliablity": ("Vehicle Reliability", 3, 2),
    "rooster_booster": ("Rooster Booster", 3, 25),
    "coordinated_clucking": ("Coordinated Clucking", 3, 50),
    "hatchery_rebuild1": ("Hatchery Rebuild", 4, 1),
    "usde_prime": ("USDE Prime Certification", 4, 1),
    "hen_house_ac": ("Hen House A/C", 4, 50),
    "superfeed": ("Super-Feed™ Diet", 4, 35),
    "microlux": ("Microlux™ Chicken Suites", 4, 10),
    "compact_incubators": ("Compact Incubators", 5, 10),
    "lightweight_boxes": ("Lightweight Boxes", 5, 40),
    "excoskeletons": ("Depot Worker Exoskeletons", 5, 2),
    "internal_hatchery3": ("Internal Hatchery Expansion", 5, 15),
    "improved_genetics": ("Improved Genetics", 5, 30),
    "traffic_management": ("Traffic Management", 6, 2),
    "motivational_clucking": ("Motivational Clucking", 6, 50),
    "driver_training": ("Driver Training", 6, 30),
    "shell_fortification": ("Shell Fortification", 6, 60),
    "egg_loading_bots": ("Egg Loading Bots", 7, 2),
    "super_alloy": ("Super Alloy Frames", 7, 50),
    "even_bigger_eggs": ("Even Bigger Eggs", 7, 5),
    "internal_hatchery4": ("Internal Hatchery Expansion", 7, 30),
    "quantum_storage": ("Quantum Egg Storage", 8, 20),
    "genetic_purification": ("Genetic Purification", 8, 100),
    "internal_hatchery5": ("Machine Learning Incubators", 8, 250),
    "time_compress": ("Time Compression", 8, 20),
    "hover_upgrades": ("Hover Upgrades", 9, 25),
    "graviton_coating": ("Graviton Coating", 9, 7),
    "grav_plating": ("Grav Plating", 9, 25),
    "chrystal_shells": ("Crystalline Shelling", 9, 100),
    "autonomous_vehicles": ("Autonomous Vehicles", 10, 5),
    "neural_linking": ("Neural Linking", 10, 30),
    "telepathic_will": ("Telepathic Will", 10, 50),
    "enlightened_chickens": ("Enlightened Chickens", 10, 150),
    "dark_containment": ("Dark Containment", 11, 25),
    "atomic_purification": ("Atomic Purification", 11, 50),
    "multi_layering": ("Multiversal Layering", 11, 3),
    "timeline_diversion": ("Timeline Diversion", 11, 50),
    "wormhole_dampening": ("Wormhole Dampening", 12, 25),
    "eggsistor": ("Eggsistor Miniturization", 12, 100),
    "micro_coupling": ("Gravitron Coupling", 12, 5),
    "neural_net_refine": ("Neural Net Refinement", 12, 25),
    "matter_reconfig": ("Matter Reconfiguration", 13, 500),
    "timeline_splicing": ("Timeline Splicing", 13, 1),
    "hyper_portalling": ("Hyper Portalling", 13, 25),
    "relativity_optimization": ("Relativity Optimization", 13, 10)}

epic_research_dictionary = {  # name, max
    "hold_to_hatch": ("Hold to Hatch", 15),
    "epic_hatchery": ("Epic Hatchery", 20),
    "epic_internal_incubators": ("Epic Int. Hatcheries", 20),
    "video_doubler_time": ("Video Doubler Time", 12),
    "epic_clucking": ("Epic Clucking", 20),
    "epic_multiplier": ("Epic Multiplier", 100),
    "cheaper_contractors": ("Cheaper Contractors", 10),
    "bust_unions": ("Bust Unions", 10),
    "cheaper_research": ("Lab Upgrade", 10),
    "epic_silo_quality": ("Silo Quality", 40),
    "silo_capacity": ("Silo Capacity", 20),
    "int_hatch_sharing": ("Internal Hatchery Sharing", 10),
    "int_hatch_calm": ("Internal Hatchery Calm", 20),
    "accounting_tricks": ("Accounting Tricks", 20),
    "soul_eggs": ("Soul Food", 140),
    "prestige_bonus": ("Prestige Bonus", 20),
    "drone_rewards": ("Drone Rewards", 20),
    "epic_egg_laying": ("Epic Comfy Nests", 20),
    "transportation_lobbyist": ("Transportation Lobbyists", 30),
    "warp_shift": ("Warp Shift", 16),
    "prophecy_bonus": ("Prophecy Bonus", 5),
    "hold_to_research": ("Hold to Research", 8)}

class Profile():

    # population @ <varint>_6_815
    # epic research @ <message>_9_72
    # boosts @ <message>_30_458
    # se @ <64bit>_34

    def transform_number(self, number, number2=None, just_transform=False):

        def exponent(number):
            _, digits, exponent = Decimal(number).as_tuple()
            return len(digits) + exponent - 1

        def mantissa(number):
            return Decimal(number).scaleb(-exponent(number)).normalize()

        def get_abbreviation(number):
            exp = exponent(number)
            dictionary = ['M', 'B', 'T', 'q', 'Q', 's', 'S', 'O', 'N', 'd', 'U', 'D', 'Td', 'qd', 'Qd', 'sd', 'Sd', 'Od', 'Nd', 'V', 'uV', 'dV', 'tV', 'qV', 'QV' , 'sV', 'SV', 'oV', 'nV', 'Tr', 'uTr']
            if exp > 5:
                return dictionary[exp // 3 - 2]
            return ""

        def prepare_number(number):
            if not just_transform:
                hex_val = number.split(" / ")[0][2:]
                unpacked = unpack("!d", bytes.fromhex(hex_val))[0]
            else:
                unpacked = number
            clean = '{0:.0f}'.format(unpacked)
            clean_dotted = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(clean))
            return unpacked, clean, clean_dotted

        if number2 is None:
            unpacked, clean, clean_dotted = prepare_number(number)
            transformed = str(round(mantissa(clean) * (10 ** (exponent(clean) % 3)), 3)) + get_abbreviation(clean)
        else:
            unpacked = number + number2
            clean = '{0:.0f}'.format(unpacked)
            transformed = str(round(mantissa(clean) * (10 ** (exponent(clean) % 3)), 3)) + get_abbreviation(clean)
            clean_dotted = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(clean))
        return unpacked, transformed, clean, clean_dotted

    def __init__(self):
        pass

    def add_user_id(self, user_id):
        self.user_id = user_id[1:-1]

    def add_username(self, username):
        self.username = username[1:-1]

    def add_drone_takedowns(self, drone_takedowns):
        self.drone_takedowns = drone_takedowns

    def add_eggs_laid(self, eggs_laid, egg_count):
        try:
            self.eggs_laid
        except AttributeError:
            self.eggs_laid = OrderedDict()
        self.eggs_laid[eggs[egg_count][0] + " Egg"] = self.transform_number(eggs_laid)

    def add_presitges(self, prestiges):
        self.prestiges = prestiges

    def add_elite_drone_takedowns(self, elite_drone_takedowns):
        self.elite_drone_takedowns = elite_drone_takedowns

    def add_last_lifetime_earnings(self, last_lifetime_earnings):
        try:
            self.last_lifetime_earnings = self.transform_number(last_lifetime_earnings)
            self.lifetime_earnings = self.transform_number(self.last_lifetime_earnings[0], self.presige_earnings[0])
        except AttributeError:
            self.last_lifetime_earnings = self.transform_number(last_lifetime_earnings)

    def add_prophecy_eggs(self, prophecy_eggs):
        self.prophecy_eggs = prophecy_eggs

    def add_soul_eggs(self, soul_eggs):
        self.soul_eggs = self.transform_number(soul_eggs)

    def add_epic_research(self, epic_research):
        try:
            self.epic_research_list
        except AttributeError:
            self.epic_research_list = OrderedDict()
        key, value = None, None
        for item in epic_research.items():
            if "<chunk>" in item[0]:
                key = item[1][1:-1]
            if "<varint>" in item[0]:
                value = item[1]
            if key is not None and value is not None:
                self.epic_research_list[key] = int(value)
                return

    def add_research(self, research):
        try:
            self.research_list
        except AttributeError:
            self.research_list = OrderedDict()
        key, value = None, None
        for item in research.items():
            if "<chunk>" in item[0]:
                key = item[1][1:-1]
            if "<varint>" in item[0]:
                value = item[1]
            if key is not None and value is not None:
                self.research_list[key] = int(value)
                return

    def add_boost(self, boost):
        try:
            self.boost_list
        except AttributeError:
            self.boost_list = OrderedDict()
        key, value = None, None
        for item in boost.items():
            if "<chunk>" in item[0]:
                key = item[1][1:-1]
            if "<varint>" in item[0]:
                value = item[1]
            if key is not None and value is not None:
                self.boost_list[key] = int(value)
                return

    def add_current_egg(self, current_egg):
        self.current_egg = eggs[int(current_egg)-1][0]

    def add_prestige_earnings(self, presige_earnings):
        try:
            self.presige_earnings = self.transform_number(presige_earnings)
            self.lifetime_earnings = self.transform_number(self.last_lifetime_earnings[0], self.presige_earnings[0])
        except AttributeError:
            self.presige_earnings = self.transform_number(presige_earnings)

    def add_farm_population(self, farm_population):
        self.farm_population = self.transform_number(int(farm_population), just_transform=True)

    def print_(self):
        print("user_id:", self.user_id)
        print("username:", self.username)
        print("drone takedowns:", self.drone_takedowns)
        print("eggs laid:", self.eggs_laid)
        print("presiges:", self.prestiges)
        print("elite drone takedowns:", self.elite_drone_takedowns)
        print("last lifetime earnings:", self.last_lifetime_earnings[1])
        print("presige earnings:", self.presige_earnings[1])
        print("lifetime earnings:", self.lifetime_earnings[1])
        print("farm population:", self.farm_population)
        print("current egg:", self.current_egg)
        print("prophecy eggs:", self.prophecy_eggs)
        print("soul eggs:", self.soul_eggs)
        print("epic research:", self.epic_research_list)
        print("research:", self.research_list)
        print("boosts:", self.boost_list)

if __name__ == '__main__':
    
    POST_data = generate_post_data.run(write=True)
    data = {'data': POST_data}
    resp = req.post("http://www.auxbrain.com/ei/first_contact", data)
    response = resp.text

    brotobuf_response = base64.b64decode(response)

    
    f = open("protobuf_response.pb", "wb")
    f.write(brotobuf_response)
    f.close()
    

    protobuf_decoded = protobuf_decoder(open("protobuf_response.pb", "rb"))
    
    json_object = None
    json_main = None
    with open(r'screenshots/1/toJSON_result.json') as json_file:
        json_object = json.load(json_file)
        for attr in json_object:
            if json_object[attr] == "root":
                continue
            json_main = attr

    profile = Profile()

    counter = 0
    for attr in json_object[json_main]:
        if counter == 0:
            profile.add_user_id(json_object[json_main][attr])
        if counter == 1:
            profile.add_username(json_object[json_main][attr])
        if counter == 5:
            counter2 = 0
            for attr2 in json_object[json_main][attr]:
                if "<varint>_6_" in attr2:
                    profile.add_drone_takedowns(json_object[json_main][attr][attr2])
                if "<64bit>_8_" in attr2:
                    profile.add_eggs_laid(json_object[json_main][attr][attr2], counter2)
                    counter2 += 1
                if "<varint>_9_" in attr2:
                    profile.add_presitges(json_object[json_main][attr][attr2])
                if "<varint>_10_" in attr2:
                    profile.add_elite_drone_takedowns(json_object[json_main][attr][attr2])
        if counter == 6:
            for attr2 in json_object[json_main][attr]:
                if "<64bit>_6_" in attr2:
                    profile.add_last_lifetime_earnings(json_object[json_main][attr][attr2])
                if "<varint>_23_" in attr2:
                    profile.add_prophecy_eggs(json_object[json_main][attr][attr2])
                if "<64bit>_34_" in attr2:
                    profile.add_soul_eggs(json_object[json_main][attr][attr2])
                if "<message>_9_" in attr2:
                    profile.add_epic_research(json_object[json_main][attr][attr2])
                if "<message>_30_" in attr2:
                    profile.add_boost(json_object[json_main][attr][attr2])
        if counter == 9:
            for attr2 in json_object[json_main][attr]:
                if "<varint>_1_" in attr2:
                    profile.add_current_egg(json_object[json_main][attr][attr2])
                if "<64bit>_2_" in attr2:
                    profile.add_prestige_earnings(json_object[json_main][attr][attr2])
                if "<varint>_6_" in attr2:
                    profile.add_farm_population(json_object[json_main][attr][attr2])
                if "<message>_18_" in attr2:
                    profile.add_research(json_object[json_main][attr][attr2])
        counter += 1

    profile.print_()
