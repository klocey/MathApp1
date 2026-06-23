import random
import dash
from dash import html, dcc, Input, Output, State, callback_context

# ==========================================
#         THEME DATA & TEMPLATES
# ==========================================
THEME_DATA = {
    "Powerpuff Girls": {
        "bg_color": "#FFF0F5",        # Light pink blossom aura
        "card_border": "#AED6F1",    # Bubbles Blue
        "accent_color": "#FF69B4",   # Powerpuff Pink
        "button_shadow": "#D81B60",
        "question_border": "#2ECC71",# Buttercup Green
        "characters": ["Blossom", "Bubbles", "Buttercup", "Mojo Jojo", "Fuzzy Lumpkins", "Professor Utonium"],
        "items": ["Chemical X drops", "star stickers", "sweet cupcakes", "unbreakable hearts", "jars of jam"],
        "images": [
            "powerpuff/1.jpg", "powerpuff/2.jpg", "powerpuff/3.jpg", "powerpuff/4.webp", 
            "powerpuff/5.jpg", "powerpuff/6.jpg", "powerpuff/7.jpg", "powerpuff/8.webp"
        ],
        "templates": {
            "+": [
                "Blossom defeated {num1} bad guys in the morning and {num2} bad guys after lunch. How many bad guys did she defeat in total?",
                "The Mayor gave Bubbles {num1} star stickers for saving Townsville. Later, she earned {num2} more. How many stickers does she have now?",
                "Professor Utonium poured {num1} drops of Chemical X into a beaker, and then added {num2} more drops. How many drops are in the beaker?",
                "{name} found {num1} {item}. Then, {friend} gave them {num2} more! How many {item} does {name} have now?",
                "There are {num1} {item} hidden in the Powerpuff lab and {num2} {item} in a Pokéball. How many are there in total?",
            ],
            "-": [
                "Buttercup found {num1} runaway robots in downtown Townsville. She already smashed {num2} of them. How many robots are left to smash?",
                "Fuzzy Lumpkins had {num1} jars of jam on his property. {name} chased him away and took {num2} jars back. How many jars does Fuzzy have left?",
                "{name} had {num1} {item}. {friend} borrowed {num2} of them to save the day. How many {item} does {name} have left?",
                "The Powerpuff Girls had {num1} emergency calls today, but {name} quickly solved {num2} of them. How many emergency calls are still waiting?"

            ],
            "*": [
                "{name} has {num1} special bags. Each bag holds exactly {num2} {item}. How many {item} does {name} have altogether?",
                "Professor Utonium made {num1} rows of treats. Each row has {num2} treats. How many total treats did he make?",
                "Mojo Jojo is building {num1} giant laser beams. Each laser beam needs exactly {num2} batteries to turn on. How many batteries does he need in total?",
                "The Narrator said the Powerpuff Girls saved Townsville {num1} times this week! If they saved {num2} citizens each time, how many total citizens did they save?"
            ],
            "/": [
                "The villain HIM cast a spell creating {num1} creepy shadow-monsters. If {num2} heroes split up to fight them equally, how many monsters does each hero fight?",
                "Ms. Keane has {num1} crayons at Pokey Oaks Kindergarten. She wants to divide them equally among {num2} kids. How many crayons does each kid get?",
                "{name} wants to share {num1} {item} equally among {num2} friendly Pokémon. How many {item} does each Pokémon get?",
                "If Bubbles splits {num1} {item} into {num2} equal neat piles, how many {item} will be in each pile?",
            ]
        }
    },
    "Pokemon": {
        "bg_color": "#FEF9E7",        # Pikachu Yellow tint
        "card_border": "#F4D03F",    # Electric Gold
        "accent_color": "#E74C3C",   # Pokeball Red
        "button_shadow": "#922B21",
        "question_border": "#3498DB",# Great Ball Blue
        "characters": ["Pikachu", "Eevee", "Mew", "Ash Ketchum", "Charizard", "Snorlax"],
        "items": ["Pokéballs", "Razz Berries", "Gym Badges", "Shiny Stones", "Potions"],
        "images": [
            "pokemon/1.webp", "pokemon/2.webp", "pokemon/3.avif", "pokemon/4.webp", 
            "pokemon/5.webp", "pokemon/6.webp", "pokemon/7.jpg", "pokemon/8.jpg"
        ],
        "templates": {
            "+": [
                "{name} caught {num1} Wild Pokémon in the forest, and then encountered {num2} more near the river. How many Pokémon did they find?",
                "Ash has {num1} {item} in his backpack. Brock gives him {num2} more to prepare for the Gym Battle. How many {item} does Ash have now?",
                "Misty found {num1} Staryu swimming in the Cerulean Gym pool and {num2} Psyduck resting nearby. How many Water-type Pokémon are there in total?",
                "A Pokémon Center has {num1} hurt Pokémon resting in the lobby and {num2} more checking in with Nurse Joy. How many total Pokémon are at the Center?",
                "Officer Jenny found {num1} missing Squirtles in the city park. Later, her Growlithe tracked down {num2} more. How many Squirtles did they rescue?",
                "{name} used {num1} Max Potions to heal their team, but they still have {num2} Max Potions left in their bag. How many did they start with?"
            ],
            "-": [
                "A wild Snorlax was guarding {num1} {item}. {name} used a Poké-Flute and safely collected {num2} of them. How many are left with Snorlax?",
                "Team Rocket stole {num1} Pokéballs, but Eevee used Swift to knock {num2} Pokéballs back out of their basket! How many do Team Rocket still have?",
                "Professor Oak had {num1} Fire-type evolution stones in his lab. He gave {num2} of them to trainers to evolve their Growlithes. How many stones are left?",
                "A wild Jigglypuff sang a song and put {num1} trainers to sleep. {num2} of those trainers woke up early by using an Awakening item. How many trainers are still asleep?",
                "A trainer brought {num1} Potions to a battle against gym leader Lt. Surge. Pikachu's Thunderbolt destroyed {num2} of them. How many Potions does the trainer have left?",
                "{name} was carrying {num1} Ultra Balls. They threw {num2} Ultra Balls trying to catch a legendary Mewtwo. How many Ultra Balls do they have left?"
            ],
            "*": [
                "{name} has {num1} Pokémon eggs. Each egg requires {num2} kilometers of walking to hatch. How many total kilometers does {name} need to walk?",
                "Pikachu unleashed {num1} Thunderbolts. If each Thunderbolt sparks {num2} sparks of electricity, how many sparks flew in total?",
                "Charizard used Flamethrower {num1} times. If each Flamethrower melts exactly {num2} blocks of ice, how many blocks of ice did Charizard melt?",
                "A Poké-Mart sells bundles of items. If {name} buys {num1} boxes, and each box contains {num2} Revive crystals, how many Revives do they get?",
                "During a double battle, {num1} friendly Pokémon each used the move Swift. If each Swift attack shoots out {num2} glowing stars, how many stars are on the screen?",
                "A group of Diglett dug {num1} tunnels under Diglett's Cave. If each tunnel goes past {num2} underground rocks, how many rocks did they tunnel past?"
            ],
            "/": [
                "{name} found {num1} delicious Razz Berries and wants to share them equally among {num2} hungry Eevees. How many berries does each Eevee get?",
                "Professor Oak has {num1} starter Pokémon that need to be sent evenly to {num2} different towns. How many Pokémon go to each town?",
                "Ash gathered {num1} magical Exp. Candies. He wants to divide them up evenly to level up his {num2} favorite party Pokémon. How many candies does each Pokémon get?",
                "A group of wild Meowth collected {num1} shiny gold coins from an island. If they split the coins equally into {num2} piles, how many coins are in each pile?",
                "Nurse Joy has {num1} clean blankets to hand out to {num2} tired Chanseys at the clinic. If she shares them evenly, how many blankets does each Chansey get?",
                "A trainer needs to sort {num1} TM battle moves into {num2} organized storage boxes. If each box gets the exact same number, how many TMs fit in a single box?"
            ]
        },
    },
    "Adventure Time": {
        "bg_color": "#E8F8F5",        # Ooo Sky Blue-Green
        "card_border": "#5DADE2",    # Finn's Backpack Blue
        "accent_color": "#F4D03F",   # Jake's Gold Magic Yellow
        "button_shadow": "#B7950B",
        "question_border": "#BB8FCE",# LSP Lumpy Purple
        "characters": ["Finn", "Jake", "Princess Bubblegum", "Marceline", "BMO", "Ice King"],
        "items": ["swords", "bacon pancakes", "Candy Kingdom gems", "ancient artifacts", "apples"],
        "images": [
            "adventuretime/1.webp", "adventuretime/2.webp", "adventuretime/3.webp", "adventuretime/4.webp", 
            "adventuretime/5.jpg", "adventuretime/6.avif", "adventuretime/7.webp", "adventuretime/8.jpg"
        ],
        "templates": {
            "+": [
                "Finn gathered {num1} {item} from the Dungeon, and Jake found another {num2} using his magic stretchy paws. How many total did they bring home?",
                "Princess Bubblegum made {num1} smart candy citizens, and then created {num2} more to guard the gate. How many candy people did she make?",
                "Lady Rainicorn flew across {num1} red rainbows in the morning and {num2} blue rainbows in the evening. How many colorful rainbows did she cross in total?",
                "Tree Trunks baked {num1} hot apple pies for Finn and {num2} sweet berry pies for Jake. How many total pies did she bake for her friends?",
                "BMO counted {num1} skateboards in Finn and Jake's treehouse, and then found {num2} more hidden under the couch. How many skateboards are there altogether?",
                "The Flame King ordered his guards to light {num1} fire torches inside the Fire Kingdom, and {num2} extra torches outside the palace. How many torches were lit?"
            ],
            "-": [
                "The Ice King kidnapped {num1} penguins, but Gunther led {num2} of them on a secret escape route! How many penguins are left in the Ice Castle?",
                "Marceline had {num1} red apples, but she sucked the red out of {num2} of them. How many apples still have their color left?",
                "Cinnamon Bun was carrying {num1} fragile jelly tarts across the Candy Kingdom, but he tripped and dropped {num2} of them. How many jelly tarts did he save?",
                "Peppermint Butler had {num1} ancient spellbooks in his secret library. He locked {num2} of them away so Finn wouldn't find them. How many spellbooks are left out?",
                "The Earl of Lemongrab shouted at {num1} lemon citizens, but {num2} of them ran away because he was being too loud. How many lemon citizens had to stay and listen?",
                "Lumpy Space Princess brought {num1} cans of smooth lump-cream to a party, but she got dramatic and threw {num2} cans out the window. How many cans are left?"
            ],
            "*": [
                "BMO built {num1} video game levels. Each level features exactly {num2} golden coins. How many total coins did BMO program?",
                "Jake can bake {num1} batches of bacon pancakes. If each batch makes {num2} pancakes, how many delicious pancakes did he cook?",
                "Finn found {num1} secret pages inside the Enchiridion hero handbook. If each page shows {num2} drawings of magical swords, how many swords are drawn in total?",
                "Marceline played {num1} rock concerts in the Nightosphere. If she rocked out to {num2} screaming demons at every single show, how many total demons heard her play?",
                "Princess Bubblegum setup {num1} rows of test tubes in her science lab. If each row contains exactly {num2} glowing chemical solutions, how many solutions did she prepare?",
                "Susan Strong gathered {num1} groups of Hyuman tribespeople. If each group carries {num2} glowing techno-sticks, how many techno-sticks are there in total?"
            ],
            "/": [
                "Princess Bubblegum needs to distribute {num1} science test tubes evenly across {num2} laboratory tables. How many tubes go on each table?",
                "Finn wants to share {num1} {item} equally among {num2} Lumpy Space villagers. How many does each villager receive?",
                "Jake wants to split {num1} slices of everything-burrito equally among {num2} of his favorite multi-flavored pups. How many slices does each puppy get?",
                "The Ice King wants to divide {num1} ice-gems evenly among his {num2} favorite wizard crowns. How many ice-gems will he place onto each crown?",
                "Peppermint Butler has {num1} shadow-potions to hand out evenly to {num2} spooky ghosts. How many shadow-potions does each ghost get?",
                "Prisma the Wish Master split {num1} floating pickles evenly into {num2} cosmic bowls for Finn and Jake. How many pickles are in a single cosmic bowl?"
            ]
        }
    },
    "TMNT": {
        "bg_color": "#EAFAF1",        # Sewer Green/Ooze
        "card_border": "#E67E22",    # Michelangelo Orange
        "accent_color": "#2ECC71",   # Turtle Green
        "button_shadow": "#196F3D",
        "question_border": "#9B59B6",# Donatello Purple
        "characters": ["Leo", "Raph", "Donnie", "Mikey", "Splinter", "Shredder"],
        "items": ["pizza slices", "ninja throwing stars", "skateboards", "mutagen canisters"],
        "images": [
            "tmnt/1.webp", "tmnt/2.jpeg", "tmnt/3.webp", "tmnt/4.jpg", 
            "tmnt/5.jpg", "tmnt/6.webp", "tmnt/7.jpeg", "tmnt/8.png"
        ],
        "templates": {
            "+": [
                "Mikey ordered {num1} pepperoni pizzas and Raph ordered {num2} cheese pizzas. How many total pizzas are arriving at the sewer lair?",
                "Donnie collected {num1} broken computer parts and found {num2} more in a scrapyard. How many parts does he have to build gadgets?",
                "April O'Neil filmed {num1} news reports about heroic rescues in the morning and {num2} reports about mysterious green ooze at night. How many reports did she film?",
                "Casey Jones has {num1} broken hockey sticks in his sports bag. He goes to the store and buys {num2} baseball bats. How many sports weapons does he have now?",
                "The Mighty Mutanimals team has {num1} mutant heroes training in the hidden warehouse, and {num2} more guarding the docks. How many heroes are there in total?",
                "The Party Wagon needs {num1} gallons of regular fuel and {num2} gallons of special turtle-juice booster to run. How many total gallons of fuel does it hold?"
            ],
            "-": [
                "Shredder deployed {num1} Foot Clan ninjas into New York City, but Leo quickly stopped {num2} of them. How many Foot Clan ninjas are left?",
                "Splinter had {num1} meditation candles. The turtles accidentally knocked over {num2} of them during practice. How many candles are left?",
                "Bebop and Rocksteady stole {num1} laser blasters from a secure lab. Raph chased them and smashed {num2} blasters with his sais. How many blasters do the villains have left?",
                "Krang launched {num1} robotic rock soldiers from Dimension X, but the turtles trapped {num2} of them back inside the portal. How many rock soldiers are still on Earth?",
                "Mikey baked {num1} weird jelly-bean and marshmallow pizzas. The other turtles got grossed out and threw {num2} of them away. How many weird pizzas are left?",
                "{name} had {num1} smoke bombs to escape from the Foot Clan. They dropped {num2} bombs into the sewer water by accident. How many smoke bombs do they have left?"
            ],
            "*": [
                "The four turtles ate {num1} boxes of pizza. If each box had exactly {num2} slices inside, how many slices did they eat altogether?",
                "Raph practiced his ninja flips {num1} times per hour. If he practiced for {num2} hours, how many flips did he do?",
                "Leo practiced his twin-katana sword strikes. If he did {num1} sets of practice routines, and each routine had {num2} sword swings, how many total swings did he practice?",
                "Donnie is working on the Shellraiser truck's computer. The system has {num1} major circuits, and each circuit requires {num2} microchips. How many total microchips does he need?",
                "Master Splinter assigned {num1} training hours to each of his {num2} turtle sons this week. How many total hours of ninja training did the turtles complete?",
                "Shredder's secret hideout has {num1} storage rooms. If each room has exactly {num2} spike-shields waiting for Foot Soldiers, how many spike-shields are there in total?"
            ],
            "/": [
                "Donnie has {num1} ninja throwing stars that he wants to divide equally into {num2} equipment belts. How many stars go into each belt?",
                "The turtles intercepted {num1} stolen mutagen canisters. If they divide them up equally into {num2} secure vaults, how many canisters fit in each vault?",
                "Mikey wants to divide {num1} hot pepperoni slices evenly among {num2} hungry pizza boxes. How many pepperoni slices will go into each box?",
                "Casey Jones found {num1} lost spray-paint cans in the subway. He splits them evenly into {num2} duffel bags to carry them home. How many cans fit in each bag?",
                "The Technodrome's main engine has {num1} warning lights. If the lights are divided evenly across {num2} control panels, how many warning lights are on each panel?",
                "April has {num1} photographs of turtle sightings to file away. If she divides them evenly into {num2} secret news folders, how many photos go into each folder?"
            ]
        }
    },
    "Transformers": {
        "bg_color": "#EBF5FB",        # Metallic Cybertron Blue
        "card_border": "#34495E",    # Decepticon Steel Gray
        "accent_color": "#3498DB",   # Autobot Blue
        "button_shadow": "#1A5276",
        "question_border": "#E74C3C",# Optimus Prime Crimson Red
        "characters": ["Optimus Prime", "Bumblebee", "Megatron", "Starscream", "Grimlock"],
        "items": ["Energon cubes", "laser blasters", "Cybertronian gears", "space sparkplugs"],
        "images": [
            "transformers/1.avif", "transformers/2.avif", "transformers/3.jpg", "transformers/4.avif", 
            "transformers/5.jpg", "transformers/6.jpg", "transformers/7.jpg", "transformers/8.jpg"
        ],
        "templates": {
            "+": [
                "Optimus Prime called {num1} Autobots to Earth, and Bumblebee recruited {num2} more. How many total Autobots are ready to defend Earth?",
                "The Autobots secured {num1} Energon cubes from the base and tracked down {num2} more. How many cubes do they have stored now?",
                "Soundwave deployed {num1} cassette spies like Laserbeak from his chest, and then launched {num2} more like Ravage. How many mechanical spies did he deploy?",
                "Ratchet repaired {num1} damaged Autobots in the morning and {num2} more after the Decepticon raid. How many total Autobots did the medic fix?",
                "The Autobot space bridge transported {num1} supply crates from Cybertron, and then brought down {num2} more crates. How many total crates arrived?",
                "Ironhide welded {num1} shields onto the base doors and {num2} shields onto the roof. How many metal shields did he weld altogether?"
            ],
            "-": [
                "Megatron launched {num1} tracking missiles at the launchpad, but Starscream accidentally knocked {num2} of them off course. How many missiles hit?",
                "Grimlock found {num1} iron car scraps to chew on, but he dropped {num2} of them when he roared. How many scraps does he have left?",
                "The Decepticons stole {num1} plasma batteries from the city power plant, but Bumblebee intercepted them and won back {num2} batteries. How many do the Decepticons still have?",
                "Wheeljack built {num1} wacky scientific inventions in his lab, but {num2} of them accidentally exploded during testing. How many working inventions does he have left?",
                "A group of {num1} Seekers flew into the sky to attack, but Optimus Prime used his laser blaster to knock {num2} of them down. How many Seekers are still flying?",
                "The Matrix of Leadership holds {num1} ancient secrets of the Primes. If Optimus Prime shares {num2} of those secrets with Hot Rod, how many secrets are left hidden?"
            ],
            "*": [
                "Bumblebee can scan and clone {num1} types of vehicles. If each vehicle has {num2} wheels, how many wheels has he scanned altogether?",
                "A Transformer team requires {num1} drops of special oil per gear. If a robot has {num2} gears, how many drops of oil are needed?",
                "Grimlock and his {num1} Dinobot friends went hunting for metal tracks. If each Dinobot crunched exactly {num2} old railroad tracks, how many tracks did they smash total?",
                "Shockwave set up {num1} guard towers on Cybertron. If each tower has exactly {num2} purple security cameras watching the borders, how many cameras are there altogether?",
                "Optimus Prime used his Energon Axe to chop through {num1} metal walls. If each wall was {num2} meters thick, how many total meters of solid metal did he chop through?",
                "Soundwave plays secret audio recordings. If he plays {num1} static tapes, and each tape captures {num2} minutes of Decepticon transmissions, how many total minutes did he record?"
            ],
            "/": [
                "Optimus Prime wants to distribute {num1} Energon cubes equally among {num2} battle stations. How many cubes go to each station?",
                "Starscream gathered {num1} space blasters to distribute evenly among {num2} Decepticon soldiers. How many blasters does each soldier get?",
                "Megatron wants to split {num1} stolen computer core servers equally among his {num2} craftiest space scientists. How many servers does each scientist get?",
                "The giant robot Omega Supreme has {num1} rocket boosters. If they are divided evenly across his {num2} landing tracks, how many boosters are on each track?",
                "Bumblebee has {num1} spare tire parts to share evenly among his {num2} favorite human mechanic friends. How many tire parts does each mechanic get?",
                "A tactical computer needs to sort {num1} Cybertronian coordinates evenly into {num2} navigation maps. How many coordinates will be saved onto each map?"
            ]
        }
    }
}

