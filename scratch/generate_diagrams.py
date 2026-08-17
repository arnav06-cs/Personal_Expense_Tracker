import os
from PIL import Image, ImageDraw, ImageFont

def create_er_diagram():
    # Width: 1600, Height: 1000
    w, h = 1600, 1050
    img = Image.new('RGB', (w, h), color='#0F172A')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        header_font = ImageFont.truetype("arial.ttf", 20)
        font = ImageFont.truetype("arial.ttf", 15)
        small_font = ImageFont.truetype("arial.ttf", 13)
    except:
        title_font = header_font = font = small_font = ImageFont.load_default()

    # Draw Title Header
    draw.rectangle([0, 0, w, 80], fill='#1E293B')
    draw.text((w//2, 40), "NOVASPEND – ENTITY RELATIONSHIP (E-R) DIAGRAM", fill='#10B981', font=title_font, anchor='mm')
    draw.line([(0, 80), (w, 80)], fill='#10B981', width=3)

    # Entities Box Definitions: (x1, y1, x2, y2, title, fields)
    boxes = {
        'User': (650, 130, 950, 360, "USER (auth_user)", [
            "PK  id  (BigAuto)",
            "    username  (VARCHAR(150))",
            "    email  (VARCHAR(254))",
            "    password  (VARCHAR(128))",
            "    is_active  (BOOLEAN)",
            "    date_joined  (DATETIME)"
        ]),
        'UserProfile': (150, 150, 450, 340, "USERPROFILE", [
            "PK  id  (BigAuto)",
            "FK  user_id  (OneToOne)",
            "    currency  (VARCHAR(10))",
            "    profile_picture  (VARCHAR)",
            "    default_budget  (DECIMAL)"
        ]),
        'Category': (150, 460, 450, 650, "CATEGORY", [
            "PK  id  (BigAuto)",
            "FK  user_id  (ForeignKey)",
            "    name  (VARCHAR(100))",
            "    color  (VARCHAR(7))"
        ]),
        'Expense': (650, 460, 950, 720, "EXPENSE", [
            "PK  id  (BigAuto)",
            "FK  user_id  (ForeignKey)",
            "FK  category_id  (ForeignKey)",
            "    title  (VARCHAR(200))",
            "    amount  (DECIMAL(10,2))",
            "    expense_date  (DATE)",
            "    payment_method  (VARCHAR)",
            "    receipt  (VARCHAR(100))",
            "    notes  (TEXT)"
        ]),
        'Income': (1150, 150, 1450, 360, "INCOME", [
            "PK  id  (BigAuto)",
            "FK  user_id  (ForeignKey)",
            "    title  (VARCHAR(200))",
            "    amount  (DECIMAL(10,2))",
            "    income_date  (DATE)",
            "    source  (VARCHAR(100))",
            "    notes  (TEXT)"
        ]),
        'Budget': (1150, 460, 1450, 650, "BUDGET", [
            "PK  id  (BigAuto)",
            "FK  user_id  (ForeignKey)",
            "    month  (INTEGER)",
            "    year  (INTEGER)",
            "    amount  (DECIMAL(10,2))"
        ])
    }

    # Function to draw entity box
    for key, (x1, y1, x2, y2, title, fields) in boxes.items():
        # Outer Card
        draw.rectangle([x1, y1, x2, y2], fill='#1E293B', outline='#334155', width=2)
        # Header Box
        draw.rectangle([x1, y1, x2, y1+40], fill='#0F172A', outline='#10B981', width=2)
        draw.text(((x1+x2)//2, y1+20), title, fill='#10B981', font=header_font, anchor='mm')
        
        # Fields
        fy = y1 + 55
        for field in fields:
            is_pk = "PK" in field
            is_fk = "FK" in field
            color = '#F59E0B' if is_pk else ('#6366F1' if is_fk else '#F8FAFC')
            draw.text((x1 + 15, fy), field, fill=color, font=font)
            fy += 24

    # Connectors (Lines and Cardinalities)
    # 1. User -> UserProfile (1 : 1)
    draw.line([(650, 240), (450, 240)], fill='#10B981', width=3)
    draw.text((610, 220), "1", fill='#10B981', font=header_font)
    draw.text((470, 220), "1", fill='#10B981', font=header_font)
    draw.text((540, 215), "has profile", fill='#94A3B8', font=small_font)

    # 2. User -> Category (1 : N)
    draw.line([(650, 280), (550, 280), (550, 550), (450, 550)], fill='#10B981', width=3)
    draw.text((630, 290), "1", fill='#10B981', font=header_font)
    draw.text((470, 530), "N", fill='#10B981', font=header_font)

    # 3. User -> Expense (1 : N)
    draw.line([(800, 360), (800, 460)], fill='#10B981', width=3)
    draw.text((815, 375), "1", fill='#10B981', font=header_font)
    draw.text((815, 435), "N", fill='#10B981', font=header_font)

    # 4. User -> Income (1 : N)
    draw.line([(950, 240), (1150, 240)], fill='#10B981', width=3)
    draw.text((970, 220), "1", fill='#10B981', font=header_font)
    draw.text((1120, 220), "N", fill='#10B981', font=header_font)

    # 5. User -> Budget (1 : N)
    draw.line([(950, 280), (1050, 280), (1050, 550), (1150, 550)], fill='#10B981', width=3)
    draw.text((970, 290), "1", fill='#10B981', font=header_font)
    draw.text((1120, 530), "N", fill='#10B981', font=header_font)

    # 6. Category -> Expense (1 : N)
    draw.line([(450, 590), (650, 590)], fill='#6366F1', width=3)
    draw.text((470, 570), "1", fill='#6366F1', font=header_font)
    draw.text((620, 570), "N", fill='#6366F1', font=header_font)
    draw.text((530, 570), "categorizes", fill='#94A3B8', font=small_font)

    # Legend at Bottom
    draw.rectangle([150, 820, 1450, 950], fill='#1E293B', outline='#334155', width=2)
    draw.text((w//2, 845), "LEGEND & CARDINALITY NOTATIONS", fill='#F8FAFC', font=header_font, anchor='mm')
    draw.text((250, 885), "[PK] Primary Key", fill='#F59E0B', font=font)
    draw.text((500, 885), "[FK] Foreign Key", fill='#6366F1', font=font)
    draw.text((750, 885), "1 : 1  One-to-One Link", fill='#10B981', font=font)
    draw.text((1050, 885), "1 : N  One-to-Many Link", fill='#10B981', font=font)

    out_path = r'C:\Users\aaap7\Documents\Personal_Expense_Tracker\scratch\er_diagram.png'
    img.save(out_path)
    print("ER Diagram generated at:", out_path)

def create_system_flowchart():
    w, h = 1600, 1200
    img = Image.new('RGB', (w, h), color='#0F172A')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        header_font = ImageFont.truetype("arial.ttf", 20)
        font = ImageFont.truetype("arial.ttf", 15)
        small_font = ImageFont.truetype("arial.ttf", 13)
    except:
        title_font = header_font = font = small_font = ImageFont.load_default()

    # Draw Title Header
    draw.rectangle([0, 0, w, 80], fill='#1E293B')
    draw.text((w//2, 40), "NOVASPEND – SYSTEM ARCHITECTURE & DATA FLOWCHART", fill='#10B981', font=title_font, anchor='mm')
    draw.line([(0, 80), (w, 80)], fill='#10B981', width=3)

    # Nodes Definitions: (x1, y1, x2, y2, title, desc, bg_color)
    nodes = {
        'User': (600, 120, 1000, 200, "1. USER / CLIENT BROWSER", "HTTP Request (GET / POST)", '#1E293B'),
        'Auth': (600, 250, 1000, 330, "2. SECURITY & AUTH GATEWAY", "CSRF Token & @login_required Check", '#334155'),
        'URL': (600, 380, 1000, 460, "3. URL ROUTER (urls.py)", "Route Dispatching to View Handlers", '#0F172A'),
        'Views': (600, 510, 1000, 590, "4. VIEW LOGIC (views.py)", "Business Logic & Query Compilation", '#1E293B'),
        'DB': (1100, 510, 1450, 590, "5. SQLITE3 DATABASE", "Django ORM Queries & Aggregations", '#0F172A'),
        
        # Subsystems Grid
        'Dash': (150, 680, 450, 850, "Dashboard & Analytics", "Chart.js Doughnut Charts\nKPI Cards & Totals", '#1E293B'),
        'Expense': (480, 680, 780, 850, "Expense & Income Logging", "CRUD Transaction Engine\nReceipt Image Uploads", '#1E293B'),
        'AI': (810, 680, 1110, 850, "NovaAI Financial Advisor", "Real-Time Spending Velocity\nAffordability Analysis Engine", '#1E293B'),
        'Arcade': (1140, 680, 1450, 850, "Savings Arcade Gamification", "5 Saver Ranks (L1-L5)\nXP Engine & 10 Badges", '#1E293B'),
        
        'MultiCurr': (300, 890, 650, 1020, "Multi-Currency & FX Engine", "INR, USD, EUR, GBP, AED\nLive Conversion Calculator", '#1E293B'),
        'Exports': (950, 890, 1300, 1020, "PDF & Excel Exporters", "ReportLab PDF Engine\nOpenPyXL Workbook Generator", '#1E293B'),

        'UI': (600, 1070, 1000, 1150, "6. EXECUTIVE DARK GLASS UI", "Rendered HTML5 Output", '#10B981')
    }

    # Draw Nodes
    for key, (x1, y1, x2, y2, title, desc, bg) in nodes.items():
        border_col = '#10B981' if key == 'UI' else '#334155'
        text_col = '#0F172A' if key == 'UI' else '#F8FAFC'
        title_col = '#0F172A' if key == 'UI' else '#10B981'
        
        draw.rectangle([x1, y1, x2, y2], fill=bg, outline=border_col, width=2)
        draw.text(((x1+x2)//2, y1 + 25), title, fill=title_col, font=header_font, anchor='mm')
        
        # Multiline desc
        lines = desc.split('\n')
        dy = y1 + 50
        for line in lines:
            draw.text(((x1+x2)//2, dy), line, fill=text_col, font=font, anchor='mm')
            dy += 20

    # Draw Connector Arrows
    # User -> Auth -> URL -> Views -> Subsystems
    draw.line([(800, 200), (800, 250)], fill='#10B981', width=3)
    draw.line([(800, 330), (800, 380)], fill='#10B981', width=3)
    draw.line([(800, 460), (800, 510)], fill='#10B981', width=3)

    # Views <-> DB
    draw.line([(1000, 550), (1100, 550)], fill='#F59E0B', width=3)
    draw.text((1050, 530), "ORM Query", fill='#F59E0B', font=small_font, anchor='mm')

    # Views -> Subsystems
    draw.line([(800, 590), (800, 640)], fill='#10B981', width=3)
    draw.line([(300, 640), (1295, 640)], fill='#10B981', width=3)
    
    draw.line([(300, 640), (300, 680)], fill='#10B981', width=3)
    draw.line([(630, 640), (630, 680)], fill='#10B981', width=3)
    draw.line([(960, 640), (960, 680)], fill='#10B981', width=3)
    draw.line([(1295, 640), (1295, 680)], fill='#10B981', width=3)

    # Subsystems -> Sub-utilities -> UI Output
    draw.line([(475, 850), (475, 890)], fill='#10B981', width=3)
    draw.line([(1125, 850), (1125, 890)], fill='#10B981', width=3)

    draw.line([(475, 1020), (475, 1050), (800, 1050), (800, 1070)], fill='#10B981', width=3)
    draw.line([(1125, 1020), (1125, 1050), (800, 1050)], fill='#10B981', width=3)

    out_path = r'C:\Users\aaap7\Documents\Personal_Expense_Tracker\scratch\system_flowchart.png'
    img.save(out_path)
    print("System Flowchart generated at:", out_path)

if __name__ == '__main__':
    create_er_diagram()
    create_system_flowchart()
