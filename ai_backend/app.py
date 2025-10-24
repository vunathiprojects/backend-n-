from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os, json, re, random
import logging
from openai import OpenAI
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    logger.error("OPENROUTER_API_KEY not found in environment variables")
    API_KEY = "invalid_key"  # Set a placeholder to prevent startup crash

# Initialize client with error handling
try:
    client = OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ChatRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    student_question: str
    chat_history: Optional[List[Dict]] = None

class StudyPlanRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    days_available: int = 7
    hours_per_day: int = 2

class NotesRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    specific_topic: Optional[str] = None
# Corrected CBSE 7th–10th Computers & English units & topics (for quickpractice)
CHAPTERS_DETAILED = {
    "7th": {
    "Computers": {
        " Chapter 1: Programming Language": [
            "What is a programming language?",
            "Types: Low-level vs High-level languages",
            "Examples and real-world uses",
            "Simple pseudocode or introduction to programming logic"
        ],
        "Chapter 2: Editing Text in Microsoft Word": [
            "Creating, saving, and opening documents",
            "Text formatting: fonts, sizes, colors, bold, italics",
            "Paragraph alignment, bullets, numbering",
            "Inserting images, tables, and hyperlinks"
        ],
        "Chapter 3: Microsoft PowerPoint": [
            "Creating slides and using slide layouts",
            "Adding and editing text and images",
            "Applying themes and transitions",
            "Running a slideshow"
        ],
        "Chapter 4: Basics of Microsoft Excel": [
            "Entering and formatting data in cells",
            "Basic formulas (SUM, AVERAGE)",
            "Creating charts from data",
            "Simple data organization (sorting and filtering)"
        ],
        "Chapter 5: Microsoft Access": [
            "Understanding databases and tables",
            "Creating a simple database",
            "Adding, editing, and searching records",
            "Basic queries"
        ]
    },
    "English": {
        "Chapter 1: Learning Together": [
            "The Day the River Spoke: Sentence completion, onomatopoeia, fill-in-the-blanks, prepositions",
            "Try Again: Phrases, metaphor and simile",
            "Three Days to See: Modal verbs, descriptive paragraph writing"
        ],
        "Chapter 2: Wit and Humour": [
            "Animals, Birds, and Dr. Dolittle: Compound words, palindrome, present perfect tense, notice writing",
            "A Funny Man: Phrasal verbs, adverbs and prepositions",
            "Say the Right Thing: Suffixes, verb forms, tenses, kinds of sentences"
        ],
        "Chapter 3: Dreams & Discoveries": [
            "My Brother's Great Invention: Onomatopoeia, binomials, phrasal verbs, idioms, simple past and past perfect tense",
            "Paper Boats: Antonyms (opposites), diary entry writing",
            "North, South, East, West: Associate words with meanings, subject-verb agreement, letter format (leave application)"
        ],
        "Chapter 4: Travel and Adventure": [
            "The Tunnel: Phrases, onomatopoeia, punctuation, descriptive paragraph writing",
            "Travel: Onomatopoeia",
            "Conquering the Summit: Phrases, parts of speech, articles, formal letter writing"
        ],
        "Chapter 5: Bravehearts": [
            "A Homage to Our Brave Soldiers: Prefix and root words, main clause, subordinate clause, subordinating conjunctions",
            "My Dear Soldiers: Collocations",
            "Rani Abbakka: Fill-in-the-blanks (spelling), speech (direct & indirect)"
        ]
    },
    "Mathematics": {
        "Chapter 1: Integers": [
            "Properties of addition and subtraction of integers",
            "Multiplication of integers",
            "Properties of multiplication of integers",
            "Division of integers",
            "Properties of division of integers"
        ],
        "Chapter 2: Fractions and Decimals": [
            "Multiplication of fractions",
            "Division of fractions",
            "Multiplication of decimal numbers",
            "Division of decimal numbers"
        ],
        "Chapter 3: Data Handling": [
            "Representative values",
            "Arithmetic mean",
            "Mode",
            "Median",
            "Use of bar graphs with different purposes"
        ],
        "Chapter 4: Simple Equations": [
            "A mind-reading game (intro activity)",
            "Setting up an equation",
            "What is an equation?",
            "More equations",
            "Application of simple equations to practical situations"
        ],
        "Chapter 5: Lines and Angles": [
            "Introduction and related angles",
            "Pairs of lines",
            "Checking for parallel lines"
        ],
        "Chapter 6: The Triangle and Its Properties": [
            "Medians of a triangle",
            "Altitudes of a triangle",
            "Exterior angle and its property",
            "Angle sum property of a triangle",
            "Two special triangles: equilateral and isosceles",
            "Sum of lengths of two sides of a triangle",
            "Right-angled triangles and Pythagoras' property"
        ],
        "Chapter 7: Comparing Quantities": [
            "Percentage– another way of comparing quantities",
            "Uses of percentages",
            "Prices related to an item (buying/selling scenarios)",
            "Charge given on borrowed money or simple interest"
        ],
        "Chapter 8: Rational Numbers": [
            "Introduction and need for rational numbers",
            "Positive and negative rational numbers",
            "Rational numbers on the number line",
            "Rational numbers in standard form",
            "Comparison of rational numbers",
            "Rational numbers between two rational numbers",
            "Operations on rational numbers"
        ],
        "Chapter 9: Perimeter and Area": [
            "Area of parallelogram",
            "Area of triangles",
            "Understanding circles (circumference/area)"
        ],
        "Chapter 10: Algebraic Expressions": [
            "Introduction to algebraic expressions",
            "Formation of expressions",
            "Terms of an expression",
            "Like and unlike terms",
            "Monomials, binomials, trinomials, polynomials",
            "Finding the value of an expression"
        ],
        "Chapter 11: Exponents and Powers": [
            "Introduction to exponents",
            "Laws of exponents",
            "Miscellaneous examples using laws of exponents",
            "Decimal number system",
            "Expressing large numbers in standard form"
        ],
        "Chapter 12: Symmetry": [
            "Lines of symmetry for regular polygons",
            "Rotational symmetry",
            "Line symmetry vs. rotational symmetry"
        ],
        "Chapter 13: Visualising Solid Shapes": [
            "Plane figures vs. solid shapes",
            "Faces, edges, vertices of 3D shapes (cubes, cuboids, cones, etc.)",
            "Visualisation from different perspectives"
        ]
    },
    "Science": {
        "Chapter1: Nutrition in Plants": [
            "Photosynthesis",
            "Modes of nutrition: Autotrophic, Heterotrophic",
            "Saprotrophic nutrition",
            "Structure of leaves"
        ],
        "Chapter2: Nutrition in Animals": [
            "Human digestive system",
            "Nutrition in different animals",
            "Feeding habits"
        ],
        "Chapter3: Fibre to Fabric": [
            "Natural fibres (Cotton, Wool, Silk)",
            "Processing of fibres",
            "Spinning, Weaving, Knitting"
        ],
        "Chapter4: Heat": [
            "Hot and cold objects",                  
            "Measurement of temperature",        
            "Laboratory thermometer",         
            "Transfer of heat",
            "Kinds of clothes we wear in summer and winter"
        ],
        "Chapter5: Acids, Bases and Salts": [
            "Acid and base indicators",
            "Natural indicators around us",
            "Neutralisation in daily life"
        ],
        "Chapter6: Physical and Chemical Changes": [
            "Changes around us",
            "Physical and chemical changes with examples",
            "Rusting of iron and its prevention",
            "Crystallisation"
        ],
        "Chapter7: Weather, Climate and Adaptations of Animals": [
            "Difference between weather and climate",
            "Climate and adaptation",
            "Effect of climate on living organisms",
            "Polar regions and tropical rainforests"
        ],
        "Chapter8: Winds, Storms and Cyclones": [
            "Air exerts pressure",
            "Air expands on heating",
            "Wind currents and convection",
            "Thunderstorms and cyclones"
        ],
        "Chapter9: Soil": [
            "Soil profile and soil types",
            "Properties of soil",
            "Soil and crops"
        ],
        "Chapter10: Respiration in Organisms": [
            "Why do we respire?",
            "Types of respiration: aerobic and anaerobic",
            "Breathing in animals and humans",
            "Breathing cycle and rate"
        ],
        "Chapter11: Transportation in Animals and Plants": [
            "Circulatory system: heart, blood, blood vessels",
            "Excretion in animals",
            "Transport of water and minerals in plants",
            "Transpiration"
        ],
        "Chapter12: Reproduction in Plants": [
            "Modes of reproduction: asexual and sexual",
            "Vegetative propagation",
            "Pollination and fertilisation",
            "Seed dispersal"
        ],
        "Chapter13: Motion and Time": [
            "Concept of speed",
            "Measurement of time",
            "Simple pendulum",
            "Distance-time graph"
        ],
        "Chapter14: Electric Current and Its Effects": [
            "Symbols of electric components",
            "Heating effect of electric current",
            "Magnetic effect of electric current",
            "Electromagnet and its uses"
        ],
        "Chapter15: Light": [
            "Reflection of light",
            "Plane mirror image formation",
            "Spherical mirrors and lenses",
            "Uses of lenses"
        ],
        "Chapter16: Water: A Precious Resource": [
            "Availability of water on earth",
            "Forms of water",
            "Groundwater and water table",
            "Water management",
            "Water scarcity and conservation"
        ],
        "Chapter17: Forests: Our Lifeline": [
            "Importance of forests",
            "Interdependence of plants and animals in forests",
            "Deforestation and conservation"
        ],
        "Chapter18: Wastewater Story": [
            "Importance of sanitation",
            "Sewage and wastewater treatment",
            "Sanitation at public places"
        ]
    },
    "History": {
        "Chapter 1: Tracing Changes through a Thousand Years": [
            "Maps and how they tell us about history",
            "New and old terminologies used by historians",
            "Historians and their sources (manuscripts, inscriptions, coins)",
            "New social and political groups",
            "Region and empire"
        ],
        "Chapter 2: New Kings and Kingdoms": [
            "Emergence of new dynasties",
            "Administration in kingdoms",
            "Warfare for wealth and power",
            "Prashastis and land grants"
        ],
        "Chapter 3: The Delhi Sultans (12th–15th Century)": [
            "Political and military expansion under rulers",
            "Administration and consolidation",
            "Construction of mosques and cities",
            "Raziya Sultan and Muhammad Tughlaq case studies"
        ],
        "Chapter 4: The Mughal Empire (16th–17th Century)": [
            "Establishment and expansion of the Mughal Empire",
            "Akbar's policies and administration (Mansabdari system, sulh-i-kul)",
            "Jahangir, Shah Jahan, Aurangzeb",
            "Relations with other rulers"
        ],
        "Chapter 5: Rulers and Buildings / Tribes, Nomads and Settled Communities": [
            "Tribal societies and their lifestyle",
            "Nomadic pastoralists",
            "Emergence of new caste-based communities",
            "Interaction between nomads and settled societies"
        ],
        "Chapter 6: Devotional Paths to the Divine": [
            "Bhakti movement and saints (Basavanna, Kabir, Mirabai, etc.)",
            "Sufi traditions",
            "New religious developments in different regions"
        ],
        "Chapter 7: The Making of Regional Cultures": [
            "Language, literature, and regional identity",
            "Regional art, dance, and music forms",
            "Case study: Kathak and Manipuri",
            "Regional traditions in temple architecture"
        ],
        "Chapter 8: Eighteenth Century Political Formations": [
            "Decline of the Mughal Empire",
            "Emergence of new independent kingdoms",
            "Marathas, Sikhs, Jats, Rajputs",
            "Regional states and their administration"
        ]
    },
    "Civics": {
        "Chapter 1: On Equality": [
            "Equality in Indian democracy",
            "Issues of inequality (caste, religion, gender, economic)",
            "Government efforts to promote equality"
        ],
        "Chapter 2: Role of the Government in Health": [
            "Public health services vs. private health services",
            "Importance of healthcare",
            "Inequality in access to healthcare",
            "Case studies"
        ],
        "Chapter 3: How the State Government Works": [
            "Role of the Governor and Chief Minister",
            "State legislature and its functioning",
            "Role of MLAs",
            "Case study of a state government decision"
        ],
        "Chapter 4: Growing up as Boys and Girls": [
            "Gender roles in society",
            "Stereotypes related to boys and girls",
            "Experiences of growing up in different societies",
            "Equality for women"
        ],
        "Chapter 5: Women Change the World": [
            "Women in education and work",
            "Struggles for equality",
            "Case studies of women achievers",
            "Laws for women's rights"
        ],
        "Chapter 6: Understanding Media": [
            "Role of media in democracy",
            "Influence of media on public opinion",
            "Commercialisation and bias in media",
            "Need for independent media"
        ],
        "Chapter 7: Markets Around Us": [
            "Weekly markets, shops, and malls",
            "Chain of markets (producers to consumers)",
            "Role of money and middlemen",
            "Impact on farmers and small traders"
        ],
        "Chapter 8: A Shirt in the Market": [
            "Process of production and distribution",
            "Globalisation and trade",
            "Role of traders, exporters, workers",
            "Consumer awareness"
        ]
    },
    "Geography": {
        "Chapter 1: Environment": [
            "Components of environment (natural, human, human-made)",
            "Ecosystem",
            "Balance in the environment"
        ],
        "Chapter 2: Inside Our Earth": [
            "Layers of the earth (crust, mantle, core)",
            "Types of rocks (igneous, sedimentary, metamorphic)",
            "Rock cycle",
            "Minerals and their uses"
        ],
        "Chapter 3: Our Changing Earth": [
            "Lithosphere movements (earthquakes, volcanoes)",
            "Major landform features (mountains, plateaus, plains)",
            "Work of rivers, wind, glaciers, sea waves"
        ],
        "Chapter 4: Air": [
            "Composition of atmosphere",
            "Structure of atmosphere",
            "Weather and climate",
            "Distribution of temperature and pressure",
            "Wind and moisture"
        ],
        "Chapter 5: Water": [
            "Distribution of water on earth",
            "Water cycle",
            "Oceans (waves, tides, currents)",
            "Importance of water"
        ],
        "Chapter 6: Human-Environment Interactions– The Tropical and the Subtropical Region": [
            "Amazon basin (equatorial region)",
            "Ganga-Brahmaputra basin (subtropical region)",
            "Life of people in these regions"
        ],
        "Chapter 7: Life in the Deserts": [
            "Hot deserts (Sahara)",
            "Cold deserts (Ladakh)",
            "Adaptations of people and animals",
            "Economic activities in deserts"
        ]
    }
},
   "8th": {
    "Computers": {
        "Chapter:1 Exception Handling in Python": [
            "Introduction to errors and exceptions",
            "Types of errors: Syntax errors, Runtime errors (exceptions), Logical errors",
            "Built-in exceptions (ZeroDivisionError, ValueError, etc.)",
            "Using try–except block",
            "try–except–else–finally structure",
            "Raising exceptions using raise",
            "Real-life examples of exception handling (division by zero, invalid input)"
        ],
        "Chapter:2 File Handling in Python": [
            "Introduction to file handling",
            "Types of files: Text files, Binary files",
            "Opening and closing files (open(), close())",
            "File modes (r, w, a, r+)",
            "Reading from a file (read(), readline(), readlines())",
            "Writing to a file (write(), writelines())",
            "File pointer and cursor movement (seek(), tell())",
            "Practical applications: saving student records, logs, etc."
        ],
        "Chapter:3 Stack (Data Structure)": [
            "Introduction to stack",
            "LIFO principle (Last In First Out)",
            "Stack operations: Push, Pop, Peek/Top",
            "Stack implementation using list in Python or modules (collections.deque)",
            "Applications: Undo operation in editors, Function call management"
        ],
        "Chapter:4 Queue (Data Structure)": [
            "Introduction to queue",
            "FIFO principle (First In First Out)",
            "Queue operations: Enqueue, Dequeue",
            "Types of queues: Simple, Circular, Deque, Priority",
            "Implementation in Python using lists or queue module",
            "Applications: Printer task scheduling, Customer service systems"
        ],
        "Chapter:5 Sorting": [
            "Importance of sorting in data organization",
            "Basic sorting techniques: Bubble Sort, Selection Sort, Insertion Sort",
            "Advanced sorting (introductory): Merge Sort, Quick Sort",
            "Sorting in Python using built-in methods: sorted() function"
        ]
    },
    "English": {
        " Unit:1 Honeydew – Prose": [
            "The Best Christmas Present in the World: Narrative comprehension, vocabulary",
            "The Tsunami: Disaster narrative, sequencing events",
            "Glimpses of the Past: Historical narrative, chronology",
            "Bepin Choudhury's Lapse of Memory: Character sketch, irony",
            "The Summit Within: Motivation, descriptive writing",
            "This is Jody's Fawn: Empathy, moral choice",
            "A Visit to Cambridge: Biographical narrative",
            "A Short Monsoon Diary: Diary entry style",
            "The Great Stone Face – I: Description, prediction",
            "The Great Stone Face – II: Conclusion, moral lesson"
        ],
        "Unit:2 Honeydew – Poems": [
            "The Ant and the Cricket: Moral fable, rhyme scheme",
            "Geography Lesson: Imagery, meaning",
            "Macavity: The Mystery Cat: Humour, personification",
            "The Last Bargain: Metaphor, symbolism",
            "The School Boy: Theme of education, freedom",
            "The Duck and the Kangaroo: Rhyme, humour",
            "When I set out for Lyonnesse: Imagination, rhyme",
            "On the Grasshopper and Cricket: Nature imagery"
        ],
        "Unit:3 It So Happened – Supplementary": [
            "How the Camel Got His Hump: Fable, character traits",
            "Children at Work: Social issue, empathy",
            "The Selfish Giant: Allegory, moral theme",
            "The Treasure Within: Education, individuality",
            "Princess September: Freedom, symbolism",
            "The Fight: Conflict resolution",
            "The Open Window: Humour, irony",
            "Jalebis: Humour, moral lesson",
            "The Comet – I: Science fiction, prediction",
            "The Comet – II: Resolution, conclusion"
        ]
    },
    "Mathematics": {
        "Chapter 1: Rational Numbers": ["Introduction", "Properties of Rational Numbers", "Representation of Rational Numbers on the Number Line", "Rational Number between Two Rational Numbers", "Word Problems"],
        "Chapter 2: Linear Equations in One Variable": ["Introduction", "Solving Equations which have Linear Expressions on one Side and Numbers on the other Side", "Some Applications", "Solving Equations having the Variable on both sides", "Some More Applications", "Reducing Equations to Simpler Form", "Equations Reducible to the Linear Form"],
        "Chapter 3: Understanding Quadrilaterals": ["Introduction", "Polygons", "Sum of the Measures of the Exterior Angles of a Polygon", "Kinds of Quadrilaterals", "Some Special Parallelograms"],
        "Chapter 4: Data Handling": ["Looking for Information", "Organising Data", "Grouping Data", "Circle Graph or Pie Chart", "Chance and Probability"],
        "Chapter 5: Squares and Square Roots": ["Introduction", "Properties of Square Numbers", "Some More Interesting Patterns", "Finding the Square of a Number", "Square Roots", "Square Roots of Decimals", "Estimating Square Root"],
        "Chapter 6: Cubes and Cube Roots": ["Introduction", "Cubes", "Cubes Roots"],
        "Chapter 7: Comparing Quantities": ["Recalling Ratios and Percentages", "Finding the Increase and Decrease Percent", "Finding Discounts", "Prices Related to Buying and Selling (Profit and Loss)", "Sales Tax/Value Added Tax/Goods and Services Tax", "Compound Interest", "Deducing a Formula for Compound Interest", "Rate Compounded Annually or Half Yearly (Semi Annually)", "Applications of Compound Interest Formula"],
        "Chapter 8: Algebraic Expressions and Identities": ["What are Expressions?", "Terms, Factors and Coefficients", "Monomials, Binomials and Polynomials", "Like and Unlike Terms", "Addition and Subtraction of Algebraic Expressions", "Multiplication of Algebraic Expressions: Introduction", "Multiplying a Monomial by a Monomial", "Multiplying a Monomial by a Polynomial", "Multiplying a Polynomial by a Polynomial", "What is an Identity?", "Standard Identities", "Applying Identities"],
        "Chapter 9: Mensuration": ["Introduction", "Let us Recall", "Area of Trapezium", "Area of General Quadrilateral", "Area of Polygons", "Solid Shapes", "Surface Area of Cube, Cuboid and Cylinder", "Volume of Cube, Cuboid and Cylinder", "Volume and Capacity"],
        "Chapter 10: Exponents and Powers": ["Introduction", "Powers with Negative Exponents", "Laws of Exponents", "Use of Exponents to Express Small Numbers in Standard Form"],
        "Chapter 11: Direct and Inverse Proportions": ["Introduction", "Direct Proportion", "Inverse Proportion"],
        "Chapter 12: Factorisation": ["Introduction", "What is Factorisation?", "Division of Algebraic Expressions", "Division of Algebraic Expressions Continued (Polynomial / Polynomial)", "Can you Find the Error?"],
        "Chapter 13: Introduction to Graphs": ["Introduction", "Linear Graphs", "Some Applications"]
    },
    "Science": {
        "Chapter:1 Crop Production and Management": ["Agriculture practices", "Crop production techniques", "Storage and preservation"],
        "Chapter:2 Microorganisms: Friend and Foe": ["Bacteria, viruses, fungi", "Useful microbes", "Harmful microbes and diseases"],
        "Chapter:3 Synthetic Fibres and Plastics": ["Types of synthetic fibres", "Characteristics and uses", "Plastics: Thermoplastics, Thermosetting"],
        "Chapter:4 Materials: Metals and Non-Metals": ["Physical and chemical properties", "Reactivity series", "Uses of metals and non-metals"],
        "Chapter:5 Coal and Petroleum": ["Fossil fuels", "Refining petroleum", "Uses of coal and petroleum"],
        "Chapter:6 Combustion and Flame": ["Types of combustion", "Structure of flame", "Fire safety"],
        "Chapter:7 Conservation of Plants and Animals": ["Biodiversity", "Endangered species", "Wildlife conservation"],
        "Chapter:8 Cell – Structure and Functions": ["Plant and animal cell", "Cell organelles", "Cell division"],
        "Chapter:9 Reproduction in Animals": ["Modes of reproduction", "Human reproductive system", "Fertilization and development"],
        "Chapter:10 Force and Pressure": ["Types of forces", "Pressure in solids, liquids, and gases", "Applications"],
        "Chapter:11 Friction": ["Advantages and disadvantages", "Reducing friction"],
        "Chapter:12 Sound": ["Production and propagation", "Characteristics of sound", "Human ear"],
        "Chapter:13 Chemical Effects of Electric Current": ["Electrolysis", "Applications in daily life"],
        "Chapter:14 Some Natural Phenomena": ["Lightning, Earthquakes, and Safety measures"],
        "Chapter:15 Light": ["Reflection, refraction, dispersion", "Human eye and defects"],
        "Chapter:16 Stars and the Solar System": ["Solar system structure", "Planets, moons, comets, and meteors"],
        "Chapter:17 Pollution of Air and Water": ["Causes and effects", "Control measures"]
    },
    "History": {
            "Chapter 1: How, When and Where": ["How do we periodise history?", "Importance of dates and events", "Sources for studying modern history", "Official records of the British administration"],
            "Chapter 2: From Trade to Territory– The Company Establishes Power": ["East India Company comes to India", "Establishment of trade centres", "Battle of Plassey and Buxar", "Expansion of British power in India", "Subsidiary alliance and doctrine of lapse"],
            "Chapter 3: Ruling the Countryside": ["The revenue system under British rule", "Permanent Settlement, Ryotwari and Mahalwari systems", "Effects of British land revenue policies", "Role of indigo cultivation and indigo revolt"],
            "Chapter 4: Tribals, Dikus and the Vision of a Golden Age": ["Tribal societies and their livelihoods", "Impact of British policies on tribal life", "Tribal revolts and resistance", "Birsa Munda and his movement"],
            "Chapter 5: When People Rebel– 1857 and After": ["Causes of the revolt of 1857", "Important centres of the revolt", "Leaders and their roles", "Suppression of the revolt", "Consequences and significance"],
            "Chapter 6: Civilising the 'Native', Educating the Nation": ["The British view on education in India", "Orientalist vs Anglicist debate", "Macaulay's Minute on Education", "Wood's Despatch", "Growth of national education system"],
            "Chapter 7: Women, Caste and Reform": ["Social reform movements in the 19th century", "Reformers and their contributions (Raja Ram Mohan Roy, Ishwar Chandra Vidyasagar, Jyotiba Phule, etc.)", "Movements against caste discrimination", "Role of women in reform and education"],
            "Chapter 8: The Making of the National Movement: 1870s–1947": ["Rise of nationalism in India", "Formation of Indian National Congress", "Moderates, extremists, and their methods", "Partition of Bengal, Swadeshi and Boycott", "Gandhian era movements (Non-Cooperation, Civil Disobedience, Quit India)", "Role of revolutionaries and other leaders", "Towards Independence and Partition"]
       
    },
    "Civics": {
            "Chapter 1: The Indian Constitution": ["Importance and features of the Constitution", "Fundamental Rights and Duties", "Directive Principles of State Policy", "Role of the Constitution in democracy"],
            "Chapter 2: Understanding Secularism": ["Meaning of secularism", "Secularism in India", "Importance of religious tolerance", "Role of the State in maintaining secularism"],
            "Chapter 3: Parliament and the Making of Laws": ["Why do we need a Parliament?", "Two Houses of Parliament (Lok Sabha, Rajya Sabha)", "Law-making process in Parliament", "Role of the President in legislation"],
            "Chapter 4: Judiciary": ["Structure of the Indian judiciary", "Independence of the judiciary", "Judicial review and judicial activism", "Public Interest Litigation (PIL)"],
            "Chapter 5: Understanding Marginalisation": ["Concept of marginalisation", "Marginalised groups in India (Adivasis, Dalits, Minorities)", "Issues faced by marginalised communities"],
            "Chapter 6: Confronting Marginalisation": ["Safeguards in the Constitution for marginalised groups", "Laws protecting marginalised communities", "Role of social reformers and activists"],
            "Chapter 7: Public Facilities": ["Importance of public facilities (water, healthcare, education, transport)", "Role of the government in providing facilities", "Issues of inequality in access to facilities"],
            "Chapter 8: Law and Social Justice": ["Need for laws to ensure social justice", "Workers' rights and protection laws", "Child labour and related legislation", "Role of government in ensuring justice"]
       
    },
    "Geography": {
            "Chapter 1: Resources": ["Types of resources (natural, human-made, human)", "Classification: renewable, non-renewable, ubiquitous, localized", "Resource conservation and sustainable development"],
            "Chapter 2: Land, Soil, Water, Natural Vegetation and Wildlife Resources": ["Land use and land degradation", "Soil types and soil conservation", "Water resources and conservation methods", "Natural vegetation types and importance", "Wildlife resources and conservation"],
            "Chapter 3: Agriculture": ["Types of farming (subsistence, intensive, commercial, plantation)", "Major crops (rice, wheat, cotton, sugarcane, tea, coffee, etc.)", "Agricultural development in different countries", "Impact of technology on agriculture"],
            "Chapter 4: Industries": ["Types of industries (raw material-based, size-based, ownership-based)", "Factors affecting location of industries", "Major industrial regions of the world", "Case studies: IT industry (Bangalore), Cotton textile industry (Ahmedabad/Osaka)"],
            "Chapter 5: Human Resources": ["Population distribution and density", "Factors influencing population distribution", "Population change (birth rate, death rate, migration)", "Population pyramid", "Importance of human resources for development"]
       
    }
},
    "9th": {
    "Computers": {
        "Chapter:1 Basics of Computer System": [
            "Introduction to computer system",
            "Components: Input devices, Output devices, Storage devices, CPU",
            "Memory types: Primary, Secondary, Cache",
            "Number system basics: binary, decimal, conversion",
            "Difference between hardware, software, firmware"
        ],
        "Chapter:2 Types of Software": [
            "What is software?",
            "Categories: System software, Utility software, Application software, Programming software",
            "Open-source vs Proprietary",
            "Freeware, Shareware, Licensed software"
        ],
        "Chapter:3 Operating System": [
            "Definition and importance of OS",
            "Functions: Process management, Memory management, File management, Device management",
            "User interface (CLI vs GUI)",
            "Types: Batch, Time-sharing, Real-time, Distributed",
            "Popular examples: Windows, Linux, Android"
        ],
        "Chapter:4 Introduction to Python Programming": [
            "Introduction to Python & its features",
            "Writing and running Python programs",
            "Variables, data types, operators",
            "Control structures: if, if-else, elif; loops: for, while",
            "Functions (introductory)"
        ],
        "Chapter:5 Introduction to Cyber Security": [
            "What is cyber security?",
            "Types of cyber threats: Malware, Viruses, Worms, Phishing, Ransomware, Spyware, Trojans",
            "Cyber safety measures: Strong passwords, 2FA, Firewalls, antivirus, backups",
            "Cyber ethics and responsible digital behavior",
            "Awareness of cyber laws (basic introduction to IT Act in India)"
        ]
    },
    "English": {
        "Unit:1 Beehive – Prose": [
            "The Fun They Had: Futuristic setting, comprehension",
            "The Sound of Music: Inspiration, biography",
            "The Little Girl: Family relationships",
            "A Truly Beautiful Mind: Biography, Albert Einstein",
            "The Snake and the Mirror: Irony, humour",
            "My Childhood: Autobiography, Dr. A.P.J. Abdul Kalam",
            "Reach for the Top: Inspiration, character sketch",
            "Kathmandu: Travelogue",
            "If I Were You: Play, dialogue comprehension"
        ],
        "Unit:2 Beehive – Poems": [
            "The Road Not Taken: Choices, symbolism",
            "Wind: Nature, strength",
            "Rain on the Roof: Imagery, childhood memories",
            "The Lake Isle of Innisfree: Peace, nature imagery",
            "A Legend of the Northland: Ballad, moral",
            "No Men Are Foreign: Universal brotherhood",
            "On Killing a Tree: Nature, destruction",
            "A Slumber Did My Spirit Seal: Theme of death, imagery"
        ],
        "Unit:3 Moments – Supplementary": [
            "The Lost Child: Childhood, emotions",
            "The Adventures of Toto: Humour, pet story",
            "Iswaran the Storyteller: Imaginative storytelling",
            "In the Kingdom of Fools: Folk tale, humour",
            "The Happy Prince: Allegory, sacrifice",
            "The Last Leaf: Hope, sacrifice",
            "A House is Not a Home: Autobiographical, resilience",
            "The Beggar: Compassion, transformation"
        ]
    },
    "Mathematics": {
        "Chapter1: Number System": ["Real Numbers"],
        "Chapter2: Algebra": ["Polynomials", "Linear Equations in Two Variables"],
        "Chapter3: Coordinate Geometry": ["Coordinate Geometry"],
        "Chapter4: Geometry": ["Introduction to Euclid's Geometry","Lines and Angles","Triangles","Quadrilaterals","Circles"],
        "Chapter5: Mensuration": ["Areas", "Surface Areas and Volumes"],
        "Chapter6: Statistics": ["Statistics"]
    },
    "Science": {
        "Chapter:1 Matter in Our Surroundings": ["States of matter", "Properties of solids, liquids, and gases", "Changes of state"],
        "Chapter:2 Is Matter Around Us Pure?": ["Mixtures, solutions, alloys", "Separation techniques"],
        "Chapter:3 Atoms and Molecules": ["Laws of chemical combination", "Atomic and molecular masses", "Mole concept"],
        "Chapter:4 Structure of the Atom": ["Discovery of electron, proton, neutron", "Atomic models"],
        "Chapter:5 The Fundamental Unit of Life": ["Cell structure", "Cell organelles", "Cell functions"],
        "Chapter:6 Tissues": ["Plant tissues", "Animal tissues"],
        "Chapter:7 Diversity of the Living Organisms – I": ["Classification of organisms", "Kingdom Monera, Protista, Fungi"],
        "Chapter:8 Diversity of the Living Organisms – II": ["Plant kingdom", "Angiosperms, Gymnosperms"],
        "Chapter:9 Diversity of the Living Organisms – III": ["Animal kingdom", "Classification of animals"],
        "Chapter:10 Motion": ["Distance, displacement, speed, velocity", "Acceleration, uniform and non-uniform motion"],
        "Chapter:11 Force and Laws of Motion": ["Newton's laws", "Momentum, force, and inertia"],
        "Chapter:12 Gravitation": ["Universal law of gravitation", "Acceleration due to gravity", "Free fall"],
        "Chapter:13 Work and Energy": ["Work done", "Kinetic and potential energy", "Power"],
        "Chapter:14 Sound": ["Propagation of sound", "Characteristics", "Echo"],
        "Chapter:15 Why Do We Fall Ill?": ["Health and diseases", "Pathogens", "Immunity and vaccination"],
        "Chapter:16 Natural Resources": ["Air, water, soil, forests, minerals", "Conservation"],
        "Chapter:17 Improvement in Food Resources": ["Crop varieties", "Animal husbandry", "Food processing"]
    },
    "History": {
        "Chapter 1: The French Revolution": [
            "French society in the late 18th century",
            "The outbreak of the Revolution",
            "France becomes a constitutional monarchy",
            "The Reign of Terror",
            "The rise of Napoleon",
            "Impact of the Revolution on France and the world"
        ],
        "Chapter 2: Socialism in Europe and the Russian Revolution": [
            "Age of social change in Europe",
            "The Russian Empire in 1914",
            "The February Revolution",
            "The October Revolution and Bolsheviks in power",
            "Stalinism and collectivisation",
            "Industrial society and social change",
            "Global influence of the Russian Revolution"
        ],
        "Chapter 3: Nazism and the Rise of Hitler": [
            "Birth of the Weimar Republic",
            "Hitler's rise to power",
            "Nazi ideology and propaganda",
            "Establishment of a Nazi state",
            "Role of youth in Nazi Germany",
            "Racial policies and Holocaust", 
            "Crimes against humanity"
        ],
        "Chapter 4: Forest Society and Colonialism": [
            "Deforestation under colonial rule",
            "Rise of commercial forestry",  
            "Rebellions in forests (Bastar, Java)",
            "Impact on local communities"
        ],
        "Chapter 5: Pastoralists in the Modern World (Periodic Assessment only)": [
            "Pastoralism as a way of life",
            "Colonial impact on pastoral communities",
            "Case studies– Maasai (Africa), Raikas (India)",
            "Pastoralism in modern times"
        ]
    },
    "Geography": {
        "Chapter 1: India– Size and Location": ["Location and extent of India", "India and its neighbours", "Significance of India's location"],
        "Chapter 2: Physical Features of India": [
            "Formation of physiographic divisions",
            "Himalayas",
            "Northern Plains",
            "Peninsular Plateau",
            "Indian Desert",
            "Coastal Plains",
            "Islands"
        ],
        "Chapter 3: Drainage": [
            "Himalayan river systems",
            "Peninsular river systems",
            "Role and importance of rivers",
            "Lakes in India",
            "River pollution and conservation"
        ],
        "Chapter 4: Climate": [
            "Factors influencing climate",
            "Monsoon mechanism",
            "Seasons in India",
            "Rainfall distribution",
            "Monsoon as a unifying bond"
        ],
        "Chapter 5: Natural Vegetation and Wildlife": [
            "Types of vegetation in India",
            "Distribution of forests",
            "Wildlife species",
            "Conservation of forests and wildlife"
        ],
        "Chapter 6: Population": [
            "Size and distribution of population",
            "Population growth and processes (birth, death, migration)",
            "Age composition",
            "Sex ratio",
            "Literacy rate",
            "Population as an asset vs liability"
        ]
    },
    "Civics": {
        "Chapter 1: What is Democracy? Why Democracy?": [
            "Meaning of democracy",
            "Main features of democracy",
            "Arguments for and against democracy",
            "Broader meaning of democracy"
        ],
        "Chapter 2: Constitutional Design": [
            "Democratic Constitution in South Africa",
            "Why a Constitution is needed",
            "Making of the Indian Constitution",
            "Guiding values of the Constitution"
        ],
        "Chapter 3: Electoral Politics": [
            "Why elections are needed",
            "Indian election system",
            "Free and fair elections",
            "Role of the Election Commission"
        ],
        "Chapter 4: Working of Institutions": [
            "Parliament and its role",
            "The Executive– President, Prime Minister, Council of Ministers",
            "Lok Sabha and Rajya Sabha",
            "The Judiciary",
            "Decision-making process in democracy"
        ],
        "Chapter 5: Democratic Rights": [
            "Importance of rights in democracy",
            "Fundamental Rights in the Indian Constitution",
            "Right to Equality, Freedom, Religion, Education, Remedies",
            "Rights in practice– case studies"
        ]
    },
    "Economics": {
        "Chapter 1: The Story of Village Palampur": [
            "Farming and non-farming activities",
            "Factors of production (land, labour, capital, entrepreneurship)",
            "Organisation of production"
        ],
        "Chapter 2: People as Resource": [
            "People as an asset vs liability",
            "Role of education in human capital formation",
            "Role of health in human capital",
            "Unemployment and its types",
            "Role of women and children in the economy"
        ],
        "Chapter 3: Poverty as a Challenge": [
            "Two typical cases of poverty",
            "Poverty trends in India",
            "Causes of poverty",
            "Anti-poverty measures and programmes"
        ],
        "Chapter 4: Food Security in India": [
            "Meaning and need for food security",
            "Dimensions of food security",
            "Public Distribution System (PDS)",
            "Role of cooperatives and government programmes"
        ]
    }
},
   "10th": {
    "Computers": {
        "Chapter 1: Computer Fundamentals": [
            "Introduction to Computer Systems",
            "Number systems: binary, decimal, octal, hexadecimal",
            "Logic gates: AND, OR, NOT (truth tables)",
            "Computer hardware components: input, output, storage, CPU",
            "Types of memory: primary, secondary, cache, virtual memory",
            "Software overview: System, Application, Utilities",
            "Computer networks: LAN, MAN, WAN, Internet, intranet, extranet",
            "Data transmission: wired vs wireless",
            "Cloud computing basics",
            "Emerging technologies: AI, IoT, Big Data (introductory)"
        ],
        "Chapter 2: Advanced GIMP (GNU Image Manipulation Program)": [
            "Introduction to GIMP interface",
            "Layers and layer management",
            "Image editing tools: crop, scale, rotate, flip, perspective",
            "Color tools: brightness/contrast, hue/saturation, levels, curves",
            "Selection tools: free select, fuzzy select, paths",
            "Using filters and effects",
            "Working with text in GIMP",
            "Creating banners, posters, digital artwork",
            "Exporting images in different formats"
        ],
        "Chapter 3: Tables (HTML)": [
            "Introduction to HTML tables",
            "Table structure: <table>, <tr>, <td>, <th>",
            "Attributes: border, cellpadding, cellspacing, align, width, height",
            "Rowspan and Colspan",
            "Adding captions, Nested tables",
            "Styling tables with CSS"
        ],
        "Chapter 4: Forms (HTML)": [
            "Introduction to forms",
            "Form elements: Textbox, Password, Radio buttons, Checkboxes, Dropdown, Text area, Buttons",
            "Attributes: name, value, placeholder, required",
            "Form validation (basic HTML5)",
            "Form action and method (GET, POST)",
            "Simple login/registration forms"
        ],
        "Chapter 5: DHTML & CSS": [
            "Dynamic HTML: HTML + CSS + JavaScript",
            "Role of JavaScript in interactive pages",
            "Examples: rollover images, dynamic content updates",
            "CSS types: Inline, Internal, External",
            "CSS syntax: selectors, properties, values",
            "Styling text, backgrounds, borders, box model",
            "Positioning: static, relative, absolute, fixed",
            "Pseudo classes: :hover, :active, :first-child",
            "CSS for tables and forms"
        ]
    },
    "English": {
        "Unit1: First Flight – Prose": [
            "A Letter to God: Faith, irony",
            "Nelson Mandela: Long Walk to Freedom: Biography, freedom struggle",
            "From the Diary of Anne Frank: Diary, war, resilience",
            "Glimpses of India: Travel, culture",
            "Madam Rides the Bus: Childhood curiosity",
            "The Sermon at Benares: Teachings of Buddha",
            "Mijbil the Otter: Pet story, humour",
            "The Proposal: One-act play, satire"
        ],
        "Unit2: First Flight – Poems": [
            "Dust of Snow: Symbolism, nature",
            "Fire and Ice: Symbolism, theme of destruction",
            "The Ball Poem: Childhood loss, learning",
            "A Tiger in the Zoo: Freedom vs captivity",
            "How to Tell Wild Animals: Humour, description",
            "The Trees: Environment, imagery",
            "Fog: Metaphor, imagery",
            "The Tale of Custard the Dragon: Humour, rhyme",
            "For Anne Gregory: Beauty, inner vs outer"
        ],
        "Unit3: Footprints Without Feet – Supplementary": [
            "A Triumph of Surgery: Pet story, care",
            "The Thief's Story: Trust, honesty",
            "The Midnight Visitor: Detective, suspense",
            "A Question of Trust: Irony, theft",
            "Footprints Without Feet: Science fiction, invisibility",
            "The Making of a Scientist: Biography, Richard Ebright",
            "The Necklace: Irony, fate",
            "Bholi: Education, empowerment",
            "The Book That Saved the Earth: Science fiction, humour"
        ]
    },
    "Mathematics": {
        "Chapter 1: Number Systems": ["Real Number"],
        "Chapter 2: Algebra": ["Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions"],
        "Chapter 3: Coordinate Geometry": ["Coordinate Geometry"],
        "Chapter 4: Geometry": ["Triangles", "Circles"],
        "Chapter 5: Trigonometry": ["Introduction to Trigonometry", "Trigonometric Identities", "Heights and Distances"],
        "Chapter 6: Mensuration": ["Areas Related to Circles", "Surface Areas and Volumes"],
        "Chapter 7: Statistics and Probability": ["Statistics", "Probability"]
    },
    "Science": {
        "Chapter 1: Chemical Reactions and Equations": ["Types of Chemical Reactions", "Writing and Balancing Chemical Equations", "Effects of Oxidation and Reduction", "Types of Oxidizing and Reducing Agents"],
        "Chapter 2: Acids, Bases, and Salts": ["Properties of Acids and Bases", "pH Scale", "Uses of Acids and Bases"],
        "Chapter 3: Metals and Non-Metals": ["Properties of Metals and Non-Metals", "Reactivity Series of Metals", "Occurrence and Extraction of Metals", "Corrosion of Metals", "Uses of Metals and Non-Metals"],
        "Chapter 4: Carbon and Its Compounds": ["Covalent Bonding", "Homologous Series", "Saturated and Unsaturated Compounds", "Functional Groups", "Important Carbon Compounds and Their Uses"],
        "Chapter 5: Periodic Classification of Elements": ["Mendeleev's Periodic Table", "Modern Periodic Table", "Properties of Elements in Groups", "Properties of Elements in Periods"],
        "Chapter 6: Life Processes": ["Nutrition", "Respiration", "Excretion"],
        "Chapter 7: Control and Coordination": ["Nervous System", "Hormones"],
        "Chapter 8: How do Organisms Reproduce?": ["Modes of Reproduction", "Reproductive Health"],
        "Chapter 9: Heredity and Evolution": ["Mendel's Experiments", "Evolution Theories"],
        "Chapter 10: Light – Reflection and Refraction": ["Mirror & Lens Formulas", "Applications"],
        "Chapter 11: Human Eye and Colourful World": ["Human Eye", "Colourful World"],
        "Chapter 12: Electricity": ["Ohm's Law", "Series & Parallel Circuits"],
        "Chapter 13: Magnetic Effects of Electric Current": ["Electromagnetism", "Applications"],
        "Chapter 14: Sources of Energy": ["Conventional Sources of Energy", "Non-Conventional Sources of Energy"],
        "Chapter 15: Our Environment": ["Ecosystem", "Ozone Layer"],
        "Chapter 16: Sustainable Management of Natural Resources": ["Forest & Wildlife", "Water Management"]
    },
    "History": {
        "Chapter 1: The Rise of Nationalism in Europe": ["French Revolution and the idea of the nation", "The making of nationalism in Europe", "The age of revolutions: 1830–1848", "The making of Germany and Italy", "Visualising the nation– nationalism and imperialism"],
        "Chapter 2: Nationalism in India": ["First World War and nationalism in India", "The Non-Cooperation Movement", "Differing strands within the movement", "Civil Disobedience Movement", "The sense of collective belonging"],
        "Chapter 3: The Making of a Global World": ["The pre-modern world", "The nineteenth century (1815–1914)", "The inter-war economy", "Rebuilding a world economy: post–1945"],
        "Chapter 4: The Age of Industrialisation": ["Before the Industrial Revolution", "Hand labour and steam power", "Industrialisation in the colonies", "Factories come up", "The peculiarities of industrial growth", "Market for goods"],
        "Chapter 5: Print Culture and the Modern World": ["The first printed books", "Print comes to Europe", "The print revolution and its impact", "The reading mania", "The nineteenth century and print", "India and the world of print", "Religious reform and public debates", "New forms of publication and literature"]
    },
    "Geography": {
        "Chapter 1: Resources and Development": ["Types of resources– natural, human, sustainable", "Development of resources", "Resource planning in India", "Land resources and land use patterns", "Land degradation and conservation measures", "Soil as a resource– classification, distribution, conservation"],
        "Chapter 2: Forest and Wildlife Resources": ["Flora and fauna in India", "Types and distribution of forests", "Depletion of forests and conservation", "Forest conservation movements (Chipko, Beej Bachao Andolan)", "Government initiatives– IUCN, Indian Wildlife Protection Act"],
        "Chapter 3: Water Resources": ["Water scarcity and its causes", "Multipurpose river projects and integrated water resources management", "Rainwater harvesting"],
        "Chapter 4: Agriculture": ["Types of farming", "Cropping patterns (Kharif, Rabi, Zaid)", "Major crops (rice, wheat, maize, pulses, oilseeds, sugarcane, cotton, jute)", "Technological and institutional reforms", "Contribution of agriculture to the national economy"],
        "Chapter 5: Minerals and Energy Resources": ["Types of minerals and their distribution", "Uses of minerals", "Conventional sources of energy– coal, petroleum, natural gas, electricity", "Non-conventional sources of energy– solar, wind, tidal, geothermal, nuclear", "Conservation of energy resources"],
        "Chapter 6: Manufacturing Industries": ["Importance of manufacturing", "Industrial location factors", "Classification of industries (based on size, ownership, raw material, product)", "Major industries– cotton, jute, iron and steel, aluminium, chemical, fertiliser, cement, automobile, IT", "Industrial pollution and environmental degradation", "Control of environmental degradation"],
        "Chapter 7: Lifelines of National Economy": ["Roadways", "Railways", "Pipelines", "Waterways", "Airways", "Communication systems", "International trade"]
    },
    "Civics": {
        "Chapter 1: Power Sharing": ["Ethnic composition of Belgium and Sri Lanka", "Majoritarianism in Sri Lanka", "Accommodation in Belgium", "Why power sharing is desirable", "Forms of power sharing"],
        "Chapter 2: Federalism": ["What makes India a federal country", "Features of federalism", "Division of powers between Union and State", "Decentralisation in India– 73rd and 74th Amendments"],
        "Chapter 3: Gender, Religion and Caste": ["Gender and politics", "Religion and politics", "Caste and politics"],
        "Chapter 4: Political Parties": ["Why do we need political parties?", "Functions of political parties", "National parties and state parties", "Challenges to political parties", "How can parties be reformed?"],
        "Chapter 5: Outcomes of Democracy": ["How do we assess democracy's outcomes?", "Accountable, responsive and legitimate government", "Economic growth and development", "Reduction of inequality and poverty", "Accommodation of social diversity", "Dignity and freedom of the citizens"]
    },
    "Economics": {
        "Chapter 1: Development": ["What development promises– different people, different goals", "Income and other goals", "National development and per capita income", "Public facilities", "Sustainability of development"],
        "Chapter 2: Sectors of the Indian Economy": ["Primary, secondary and tertiary sectors", "Historical change in sectors", "Rising importance of tertiary sector", "Division of sectors as organised and unorganised", "Employment trends"],
        "Chapter 3: Money and Credit": ["Role of money in the economy", "Formal and informal sources of credit", "Self-Help Groups (SHGs)", "Credit and its terms"],
        "Chapter 4: Globalisation and the Indian Economy": ["Production across countries", "Interlinking of production across countries", "Foreign trade and integration of markets", "Globalisation and its impact", "Role of WTO", "Struggle for fair globalisation"],
        "Chapter 5: Consumer Rights": ["Consumer movement in India", "Consumer rights and duties", "Consumer awareness", "Role of consumer forums and NGOs"]
    }
}
}