# Add matching image files to your local assets directory
BACKGROUND_IMAGES = [
    "powerpuff/1.jpg", 
    "powerpuff/2.jpg", 
    "powerpuff/3.jpg", 
    "powerpuff/4.webp", 
    "powerpuff/5.jpg", 
    "powerpuff/6.jpg", 
    "powerpuff/7.jpg", 
    "powerpuff/8.webp", 
    
    "adventuretime/1.webp",
    "adventuretime/2.webp",
    "adventuretime/3.webp",
    "adventuretime/4.webp",
    "adventuretime/5.jpg",
    "adventuretime/6.avif",
    "adventuretime/7.webp",
    "adventuretime/8.jpg",
    
    "pokemon/1.webp",
    "pokemon/2.webp",
    "pokemon/3.avif",
    "pokemon/4.webp",
    "pokemon/5.webp",
    "pokemon/6.webp",
    "pokemon/7.jpg",
    "pokemon/8.jpg",
    
    "tmnt/1.webp",
    "tmnt/2.jpeg",
    "tmnt/3.webp",
    "tmnt/4.jpg",
    "tmnt/5.jpg",
    "tmnt/6.webp",
    "tmnt/7.jpeg",
    "tmnt/8.png",
    
    "transformers/1.avif",
    "transformers/2.avif",
    "transformers/3.jpg",
    "transformers/4.avif",
    "transformers/5.jpg",
    "transformers/6.jpg",
    "transformers/7.jpg",
    "transformers/8.jpg",

]


