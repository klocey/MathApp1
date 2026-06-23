import random
import dash
from dash import html, dcc, Input, Output, State, callback_context

# --- POWERPUFF GIRLS & POKÉMON DATA ---
CHARACTERS = ["Blossom", "Bubbles", "Buttercup", "Pikachu", "Eevee", "Mew", "Mojo Jojo", "Ash"]
ITEMS = ["Pokéballs", "enchanted hearts", "sweet cupcakes", "star stickers", "Berry treats", "candy pieces"]

# Add the filenames of the images you have saved in your assets folder here!
BACKGROUND_IMAGES = [
    "dg2ryx8-a2d8ad53-6041-449b-8002-3429bb2e5aa2.jpg", 
    "tout.jpg", 
    "GvULmuVWoAAcE_8.jpg",
    "2FaDOZ.webp",
    "wp11066346.jpg",
    "0Btusv.webp",
    "the-powerpuff-girls-enwsqsc0jfv7sgno.jpg",
    "76687-Powerpuff_Girls.jpg",

]

WORD_PROBLEM_TEMPLATES = {
    "+": [
        "{name} found {num1} {item}. Then, {friend} gave them {num2} more! How many {item} does {name} have now?",
        "There are {num1} {item} hidden in the Powerpuff lab and {num2} {item} in a Pokéball. How many are there in total?"
    ],
    "-": [
        "{name} had {num1} {item}. {friend} borrowed {num2} of them to save the day. How many {item} does {name} have left?",
        "Mojo Jojo stole {num1} {item}, but {name} managed to win back {num2} of them! How many {item} does Mojo Jojo still have?"
    ],
    "*": [
        "{name} has {num1} special bags. Each bag holds exactly {num2} {item}. How many {item} does {name} have altogether?",
        "Professor Utonium made {num1} rows of treats. Each row has {num2} {item}. How many total {item} did he make?"
    ],
    "/": [
        "{name} wants to share {num1} {item} equally among {num2} friendly Pokémon. How many {item} does each Pokémon get?",
        "If Bubbles splits {num1} {item} into {num2} equal neat piles, how many {item} will be in each pile?"
    ]
}

# --- HELPER FUNCTION TO GENERATE PROBLEMS ---
def generate_problem():
    op = random.choice(["+", "-", "*", "/"])
    is_word_problem = random.choice([True, False])
    
    if op == "+":
        num1 = random.randint(0, 50)
        num2 = random.randint(0, 50)
        answer = num1 + num2
    elif op == "-":
        num1 = random.randint(0, 100)
        num2 = random.randint(0, num1)
        answer = num1 - num2
    elif op == "*":
        num1 = random.randint(1, 10)
        num2 = random.randint(0, 10)
        answer = num1 * num2
    elif op == "/":
        num2 = random.randint(1, 10)
        answer = random.randint(0, 10)
        num1 = num2 * answer 
        
    if is_word_problem:
        char_pool = CHARACTERS.copy()
        name = random.choice(char_pool)
        char_pool.remove(name)
        friend = random.choice(char_pool)
        
        template = random.choice(WORD_PROBLEM_TEMPLATES[op])
        question = template.format(
            name=name,
            friend=friend,
            item=random.choice(ITEMS),
            num1=num1,
            num2=num2
        )
    else:
        op_symbol = "÷" if op == "/" else ("×" if op == "*" else op)
        question = f"What is {num1} {op_symbol} {num2}?"
        
    return question, answer

# --- INITIALIZE DASH APP ---
app = dash.Dash(__name__)