# CBSE 7th–10th chapters (subtopics removed) for mocktest
CHAPTERS_SIMPLE = {
    "7th": {
        "Computers": [
            "Chapter 1: Programming Language",
            "Chapter 2: Editing Text in Microsoft Word",
            "Chapter 3: Microsoft PowerPoint",
            "Chapter 4: Basics of Microsoft Excel",
            "Chapter 5: Microsoft Access"
        ],
        "English": [
            "Unit 1: Learning Together",
            "Unit 2: Wit and Humour",
            "Unit 3: Dreams & Discoveries",
            "Unit 4: Travel and Adventure",
            "Unit 5: Bravehearts"
        ],
        "Maths": [
            "Chapter 1: Integers",
            "Chapter 2: Fractions and Decimals",
            "Chapter 3: Data Handling",
            "Chapter 4: Simple Equations",
            "Chapter 5: Lines and Angles",
            "Chapter 6: The Triangle and Its Properties",
            "Chapter 7: Comparing Quantities",
            "Chapter 8: Rational Numbers",
            "Chapter 9: Perimeter and Area",
            "Chapter 10: Algebraic Expressions",
            "Chapter 11: Exponents and Powers",
            "Chapter 12: Symmetry",
            "Chapter 13: Visualising Solid Shapes"
        ],
        "Science": [
            "Chapter1: Nutrition in Plants",
            "Chapter2: Nutrition in Animals",
            "Chapter3: Fibre to Fabric",
            "Chapter4: Heat",
            "Chapter5: Acids, Bases and Salts",
            "Chapter6: Physical and Chemical Changes",
            "Chapter7: Weather, Climate and Adaptations of Animals",
            "Chapter8: Winds, Storms and Cyclones",
            "Chapter9: Soil",
            "Chapter10: Respiration in Organisms",
            "Chapter11: Transportation in Animals and Plants",
            "Chapter12: Reproduction in Plants",
            "Chapter13: Motion and Time",
            "Chapter14: Electric Current and Its Effects",
            "Chapter15: Light",
            "Chapter16: Water: A Precious Resource",
            "Chapter17: Forests: Our Lifeline",
            "Chapter18: Wastewater Story"
        ],
        "History": [
            "Chapter 1: Tracing Changes through a Thousand Years",
            "Chapter 2: New Kings and Kingdoms",
            "Chapter 3: The Delhi Sultans (12th–15th Century)",
            "Chapter 4: The Mughal Empire (16th–17th Century)",
            "Chapter 5: Rulers and Buildings / Tribes, Nomads and Settled Communities",
            "Chapter 6: Devotional Paths to the Divine",
            "Chapter 7: The Making of Regional Cultures",
            "Chapter 8: Eighteenth Century Political Formations"
        ],
        "Civics": [
            "Chapter 1: On Equality",
            "Chapter 2: Role of the Government in Health",
            "Chapter 3: How the State Government Works",
            "Chapter 4: Growing up as Boys and Girls",
            "Chapter 5: Women Change the World",
            "Chapter 6: Understanding Media",
            "Chapter 7: Markets Around Us",
            "Chapter 8: A Shirt in the Market"
        ],
        "Geography": [
            "Chapter 1: Environment",
            "Chapter 2: Inside Our Earth",
            "Chapter 3: Our Changing Earth",
            "Chapter 4: Air",
            "Chapter 5: Water",
            "Chapter 6: Human-Environment Interactions– The Tropical and the Subtropical Region",
            "Chapter 7: Life in the Deserts"
        ]
    },
    "8th": {
        "Computers": [
            "Chapter 1: Exception Handling in Python",
            "Chapter 2: File Handling in Python",
            "Chapter 3: Stack (Data Structure)",
            "Chapter 4: Queue (Data Structure)",
            "Chapter 5: Sorting"
        ],
        "English": [
            "Unit1: Honeydew – Prose",
            "Unit2: Honeydew – Poems",
            "Unit3: It So Happened – Supplementary"
        ],
        "Maths": [
            "Chapter 1: Rational Numbers",
            "Chapter 2: Linear Equations in One Variable",
            "Chapter 3: Understanding Quadrilaterals",
            "Chapter 4: Data Handling",
            "Chapter 5: Squares and Square Roots",
            "Chapter 6: Cubes and Cube Roots",
            "Chapter 7: Comparing Quantities",
            "Chapter 8: Algebraic Expressions and Identities",
            "Chapter 9: Mensuration",
            "Chapter 10: Exponents and Powers",
            "Chapter 11: Direct and Inverse Proportions",
            "Chapter 12: Factorisation",
            "Chapter 13: Introduction to Graphs"
        ],
        "Science": [
            "Chapter 1: Crop Production and Management",
            "Chapter 2: Microorganisms: Friend and Foe",
            "Chapter 3: Synthetic Fibres and Plastics",
            "Chapter 4: Materials: Metals and Non-Metals",
            "Chapter 5: Coal and Petroleum",
            "Chapter 6: Combustion and Flame",
            "Chapter 7: Conservation of Plants and Animals",
            "Chapter 8: Cell – Structure and Functions",
            "Chapter 9: Reproduction in Animals",
            "Chapter 10: Force and Pressure",
            "Chapter 11: Friction",
            "Chapter 12: Sound",
            "Chapter 13: Chemical Effects of Electric Current",
            "Chapter 14: Some Natural Phenomena",
            "Chapter 15: Light",
            "Chapter 16: Stars and the Solar System",
            "Chapter 17: Pollution of Air and Water"
        ],
        "History": [
                "Chapter 1: How, When and Where",
                "Chapter 2: From Trade to Territory– The Company Establishes Power",
                "Chapter 3: Ruling the Countryside",
                "Chapter 4: Tribals, Dikus and the Vision of a Golden Age",
                "Chapter 5: When People Rebel– 1857 and After",
                "Chapter 6: Civilising the 'Native', Educating the Nation",
                "Chapter 7: Women, Caste and Reform",
                "Chapter 8: The Making of the National Movement: 1870s–1947"
            ],
        "Civics":  [
                "Chapter 1: The Indian Constitution",
                "Chapter 2: Understanding Secularism",
                "Chapter 3: Parliament and the Making of Laws",
                "Chapter 4: Judiciary",
                "Chapter 5: Understanding Marginalisation",
                "Chapter 6: Confronting Marginalisation",
                "Chapter 7: Public Facilities",
                "Chapter 8: Law and Social Justice"
            ],
        "Geography": [
                "Chapter 1: Resources",
                "Chapter 2: Land, Soil, Water, Natural Vegetation and Wildlife Resources",
                "Chapter 3: Agriculture",
                "Chapter 4: Industries",
                "Chapter 5: Human Resources"
            ]
    },
    "9th": {
        "Computers": [
            "Chapter 1: Basics of Computer System",
            "Chapter 2: Types of Software",
            "Chapter 3: Operating System",
            "Chapter 4: Introduction to Python Programming",
            "Chapter 5: Introduction to Cyber Security"
        ],
        "English": [
            "Unit1: Beehive – Prose",
            "Unit2: Beehive – Poems",
            "Unit3: Moments – Supplementary"
        ],
        "Maths": [
            "Chapter 1 : Number System",
            "Chapter 2 : Algebra",
            "Chapter 3 : Coordinate Geometry",
            "Chapter 4 : Geometry",
            "Chapter 5 :  Mensuration",
            "Chapter 6 : Statistics"
        ],
        "Science": [
            "Chapter 1 : Matter in Our Surroundings",
            "Chapter 2 :Is Matter Around Us Pure?",
            "Chapter 3 :Atoms and Molecules",
            "Chapter 4 :Structure of the Atom",
            "Chapter 5 :The Fundamental Unit of Life",
            "Chapter 6 :Tissues",
            "Chapter 7 :Diversity of the Living Organisms – I",
            "Chapter 8 :Diversity of the Living Organisms – II",
            "Chapter 9 :Diversity of the Living Organisms – III",
            "Chapter 10 :Motion",
            "Chapter 11 :Force and Laws of Motion",
            "Chapter 12 :Gravitation",
            "Chapter 13 :Work and Energy",
            "Chapter 14 :Sound",
            "Chapter 15 :Why Do We Fall Ill?",
            "Chapter 16 :Natural Resources",
            "Chapter 17 :Improvement in Food Resources"
        ],
        "History": [
            "Chapter 1: The French Revolution",
            "Chapter 2: Socialism in Europe and the Russian Revolution",
            "Chapter 3: Nazism and the Rise of Hitler",
            "Chapter 4: Forest Society and Colonialism",
            "Chapter 5: Pastoralists in the Modern World (Periodic Assessment only)"
        ],
        "Geography": [
            "Chapter 1: India– Size and Location",
            "Chapter 2: Physical Features of India",
            "Chapter 3: Drainage",
            "Chapter 4: Climate",
            "Chapter 5: Natural Vegetation and Wildlife",
            "Chapter 6: Population"
        ],
        "Civics": [
            "Chapter 1: What is Democracy? Why Democracy?",
            "Chapter 2: Constitutional Design",
            "Chapter 3: Electoral Politics",
            "Chapter 4: Working of Institutions",
            "Chapter 5: Democratic Rights"
        ],
        "Economics": [
            "Chapter 1: The Story of Village Palampur",
            "Chapter 2: People as Resource",
            "Chapter 3: Poverty as a Challenge",
            "Chapter 4: Food Security in India"
        ]
    },
    "10th": {
        "Computers": [
            "Chapter 1: Computer Fundamentals",
            "Chapter 2: Advanced GIMP (GNU Image Manipulation Program)",
            "Chapter 3: Tables (HTML)",
            "Chapter 4: Forms (HTML)",
            "Chapter 5: DHTML & CSS"
        ],
        "English": [
            "Unit 1:First Flight – Prose",
            "Unit 2:First Flight – Poems",
            "Unit 3:Footprints Without Feet – Supplementary"
        ],
        "Mathematics": [
            "Chapter 1: Number Systems",
            "Chapter 2: Algebra",
            "Chapter 3: Coordinate Geometry",
            "Chapter 4: Geometry",
            "Chapter 5: Trigonometry",
            "Chapter 6: Mensuration",
            "Chapter 7: Statistics and Probability"
        ],
        "Science": [
            "Chapter 1: Chemical Reactions and Equations",
            "Chapter 2: Acids, Bases, and Salts",
            "Chapter 3: Metals and Non-Metals",
            "Chapter 4: Carbon and Its Compounds",
            "Chapter 5: Periodic Classification of Elements",
            "Chapter 6: Life Processes",
            "Chapter 7: Control and Coordination",
            "Chapter 8: How do Organisms Reproduce?",
            "Chapter 9: Heredity and Evolution",
            "Chapter 10: Light – Reflection and Refraction",
            "Chapter 11: Human Eye and Colourful World",
            "Chapter 12: Electricity",
            "Chapter 13: Magnetic Effects of Electric Current",
            "Chapter 14: Sources of Energy",
            "Chapter 15: Our Environment",
            "Chapter 16: Sustainable Management of Natural Resources"
        ],
        "History": [
            "Chapter 1: The Rise of Nationalism in Europe",
            "Chapter 2: Nationalism in India",
            "Chapter 3: The Making of a Global World",
            "Chapter 4: The Age of Industrialisation",
            "Chapter 5: Print Culture and the Modern World"
        ],
        "Geography": [
            "Chapter 1: Resources and Development",
            "Chapter 2: Forest and Wildlife Resources",
            "Chapter 3: Water Resources",
            "Chapter 4: Agriculture",
            "Chapter 5: Minerals and Energy Resources",
            "Chapter 6: Manufacturing Industries",
            "Chapter 7: Lifelines of National Economy"
        ],
        "Civics": [
            "Chapter 1: Power Sharing",
            "Chapter 2: Federalism",
            "Chapter 3: Gender, Religion and Caste",
            "Chapter 4: Political Parties",
            "Chapter 5: Outcomes of Democracy"
        ],
        "Economics": [
            "Chapter 1: Development",
            "Chapter 2: Sectors of the Indian Economy",
            "Chapter 3: Money and Credit",
            "Chapter 4: Globalisation and the Indian Economy",
            "Chapter 5: Consumer Rights"
        ]
    }
}
MAX_PREVIOUS_QUESTIONS = 100
PREVIOUS_QUESTIONS_QUICK = {}
PREVIOUS_QUESTIONS_MOCK = {}