# --- HELPER LOGIC TO GENERATE PROBLEMS ---
def generate_problem_by_theme(theme_name):
    cfg = THEME_DATA[theme_name]
    op = random.choice(["+", "-", "*", "/"])
    is_word_problem = random.choice([True, False])
    
    if op == "+":
        num1, num2 = random.randint(0, 50), random.randint(0, 50)
        answer = num1 + num2
    elif op == "-":
        num1 = random.randint(0, 100)
        num2 = random.randint(0, num1)
        answer = num1 - num2
    elif op == "*":
        num1, num2 = random.randint(1, 10), random.randint(0, 10)
        answer = num1 * num2
    elif op == "/":
        num2 = random.randint(1, 10)
        answer = random.randint(0, 10)
        num1 = num2 * answer 
        
    if is_word_problem:
        char_pool = cfg["characters"].copy()
        name = random.choice(char_pool)
        char_pool.remove(name)
        friend = random.choice(char_pool)
        
        template = random.choice(cfg["templates"][op])
        question = template.format(
            name=name,
            friend=friend,
            item=random.choice(cfg["items"]),
            num1=num1,
            num2=num2
        )
    else:
        op_symbol = "÷" if op == "/" else ("×" if op == "*" else op)
        question = f"What is {num1} {op_symbol} {num2}?"
        
    return question, answer

