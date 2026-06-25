import os
import random
import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

# Import the massive theme library dictionary from our local file
from themes import THEME_DATA

# --- DAD JOKES LOADING ENGINE ---
DEFAULT_JOKES = [
    ("Why did the cookie go to the hospital?", "Because it felt crummy!"),
    ("What do you call a sleeping dinosaur?", "A dino-snore!")
]

def load_dad_jokes():
    joke_file = os.path.join("assets", "dad_jokes.txt")
    if not os.path.exists(joke_file):
        return DEFAULT_JOKES
    
    jokes = []
    with open(joke_file, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                setup, punchline = line.strip().split("|", 1)
                jokes.append((setup.strip(), punchline.strip()))
    return jokes if jokes else DEFAULT_JOKES

DAD_JOKES = load_dad_jokes()


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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(id='main-bg-container', style={
    'fontFamily': '"Comic Sans MS", "Chalkboard SE", sans-serif', 'padding': '15px',
    'height': '100vh', 'boxSizing': 'border-box', 'display': 'flex', 'flexDirection': 'row',
    'backgroundSize': 'cover', 'backgroundPosition': 'center', 'transition': 'background-image 0.5s ease-in-out',
    'overflow': 'hidden', 'backgroundColor': '#FFF0F5'
}, children=[
    
    # Modal for Reward (Dad Joke / GIF Popup)
    dbc.Modal(
        id="joke-modal",
        is_open=False,
        centered=True,
        children=[
            dbc.ModalHeader(dbc.ModalTitle("🎉 Great Job! 🎉"), style={'fontFamily': '"Comic Sans MS"', 'color': '#2C3E50'}),
            dbc.ModalBody(id="joke-modal-body", style={'fontFamily': '"Comic Sans MS"', 'fontSize': '20px', 'textAlign': 'center'}),
            dbc.ModalFooter(
                dbc.Button("Next Question! ➡️", id="close-joke-btn", className="ms-auto", n_clicks=0, style={'fontWeight': 'bold', 'borderRadius': '20px'})
            ),
        ],
    ),

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
        html.H3("😄 Choose A Theme", style={'color': '#2C3E50', 'marginTop': '0', 'marginBottom': '2vh', 'textAlign': 'center'}),
        dcc.Dropdown(
            id='theme-selector',
            options=[{'label': t, 'value': t} for t in THEME_DATA.keys()],
            value='Powerpuff Girls',
            clearable=False,
            style={'fontFamily': "Comic Sans MS", 'fontWeight': 'bold', 'width': '18vw', 'height': '6vh'}
        ),
        html.Div(style={'flexGrow': '1'}),
    ]),
    
    # Central Testing Dashboard Card
    html.Div(id='central-game-card', style={
        'backgroundColor': 'rgba(255, 255, 255, 0.8)', 
        'width': '50vw', 
        'margin': 'auto', 
        'borderRadius': '25px', 
        'padding': '20px 30px', 
        'boxShadow': '0px 8px 20px rgba(0, 0, 0, 0.2)',
        'border': '6px solid #AED6F1', 'boxSizing': 'border-box', 'textAlign': 'center'
    }, children=[
        html.H1(id='app-title', children="🌟 LAB ROOM! 🌟", style={'color': '#FF69B4', 'fontSize': '28px', 'fontWeight': 'bold', 'margin': '0 0 5px 0'}),
        html.Div(id='app-subtitle', children="Can you solve this challenge?", style={'color': '#5DADE2', 'fontSize': '20px', 'fontWeight': 'bold'}),
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
                'fontSize': '26px', 'width': '110px', 'textAlign': 'center', 'borderRadius': '12px', 
                'border': '3px solid #FFB6C1', 'padding': '6px', 'fontWeight': 'bold',
                'display': 'inline-block', 'vertical-align': 'top', "margin-right": "1%",
            }),
            html.Button('💥 Check Answer!', id='submit-btn', n_clicks=0, style={
                'fontSize': '18px', 'color': 'white', 'border': 'none', 'padding': '12px 30px', 
                'borderRadius': '50px', 'cursor': 'pointer', 'fontWeight': 'bold',
                'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1%',
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
#               APP LOGIC
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
    Output('question-box', 'style'),
    Output('user-answer', 'style'),
    Output('joke-modal', 'is_open'),          
    Output('joke-modal-body', 'children'),    
    Input('submit-btn', 'n_clicks'),
    Input('theme-selector', 'value'),
    Input('close-joke-btn', 'n_clicks'),      
    State('user-answer', 'value'),
    State('correct-answer', 'data'),
    State('score-tracker', 'data'),
    State('question-box', 'children'),
    State('main-bg-container', 'style'),
    State('central-game-card', 'style'),
    State('submit-btn', 'style'),
    State('question-box', 'style'),
    State('user-answer', 'style'),
    prevent_initial_call=False
)
def run_themed_game(submit_clicks, active_theme, close_clicks, user_ans, current_correct, score, current_question, bg_style, card_style, btn_style, q_box_style, input_style):
    ctx = callback_context
    cfg = THEME_DATA[active_theme]
    
    def format_score_text(s):
        pct = int((s['correct'] / s['total']) * 100) if s['total'] > 0 else 0
        return f"⭐ Badges: {s['correct']} / {s['total']} | Success Rate: {pct}% ⭐"

    title_text = f"🌟 {active_theme.upper()} MATH LAB! 🌟"
    title_style = {'color': cfg['accent_color'], 'fontSize': '28px', 'fontWeight': 'bold', 'margin': '0 0 5px 0'}
    subtitle_style = {'color': cfg['accent_color'], 'fontSize': '20px', 'fontWeight': 'bold'}
    
    bg_style['backgroundColor'] = cfg['bg_color']
    card_style['border'] = f"6px solid {cfg['card_border']}"
    q_box_style['border'] = f"4px solid {cfg['question_border']}"
    input_style['border'] = f"3px solid {cfg['accent_color']}"
    
    new_btn_style = {
        'fontSize': '18px', 'backgroundColor': cfg['accent_color'], 'color': 'white', 'border': 'none', 
        'padding': '12px 30px', 'borderRadius': '50px', 'cursor': 'pointer', 'fontWeight': 'bold', 
        'boxShadow': f"0px 4px 0px {cfg['button_shadow']}", 'display': 'inline-block', 'margin-left': '1%', 'vertical-align': 'top',
    }

    triggered_id = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    if triggered_id == 'close-joke-btn.n_clicks':
        return current_question, current_correct, "", score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style, False, ""

    if not triggered_id or triggered_id == 'theme-selector.value':
        next_q, next_ans = generate_problem_by_theme(active_theme)
        if cfg.get("images"):
            bg_style['backgroundImage'] = f"url('/assets/{random.choice(cfg['images'])}')"
        return next_q, next_ans, f" Switched to {active_theme}! Go!", score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style, False, ""

    if user_ans is None:
        reminder = html.Span("Type a number first! 🤔", style={'color': '#E67E22'})
        return current_question, current_correct, reminder, score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style, False, ""

    # Process correct/incorrect logic
    is_correct = int(user_ans) == current_correct
    reward_layout = ""
    
    if is_correct:
        feedback = html.Span("✅ Correct! Magnificent job! ✅", style={'color': '#2ECC71'})
        score['correct'] += 1
        
        # --- NEW ALTERNATING REWARD LOGIC ---
        reward_type = random.choice(["joke", "gif", "gif"])
        
        # Safety fallback if a theme doesn't have gifs listed
        if reward_type == "gif" and (not cfg.get("gifs") or len(cfg["gifs"]) == 0):
            reward_type = "joke"
            
        if reward_type == "joke":
            joke_setup, joke_punchline = random.choice(DAD_JOKES)
            reward_layout = html.Div([
                html.P(f"👉 {joke_setup}", style={'fontWeight': 'bold', 'fontSize': '22px'}),
                html.Br(),
                html.P(f"✨ {joke_punchline} ✨", style={'color': '#E74C3C', 'fontWeight': 'bold', 'fontSize': '24px'})
            ])
        else:
            chosen_gif = random.choice(cfg["gifs"])
            reward_layout = html.Div([
                html.P("🎉 Virtual High Five! 🎉", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                html.Img(
                    src=f"/assets/{chosen_gif}", 
                    style={'maxWidth': '100%', 'maxHeight': '300px', 'borderRadius': '15px', 'boxShadow': '0px 4px 10px rgba(0,0,0,0.15)'}
                )
            ])
    else:
        feedback = html.Span(f"❌ Close! The right answer was {current_correct}.", style={'color': '#E74C3C'})
    
    score['total'] += 1

    next_q, next_ans = generate_problem_by_theme(active_theme)
    if cfg.get("images"):
        bg_style['backgroundImage'] = f"url('/assets/{random.choice(cfg['images'])}')"

    return next_q, next_ans, feedback, score, format_score_text(score), "", bg_style, card_style, title_text, title_style, subtitle_style, new_btn_style, q_box_style, input_style, is_correct, reward_layout


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)