# Fallback quiz data when API is unavailable
FALLBACK_QUIZZES = {
    "What is a programming language?": [
        {
            "question": "What is a programming language?",
            "options": [
                "A way to communicate with computers",
                "A type of computer hardware",
                "A computer game",
                "A type of internet connection"
            ],
            "answer": "A way to communicate with computers"
        },
        {
            "question": "Which of the following is NOT a programming language?",
            "options": [
                "Python",
                "Java",
                "HTML",
                "Microsoft Word"
            ],
            "answer": "Microsoft Word"
        },
        {
            "question": "What does HTML stand for?",
            "options": [
                "HyperText Markup Language",
                "High Tech Modern Language",
                "Home Tool Markup Language",
                "Hyperlink and Text Markup Language"
            ],
            "answer": "HyperText Markup Language"
        },
        {
            "question": "Which programming language is known for its simplicity?",
            "options": [
                "Python",
                "C++",
                "Assembly",
                "Machine Code"
            ],
            "answer": "Python"
        },
        {
            "question": "What is the purpose of a compiler?",
            "options": [
                "To translate code into machine language",
                "To debug programs",
                "To design user interfaces",
                "To connect to the internet"
            ],
            "answer": "To translate code into machine language"
        },
        {
            "question": "Which of these is a high-level programming language?",
            "options": [
                "Python",
                "Assembly",
                "Machine Code",
                "Binary"
            ],
            "answer": "Python"
        },
        {
            "question": "What does IDE stand for?",
            "options": [
                "Integrated Development Environment",
                "Internet Data Exchange",
                "Internal Design Engine",
                "Interactive Data Entry"
            ],
            "answer": "Integrated Development Environment"
        },
        {
            "question": "Which programming language is used for web development?",
            "options": [
                "JavaScript",
                "Python",
                "C++",
                "Assembly"
            ],
            "answer": "JavaScript"
        },
        {
            "question": "What is a variable in programming?",
            "options": [
                "A container that stores data",
                "A type of function",
                "A programming language",
                "A computer component"
            ],
            "answer": "A container that stores data"
        },
        {
            "question": "Which of these is a programming paradigm?",
            "options": [
                "Object-Oriented Programming",
                "Web Browsing",
                "File Management",
                "Data Storage"
            ],
            "answer": "Object-Oriented Programming"
        }
    ]
}