# ==========================================
#              DASH LAYOUT
# ==========================================
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(id='main-bg-container', style={
    'fontFamily': '"Comic Sans MS", "Chalkboard SE", sans-serif', 'padding': '15px',
    'height': '100vh', 'boxSizing': 'border-box', 'display': 'flex', 'flexDirection': 'row',
    'backgroundSize': 'cover', 'backgroundPosition': 'center', 'transition': 'background-image 0.5s ease-in-out',
    'overflow': 'hidden', 'backgroundColor': '#FFF0F5'
}, children=[
    
    # Left-Side Theme Control Panel
    html.Div(style={
        'width': '20vw', 'height': '9vw',
        'backgroundColor': 'rgba(255, 255, 255, 0.9)', 
        'borderRadius': '20px',
        'padding': '10px', 
        'boxShadow': '5px 5px 15px rgba(0,0,0,0.1)', 
        'display': 'flex', 
        'flexDirection': 'column', 
        'marginRight': '20px', 
        'border': '4px solid #ced9e4', 
        'boxSizing': 'border-box',
    }, children=[
        html.H3("😄 Choose A Theme", style={'color': '#2C3E50', 'marginTop': '0', 'textAlign': 'center'}),
        dcc.Dropdown(
            id='theme-selector',
            options=[{'label': t, 'value': t} for t in THEME_DATA.keys()],
            value='Powerpuff Girls',
            clearable=False,
            style={'fontFamily': 'sans-serif', 
                   'fontWeight': 'bold'}
        ),
        html.Div(style={'flexGrow': '1'}),
        #html.Small("Change themes anytime to swap questions and colors!", style={'color': '#7F8C8D', 'textAlign': 'center'})
    ]),
    
    # Central Testing Dashboard Card
    html.Div(id='central-game-card', style={
        'backgroundColor': 'rgba(255, 255, 255, 0.95)', 
        #'maxWidth': '60vw', 
        'width': '50vw', 
        'margin': 'auto', 
        'borderRadius': '25px', 
        'padding': '20px 30px', 
        'boxShadow': '0px 8px 20px rgba(0, 0, 0, 0.2)',
        'border': '6px solid #AED6F1', 'boxSizing': 'border-box', 'textAlign': 'center'
    }, children=[
        
        html.H1(id='app-title', children="🌟 LAB ROOM! 🌟", style={
            'color': '#FF69B4', 'fontSize': '28px', 'fontWeight': 'bold', 'margin': '0 0 5px 0'
        }),
        html.Div(id='app-subtitle', children="Can you solve this challenge?", style={'color': '#5DADE2', 'fontSize': '16px', 'fontWeight': 'bold'}),
        html.Hr(style={'border': '1px dashed #FFB6C1', 'margin': '15px 0'}),
        
        # Action Notification Area
        html.Div(id='last-action-feedback', style={'fontSize': '18px', 'fontWeight': 'bold', 'minHeight': '30px', 'marginBottom': '10px'}),

        # Target Word/Math Problem Box
        html.Div(id='question-box', style={
            'fontSize': '20px', 'fontWeight': 'bold', 'margin': '15px 0', 
            'minHeight': '60px', 'color': '#2C3E50', 'padding': '12px',
            'backgroundColor': '#EAFAF1', 'borderRadius': '15px', 'border': '3px solid #2ECC71' 
        }),
        
        # User Interface Blocks
        html.Div([
            dcc.Input(id='user-answer', type='number', placeholder='?', style={
                'fontSize': '26px', 'width': '110px', 'textAlign': 'center', 
                'borderRadius': '12px', 'border': '3px solid #FFB6C1', 'padding': '6px', 'fontWeight': 'bold'
            }),
            html.Br(), html.Br(),
            html.Button('💥 Check Answer!', id='submit-btn', n_clicks=0, n_clicks_timestamp=0, style={
                'fontSize': '18px', 'color': 'white', 'border': 'none', 'padding': '12px 30px', 
                'borderRadius': '50px', 'cursor': 'pointer', 'fontWeight': 'bold'
            }),
        ]),
        
        # Score Tracking Metric Area
        html.Div(id='score-box', style={
            'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '20px', 
            'color': '#2ECC71', 'backgroundColor': '#F4F6F6', 'padding': '10px', 'borderRadius': '12px'
        }),
    ]),
    
    # Store Engine Hooks
    dcc.Store(id='correct-answer'),
    dcc.Store(id='score-tracker', data={'correct': 0, 'total': 0})
])