# Base Main Layout
app.layout = html.Div(id='main-bg-container', style={
    'fontFamily': '"Comic Sans MS", "Chalkboard SE", sans-serif', 'textAlign': 'center', 'padding': '30px',
    'minHeight': '100vh', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center',
    'backgroundSize': 'cover', 'backgroundPosition': 'center', 'transition': 'background-image 0.5s ease-in-out'
}, children=[
    
    # Main Content Card
    html.Div(style={
        'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'maxWidth': '650px', 'margin': 'auto', 'borderRadius': '30px',
        'padding': '40px', 'boxShadow': '0px 10px 25px rgba(0, 0, 0, 0.2)',
        'border': '8px solid #AED6F1' 
    }, children=[
        
        html.H1("🌟 POWERPUFF MATH LAB! 🌟", style={
            'color': '#FF69B4', 'fontSize': '36px', 'fontWeight': 'bold', 
            'textShadow': '2px 2px #F1948A', 'marginBottom': '10px'
        }),
        html.Div("Can you help save Townsville using math?", style={'color': '#5DADE2', 'fontSize': '18px', 'fontWeight': 'bold'}),
        html.Hr(style={'border': '2px dashed #FFB6C1', 'margin': '25px 0'}),
        
        # Persistent Banner for Previous Answer Feedback
        html.Div(id='last-action-feedback', style={
            'fontSize': '20px', 'fontWeight': 'bold', 'minHeight': '40px', 'marginBottom': '15px'
        }),

        # Question Display Box
        html.Div(id='question-box', style={
            'fontSize': '24px', 'fontWeight': 'bold', 'margin': '20px 0', 
            'minHeight': '80px', 'color': '#2C3E50', 'padding': '15px',
            'backgroundColor': '#EAFAF1', 'borderRadius': '20px', 'border': '3px solid #2ECC71' 
        }),
        
        # Input & Single-Button Interface
        html.Div([
            dcc.Input(id='user-answer', type='number', placeholder='?', style={
                'fontSize': '32px', 'width': '140px', 'textAlign': 'center', 
                'borderRadius': '15px', 'border': '4px solid #FFB6C1', 'padding': '10px',
                'color': '#FF69B4', 'fontWeight': 'bold'
            }),
            html.Br(), html.Br(),
            html.Button('💥 Check Answer!', id='submit-btn', n_clicks=0, n_clicks_timestamp=0, style={
                'fontSize': '22px', 'backgroundColor': '#FF69B4', 'color': 'white', 
                'border': 'none', 'padding': '15px 35px', 'borderRadius': '50px', 'cursor': 'pointer',
                'fontWeight': 'bold', 'boxShadow': '0px 5px 0px #D81B60'
            }),
        ]),
        
        # Score Tracker Footer (Records Badges and % Correct)
        html.Div(id='score-box', style={
            'fontSize': '22px', 'fontWeight': 'bold', 'marginTop': '30px', 
            'color': '#2ECC71', 'backgroundColor': '#F4F6F6', 'padding': '15px', 'borderRadius': '15px'
        }),
    ]),
    
    # Game State Stores
    dcc.Store(id='correct-answer'),
    dcc.Store(id='score-tracker', data={'correct': 0, 'total': 0})
])

# --- APP GAMEPLAY LOGIC ---
@app.callback(
    Output('question-box', 'children'),
    Output('correct-answer', 'data'),
    Output('last-action-feedback', 'children'),
    Output('score-tracker', 'data'),
    Output('score-box', 'children'),
    Output('user-answer', 'value'),
    Output('main-bg-container', 'style'),
    Input('submit-btn', 'n_clicks'),
    State('user-answer', 'value'),
    State('correct-answer', 'data'),
    State('score-tracker', 'data'),
    State('question-box', 'children'),
    State('main-bg-container', 'style'),
    prevent_initial_call=False
)
def manage_game(submit_clicks, user_ans, current_correct, score, current_question, current_bg_style):
    ctx = callback_context
    
    # Helper to calculate scoring metrics
    def format_score_text(s):
        pct = int((s['correct'] / s['total']) * 100) if s['total'] > 0 else 0
        return f"⭐ Badges: {s['correct']} / {s['total']} | Success Rate: {pct}% ⭐"

    # 1. INITIAL LOAD: Generate first problem and set a random background
    if not ctx.triggered:
        q_text, q_ans = generate_problem()
        chosen_bg = random.choice(BACKGROUND_IMAGES)
        current_bg_style['backgroundImage'] = f"url('/assets/{chosen_bg}')"
        return q_text, q_ans, "Welcome! Good luck! 🎉", score, format_score_text(score), "", current_bg_style
        
    # 2. CLICKED CHECK ANSWER
    if user_ans is None:
        # Prompt validation without changing problem state or breaking strict sequence
        reminder_text = html.Span("Type a number first! 🤔", style={'color': '#E67E22'})
        return current_question, current_correct, reminder_text, score, format_score_text(score), "", current_bg_style

    # Score the response
    if int(user_ans) == current_correct:
        feedback_element = html.Span("💖 Correct! Great job! 💖", style={'color': '#2ECC71'})
        score['correct'] += 1
    else:
        feedback_element = html.Span(f"❌ Close! The last one was {current_correct}.", style={'color': '#E74C3C'})
        
    score['total'] += 1
    
    # Seamless single-button loop: instantly flip to the next question and cycle background
    next_q_text, next_q_ans = generate_problem()
    chosen_bg = random.choice(BACKGROUND_IMAGES)
    current_bg_style['backgroundImage'] = f"url('/assets/{chosen_bg}')"
    
    return next_q_text, next_q_ans, feedback_element, score, format_score_text(score), "", current_bg_style


# --- MODIFIED WEB SERVER HOOK FOR LINUX ENVIRONMENT ---
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
    
    