def get_fallback_quiz(subtopic: str, difficulty: str, language: str):
    """Return a fallback quiz when API is unavailable"""
    logger.info(f"Using fallback quiz for: {subtopic}")
    
    # Get fallback quiz or create default
    quiz_data = FALLBACK_QUIZZES.get(subtopic, None)
    
    if quiz_data is None:
        # Generate 10 DIFFERENT questions for unknown topics
        quiz_data = []
        
        # Define different question templates based on subtopic
        question_templates = [
            f"What is the definition of {subtopic}?",
            f"Which of the following is NOT related to {subtopic}?",
            f"What are the main characteristics of {subtopic}?",
            f"How does {subtopic} work?",
            f"What are the types of {subtopic}?",
            f"What is the importance of {subtopic}?",
            f"Which statement about {subtopic} is correct?",
            f"What are the applications of {subtopic}?",
            f"How is {subtopic} different from similar concepts?",
            f"What are the properties of {subtopic}?"
        ]
        
        # Define different option patterns
        option_patterns = [
            ["Correct definition", "Incorrect definition", "Partial definition", "Opposite definition"],
            ["Related concept 1", "Related concept 2", "Unrelated concept", "Related concept 3"],
            ["Characteristic 1", "Characteristic 2", "Characteristic 3", "Non-characteristic"],
            ["Process A", "Process B", "Process C", "Incorrect process"],
            ["Type 1", "Type 2", "Type 3", "Non-type"],
            ["Reason 1", "Reason 2", "Reason 3", "Not important"],
            ["True statement", "False statement 1", "False statement 2", "False statement 3"],
            ["Application 1", "Application 2", "Application 3", "Non-application"],
            ["Difference A", "Difference B", "Difference C", "No difference"],
            ["Property 1", "Property 2", "Property 3", "Non-property"]
        ]
        
        for i in range(10):
            question_template = question_templates[i % len(question_templates)]
            option_pattern = option_patterns[i % len(option_patterns)]
            
            quiz_data.append({
                "question": question_template,
                "options": option_pattern,
                "answer": option_pattern[0]  # First option is always correct
            })
    
    return {
        "quiz": quiz_data,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "language": language,
        "source": "fallback"
    }