# ==========================================
#              APP LOGIC
# ==========================================
@app.callback(
    Output('question-box', 'children'),
    Output('correct-answer', 'data'),
    Output('last-action-feedback', 'children'),
    Output('score-tracker', 'data'),
    Output('score-box', 'children'),
    Output('user-answer', 'value'),
    Output('main-bg-container', 'style'),
    Output('central-game-card', 'style'),
    Output('app-title', 'children'),
    Output('app-title', 'style'),
    Output('app-subtitle', 'style'),
    Output('submit-btn', 'style'),
    Input('submit-btn', 'n_clicks'),
    Input('theme-selector', 'value'),
    State('user-answer', 'value'),
    State('correct-answer', 'data'),
    State('score-tracker', 'data'),
    State('question-box', 'children'),
    State('main-bg-container', 'style'),
    State('central-game-card', 'style'),
    State('submit-btn', 'style'),
    prevent_initial_call=False
)
def run_themed_game(submit_clicks, active_theme, user_ans, current_correct, score, current_question, bg_style, card_style, btn_style):
    ctx = callback_context
    cfg = THEME_DATA[active_theme]
    
    # Helper tracker strings
    def format_score_text(s):
        pct = int((s['correct'] / s['total']) * 100) if s['total'] > 0 else 0
        return f"⭐ Badges: {s['correct']} / {s['total']} | Success Rate: {pct}% ⭐"

    # Define full contextual UI updates based on configurations
    title_text = f"🌟 {active_theme.upper()} MATH LAB! 🌟"
    title_style = {'color': cfg['accent_color'], 'fontSize': '28px', 'fontWeight': 'bold', 'margin': '0 0 5px 0'}
    subtitle_style = {'color': cfg['card_border'], 'fontSize': '16px', 'fontWeight': 'bold'}
    
    # Mutate background wrapper colors & image paths
    bg_style['backgroundColor'] = cfg['bg_color']
    card_style['border'] = f"6px solid {cfg['card_border']}"
    
    # Re-render actionable buttons
    new_btn_style = {
        'fontSize': '18px', 'backgroundColor': cfg['accent_color'], 'color': 'white', 
        'border': 'none', 'padding': '12px 30px', 'borderRadius': '50px', 'cursor': 'pointer',
        'fontWeight': 'bold', 'boxShadow': f"0px 4px 0px {cfg['button_shadow']}"
    }

    # Trigger branch evaluation 
    triggered_id = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    # Condition A: Theme was swapped OR application booted up fresh
    if not triggered_id or triggered_id == 'theme-selector.value':
        next_q, next_ans = generate_problem_by_theme(active_theme)
        if BACKGROUND_IMAGES:
            # Swap background image cleanly using only the current theme's images
            if cfg["images"]:
                chosen_bg = random.choice(cfg["images"])
                bg_style['backgroundImage'] = f"url('/assets/{chosen_bg}')"
        return next_q, next_ans, f" Switched to {active_theme}! Go!", score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style

    # Condition B: Form Submission
    if user_ans is None:
        reminder = html.Span("Type a number first! 🤔", style={'color': '#E67E22'})
        return current_question, current_correct, reminder, score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style

    # Process correct/incorrect logic
    if int(user_ans) == current_correct:
        feedback = html.Span("✅ Correct! Magnificent job! ✅", style={'color': '#2ECC71'})
        score['correct'] += 1
    else:
        feedback = html.Span(f"❌ Not quite! The correct answer was {current_correct}.", style={'color': '#E74C3C'})
    score['total'] += 1

    # Advance to the next question automatically
    next_q, next_ans = generate_problem_by_theme(active_theme)
    if BACKGROUND_IMAGES:
        # Swap background image cleanly using only the current theme's images
        if cfg["images"]:
            chosen_bg = random.choice(cfg["images"])
            bg_style['backgroundImage'] = f"url('/assets/{chosen_bg}')"

    return next_q, next_ans, feedback, score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)