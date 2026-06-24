import random
import dash
from dash import html, dcc, Input, Output, State, callback_context

# ==========================================
#         THEME DATA & TEMPLATES
# ==========================================
THEME_DATA = {
    "Powerpuff Girls": {
        "bg_color": "#FFF0F5",        # Light pink blossom aura
        "card_border": "#7cbde9",    # Bubbles Blue
        "accent_color": "#FF69B4",   # Powerpuff Pink
        "button_shadow": "#D81B60",
        "question_border": "#2ECC71",# Buttercup Green
        "characters": ["Blossom", "Bubbles", "Buttercup", "Mojo Jojo", "Fuzzy Lumpkins", "Professor Utonium"],
        "items": ["Chemical X drops", "star stickers", "sweet cupcakes", "unbreakable hearts", "jars of jam"],
        "images": [
            "powerpuff/1.jpg", "powerpuff/2.jpg", "powerpuff/3.jpg", "powerpuff/4.webp", 
            "powerpuff/5.jpg", "powerpuff/6.jpg", "powerpuff/7.jpg", "powerpuff/8.webp",
            "powerpuff/9.webp", "powerpuff/10.avif", "powerpuff/11.jpg", "powerpuff/12.png", 
            "powerpuff/13.png", "powerpuff/14.jpg",  "powerpuff/15.png", "powerpuff/16.jpg", 
            "powerpuff/17.webp", "powerpuff/18.jpg", "powerpuff/19.jpg", "powerpuff/20.webp",
            "powerpuff/21.avif", "powerpuff/22.jpg", "powerpuff/23.png", 
            
        ],
        "templates": {
            "+": [
                "Blossom defeated {num1} bad guys in the morning and {num2} bad guys after lunch. How many bad guys did she defeat in total?",
                "The Mayor gave Bubbles {num1} star stickers for saving Townsville. Later, she earned {num2} more. How many stickers does she have now?",
                "Professor Utonium poured {num1} drops of Chemical X into a beaker, and then added {num2} more drops. How many drops are in the beaker?",
                "{name} found {num1} {item}. Then, {friend} gave them {num2} more! How many {item} does {name} have now?",
                "There are {num1} {item} hidden in the Powerpuff lab and {num2} {item} in a Pokéball. How many are there in total?",
                "Mojo Jojo bought {num1} blueprints for a giant robot, and then stole {num2} more from the city museum. How many blueprints does he have now?",
                "Princess Morbucks bought {num1} shiny diamond crowns from France and {num2} golden tiaras from London. How many hats does she have altogether?",
                "The Gangreen Gang found {num1} old soda cans in the junkyard, and Ace found {num2} more in a trash bin. How many cans do they have total?",
                "The Talking Dog saw {num1} regular cats walking down the sidewalk and {num2} mutant monsters running by. How many animals did he see in total?",
                "Bubbles drew {num1} pictures of Octi in her bedroom and {num2} pictures of cute puppies in class. How many total pictures did she draw?",
                "The Amoeba Boys sneaked into {num1} banks on Tuesday and {num2} jewelry stores on Wednesday trying to be bad guys. How many places did they target total?",
                "The Rowdyruff Boys caused {num1} problems in downtown Townsville and {num2} problems near the park. How many problems did they cause altogether?",
                "Sedusa stole {num1} lipsticks from the beauty salon and {num2} diamond necklaces from the vault. How many items did she steal in total?",
                "The Mayor's emergency Hotline phone rang {num1} times before lunch and {num2} times after lunch. How many times did the Hotline ring today?",
                "Ms. Keane placed {num1} gold stars on the homework board and {num2} stars on the reading chart. How many total stars did she place?",
                "Buttercup smashed {num1} of Mojo's robotic monkeys, and Blossom froze {num2} more with her ice breath. How many robot monkeys did they defeat?",
                "Professor Utonium bought {num1} boxes of sugar and {num2} boxes of spice to create the perfect little girls. How many ingredient boxes did he buy?",
                "Brick threw {num1} heavy rocks at a sign, and Butch threw {num2} rocks at a lamppost. How many total rocks did the Rowdyruff Boys throw?",
                "The Townsville Police Department locked up {num1} criminals yesterday and {num2} criminals today. How many criminals did they lock up total?",
                "Boomer found {num1} pieces of sticky blue bubblegum under his shoe and {num2} pieces on a bench. How many total pieces did he find?"
            ],
            "-": [
                "Buttercup found {num1} runaway robots in downtown Townsville. She already smashed {num2} of them. How many robots are left to smash?",
                "Fuzzy Lumpkins had {num1} jars of jam on his property. {name} chased him away and took {num2} jars back. How many jars does Fuzzy have left?",
                "{name} had {num1} {item}. {friend} borrowed {num2} of them to save the day. How many {item} does {name} have left?",
                "The Powerpuff Girls had {num1} emergency calls today, but {name} quickly solved {num2} of them. How many emergency calls are still waiting?",
                "Mojo Jojo stole {num1} laser blasters from the observatory, but Bubbles used her sonic scream to shatter {num2} of them. How many blasters does Mojo have left?",
                "Princess Morbucks had {num1} expensive bags of money. She spent {num2} of them trying to buy superpowers. How many bags of money does she have left?",
                "The Gangreen Gang had {num1} stolen skateboards, but Buttercup chased them down and took {num2} of them back. How many skateboards do they still keep?",
                "The Mayor had {num1} jars of sweet pickles in his desk drawer. He ate {num2} of them during a meeting. How many jars of pickles are left?",
                "Mojo Jojo built {num1} mechanical mind-control helmets, but Blossom crushed {num2} of them with her super strength. How many working helmets are left?",
                "The Amoeba Boys had {num1} germs to spread around Pokey Oaks Kindergarten, but Ms. Keane made them use soap and washed away {num2} germs. How many germs are left?",
                "The Rowdyruff Boys targeted {num1} buildings in Townsville, but the Powerpuff Girls defended {num2} of them perfectly. How many buildings were left damaged?",
                "Sedusa pulled {num1} hair-whips out to fight, but Buttercup used her laser eyes to singe and cut off {num2} of them. How many hair-whips does Sedusa have left?",
                "Professor Utonium made {num1} pancakes for breakfast. Him and the girls ate {num2} of them before the hotline rang. How many pancakes are left?",
                "A monster from Monster Isle brought {num1} giant eggs to town, but {name} cracked {num2} of them safely before they could hatch. How many eggs are left?",
                "The giant robot DYNAMO had {num1} missile chargers ready, but the Mayor accidentally disconnected {num2} of them. How many missiles are left ready to fire?",
                "Fuzzy Lumpkins had {num1} logs stacked up on his porch. He threw {num2} of them at trespassers who stepped on his property. How many logs does he have left?"
            ],
            "*": [
                "{name} has {num1} special bags. Each bag holds exactly {num2} {item}. How many {item} does {name} have altogether?",
                "Professor Utonium made {num1} rows of treats. Each row has {num2} treats. How many total treats did he make?",
                "Mojo Jojo is building {num1} giant laser beams. Each laser beam needs exactly {num2} batteries to turn on. How many batteries does he need in total?",
                "The Narrator said the Powerpuff Girls saved Townsville {num1} times this week! If they saved {num2} citizens each time, how many total citizens did they save?",
                "The Gangreen Gang has {num1} members. If each member eats exactly {num2} bags of sour candies, how many bags of candy did they eat total?",
                "Princess Morbucks ordered {num1} vault trucks to deliver gold. If each truck holds {num2} golden bricks, how many gold bricks did she buy?",
                "The Amoeba Boys found {num1} mud puddles. If each puddle has {num2} slimy frogs inside, how many total frogs did they find?",
                "Mojo Jojo's volcano lair has {num1} computer screens. If each screen shows {num2} secret security camera angles, how many total angles is he watching?",
                "The Powerpuff Girls have {num1} superpower training rooms. If each room has {num2} target dummies to punch, how many total targets do they have?",
                "Bubbles sorted her stuffed animals into {num1} neat rows. If each row has exactly {num2} toys, how many stuffed animals are in her room?",
                "The Rowdyruff Boys flew around {num1} city blocks. If they knocked over {num2} trash cans on every single block, how many total trash cans did they knock over?",
                "Fuzzy Lumpkins played his banjo for {num1} hours. If he sang exactly {num2} country songs every hour, how many total songs did his neighbors have to hear?",
                "The villain HIM has {num1} red capes. If each cape has {num2} dark magic spikes on the back, how many magic spikes are there altogether?",
                "Sedusa has {num1} disguise kits. If each kit contains {num2} different colored wigs, how many total wigs does she have to trick the Mayor?",
                "Professor Utonium has {num1} storage shelves in the lab. If each shelf holds exactly {num2} backup beakers of Chemical X, how many beakers are there total?",
                "The Narrator told {num1} stories about the girls. If each story featured exactly {num2} giant monsters attacking the town, how many monsters were there total?"
            ],
            "/": [
                "The villain HIM cast a spell creating {num1} creepy shadow-monsters. If {num2} heroes split up to fight them equally, how many monsters does each hero fight?",
                "Ms. Keane has {num1} crayons at Pokey Oaks Kindergarten. She wants to divide them equally among {num2} kids. How many crayons does each kid get?",
                "{name} wants to share {num1} {item} equally among {num2} friendly Pokémon. How many {item} does each Pokémon get?",
                "If Bubbles splits {num1} {item} into {num2} equal neat piles, how many {item} will be in each pile?",
                "Mojo Jojo captured {num1} stolen diamonds. He wants to divide them equally into {num2} secret hiding spots in his observatory. How many diamonds go in each spot?",
                "The Powerpuff Girls recovered {num1} stolen packages from the Gangreen Gang. If the 3 girls split the load evenly to carry them home, how many packages does each girl carry?",
                "Princess Morbucks bought {num1} pure-gold puppy statues. She wants to arrange them evenly across her {num2} mansion balconies. How many statues go on each balcony?",
                "The Mayor has {num1} emergency phone buttons to distribute evenly into {num2} security control rooms. How many buttons fit in each control room?",
                "Professor Utonium has {num1} test tubes of antidote. He splits them evenly into {num2} protective medical boxes. How many test tubes are in a single box?",
                "The Rowdyruff Boys found {num1} stolen laser pistols. If they share them completely evenly between Brick, Boomer, and Butch, how many pistols does each boy get?",
                "Fuzzy Lumpkins gathered {num1} meat pies from his shack. He divides them evenly among his {num2} family cousins. How many pies does each cousin get?",
                "The Amoeba Boys want to split {num1} stolen cough drops evenly among their {num2} members. How many cough drops does each member get?",
                "The Townsville Bank needs to move {num1} safe keys into {num2} secure vaults. If every vault gets the same number, how many keys are in each vault?",
                "Bubbles found {num1} lost blue jay feathers in the park. She splits them evenly into {num2} scrapbooks. How many feathers are in each scrapbook?",
                "Buttercup has {num1} punch-bags to set up across {num2} gym corners. If she divides them evenly, how many punch-bags go into each corner?",
                "Blossom has {num1} tracking maps to distribute evenly among {num2} police cars. How many maps does each police car receive?"
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
            "pokemon/5.webp", "pokemon/6.webp", "pokemon/7.jpg", "pokemon/8.jpg",
            "pokemon/9.jpg", "pokemon/10.avif", "pokemon/11.webp", "pokemon/12.webp"
            
        ],
        "templates": {
            "+": [
                "{name} caught {num1} Wild Pokémon in the forest, and then encountered {num2} more near the river. How many Pokémon did they find?",
                "Ash has {num1} {item} in his backpack. Brock gives him {num2} more to prepare for the Gym Battle. How many {item} does Ash have now?",
                "Misty found {num1} Staryu swimming in the Cerulean Gym pool and {num2} Psyduck resting nearby. How many Water-type Pokémon are there in total?",
                "A Pokémon Center has {num1} hurt Pokémon resting in the lobby and {num2} more checking in with Nurse Joy. How many total Pokémon are at the Center?",
                "Officer Jenny found {num1} missing Squirtles in the city park. Later, her Growlithe tracked down {num2} more. How many Squirtles did they rescue?",
                "{name} used {num1} Max Potions to heal their team, but they still have {num2} Max Potions left in their bag. How many did they start with?",
                # --- NEW POKÉMON ADDITIONS ---
                "Todd Snap took {num1} photos of flying Pidgeots and {num2} photos of splashing Magikarps on the Pokémon Island. How many photos did he take in total?",
                "A Trainer bought {num1} Great Balls at the Pewter City Poké Mart and {num2} Ultra Balls at the Cerulean City Poké Mart. How many Pokéballs did they buy altogether?",
                "In the Safari Zone, {name} spotted {num1} wild Tauros running in a herd and {num2} wild Kangaskhan resting in the grass. How many Pokémon did they spot?",
                "A wild Combee collected {num1} drops of sweet honey from pink flowers and {num2} drops from yellow flowers. How many drops of honey did it collect total?",
                "May's Torchic found {num1} spicy Bluk Berries on a bush, and Max found {num2} sweet Nanab Berries. How many total berries did they gather?",
                "A group of trainers found {num1} fossilized Helix Shards in Mt. Moon, and then discovered {num2} Dome Fossils. How many ancient fossils did they find altogether?",
                "Gym Leader Sabrina has {num1} Alakazam training cards on her desk and {num2} Kadabra trading cards on her shelf. How many Psychic cards does she have total?",
                "A wild Ditto transformed into a Pikachu {num1} times in the morning and into a Charizard {num2} times in the afternoon. How many total transformations did it perform?",
                "Team Rocket's Meowth polished {num1} shiny gold coins from his own forehead and {num2} coins he found on the ground. How many polished coins does he have now?",
                "An elite breeder hatched {num1} Pichu eggs last week and {num2} Togepi eggs this week. How many baby Pokémon eggs did they hatch in total?",
                "Tracey Sketchit drew {num1} charcoal sketches of a wild Marill and {num2} sketches of a Scyther. How many total sketches did he finish?",
                "A Poké-Sitter is watching {num1} playful Clefairys in the backyard and {num2} sleeping Jigglypuffs in the nursery. How many total Pokémon are they sitting?",
                "In the underground cave, a Geodude rolled past {num1} trainers and a giant Onix crashed past {num2} trainers. How many total trainers did they startle?",
                "Gary Oak won {num1} shiny gym badges in the Kanto region, and then went to Johto and won {num2} more badges. How many total badges does Gary have?",
                "A Hoenn Coordinator earned {num1} Contest Ribbons for Beauty and {num2} Contest Ribbons for Toughness. How many ribbons do they have hanging on their wall?",
                "The Silph Co. factory manufactured {num1} standard Master Balls in the first assembly line and {num2} Master Balls in the second line. How many total Master Balls were made?",
                "Professor Rowan identified {num1} Sinnoh regional variants of standard Pokémon and {num2} brand new species. How many total discoveries did he log?",
                "A wild Dragonite delivered {num1} secret letters to the Indigo Plateau and {num2} urgent letters to New Island. How many total letters did it deliver?"
            ],
            "-": [
                "A wild Snorlax was guarding {num1} {item}. {name} used a Poké-Flute and safely collected {num2} of them. How many are left with Snorlax?",
                "Team Rocket stole {num1} Pokéballs, but Eevee used Swift to knock {num2} Pokéballs back out of their basket! How many do Team Rocket still have?",
                "Professor Oak had {num1} Fire-type evolution stones in his lab. He gave {num2} of them to trainers to evolve their Growlithes. How many stones are left?",
                "A wild Jigglypuff sang a song and put {num1} trainers to sleep. {num2} of those trainers woke up early by using an Awakening item. How many trainers are still asleep?",
                "A trainer brought {num1} Potions to a battle against gym leader Lt. Surge. Pikachu's Thunderbolt destroyed {num2} of them. How many Potions does the trainer have left?",
                "{name} was carrying {num1} Ultra Balls. They threw {num2} Ultra Balls trying to catch a legendary Mewtwo. How many Ultra Balls do they have left?",
                # --- NEW POKÉMON SUBTRACTIONS ---
                "A wild Sudowoodo was blocking a road made of {num1} stone paths. Squirtle used Water Gun to clean off {num2} paths so cars could drive. How many paths are still blocked?",
                "Jessie and James had {num1} mechanical traps set up to catch Pikachu, but Ash's Charizard used Flamethrower to melt {num2} of them. How many traps do they have left?",
                "A trainer had {num1} Rare Candies hidden in their item bag. They fed {num2} of them to their Dragonair to help it evolve. How many Rare Candies are left?",
                "The Viridian Forest had {num1} wild Caterpies hiding in the tall grass. A flock of Pidgeottos flew down and scared {num2} of them away. How many Caterpies are left?",
                "Brock cooked {num1} bowls of hot Pokémon stew for the campsite. The hungry mud-skipper Mudkip ate {num2} bowls all by itself. How many bowls of stew are left?",
                "The Celadon Department Store had {num1} plush Lapras dolls on the display shelf. Eager young trainers bought {num2} of them in ten minutes. How many dolls are left?",
                "Misty had {num1} ocean badges inside her special display case. She accidentally dropped the case into the sea and lost {num2} badges. How many badges does she have left?",
                "A wild Diglett dug {num1} holes in a beautiful garden. The local Ground-type trainer filled in {num2} of the holes with fresh dirt. How many holes are still open?",
                "A package of {num1} sweet Zinc supplements was ordered for a competitive team. A hungry Munchlax snatched {num2} supplements out of the box. How many are left?",
                "Professor Elm had {num1} Johto starter catalogs ready for new trainers. He handed out {num2} catalogs to trainers from New Bark Town. How many catalogs are left?",
                "The local gym leader had {num1} dynamic Technical Machines (TMs) to give as rewards. After a busy day of battles, {num2} trainers won their matches. How many TMs are left?",
                "A wild Psyduck had a headache that lasted {num1} minutes. After relaxing near Misty for {num2} minutes, its headache began to ease. How many minutes of headache are left?",
                "A massive flock of {num1} Zubats filled the dark tunnels of Rock Tunnel. A trainer used a Max Repel spray and cleared {num2} Zubats away. How many Zubats are still nearby?",
                "The Squirtle Squad stole {num1} sweet treats from the town bakery, but Officer Jenny convinced them to return {num2} of them. How many treats do they still have?",
                "A wild Gengar cast {num1} spooky illusions inside the Lavender Town Pokémon Tower. A brave Gastly used Night Shade to dispel {num2} illusions. How many are left?",
                "A collector owned {num1} ultra-rare holographic Charizard cards. They traded {num2} of them to get an ancient Mew card. How many Charizard cards do they have left?",
                "An item machine printed {num1} clean Escape Ropes for explorers. A group of hikers took {num2} ropes to climb Mt. Coronet. How many Escape Ropes are left in the machine?",
                "A trainer had {num1} custom Apricorn Pokéballs crafted by Kurt in Azalea Town. They used {num2} Heavy Balls to catch a heavy Donphan. How many Apricorn balls are left?"
            ],
            "*": [
                "{name} has {num1} Pokémon eggs. Each egg requires {num2} kilometers of walking to hatch. How many total kilometers does {name} need to walk?",
                "Pikachu unleashed {num1} Thunderbolts. If each Thunderbolt sparks {num2} sparks of electricity, how many sparks flew in total?",
                "Charizard used Flamethrower {num1} times. If each Flamethrower melts exactly {num2} blocks of ice, how many blocks of ice did Charizard melt?",
                "A Poké-Mart sells bundles of items. If {name} buys {num1} boxes, and each box contains {num2} Revive crystals, how many Revives do they get?",
                "During a double battle, {num1} friendly Pokémon each used the move Swift. If each Swift attack shoots out {num2} glowing stars, how many stars are on the screen?",
                "A group of Diglett dug {num1} tunnels under Diglett's Cave. If each tunnel goes past {num2} underground rocks, how many rocks did they tunnel past?",
                # --- NEW POKÉMON MULTIPLICATION ---
                "A wild Exeggcute has {num1} groups of psychic eggs. If every single group contains exactly {num2} individual eggs, how many individual eggs are there total?",
                "Team Rocket built {num1} robot Meowth mechs. If each robot mech requires exactly {num2} heavy steel screws to stay together, how many total screws do they need?",
                "A legendary Suicune ran across {num1} large lakes. If it purified exactly {num2} gallons of dirty water in every lake, how many gallons of water did Suicune purify?",
                "An elite trainer has {num1} high-tech Pokéball utility belts. If each belt holds exactly {num2} Ultra Balls, how many Ultra Balls can the trainer carry in total?",
                "A wild Blastoise fired its dual water cannons {num1} times. If each burst shoots out {num2} gallons of high-pressure water, how many gallons did it shoot total?",
                "A standard Pokémon League arena has {num1} stadium rows. If each row contains exactly {num2} excited cheering fans, how many total fans are in the arena?",
                "Ash bought {num1} packs of delicious Pokémon food from a local market. If each pack feeds exactly {num2} of his party monsters, how many monsters can he feed?",
                "A group of {num1} industrious Sandshrews dug through the sand dunes. If each Sandshrew uncovered {num2} buried Stardust gems, how many gems did they find total?",
                "A skilled Gym Leader uses {num1} training arenas. If each arena requires exactly {num2} bright halogen floodlights to operate at night, how many floodlights are used?",
                "A wild Butterfree fluttered its wings {num1} times. If each wing flutter drops exactly {num2} sparkles of glowing sleep powder, how many powder sparkles dropped?",
                "Professor Oak ordered {num1} shipment crates of brand new red Pokédexes. If each crate holds {num2} Pokédexes, how many total Pokédexes arrived for new trainers?",
                "A dedicated breeder planted {num1} garden rows of magical Pecha Berries. If each row yields exactly {num2} ripe berries, how many total berries can be harvested?",
                "A group of {num1} wild Machops are helping move boxes in Vermilion City. If each Machop lifts exactly {num2} heavy wooden boxes, how many boxes do they move total?",
                "The legendary bird Articuno created {num1} massive ice blizzards. If each blizzard freezes exactly {num2} pine trees solid, how many total trees were frozen?",
                "A standard Poké Mart displays {num1} shelves of status-healing sprays. If each shelf holds exactly {num2} bottles of Full Heal, how many bottles are on display?",
                "A wild Magneton has {num1} magnetic segments floating around its core. If each segment generates {num2} units of electric currents, how many total units are generated?",
                "A trainer won {num1} consecutive battle rounds at the Battle Frontier. If each round awards them {num2} Battle Points (BP), how many total points did they earn?",
                "The mysterious Unown alphabet has {num1} ancient stone tablets hidden in the ruins. If each tablet has {num2} symbols carved into it, how many total symbols are there?"
            ],
            "/": [
                "{name} found {num1} delicious Razz Berries and wants to share them equally among {num2} hungry Eevees. How many berries does each Eevee get?",
                "Professor Oak has {num1} starter Pokémon that need to be sent evenly to {num2} different towns. How many Pokémon go to each town?",
                "Ash gathered {num1} magical Exp. Candies. He wants to divide them up evenly to level up his {num2} favorite party Pokémon. How many candies does each Pokémon get?",
                "A group of wild Meowth collected {num1} shiny gold coins from an island. If they split the coins equally into {num2} piles, how many coins are in each pile?",
                "Nurse Joy has {num1} clean blankets to hand out to {num2} tired Chanseys at the clinic. If she shares them evenly, how many blankets does each Chansey get?",
                "A trainer needs to sort {num1} TM battle moves into {num2} organized storage boxes. If each box gets the exact same number, how many TMs fit in a single box?",
                # --- NEW POKÉMON DIVISION ---
                "A wild Bulbasaur harvested {num1} large solar seeds using its vine whips. It wants to distribute them evenly into {num2} soft soil patches. How many seeds go into each patch?",
                "Officer Jenny intercepted {num1} stolen water pumps from Team Rocket. She splits them evenly among her {num2} Squirtle Squad members. How many pumps does each Squirtle get?",
                "A Pokémon Ranger rescued {num1} trapped Mareep from a storm. They split the Mareep evenly into {num2} sheltered farm barns. How many Mareep go into each barn?",
                "A Berry Master has {num1} sour Cheri Berries to make Pokéblocks. If she splits them evenly into {num2} blending machines, how many berries go into each blender?",
                "The legendary Mew hidden in the jungle dropped {num1} glowing ancient feathers. If {num2} explorers divide them up completely evenly, how many feathers does each explorer keep?",
                "A local gym needs to store {num1} matching training weights. If the fighting-type leader divides them evenly among {num2} Machokes, how many weights does each Machoke carry?",
                "A group of wild Lapras are transporting {num1} human travelers across the sea. If the travelers are divided completely evenly across {num2} Lapras shells, how many ride on each?",
                "A high-tech lab synthesized {num1} microchips for Porygon updates. If they distribute them evenly to {num2} server terminals, how many chips go to each terminal?",
                "A trainer won {num1} shiny protective cases for their Pokéballs. They split the cases evenly among their {num2} favorite storage shelves. How many cases go on each shelf?",
                "The Indigo Plateau kitchen prepared {num1} stamina biscuits for the Elite Four. If the biscuits are shared completely evenly among the {num2} champions, how many does each eat?",
                "A wild Scyther cut down {num1} thick bamboo stalks in the forest. It stacks them completely evenly into {num2} neat piles. How many bamboo stalks are in each pile?",
                "A maritime captain found {num1} old sailor caps washed up on the slateport docks. He splits them evenly into {num2} storage chests. How many caps fit in each chest?",
                "A trainer has {num1} colorful stickers to decorate their Pokéballs. If they divide them evenly across {num2} Capsule cases, how many stickers go on a single capsule?",
                "A group of wild Geodudes found {num1} underground evolutionary Moon Stones. If they split them evenly among {num2} secret caves, how many stones are placed in each cave?",
                "An engineering team built {num1} solar panels for a power plant ran by Electabuzz. If the panels are split evenly across {num2} roofs, how many panels go on each roof?",
                "A group of researchers collected {num1} samples of mysterious pink ooze from a Muk habitat. They divide them evenly into {num2} test tubes. How many samples go in each tube?",
                "The Mossdeep Space Center needs to map {num1} shooting stars. If they divide the stars evenly among {num2} astronomical telescopes, how many stars are tracked per telescope?",
                "A trainer has {num1} delicious mental herbs to snap their team out of confusion. They divide them evenly into {num2} first-aid pockets. How many herbs go into each pocket?"
            ]
        }
    },
    "Adventure Time": {
        "bg_color": "#E8F8F5",        # Ooo Sky Blue-Green
        "card_border": "#5DADE2",    # Finn's Backpack Blue
        "accent_color": "#029AC3",   # Jake's Gold Magic Yellow
        "button_shadow": "#4ed7fd",
        "question_border": "#BB8FCE",# LSP Lumpy Purple
        "characters": ["Finn", "Jake", "Princess Bubblegum", "Marceline", "BMO", "Ice King"],
        "items": ["swords", "bacon pancakes", "Candy Kingdom gems", "ancient artifacts", "apples"],
        "images": [
            "adventuretime/1.webp", "adventuretime/2.webp", "adventuretime/3.webp", "adventuretime/4.webp", 
            "adventuretime/5.jpg", "adventuretime/6.avif", "adventuretime/7.webp", "adventuretime/8.jpg",
            "adventuretime/9.webp", "adventuretime/10.avif", "adventuretime/11.webp", "adventuretime/12.webp", 
        ],
        "templates": {
            "+": [
                "Finn gathered {num1} {item} from the Dungeon, and Jake found another {num2} using his magic stretchy paws. How many total did they bring home?",
                "Princess Bubblegum made {num1} smart candy citizens, and then created {num2} more to guard the gate. How many candy people did she make?",
                "Lady Rainicorn flew across {num1} red rainbows in the morning and {num2} blue rainbows in the evening. How many colorful rainbows did she cross in total?",
                "Tree Trunks baked {num1} hot apple pies for Finn and {num2} sweet berry pies for Jake. How many total pies did she bake for her friends?",
                "BMO counted {num1} skateboards in Finn and Jake's treehouse, and then found {num2} more hidden under the couch. How many skateboards are there altogether?",
                "The Flame King ordered his guards to light {num1} fire torches inside the Fire Kingdom, and {num2} extra torches outside the palace. How many torches were lit?",
                # --- NEW ADVENTURE TIME ADDITIONS ---
                "Choose Goose laid out {num1} rhyming shields on his display rug and {num2} enchanted boots on a wooden bench. How many total items does he have for sale?",
                "Shelby the worm found {num1} damp dirt crumbs inside Jake's violin body, and then discovered {num2} more under a rug. How many crumbs did he find total?",
                "The Party God summoned {num1} floating wolf heads in the morning and {num2} more at midnight to keep the rave going. How many wolf heads were summoned total?",
                "Sweet P picked {num1} fresh yellow dandelions in the meadow and {num2} red tulips to give to Tree Trunks. How many flowers did he pick altogether?",
                "Huntress Wizard set up {num1} log traps in the forest paths and {num2} arrow targets in the trees. How many total training setups does she have?",
                "Root Beer Guy filed {num1} police reports about missing bananas and {num2} reports about suspicious candy behavior. How many reports did he file in total?",
                "Marceline bought {num1} custom bass guitar strings from the music shop and {num2} silver tuning pegs. How many instrument parts did she buy altogether?",
                "The Duke of Nuts ordered {num1} boxes of macadamias and {num2} boxes of cashews for his Royal dinner. How many nut boxes did he order in total?",
                "Canyon discovered {num1} ancient water sources in the desert canyon and {num2} deep springs in the rock face. How many water sources did she discover?",
                "James Baxter the horse bounced on his beach ball past {num1} sad townspeople, and then cheered up {num2} more by neighing. How many people did he encounter?",
                "Grob Gob Glob Grod calculated {num1} cosmic path variations across space, and then found {num2} extra trajectories. How many paths did they map total?",
                "The Ancient Psychic Tandem War Elephant gave a ride to {num1} candy kids on its back and {num2} candy kids on its tusks. How many kids rode the elephant total?",
                "Me-Mow hid {num1} tiny poisonous vials inside a hollow log and {num2} vials inside a hollow stone. How many total vials did the assassin hide?",
                "Rattleballs swept {num1} dusty corners of the old junkyard arena before noon, and then cleaned {num2} more corners. How many corners did he sweep total?",
                "The Gumball Guardians scanned the northern borders and spotted {num1} incoming pests, then scanned the southern walls and saw {num2} more. How many pests did they spot?",
                "Susan Strong collected {num1} old electrical batteries from the underground lockers and {num2} copper wires from the walls. How many mechanical items did she secure?",
                "Abracadaniel conjured {num1} rainbow sparks out of his wooden wand, and then cast a spell for {num2} floating soap bubbles. How many magic objects did he generate?",
                "Finn bought {num1} standard health potions from the wizard shop, and then found {num2} hidden in a chest. How many health potions does he have now?"
            ],
            "-": [
                "The Ice King kidnapped {num1} penguins, but Gunther led {num2} of them on a secret escape route! How many penguins are left in the Ice Castle?",
                "Marceline had {num1} red apples, but she sucked the red out of {num2} of them. How many apples still have their color left?",
                "Cinnamon Bun was carrying {num1} fragile jelly tarts across the Candy Kingdom, but he tripped and dropped {num2} of them. How many jelly tarts did he save?",
                "Peppermint Butler had {num1} ancient spellbooks in his secret library. He locked {num2} of them away so Finn wouldn't find them. How many spellbooks are left out?",
                "The Earl of Lemongrab shouted at {num1} lemon citizens, but {num2} of them ran away because he was being too loud. How many lemon citizens had to stay and listen?",
                "Lumpy Space Princess brought {num1} cans of smooth lump-cream to a party, but she got dramatic and threw {num2} cans out the window. How many cans are left?",
                # --- NEW ADVENTURE TIME SUBTRACTIONS ---
                "Flame Princess summoned {num1} protective fire walls to block King of Ooo, but {num2} of the walls sputtered out due to rain. How many fire walls are still burning?",
                "The Lich possessed {num1} ancient skeletal warriors in his dark lair, but Finn smashed {num2} of them with the Grass Sword. How many skeletal warriors are left?",
                "Magic Man had {num1} magical tricks prepared to confuse travelers, but Jake's giant hand swatted {num2} of his illusions away. How many tricks does Magic Man have left?",
                "Hunson Abadeer brought {num1} soul-reaping amulets from the Nightosphere, but Marceline stole {num2} of them to hide on Earth. How many amulets does he keep?",
                "Starchy the Gravedigger had {num1} golden radio antennae for his radio show, but a rogue candy zombie broke {num2} of them. How many antennae are left working?",
                "The Cloud King built {num1} fluffy cloud chairs for a sky assembly, but a strong wind current blew {num2} chairs away into the trees. How many cloud chairs are left?",
                "The Goblin King had {num1} royal rules written on his throne room wall, but Finn pointed out that {num2} of the rules were completely silly and crossed them off. How many rules remain?",
                "Prismo had {num1} magical time-paradox pickles floating in his cosmic hot tub, but Jake ate {num2} of them without asking. How many time-pickles are left?",
                "The Banana Guards setup {num1} patrol barricades around the royal palace, but {num2} of the barricades fell down when a horse sneezed. How many barricades are left standing?",
                "Tiffany had {num1} poison knives hidden in his boots to fight Finn, but Jake grew his foot giant and stomped on {num2} of the knives. How many knives does Tiffany have left?",
                "The Grand Master Wizard had {num1} spell tokens inside his glowing pouch. He spent {num2} tokens to enter the wizard secret club. How many tokens does he have left?",
                "Neptr built {num1} automatic pie-throwing launcher bots, but Buttercup the cow kicked {num2} of them into the mud. How many pie-launchers are left working?",
                "Goliad had {num1} psychic thoughts trying to control the town, but Stormo fired {num2} heroic mental blocks to stop them completely. How many controlling thoughts got through?",
                "Party Pat had {num1} glow-sticks packed for the belly-of-the-whale party, but {num2} of them leaked out early and lost their glow. How many bright glow-sticks are left?",
                "The King of Ooo printed {num1} fake certificates of royalty to trick people, but Princess Bubblegum tore up {num2} of them on the spot. How many fake papers are left?",
                "Dr. Princess had {num1} clean bandages inside her emergency kit box. She used {num2} of them to cover Finn's battle scratches. How many bandages are left?",
                "The Marauders had {num1} wooden clubs ready for a village raid, but Billy used his gauntlet to vaporize {num2} clubs instantly. How many clubs are left with the Marauders?",
                "The Cosmic Owl had {num1} golden feathers fall out while dreaming. He gave {num2} feathers to Prismo as a friendly gift. How many golden feathers does the Cosmic Owl have left?"
            ],
            "*": [
                "BMO built {num1} video game levels. Each level features exactly {num2} golden coins. How many total coins did BMO program?",
                "Jake can bake {num1} batches of bacon pancakes. If each batch makes {num2} pancakes, how many delicious pancakes did he cook?",
                "Finn found {num1} secret pages inside the Enchiridion hero handbook. If each page shows {num2} drawings of magical swords, how many swords are drawn in total?",
                "Marceline played {num1} rock concerts in the Nightosphere. If she rocked out to {num2} screaming demons at every single show, how many total demons heard her play?",
                "Princess Bubblegum setup {num1} rows of test tubes in her science lab. If each row contains exactly {num2} glowing chemical solutions, how many solutions did she prepare?",
                "Susan Strong gathered {num1} groups of Hyuman tribespeople. If each group carries {num2} glowing techno-sticks, how many techno-sticks are there in total?",
                # --- NEW ADVENTURE TIME MULTIPLICATION ---
                "The Earl of Lemongrab built {num1} rows of sound-proof cages. If each row contains exactly {num2} screaming lemon drops, how many lemon drops are caged total?",
                "Lumpy Space Princess wrote {num1} draft chapters for her gossip book. If each chapter features exactly {num2} dramatic rumors about Brad, how many rumors did she write?",
                "The Ice King made {num1} frozen ice sculptures of Princess Bubblegum. If each sculpture requires {num2} flawless crystal gems for the eyes, how many gems did he use?",
                "Tree Trunks has {num1} garden plots for her apple trees. If each plot contains exactly {num2} organic apple trees, how many apple trees does she have total?",
                "Gunther the penguin organized {num1} marching columns of kittens. If each column has exactly {num2} mind-controlled kittens wearing hats, how many kittens are there?",
                "Peppermint Butler drew {num1} dark magic pentagram circles on the floor. If each circle needs {num2} shadow candles lit around it, how many candles does he need total?",
                "Flame Princess sent {num1} fire elemental sparks flying into the air. If each spark multiplies into {num2} tiny fireflies, how many fireflies are on screen?",
                "Cinnamon Bun bought {num1} crates of sugar bricks to build a candy wall. If each crate holds exactly {num2} pink sugar bricks, how many bricks does he have altogether?",
                "Magic Man transformed into {num1} different forest birds. If each bird laid exactly {num2} trick eggs that hatch into bubbles, how many bubble eggs are in the nest?",
                "The Lich cast {num1} dark green spells of decay. If each spell destroys exactly {num2} ancient oak trees in the forest, how many trees were destroyed total?",
                "Choose Goose packed {num1} storage bags for the flea market. If each bag contains exactly {num2} rhyming joke books, how many joke books does he have total?",
                "The Banana Guard sergeant set up {num1} guard towers on the outer wall. If each tower has exactly {num2} banana spears ready, how many spears are on the walls?",
                "Hunson Abadeer ordered {num1} soul-crushing machines for his office. If each machine has {num2} heavy stamping gears running, how many gears are stamping in total?",
                "BMO played {num1} rounds of Conversation Parade. If each round features exactly {num2} weird computer questions, how many total questions did BMO ask?",
                "Susan Strong dug through {num1} ancient tech junk containers. If each container holds exactly {num2} matching fish-hats, how many fish-hats did she recover total?",
                "The Gumball Guardians fired {num1} synchronized laser blasts. If each laser blast vaporizes exactly {num2} rogue invaders, how many invaders did they destroy?",
                "Prismo generated {num1} timeline paths inside the wish matrix. If each path awards Finn {num2} gold ruby gems, how many ruby gems did Prismo create in total?",
                "Billy the Hero fought {num1} giant ocean Krakens. If each Kraken had exactly {num2} heavy tentacles swinging at him, how many tentacles did Billy have to slice through?"
            ],
            "/": [
                "Princess Bubblegum needs to distribute {num1} science test tubes evenly across {num2} laboratory tables. How many tubes go on each table?",
                "Finn wants to share {num1} {item} equally among {num2} Lumpy Space villagers. How many does each villager receive?",
                "Jake wants to split {num1} slices of everything-burrito equally among {num2} of his favorite multi-flavored pups. How many slices does each puppy get?",
                "The Ice King wants to divide {num1} ice-gems evenly among his {num2} favorite wizard crowns. How many ice-gems will he place onto each crown?",
                "Peppermint Butler has {num1} shadow-potions to hand out evenly to {num2} spooky ghosts. How many shadow-potions does each ghost get?",
                "Prismo the Wish Master split {num1} floating pickles evenly into {num2} cosmic bowls for Finn and Jake. How many pickles are in a single cosmic bowl?",
                # --- NEW ADVENTURE TIME DIVISION ---
                "The Earl of Lemongrab has {num1} sour lemon drops that he wants to divide evenly across {num2} locked lunchboxes. How many drops go into each lunchbox?",
                "Flame Princess has {num1} glowing coal chunks to distribute evenly to her {num2} fire salamander pets. How many coal chunks does each salamander receive?",
                "Marceline gathered {num1} old vinyl record albums. She sorts them completely evenly into {num2} wooden crates. How many records fit in a single crate?",
                "Tree Trunks wants to slice up {num1} warm pumpkin pies completely evenly among {num2} fly-log travelers. How many pie slices does each traveler get?",
                "BMO has {num1} digital pixel stars saved in memory. If BMO splits them evenly across {num2} video screen files, how many stars are in each file?",
                "Lumpy Space Princess found {num1} plastic jewel rings in the trash. She shares them evenly among her {num2} phone friends. How many rings does each friend get?",
                "The Cosmic Owl needs to sort {num1} premonition dream boards evenly across {num2} golden cloud lockers. How many boards go into each cloud locker?",
                "Root Beer Guy has {num1} shiny law enforcement badges to split evenly between {num2} newly hired Banana Guards. How many badges does each guard get?",
                "The Lich has {num1} green pools of toxic mutagen waste. If he splits the pools evenly among {num2} ancient wells, how many pools are mapped to each well?",
                "Choose Goose has {num1} magical feathers that he wants to sort evenly across {num2} velvet inkwells. How many feathers go into each inkwell?",
                "Cinnamon Bun has {num1} round gingerbread wheels. He distributes them completely evenly across {num2} candy emergency wagons. How many wheels go on each wagon?",
                "Magic Man has {num1} flying bird wings to sort evenly into {num2} mysterious magician hats. How many wings go into each hat?",
                "The Goblin King has {num1} leather back-scratchers to distribute evenly among {num2} groveling servants. How many back-scratchers does each servant get?",
                "Susan Strong has {num1} heavy metal salvage gears. She divides them up evenly among {num2} toolbags for the tracking group. How many gears fit in each bag?",
                "The Party God has {num1} golden confetti party blast poppers. He distributes them evenly across {num2} disco dance floors. How many poppers go to each floor?",
                "Grob Gob Glob Grod has {num1} space-helmet cleaning cloths. They divide them evenly among their {num2} floating deity heads. How many cloths does each head get?",
                "The Ancient Psychic Tandem War Elephant has {num1} tracking maps saved in its mental brain. It shares them evenly with {num2} chosen heroes. How many maps does each hero get?",
                "Abracadaniel has {num1} colorful magic ribbons. He splits them completely evenly across {num2} wizard sleeves. How many ribbons are tucked into each sleeve?"
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
                "The Party Wagon needs {num1} gallons of regular fuel and {num2} gallons of special turtle-juice booster to run. How many total gallons of fuel does it hold?",
                # --- NEW TMNT ADDITIONS ---
                "Metalhead scanned {num1} Foot bots in the subway and {num2} bots on the rooftops. How many total enemies did the robot turtle scan?",
                "Usagi Yojimbo defeated {num1} rogue samurai in the forest and {num2} in the village square. How many total adversaries did the rabbit ronin stop?",
                "The Neutrinos drove their flying hot rod car through {num1} dimensional portals on Monday and {num2} portals on Tuesday. How many portals did they cross?",
                "Leatherhead gathered {num1} wooden logs to build a swamp fort and found {num2} steel pipes in the sewer. How many construction pieces does he have total?",
                "Baxter Stockman built {num1} mechanical Mouser robots in his main lab and {num2} Mousers in a secret warehouse. How many total Mousers did he build?",
                "Karai ordered {num1} elite Foot archers and {num2} ninja assassins to ambush the turtles. How many total warriors did she deploy?",
                "Slash found {num1} spiked plastic palm trees for his terrarium and {num2} jagged rocks. How many items did the mutant turtle collect total?",
                "The Triceraton empire launched {num1} battle cruisers from their home planet and {num2} cruisers from their space station. How many starships are in the fleet?",
                "Ace Duck bought {num1} flight goggles from the pilot shop and {num2} custom leather bomber jackets. How many gear pieces does he have total?",
                "Mutagen Man absorbed {num1} gallons of glowing yellow waste and {num2} gallons of chemical ooze. How many total gallons are inside his containment suit?",
                "Wingnut found {num1} radar chips in the junkyard and Screwloose found {num2} tracking wires. How many total gadget pieces did the alien bat duo find?",
                "The turtles bought {num1} brown trench coats and {num2} fedora hats to go grocery shopping undercover. How many clothing items did they buy altogether?",
                "Mondays are tough, so Mikey put {num1} scoops of peanut butter and {num2} scoops of clam chowder onto his giant pizza. How many scoops did he use?",
                "The Channel 6 News van drove {num1} miles to cover a jewelry heist and {num2} miles to cover a giant sewer mutant sighting. How many miles did it drive total?",
                "Rahzar found {num1} ancient bone clubs in the museum basement, and Tokka found {num2} large shields. How many weapons did the mutant duo secure?",
                "Splinter bought {num1} containers of green tea leaves and {num2} packages of herbal roots. How many tea supplies did the master purchase?",
                "Ice Cream Kitty froze {num1} sweet strawberry sprinkles and {num2} chocolate chips inside her sewer freezer box. How many treats are frozen total?",
                "The Pizza Thrower vehicle was loaded with {num1} high-speed cheese pizzas and {num2} deep-dish supreme pizzas. How many total pizzas are ready to fire?"
            ],
            "-": [
                "Shredder deployed {num1} Foot Clan ninjas into New York City, but Leo quickly stopped {num2} of them. How many Foot Clan ninjas are left?",
                "Splinter had {num1} meditation candles. The turtles accidentally knocked over {num2} of them during practice. How many candles are left?",
                "Bebop and Rocksteady stole {num1} laser blasters from a secure lab. Raph chased them and smashed {num2} blasters with his sais. How many blasters do the villains have left?",
                "Krang launched {num1} robotic rock soldiers from Dimension X, but the turtles trapped {num2} of them back inside the portal. How many rock soldiers are still on Earth?",
                "Mikey baked {num1} weird jelly-bean and marshmallow pizzas. The other turtles got grossed out and threw {num2} of them away. How many weird pizzas are left?",
                "{name} had {num1} smoke bombs to escape from the Foot Clan. They dropped {num2} bombs into the sewer water by accident. How many smoke bombs do they have left?",
                # --- NEW TMNT SUBTRACTIONS ---
                "Baxter Stockman unleashed {num1} small Mouser robots to chew through the server lines, but Donnie deactivated {num2} of them with an EMP pulse. How many Mousers are left?",
                "The Triceraton army set up {num1} plasma gravity traps across Manhattan, but Leo sliced through {num2} of them with his katanas. How many traps are still active?",
                "Karai had {num1} smoke pellets ready for a swift rooftop escape, but Raph kicked her pouch and broke {num2} of them. How many pellets does she have left?",
                "The Purple Dragons street gang stole {num1} expensive sports motorbikes, but Casey Jones smashed {num2} of them with a cricket bat. How many bikes do they have left?",
                "Shredder forged {num1} sharp steel blades for his armor suit, but Splinter shattered {num2} blades during an intense dojo battle. How many blades are left on his armor?",
                "Krang filled {num1} power cells for his giant android body, but Mikey disconnected {num2} cells while looking for a light switch. How many cells are still powered?",
                "The Technodrome had {num1} functional escape pods, but a massive sewer earthquake jammed {num2} of them shut. How many working escape pods are left?",
                "April O'Neil printed out {num1} top-secret files about the Foot Clan's docks hideout, but she dropped {num2} files into a puddle while running. How many files are still readable?",
                "Metalhead was charged with {num1} laser mini-missiles, but he fired {num2} of them to blast a hole through a brick wall. How many missiles does the robot turtle have left?",
                "Bebop had {num1} retro punk music tapes in his boombox bag, but Rocksteady stepped on {num2} of them by accident. How many music tapes survived?",
                "Leatherhead caught {num1} fresh sewer swamp-rats for his dinner, but Mikey felt bad for them and let {num2} of them escape. How many rats are left?",
                "The Mighty Mutanimals team prepared {num1} smoke shields for a rescue raid, but Slash dropped {num2} shields in the truck. How many smoke shields are left ready?",
                "Usagi Yojimbo carried {num1} traditional throwing daggers in his sash, but he used {num2} of them to cut a rope bridge down. How many daggers does he keep?",
                "The Neutrinos brought {num1} space crystals from Dimension X to power their car, but {num2} crystals dissolved in Earth's air. How many space crystals are left?",
                "Shredder's elite guards had {num1} gold kunai spears, but Donnie's bo staff knocked {num2} spears directly into the river. How many spears are left?",
                "The Channel 6 News station had {num1} micro-video cameras, but Vernon broke {num2} of them while running away from a giant mutant wasp. How many cameras are left?",
                "Muckman had {num1} heaps of garbage loaded into his trash gun, but he accidentally spilled {num2} heaps into a dumpster. How many garbage heaps are left to shoot?",
                "The turtles had {num1} retro arcade game tokens inside their treehouse jar, but Mikey spent {num2} of them playing Rad Racer down at the corner arcade. How many tokens are left?"
            ],
            "*": [
                "The four turtles ate {num1} boxes of pizza. If each box had exactly {num2} slices inside, how many slices did they eat altogether?",
                "Raph practiced his ninja flips {num1} times per hour. If he practiced for {num2} hours, how many flips did he do?",
                "Leo practiced his twin-katana sword strikes. If he did {num1} sets of practice routines, and each routine had {num2} sword swings, how many total swings did he practice?",
                "Donnie is working on the Shellraiser truck's computer. The system has {num1} major circuits, and each circuit requires {num2} microchips. How many total microchips does he need?",
                "Master Splinter assigned {num1} training hours to each of his {num2} turtle sons this week. How many total hours of ninja training did the turtles complete?",
                "Shredder's secret hideout has {num1} storage rooms. If each room has exactly {num2} spike-shields waiting for Foot Soldiers, how many spike-shields are there in total?",
                # --- NEW TMNT MULTIPLICATION ---
                "A Foot Clan training camp has {num1} practice mats. If each mat has exactly {num2} ninja recruits practicing kicks, how many recruits are training total?",
                "Casey Jones bought {num1} boxes of golf balls to throw at bad guys. If each box contains exactly {num2} golf balls, how many balls does he have total?",
                "Bebop and Rocksteady ordered {num1} crates of laser guns. If each crate contains {num2} blasters, how many blasters do the bumbling mutants have altogether?",
                "The Triceraton empire has {num1} space battleships. If each ship is armed with exactly {num2} laser cannons, how many laser cannons are in the fleet?",
                "April O'Neil has {num1} reporting notebooks. If each notebook has exactly {num2} pages of notes about turtle sightings, how many pages of notes does she have?",
                "Donnie built {num1} automated tracking sensors. If each sensor requires exactly {num2} tiny copper coils to pick up mutagen signals, how many coils does he need?",
                "The Party Wagon has {num1} armor-plated doors. If each door has exactly {num2} metal rivets holding it together, how many total rivets are on the doors?",
                "Mikey's custom skateboard has {num1} sticker zones. If he puts exactly {num2} pizza stickers in each zone, how many stickers are on his skateboard total?",
                "Baxter Stockman's computer terminal ran {num1} virus algorithms. If each algorithm hacks into {num2} city servers, how many servers did he infect total?",
                "Metalhead fired {num1} continuous volleys of sparks. If each volley releases exactly {num2} blinding blue sparks, how many total sparks flew into the room?",
                "The Mighty Mutanimals has {num1} supply weapon racks. If each weapon rack holds exactly {num2} spiked clubs, how many clubs do they have in total?",
                "Usagi Yojimbo completed {num1} meditation sessions. If each session lasted exactly {num2} minutes under the waterfall, how many total minutes did he meditate?",
                "The Neutrinos have {num1} cosmic hoverboards. If each board requires exactly {num2} neon power rods to float, how many power rods do they need in total?",
                "Karai mapped out {num1} distinct getaway routes. If each route goes past exactly {num2} secret alleyway drop-boxes, how many drop-boxes are there altogether?",
                "Mousers travel in packs. If there are {num1} packs of Mousers, and each pack contains exactly {num2} robots, how many Mousers are chewing through the walls?",
                "Leatherhead dug {num1} underwater escape tunnels. If each tunnel has exactly {num2} air pocket chambers to rest in, how many air chambers did he dig total?",
                "The local sewer pipeline has {num1} pressure valves. If each valve requires exactly {num2} wrench turns from Donnie to stop leaking, how many turns must he make?",
                "The turtles ordered {num1} family-size cases of hot sauce. If each case contains exactly {num2} spicy bottles, how many hot sauce bottles do they have total?"
            ],
            "/": [
                "Donnie has {num1} ninja throwing stars that he wants to divide equally into {num2} equipment belts. How many stars go into each belt?",
                "The turtles intercepted {num1} stolen mutagen canisters. If they divide them up equally into {num2} secure vaults, how many canisters fit in each vault?",
                "Mikey wants to divide {num1} hot pepperoni slices evenly among {num2} hungry pizza boxes. How many pepperoni slices will go into each box?",
                "Casey Jones found {num1} lost spray-paint cans in the subway. He splits them evenly into {num2} duffel bags to carry them home. How many cans fit in each bag?",
                "The Technodrome's main engine has {num1} warning lights. If the lights are divided evenly across {num2} control panels, how many warning lights are on each panel?",
                "April has {num1} photographs of turtle sightings to file away. If she divides them evenly into {num2} secret news folders, how many photos go into each folder?",
                # --- NEW TMNT DIVISION ---
                "Splinter has {num1} ancient scrolls containing ninja secrets. He divides them equally among his {num2} turtle sons. How many scrolls does each brother get?",
                "Shredder obtained {num1} stolen military radio codes. He wants to divide them up evenly among {num2} Foot Clan captains. How many codes does each captain get?",
                "Bebop and Rocksteady stole {num1} stolen plasma bars from a warehouse. If they divide them completely evenly between themselves, how many bars does each mutant get?",
                "The Triceraton commander wants to split {num1} laser rifles evenly into {num2} standard soldier lockers. How many rifles will be placed in each locker?",
                "Donnie has {num1} backup grapple-hooks. He wants to store them completely evenly across {num2} repair shelves. How many hooks go on each shelf?",
                "Karai has {num1} steel training swords. She divides them up evenly across {num2} weapon racks in the Foot dojo. How many swords go on each rack?",
                "The Channel 6 News room has {num1} blank videotapes to distribute. If they split them evenly among {num2} field reporters, how many tapes does each reporter get?",
                "The Mighty Mutanimals recovered {num1} medical supply kits. If they share them evenly among their {num2} secret bases, how many kits go to each base?",
                "Usagi Yojimbo has {num1} ancient iron coins. He splits them completely evenly among {num2} poor villagers. How many coins does each villager receive?",
                "Baxter Stockman has {num1} spare mechanical gears. He divides them up completely evenly into {num2} repair boxes. How many gears fit in a single box?",
                "The Neutrinos have {num1} gallons of ultra-fuel. If they distribute the fuel evenly across {num2} flying hot rods, how many gallons does each vehicle get?",
                "Leatherhead found {num1} water filters in an abandoned subway station. He divides them evenly across {num2} sewer zones. How many filters go into each zone?",
                "Metalhead has {num1} gigabytes of defensive battle data to upload. If he divides the data evenly into {num2} core storage drives, how many gigabytes go into each drive?",
                "Mikey has {num1} custom skateboard wheels. He divides them completely evenly into {num2} replacement sets. How many wheels are in each set?",
                "A group of Foot ninjas stole {num1} smoke grenades. If they distribute them evenly across {num2} ninja gear belts, how many smoke grenades go into each belt?",
                "Raph has {num1} spare leather wrappings for his weapon handles. He divides them evenly across {num2} storage hooks. How many wrappings go on each hook?",
                "Leo has {num1} target arrows to use for practice. If he shoots them completely evenly into {num2} straw targets, how many arrows hit each target?",
                "The sewer water system has {num1} backup drainage valves. If they are spread completely evenly across {num2} overflow walls, how many valves are installed on each wall?"
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
                "Ironhide welded {num1} shields onto the base doors and {num2} shields onto the roof. How many metal shields did he weld altogether?",
                # --- NEW TRANSFORMERS ADDITIONS ---
                "The Autobot computer Teletraan-1 scanned {num1} civilian sports cars and {num2} jet fighters to find new alt-modes. How many vehicles did it scan total?",
                "Jazz played {num1} loud rock songs to distract Decepticons, and Blaster blasted {num2} more hip-hop tracks. How many songs did they play altogether?",
                "The Constructicons gathered {num1} heavy steel beams to build a fortress and {num2} titanium columns. How many building pieces did they collect total?",
                "Perceptor cataloged {num1} strange cosmic space anomalies and {num2} radio signals coming from deep space. How many total discoveries did the scientist log?",
                "Sideswipe completed {num1} high-speed stunts on the test track, and his twin Sunstreaker completed {num2} stunts. How many total stunts did the brothers do?",
                "The Insecticons devoured {num1} fields of metal farm machinery and {num2} grain silos. How many mechanical targets did they destroy altogether?",
                "Ultra Magnus loaded {num1} heavy missile pods onto the front bumper of his trailer and {num2} pods onto the sides. How many pods did he load total?",
                "Unicron consumed {num1} small spacer asteroid moons and {num2} mechanical rogue comets. How many celestial bodies did the planet-eater swallow?",
                "Cliffjumper fired {num1} rounds of glass gas from his bazooka, and Mirage generated {num2} holographic decoy illusions. How many tactical moves did they use total?",
                "The giant city-bot Metroplex deployed {num1} internal defense drones from his left tower and {num2} drones from his right gate. How many drones are active total?",
                "Rumble pounded his pile-driver arms into the ground and caused {num1} major earthquakes, while Frenzy caused {num2} minor tremors. How many seismic events occurred total?",
                "Skywarp warped through {num1} space warp rifts before his fuel got low, and Thundercracker warped through {num2} rifts. How many total warp jumps did they complete?",
                "A human ally named Spike Witwicky found {num1} old laser pistols in the Ark shipwreck and Sparkplug found {num2} toolsets. How many gear pieces did they recover?",
                "Alpha Trion recorded {num1} historic Cybertronian wars in the Covenant of Primus and logged {num2} peace treaties. How many total documents did he write?",
                "The Dinobot Slag smashed {num1} stone pillars with his triceratops horn, and Sludge stomped down {num2} rock walls. How many obstacles did they demolish total?",
                "The giant defense station Trypticon powered up {num1} internal fusion cannons and {num2} plasma beam arrays. How many total weapons systems are active?",
                "Prowl organized {num1} police tactical blueprints for a street defense and {num2} highway intercept maps. How many strategy guides did he finish?",
                "A hidden bunker stored {num1} ancient cyber-relics from the Golden Age of Cybertron, and an excavation uncovered {num2} more. How many relics do they have now?"
            ],
            "-": [
                "Megatron launched {num1} tracking missiles at the launchpad, but Starscream accidentally knocked {num2} of them off course. How many missiles hit?",
                "Grimlock found {num1} iron car scraps to chew on, but he dropped {num2} of them when he roared. How many scraps does he have left?",
                "The Decepticons stole {num1} plasma batteries from the city power plant, but Bumblebee intercepted them and won back {num2} batteries. How many do the Decepticons still have?",
                "Wheeljack built {num1} wacky scientific inventions in his lab, but {num2} of them accidentally exploded during testing. How many working inventions does he have left?",
                "A group of {num1} Seekers flew into the sky to attack, but Optimus Prime used his laser blaster to knock {num2} of them down. How many Seekers are still flying?",
                "The Matrix of Leadership holds {num1} ancient secrets of the Primes. If Optimus Prime shares {num2} of those secrets with Hot Rod, how many secrets are left hidden?",
                # --- NEW TRANSFORMERS SUBTRACTIONS ---
                "Soundwave loaded {num1} data cartridges into his internal data bank, but Blaster broadcast a jammer signal that wiped {num2} cartridges completely. How many are left?",
                "The Constructicons formed the giant robot Devastator using {num1} heavy construction vehicles, but Optimus Prime blasted {num2} vehicles back out of the link. How many stay joined?",
                "The Insecticons cloned themselves into a swarm of {num1} robotic bugs, but Ironhide sprayed liquid nitrogen and froze {num2} clones solid. How many bugs are still swarming?",
                "Shockwave kept {num1} sentinel drones guarding the Space Bridge core on Cybertron, but a rogue explosion shorted out {num2} of them. How many sentinels are still active?",
                "A supply convoy was carrying {num1} barrels of refined hydro-grease, but Starscream's null-ray zapped the transport and leaked {num2} barrels into the canyon. How many are left?",
                "The giant robot Omega Supreme had {num1} defense shields active while orbiting Earth, but asteroid collisions cracked {num2} shields. How many intact shields are left?",
                "Perceptor prepared {num1} chemical slides of Cybertronian rust under his microscope lens, but he accidentally dropped {num2} slides on the floor. How many slides are left?",
                "Ratchet brought {num1} spare laser-welders to a battlefield repair zone, but {num2} of them lost their battery charge in the cold. How many working welders does he have left?",
                "Megatron forged {num1} dark energon crystals in his hidden smelting pool, but Bumblebee sneaked in and crushed {num2} of them. How many dark crystals remain?",
                "The Autobot base security grid had {num1} operational laser camera turrets, but Laserbeak flew past and snipped the wires of {num2} turrets. How many turrets are still working?",
                "Jazz had {num1} nitro-boost canisters installed inside his car engine frame, but he used up {num2} canisters escaping a Decepticon seeker trap. How many does he keep?",
                "The Dinobot Swoop collected {num1} shiny piece of gold foil scrap from a canyon peak, but he lost {num2} of them when flying through a thunderstorm. How many does he have left?",
                "Teletraan-1 was processing {num1} satellite image streams of the desert, but Megatron's transmission hacked and froze {num2} streams. How many clear images are left?",
                "The Combaticons stole {num1} military warheads from a human army base, but Hound used holographic projections to trick them into dropping {num2} warheads. How many do they keep?",
                "Wheeljack built {num1} high-voltage shock gloves to trap Frenzy, but the gloves malfunctioned and lost power in {num2} seconds. How many seconds of charge do they have left?",
                "A squadron of {num1} Decepticon tank drones guarded the energon mine, but Grimlock transformed into a T-Rex and stomped {num2} drones into flat scrap metal. How many are left?",
                "The Autobots gathered {num1} computer replacement processors from Cybertron, but {num2} of them were incompatible with Earth's grid system. How many processors can they actually use?",
                "Starscream hidden {num1} secret laser snipers inside an extinct volcano, but Megatron discovered his treachery and seized {num2} of them. How many snipers does Starscream have left?"
            ],
            "*": [
                "Bumblebee can scan and clone {num1} types of vehicles. If each vehicle has {num2} wheels, how many wheels has he scanned altogether?",
                "A Transformer team requires {num1} drops of special oil per gear. If a robot has {num2} gears, how many drops of oil are needed?",
                "Grimlock and his {num1} Dinobot friends went hunting for metal tracks. If each Dinobot crunched exactly {num2} old railroad tracks, how many tracks did they smash total?",
                "Shockwave set up {num1} guard towers on Cybertron. If each tower has exactly {num2} purple security cameras watching the borders, how many cameras are there altogether?",
                "Optimus Prime used his Energon Axe to chop through {num1} metal walls. If each wall was {num2} meters thick, how many total meters of solid metal did he chop through?",
                "Soundwave plays secret audio recordings. If he plays {num1} static tapes, and each tape captures {num2} minutes of Decepticon transmissions, how many total minutes did he record?",
                # --- NEW TRANSFORMERS MULTIPLICATION ---
                "The Insecticons set up {num1} electronic hive nests. If each hive nest contains exactly {num2} robotic locust micro-drones, how many micro-drones are there total?",
                "Devastator stomped on {num1} steel skyscrapers. If each skyscraper collapsed into exactly {num2} tons of heavy industrial scrap debris, how many tons of scrap did he create?",
                "The Ark spaceship has {num1} computer hardware racks. If each hardware rack links up exactly {num2} warning system lights, how many warning lights are installed?",
                "Wheeljack ordered {num1} cases of high-grade copper wires. If each case contains exactly {num2} spools of insulated wire, how many spools did he get altogether?",
                "A group of Seekers flew in {num1} V-shaped formations. If each formation features exactly {num2} supersonic jet fighters, how many jet fighters are in the sky?",
                "Megatron fired his Fusion Cannon {num1} times. If each laser blast vaporizes exactly {num2} meters of concrete blast walls, how many meters of concrete were destroyed?",
                "The space bridge needs to open {num1} times this week. If each warp sequence requires exactly {num2} power cells to stabilize the portal, how many cells are consumed?",
                "Autobot Hound set up {num1} projector fields. If each projector field generates exactly {num2} hyper-realistic military decoy trucks, how many decoy trucks are projected?",
                "The Dinobot Snarl has {num1} golden plates on his stegosaurus back. If each golden plate absorbs exactly {num2} megawatts of solar energy, how many megawatts does he store?",
                "Soundwave has {num1} cassette deck slots inside his storage trunk. If each slot holds exactly {num2} micro-cassette spies, how many cassette spies can he store altogether?",
                "Ratchet sorted {num1} medical toolbags for an emergency field hospital. If each bag contains exactly {num2} laser scalpels, how many scalpels does the medic have ready?",
                "The Decepticon warship Nemesis has {num1} hangar bays. If each hangar bay holds exactly {num2} small interstellar escape starships, how many escape ships are docked total?",
                "Unicron targeted {num1} solar systems. If he plans to consume exactly {num2} automated fuel moons in every single system, how many moons will he devour?",
                "Autobot Mirage can stay invisible for {num1} minutes per battery charge. If he uses {num2} fully charged spare batteries, how many total minutes can he remain stealthy?",
                "The Predacons organized {num1} hunting patrols through the iron jungle. If each hunting patrol deploys exactly {num2} tracking mechanical panthers, how many panthers are out?",
                "Ironhide welded {num1} sheet metal patches onto the Ark's main hull armor. If each metal patch requires exactly {num2} titanium rivets, how many rivets did he use total?",
                "A group of {num1} engineering bots are repairing Cybertron's main highway grids. If each bot replaces exactly {num2} heavy fiber cables, how many cables are installed?",
                "The Matrix of Leadership shone its light through {num1} dark catacombs. If each catacomb has {num2} corrupted control nodes that get purified, how many nodes were saved?"
            ],
            "/": [
                "Optimus Prime wants to distribute {num1} Energon cubes equally among {num2} battle stations. How many cubes go to each station?",
                "Starscream gathered {num1} space blasters to distribute evenly among {num2} Decepticon soldiers. How many blasters does each soldier get?",
                "Megatron wants to split {num1} stolen computer core servers equally among his {num2} craftiest space scientists. How many servers does each scientist get?",
                "The giant robot Omega Supreme has {num1} rocket boosters. If they are divided evenly across his {num2} landing tracks, how many boosters are on each track?",
                "Bumblebee has {num1} spare tire parts to share evenly among his {num2} favorite human mechanic friends. How many tire parts does each mechanic get?",
                "A tactical computer needs to sort {num1} Cybertronian coordinates evenly into {num2} navigation maps. How many coordinates will be saved onto each map?",
                # --- NEW TRANSFORMERS DIVISION ---
                "The Constructicons stole {num1} heavy plasma generators. If they split them up completely evenly across their {num2} members, how many generators does each construct get?",
                "Soundwave recovered {num1} secret audio spy transmissions from the human network. He divides them evenly into {num2} encrypted data folders. How many files go in each?",
                "Autobot Jazz has {num1} laser speakers to set up for a celebration party. If he distributes them evenly across {num2} audio stages, how many speakers go on each stage?",
                "Wheeljack synthesized {num1} gallons of highly volatile jet fuel booster. He splits the fuel evenly into {num2} pressurized containers. How many gallons are in a container?",
                "A squadron of Seekers intercepted {num1} communication tracking radar dishes. If they sort them evenly across {num2} surveillance outposts, how many dishes go to each?",
                "The Dinobot Grimlock gathered {num1} shiny crown jewels from an ancient chamber. He splits them completely evenly among his {num2} Dinobot teammates. How many jewels does each get?",
                "An Autobot tactical squad recovered {num1} stolen mechanical blueprints from a base. If they divide them evenly into {num2} secure wall safes, how many files fit in each?",
                "The computer Teletraan-1 has {num1} planetary emergency alerts to display. If the alerts are split evenly across {num2} monitor screens, how many alerts show on a single screen?",
                "Autobot Ratchet has {num1} replacement micro-chips for damaged circuits. He splits them completely evenly among {num2} deactivated soldiers. How many chips does each get?",
                "Shockwave has {num1} barrels of liquid coolant to preserve the Space Bridge core. He divides them completely evenly among {num2} reactor pillars. How many barrels go to each?",
                "Megatron wants to distribute {num1} laser mini-cannons evenly across {num2} defense barricades around Kaon city. How many mini-cannons are mounted on each barricade?",
                "The giant bot Metroplex has {num1} repair drones available. If he divides the drone crew completely evenly across his {num2} main landing bays, how many drones go to each bay?",
                "Perceptor has {num1} crystalline magnifying glass lenses to organize. He packs them completely evenly into {num2} cushioned laboratory kits. How many lenses fit in a kit?",
                "Autobot Springer has {num1} spare helicopter rotor blades. He distributes them completely evenly among {num2} flight transport storage lockers. How many blades go in each?",
                "A mining operation extracted {num1} tons of raw metal ore. The Decepticons divide the load completely evenly across {num2} cargo hover-trains. How many tons go on each train?",
                "Blaster has {num1} music tape cassettes to share. If he divides them completely evenly among his {num2} favorite human friends, how many tapes does each friend receive?",
                "The Autobot Elite Guard has {num1} star navigation medals to award. If they are distributed completely evenly among {num2} starship captains, how many medals does each get?",
                "A tactical scanner logged {num1} heat signatures from deep space. If the tracking signatures are divided evenly among {num2} computer analysis hubs, how many go to each hub?"
            ]
        }
    }
}


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
        'width': '20vw', 'height': '16vh',
        'backgroundColor': 'rgba(255, 255, 255, 0.6)', 
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
            style={'fontFamily': "Comic Sans MS", 
                   'fontWeight': 'bold',
                   'width': '18vw', 
                   'height': '6vh',
                   }
        ),
        html.Div(style={'flexGrow': '1'}),
        #html.Small("Change themes anytime to swap questions and colors!", style={'color': '#7F8C8D', 'textAlign': 'center'})
    ]),
    
    # Central Testing Dashboard Card
    html.Div(id='central-game-card', style={
        'backgroundColor': 'rgba(255, 255, 255, 0.8)', 
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
        html.Div(id='app-subtitle', children="Can you solve this challenge?", style={'color': '#5DADE2', 'fontSize': '20px', 'fontWeight': 'bold'}),
        html.Hr(style={'border': '1px dashed #FFB6C1', 'margin': '15px 0'}),
        
        # Action Notification Area
        html.Div(id='last-action-feedback', style={'fontSize': '18px', 'fontWeight': 'bold', 'minHeight': '30px', 'marginBottom': '10px'}),

        # Target Word/Math Problem Box
        html.Div(id='question-box', style={
            'fontSize': '20px', 'fontWeight': 'bold', 'margin': '15px 0', 
            'minHeight': '60px', 'color': '#2C3E50', 'padding': '12px',
            'backgroundColor': '#EAFAF1', 
            'borderRadius': '15px', 'border': '3px solid #2ECC71' 
        }),
        
        # User Interface Blocks
        html.Div([
            dcc.Input(id='user-answer', type='number', placeholder='?', style={
                'fontSize': '26px', 
                'width': '110px', 
                'textAlign': 'center', 
                'borderRadius': '12px', 
                'border': '3px solid #FFB6C1', 
                'padding': '6px', 
                'fontWeight': 'bold',
                'display': 'inline-block',
                'vertical-align': 'top',
                "margin-right": "1%",
            }),
            html.Button('💥 Check Answer!', id='submit-btn', n_clicks=0, n_clicks_timestamp=0, style={
                'fontSize': '18px', 
                'color': 'white', 
                'border': 'none', 
                'padding': '12px 30px', 
                'borderRadius': '50px', 
                'cursor': 'pointer', 
                'fontWeight': 'bold',
                'display': 'inline-block',
                'vertical-align': 'top',
                'margin-left': '1%',
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
    Output('question-box', 'style'),   # <-- NEW OUTPUT
    Output('user-answer', 'style'),   # <-- NEW OUTPUT
    Input('submit-btn', 'n_clicks'),
    Input('theme-selector', 'value'),
    State('user-answer', 'value'),
    State('correct-answer', 'data'),
    State('score-tracker', 'data'),
    State('question-box', 'children'),
    State('main-bg-container', 'style'),
    State('central-game-card', 'style'),
    State('submit-btn', 'style'),
    State('question-box', 'style'),   # <-- NEW STATE
    State('user-answer', 'style'),   # <-- NEW STATE
    prevent_initial_call=False
)
def run_themed_game(submit_clicks, active_theme, user_ans, current_correct, score, current_question, bg_style, card_style, btn_style, q_box_style, input_style):
    ctx = callback_context
    cfg = THEME_DATA[active_theme]
    
    # Helper tracker strings
    def format_score_text(s):
        pct = int((s['correct'] / s['total']) * 100) if s['total'] > 0 else 0
        return f"⭐ Badges: {s['correct']} / {s['total']} | Success Rate: {pct}% ⭐"

    # Define full contextual UI updates based on configurations
    title_text = f"🌟 {active_theme.upper()} MATH LAB! 🌟"
    title_style = {'color': cfg['accent_color'], 'fontSize': '28px', 'fontWeight': 'bold', 'margin': '0 0 5px 0'}
    subtitle_style = {'color': cfg['accent_color'], 'fontSize': '20px', 'fontWeight': 'bold'}
    
    # Mutate layout wrapper borders & colors
    bg_style['backgroundColor'] = cfg['bg_color']
    card_style['border'] = f"6px solid {cfg['card_border']}"
    
    # DYNAMIC THEME BORDERS GENERATION HERE
    q_box_style['border'] = f"4px solid {cfg['question_border']}"
    input_style['border'] = f"3px solid {cfg['accent_color']}"
    
    # Re-render actionable buttons
    new_btn_style = {
        'fontSize': '18px', 
        'backgroundColor': cfg['accent_color'], 
        'color': 'white', 
        'border': 'none', 
        'padding': '12px 30px', 
        'borderRadius': '50px', 
        'cursor': 'pointer',
        'fontWeight': 'bold', 
        'boxShadow': f"0px 4px 0px {cfg['button_shadow']}",
        'display': 'inline-block',
        'margin-left': '1%',
        'vertical-align': 'top',
    }

    # Trigger branch evaluation 
    triggered_id = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    # Condition A: Theme was swapped OR application booted up fresh
    if not triggered_id or triggered_id == 'theme-selector.value':
        next_q, next_ans = generate_problem_by_theme(active_theme)
        if cfg["images"]:
            bg_style['backgroundImage'] = f"url('/assets/{random.choice(cfg['images'])}')"
        return next_q, next_ans, f" Switched to {active_theme}! Go!", score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style

    # Condition B: Blank Form Submission Safety Check
    if user_ans is None:
        reminder = html.Span("Type a number first! 🤔", style={'color': '#E67E22'})
        return current_question, current_correct, reminder, score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style

    # Process correct/incorrect logic
    if int(user_ans) == current_correct:
        feedback = html.Span("✅ Correct! Magnificent job! ✅", style={'color': '#2ECC71'})
        score['correct'] += 1
    else:
        feedback = html.Span(f"❌ Close! The right answer was {current_correct}.", style={'color': '#E74C3C'})
    score['total'] += 1

    # Advance to the next question automatically
    next_q, next_ans = generate_problem_by_theme(active_theme)
    if cfg["images"]:
        bg_style['backgroundImage'] = f"url('/assets/{random.choice(cfg['images'])}')"

    return next_q, next_ans, feedback, score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
    
    
    