# Language instruction mapping
LANGUAGE_INSTRUCTIONS = {
    "English": "Generate all questions and options in English.",
    "Telugu": "Generate all questions and options in Telugu language (తెలుగు). Use Telugu script.",
    "Hindi": "Generate all questions and options in Hindi language (हिंदी). Use Devanagari script.",
    "Tamil": "Generate all questions and options in Tamil language (தமிழ்). Use Tamil script.",
    "Kannada": "Generate all questions and options in Kannada language (ಕನ್ನಡ). Use Kannada script.",
    "Malayalam": "Generate all questions and options in Malayalam language (മലയാളം). Use Malayalam script."
}

# Quick Practice Endpoints
@app.get("/classes")
def get_classes():
    logger.info("Fetching available classes")
    return JSONResponse(content={"classes": list(CHAPTERS_DETAILED.keys())})

@app.get("/chapters")
def get_subjects(class_name: str):
    logger.info(f"Fetching subjects for class: {class_name}")
    subjects = CHAPTERS_DETAILED.get(class_name)
    if not subjects:
        logger.error(f"Invalid class: {class_name}")
        raise HTTPException(status_code=400, detail="Invalid class")
    return JSONResponse(content={"chapters": list(subjects.keys())})

@app.get("/subtopics")
def get_subtopics(class_name: str, subject: str):
    logger.info(f"Fetching subtopics for class: {class_name}, subject: {subject}")
    subjects = CHAPTERS_DETAILED.get(class_name)
    if not subjects or subject not in subjects:
        logger.error(f"Invalid subject: {subject} or class: {class_name}")
        raise HTTPException(status_code=400, detail="Invalid subject or class")
    subtopics = subjects[subject]
    return JSONResponse(content={"subtopics": subtopics})

@app.get("/quiz")
def get_quiz(
    subtopic: str,
    retry: bool = False,
    currentLevel: int = None,
    language: str = "English"
):
    try:
        previous = PREVIOUS_QUESTIONS_QUICK.get(subtopic, []) if not retry else []

        # Use the level from frontend if provided
        if currentLevel is not None:
            current_level = currentLevel
        else:
            # fallback if frontend doesn't provide level
            num_prev = len(previous)
            if num_prev == 0:
                current_level = 1
            elif num_prev == 1:
                current_level = 2
            else:
                current_level = 3

        difficulty_map = {1: "simple", 2: "medium", 3: "hard"}
        difficulty = difficulty_map.get(current_level, "simple")

        logger.info(f"Generating quiz for subtopic: {subtopic}, difficulty: {difficulty}, retry: {retry}, level: {current_level}, language: {language}")
       
        # Get language instruction
        language_instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS["English"])

        prompt = f"""
        Generate 10 multiple-choice questions for "{subtopic}".
        Difficulty: {difficulty}.
        {language_instruction}
       
        IMPORTANT INSTRUCTIONS:
        - ALL questions, options, and content MUST be in {language} language only.
        - Do NOT mix English with the target language.
        - Use proper script for the selected language.
        - Avoid repeating these questions: {previous}.
       
        IMPORTANT FORMAT REQUIREMENTS:
        - Each question should have exactly 4 options as an array: ["option1", "option2", "option3", "option4"]
        - The answer should be the actual text of the correct option, NOT a letter
        - Return ONLY a JSON array with keys: question, options (array), answer (actual option text)
       
        Example format (in {language}):
        [
          {{
            "question": "[Question text in {language}]",
            "options": ["[Option 1 in {language}]", "[Option 2 in {language}]", "[Option 3 in {language}]", "[Option 4 in {language}]"],
            "answer": "[Correct option text in {language}]"
          }}
        ]
        """

        # Check if client is available
        if client is None:
            logger.warning("OpenAI client not available, using fallback quiz")
            return get_fallback_quiz(subtopic, difficulty, language)
            
        try:
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-001",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9
            )
        except Exception as api_error:
            logger.error(f"API call failed: {api_error}")
            # Fallback: Return sample quiz when API is unavailable
            return get_fallback_quiz(subtopic, difficulty, language)

        message_content = response.choices[0].message.content
        text = ""
        if isinstance(message_content, list):
            for block in message_content:
                if block.get("type") == "text":
                    text += block.get("text", "")
        else:
            text = str(message_content)

        # Clean up markdown code blocks if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

        try:
            quiz_json = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if not match:
                logger.error(f"AI did not return valid JSON: {text[:200]}")
                raise ValueError(f"AI did not return valid JSON: {text[:200]}")
            quiz_json = json.loads(match.group(0))

        # Process and validate the quiz
        processed_quiz = []
        for q in quiz_json:
            if not all(key in q for key in ["question", "options", "answer"]):
                continue
               
            # Ensure options is a list with exactly 4 items
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                continue
               
            # Ensure the answer exists in the options
            if q["answer"] not in q["options"]:
                # Try to fix by finding the closest match
                continue
               
            processed_quiz.append(q)

        # Shuffle the quiz questions
        random.shuffle(processed_quiz)
       
        # Shuffle options while preserving correct answer
        for q in processed_quiz:
            # Create a mapping of original positions
            original_options = q["options"].copy()
            correct_answer = q["answer"]
           
            # Shuffle the options
            random.shuffle(q["options"])
           
            # The answer remains the same text, not the position
            # This ensures the answer is always the correct option text
           
        if not retry:
            PREVIOUS_QUESTIONS_QUICK[subtopic] = previous + [q["question"] for q in processed_quiz]

        logger.info(f"Generated {len(processed_quiz)} questions for subtopic: {subtopic} in {language}")
       
        return JSONResponse(content={
            "currentLevel": current_level,
            "quiz": processed_quiz
        })

    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# AI Assistant Endpoints
def _classify_question_type(question: str) -> str:
    """Classify the type of question for better response handling"""
    question_lower = question.lower()
   
    if any(word in question_lower for word in ['study plan', 'schedule', 'timetable', 'how to study', 'plan']):
        return "study_plan"
    elif any(word in question_lower for word in ['notes', 'summary', 'key points', 'important points', 'write down']):
        return "notes"
    elif any(word in question_lower for word in ['explain', 'what is', 'how does', 'why', 'meaning', 'define']):
        return "explanation"
    elif any(word in question_lower for word in ['practice', 'exercise', 'question', 'problem', 'solve', 'worksheet']):
        return "practice"
    elif any(word in question_lower for word in ['related', 'connect', 'application', 'real world', 'where used']):
        return "related_concepts"
    elif any(word in question_lower for word in ['example', 'examples', 'sample']):
        return "examples"
    else:
        return "general"

# AI Assistant Endpoints
@app.post("/ai-assistant/chat")
async def ai_assistant_chat(request: ChatRequest):
    try:
        class_level = request.class_level
        subject = request.subject
        chapter = request.chapter
        student_question = request.student_question
        chat_history = request.chat_history or []
       
        # Get language preference
        language = "English"
       
        # Enhanced prompt with better formatting instructions
        prompt = f"""
        You are an AI Learning Assistant for a {class_level} student studying {subject}, specifically chapter: {chapter}.
       
        Student's Question: "{student_question}"
       
        Previous conversation context: {chat_history[-5:] if chat_history else "No previous context"}
       
        Based on the student's question, provide a helpful, educational response with EXCELLENT STRUCTURE and CHILD-FRIENDLY formatting.
       
        **CRITICAL FORMATTING RULES:**
        1. Use CLEAR HEADINGS with emojis
        2. Use BULLET POINTS and NUMBERED LISTS
        3. Use SIMPLE LANGUAGE for children
        4. Add VISUAL SEPARATORS like lines between sections
        5. Use LARGE FONT indicators for important points
        6. Include PRACTICAL EXAMPLES
        7. Add SUMMARY TABLES where helpful
        8. Use COLOR INDICATORS (🔴 🟢 🔵 🟡)
       
        **RESPONSE TYPES:**
       
        1. STUDY PLAN Response Structure:
           🗓️ WEEKLY STUDY PLAN
           ───────────────────
           📅 Day 1: [Topic]
           • Time: [Duration]
           • Activities: [List]
           • Practice: [Specific tasks]
           ───────────────────
           
        2. NOTES Response Structure:
           📚 CHAPTER NOTES
           ───────────────
           🔹 Key Concept 1
           • Definition: [Simple definition]
           • Example: [Real-world example]
           • Remember: [Important point]
           ───────────────
           
        3. EXPLANATION Response Structure:
           💡 CONCEPT EXPLANATION
           ────────────────────
           🎯 What is it?
           [Simple definition]
           
           👀 How it works:
           [Step-by-step]
           
           🌍 Real Example:
           [Child-friendly example]
           ────────────────────
           
        4. PRACTICE QUESTIONS Structure:
           📝 PRACTICE TIME
           ───────────────
           🟢 EASY Question:
           [Question]
           
           🟡 MEDIUM Question:
           [Question]
           
           🔴 CHALLENGE Question:
           [Question]
           
           ✅ SOLUTIONS:
           [Step-by-step solutions]
           ───────────────
       
        Make it VISUALLY APPEALING and EASY TO READ for a child!
        """
       
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
       
        message_content = response.choices[0].message.content
        text = ""
        if isinstance(message_content, list):
            for block in message_content:
                if block.get("type") == "text":
                    text += block.get("text", "")
        else:
            text = str(message_content)
       
        return JSONResponse(content={
            "success": True,
            "response": text,
            "type": _classify_question_type(student_question)
        })
       
    except Exception as e:
        logger.error(f"Error in AI assistant: {str(e)}")
        return JSONResponse(content={
            "success": False,
            "response": "I apologize, but I'm having trouble processing your request right now. Please try again.",
            "type": "error"
        }, status_code=500)

@app.post("/ai-assistant/generate-study-plan")
async def generate_study_plan(request: StudyPlanRequest):
    """Generate a detailed study plan for a specific chapter"""
    try:
        class_level = request.class_level
        subject = request.subject
        chapter = request.chapter
        days_available = request.days_available
        hours_per_day = request.hours_per_day
       
        prompt = f"""
        Create a SUPER STRUCTURED and CHILD-FRIENDLY {days_available}-day study plan for a {class_level} student studying {subject}, chapter: {chapter}.
       
        **FORMATTING REQUIREMENTS:**
       
        🗓️ {days_available}-DAY STUDY PLAN FOR {chapter.upper()}
        ═══════════════════════════════════════
       
        📊 QUICK OVERVIEW:
        • Total Days: {days_available}
        • Daily Study: {hours_per_day} hours
        • Subject: {subject}
        • Chapter: {chapter}
       
        📅 DAILY BREAKDOWN:
        ───────────────────
       
        DAY 1: [Main Topic]
        🕐 Time: [Specific time allocation]
        📚 What to Study:
        • Topic 1: [Details]
        • Topic 2: [Details]
        ✍️ Practice:
        • [Specific practice tasks]
        ✅ Check: [Self-check points]
       
        DAY 2: [Main Topic]
        🕐 Time: [Specific time allocation]
        📚 What to Study:
        • Topic 1: [Details]
        • Topic 2: [Details]
        ✍️ Practice:
        • [Specific practice tasks]
        ✅ Check: [Self-check points]
       
        🎯 WEEKLY GOALS:
        • Goal 1: [Specific achievement]
        • Goal 2: [Specific achievement]
       
        💡 STUDY TIPS:
        • Tip 1: [Practical tip]
        • Tip 2: [Practical tip]
       
        Make it COLORFUL and EASY TO FOLLOW for a child!
        Use EMOJIS and CLEAR SECTIONS!
        """
       
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
       
        message_content = response.choices[0].message.content
        text = str(message_content) if not isinstance(message_content, list) else message_content[0].get("text", "")
       
        return JSONResponse(content={
            "success": True,
            "study_plan": text
        })
       
    except Exception as e:
        logger.error(f"Error generating study plan: {str(e)}")
        return JSONResponse(content={
            "success": False,
            "study_plan": "Unable to generate study plan at this time."
        }, status_code=500)

@app.post("/ai-assistant/generate-notes")
async def generate_notes(request: NotesRequest):
    """Generate comprehensive notes for a chapter or specific topic"""
    try:
        class_level = request.class_level
        subject = request.subject
        chapter = request.chapter
        specific_topic = request.specific_topic
       
        topic_specific = f" on {specific_topic}" if specific_topic else ""
       
        prompt = f"""
        Generate SUPER ORGANIZED and CHILD-FRIENDLY study notes for a {class_level} student studying {subject}, chapter: {chapter}{topic_specific}.
       
        **REQUIRED FORMAT:**
       
        📚 {chapter.upper()} - STUDY NOTES
        ═══════════════════════════
       
        🎯 CHAPTER AT A GLANCE:
        • Main Topics: [List 3-4 main topics]
        • Key Skills: [What they'll learn]
        • Difficulty: 🟢 Easy / 🟡 Medium / 🔴 Hard
       
        🔍 KEY CONCEPTS:
        ─────────────────
       
        🔹 Concept 1: [Concept Name]
        • What it is: [Simple definition]
        • Example: 🌟 [Real example]
        • Remember: 💡 [Key point]
        • Formula: 📐 [If applicable]
       
        🔹 Concept 2: [Concept Name]
        • What it is: [Simple definition]
        • Example: 🌟 [Real example]
        • Remember: 💡 [Key point]
        • Formula: 📐 [If applicable]
       
        📋 IMPORTANT POINTS TABLE:
        ─────────────────────────
        | Point | Description | Remember |
        |-------|-------------|----------|
        | [1] | [Description] | [Memory tip] |
        | [2] | [Description] | [Memory tip] |
       
        💪 PRACTICE READY:
        • Quick Questions: [2-3 simple questions]
        • Think About: [1 critical thinking question]
       
        📝 SUMMARY:
        • Main Idea 1: [Summary point]
        • Main Idea 2: [Summary point]
        • Main Idea 3: [Summary point]
       
        Use LOTS OF EMOJIS, CLEAR SECTIONS, and CHILD-FRIENDLY LANGUAGE!
        Make it VISUALLY APPEALING!
        """
       
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
       
        message_content = response.choices[0].message.content
        text = str(message_content) if not isinstance(message_content, list) else message_content[0].get("text", "")
       
        return JSONResponse(content={
            "success": True,
            "notes": text
        })
       
    except Exception as e:
        logger.error(f"Error generating notes: {str(e)}")
        return JSONResponse(content={
            "success": False,
            "notes": "Unable to generate notes at this time."
        }, status_code=500)
# Mock Test Endpoints
@app.get("/mock_classes")
def get_mock_classes():
    logger.info("Fetching available classes for mock test")
    return JSONResponse(content={"classes": list(CHAPTERS_SIMPLE.keys())})

@app.get("/mock_subjects")
def get_mock_subjects(class_name: str):
    logger.info(f"Fetching subjects for class: {class_name}")
    subjects = CHAPTERS_SIMPLE.get(class_name)
    if not subjects:
        logger.error(f"Invalid class: {class_name}")
        raise HTTPException(status_code=400, detail="Invalid class")
    return JSONResponse(content={"subjects": list(subjects.keys())})

@app.get("/quick-practice")
def get_quick_practice():
    """
    Temporary endpoint for quick practice - returns mock data similar to mock_subjects
    """
    logger.info("Fetching quick practice data")
    
    # Return mock data similar to what frontend expects
    return JSONResponse(content={
        "message": "Quick Practice endpoint is working!",
        "status": "success",
        "data": {
            "available_classes": list(CHAPTERS_SIMPLE.keys()),
            "subjects": ["Computers", "English", "Mathematics", "Science", "History", "Geography", "Civics", "Economics"],
            "quick_practice_available": True
        }
    })

@app.get("/mock_chapters")
def get_mock_chapters(class_name: str, subject: str):
    logger.info(f"Fetching chapters for class: {class_name}, subject: {subject}")
    subjects = CHAPTERS_SIMPLE.get(class_name)
    if not subjects or subject not in subjects:
        logger.error(f"Invalid subject: {subject} or class: {class_name}")
        raise HTTPException(status_code=400, detail="Invalid subject or class")
    chapters = subjects[subject]
    if isinstance(chapters, dict):
        chapters = [chapter for sublist in chapters.values() for chapter in sublist]
    return JSONResponse(content={"chapters": chapters})

@app.get("/mock_test")
def get_mock_test(
    class_name: str,
    subject: str,
    chapter: str,
    retry: bool = False,
    language: str = "English",
    num_questions: int = 50
):
    try:
        previous = PREVIOUS_QUESTIONS_MOCK.get(chapter, []) if not retry else []

        # Automatic difficulty progression
        num_prev = len(previous)
        if num_prev == 0:
            current_level = 1
            difficulty = "simple"
        elif num_prev == 1:
            current_level = 2
            difficulty = "medium"
        else:
            current_level = 3
            difficulty = "hard"
       
        logger.info(f"Generating mock test for class: {class_name}, subject: {subject}, chapter: {chapter}, difficulty: {difficulty}, language: {language}, retry: {retry}, num_questions: {num_questions}")

        subjects = CHAPTERS_SIMPLE.get(class_name)
        if not subjects or subject not in subjects:
            logger.error(f"Invalid subject: {subject} or class: {class_name}")
            raise HTTPException(status_code=400, detail="Invalid subject or class")

        chapters = subjects[subject]
        if isinstance(chapters, dict):
            for key, chapter_list in chapters.items():
                if chapter in chapter_list:
                    break
            else:
                logger.error(f"Invalid chapter: {chapter} for subject: {subject}")
                raise HTTPException(status_code=400, detail="Invalid chapter")
        elif chapter not in chapters:
            logger.error(f"Invalid chapter: {chapter} for subject: {subject}")
            raise HTTPException(status_code=400, detail="Invalid chapter")

        if len(previous) > MAX_PREVIOUS_QUESTIONS:
            previous = previous[-MAX_PREVIOUS_QUESTIONS:]
            logger.info(f"Truncated previous questions for chapter: {chapter} to {MAX_PREVIOUS_QUESTIONS}")

        # Get language instruction
        language_instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS["English"])

        prompt = f"""
        Generate {num_questions} multiple-choice questions for "{chapter}" in {subject} for class {class_name}.
        Difficulty: {difficulty}.
        {language_instruction}
       
        IMPORTANT INSTRUCTIONS:
        - ALL questions, options, and content MUST be in {language} language only.
        - Do NOT mix English with the target language.
        - Use proper script for the selected language.
        - Avoid repeating these questions: {previous}.
       
        FORMAT REQUIREMENTS:
        - Each question must have exactly 4 options as a JSON object {{"A": "option text", "B": "another option", "C": "third option", "D": "fourth option"}}.
        - The answer must be the label "A", "B", "C", or "D".
        - Return ONLY a JSON array of objects with keys: question, options, answer.
       
        Example format (in {language}):
        [
          {{
            "question": "[Question text in {language}]",
            "options": {{
              "A": "[Option A in {language}]",
              "B": "[Option B in {language}]",
              "C": "[Option C in {language}]",
              "D": "[Option D in {language}]"
            }},
            "answer": "C"
          }}
        ]
        """

        logger.info(f"Sending prompt to AI for chapter: {chapter} in {language}")
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        message_content = response.choices[0].message.content
        text = ""
        if isinstance(message_content, list):
            for block in message_content:
                if block.get("type") == "text":
                    text += block.get("text", "")
        else:
            text = str(message_content)

        text = text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

        try:
            quiz_json = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if not match:
                return JSONResponse(content={"currentLevel": current_level, "quiz": []}, status_code=200)
            quiz_json = json.loads(match.group(0))

        if not isinstance(quiz_json, list):
            return JSONResponse(content={"currentLevel": current_level, "quiz": []}, status_code=200)

        processed_quiz = []
        for q in quiz_json:
            if not all(key in q for key in ["question", "options", "answer"]):
                continue
            if isinstance(q["options"], list) and len(q["options"]) == 4:
                q["options"] = {chr(65 + i): opt for i, opt in enumerate(q["options"])}
            elif not isinstance(q["options"], dict) or len(q["options"]) != 4:
                continue
            if q["answer"] not in q["options"]:
                continue

            items = list(q["options"].items())
            random.shuffle(items)
            new_options = {}
            new_answer = None
            for new_idx, (old_label, text_opt) in enumerate(items):
                new_label = chr(65 + new_idx)
                new_options[new_label] = text_opt
                if old_label == q["answer"]:
                    new_answer = new_label
            q["options"] = new_options
            q["answer"] = new_answer
            processed_quiz.append(q)

        while len(processed_quiz) < 50:
            processed_quiz.append({
                "id": len(processed_quiz),
                "question": f"Placeholder Question {len(processed_quiz) + 1}",
                "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
                "answer": "A"
            })

        if not retry:
            PREVIOUS_QUESTIONS_MOCK[chapter] = previous + [q["question"] for q in processed_quiz]
            if len(PREVIOUS_QUESTIONS_MOCK[chapter]) > MAX_PREVIOUS_QUESTIONS:
                PREVIOUS_QUESTIONS_MOCK[chapter] = PREVIOUS_QUESTIONS_MOCK[chapter][-MAX_PREVIOUS_QUESTIONS:]

        return JSONResponse(content={
            "currentLevel": current_level,
            "quiz": processed_quiz
        })

    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(content={"currentLevel": 1, "quiz": []}, status_code=200)

@app.get("/")
def read_root():
    return {"message": "AI Learning Assistant API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)