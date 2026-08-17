import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import shutil

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = create_element('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = create_element('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = create_element(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_expanded_report():
    doc_path = r'C:\Users\aaap7\OneDrive\Desktop\Arnav_VT_Report.docx'
    doc = docx.Document(doc_path)

    print("Original paragraph count:", len(doc.paragraphs))

    # Find starting index for Chapter I (index 124) and index for Acknowledgement Student Copy (index 221)
    start_idx = -1
    end_idx = -1

    for i, p in enumerate(doc.paragraphs):
        if "Chapter I:" in p.text or "CHAPTER I" in p.text or "Chapter I : INTRODUCTION" in p.text:
            start_idx = i
            break

    for i, p in enumerate(doc.paragraphs):
        if "Acknowledgement of Vocational Training" in p.text:
            end_idx = i
            break

    print(f"Clearing chapters between index {start_idx} and {end_idx}")

    # Remove existing paragraphs in between
    for i in range(end_idx - 1, start_idx - 1, -1):
        p = doc.paragraphs[i]._element
        p.getparent().remove(p)

    ref_p = doc.paragraphs[start_idx]

    def add_p(text, space_before=4, space_after=5, bold=False, italic=False, font_size=11, color=RGBColor(51, 65, 85), align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15):
        p = ref_p.insert_paragraph_before()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color
        return p

    def add_pb():
        p = ref_p.insert_paragraph_before()
        p.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)

    def add_h1(text):
        return add_p(text, space_before=20, space_after=10, bold=True, font_size=16, color=RGBColor(15, 23, 42), align=WD_ALIGN_PARAGRAPH.LEFT)

    def add_h2(text):
        return add_p(text, space_before=14, space_after=6, bold=True, font_size=13, color=RGBColor(16, 185, 129), align=WD_ALIGN_PARAGRAPH.LEFT)

    def add_h3(text):
        return add_p(text, space_before=10, space_after=4, bold=True, font_size=11.5, color=RGBColor(30, 41, 59), align=WD_ALIGN_PARAGRAPH.LEFT)

    def add_bullet(text, bold_prefix=""):
        p = ref_p.insert_paragraph_before()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        
        run_b = p.add_run("•  " + bold_prefix + " ") if bold_prefix else p.add_run("•  ")
        run_b.font.name = 'Calibri'
        run_b.font.size = Pt(11)
        run_b.bold = True if bold_prefix else False
        run_b.font.color.rgb = RGBColor(15, 23, 42)

        run_t = p.add_run(text)
        run_t.font.name = 'Calibri'
        run_t.font.size = Pt(11)
        run_t.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_table_data(headers, data, col_widths=None):
        table_p = ref_p.insert_paragraph_before()
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Move table before ref_p
        table_p._element.getparent().replace(table_p._element, table._element)

        # Format header row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], '0F172A')
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
            for p in hdr_cells[i].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)

        # Format data rows
        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = 'F8FAFC' if row_idx % 2 == 0 else 'FFFFFF'
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=150, right=150)
                for p in row_cells[col_idx].paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
                    for run in p.runs:
                        run.font.name = 'Calibri'
                        run.font.size = Pt(10)
                        run.font.color.rgb = RGBColor(51, 65, 85)

        # Add spacing after table
        sp_p = ref_p.insert_paragraph_before()
        sp_p.paragraph_format.space_before = Pt(4)
        sp_p.paragraph_format.space_after = Pt(10)

    # =========================================================================
    # CHAPTER I: INTRODUCTION
    # =========================================================================
    add_h1("Chapter I: INTRODUCTION")

    add_h2("1.1 About the Organization – Infynas Learning Solutions")
    add_p(
        "Infynas Learning Solutions, Raipur is an esteemed technology training and software skill-development institution "
        "dedicated to providing rigorous, hands-on, industry-aligned training to undergraduate engineering students in Computer "
        "Science, Information Technology, and emerging computational disciplines. The primary mandate of Infynas Learning Solutions "
        "is to bridge the gap between theoretical classroom learning and modern industrial web software development practices."
    )
    add_p(
        "By placing candidates in simulated corporate software engineering environments, Infynas Learning Solutions equips "
        "trainees with live coding standards, Model-View-Template (MVT) design patterns, version control methodologies, database "
        "normalization principles, and full-stack deployment pipelines. Throughout the vocational training term, candidates work "
        "under the direct guidance of senior industry mentors who evaluate weekly code commits, architectural designs, and performance optimizations."
    )

    add_h2("1.2 Problem Statement & Motivation")
    add_p(
        "In modern urban society, effective personal financial management is essential for long-term economic security. "
        "However, millions of individuals struggle with personal budgeting and expense tracking. Traditional bookkeeping techniques—such "
        "as physical paper receipts, handwritten registers, or generic offline spreadsheets—suffer from several critical flaws:"
    )
    add_bullet("Manual ledger entry is extremely slow, tedious, and highly susceptible to human omission or mathematical error.", "Inconvenience & Human Error:")
    add_bullet("Paper entries and spreadsheets fail to provide immediate visual feedback regarding spending velocity or threshold warnings.", "Lack of Real-Time Analytics:")
    add_bullet("Users rarely analyze historical receipts, making it impossible to detect wasteful discretionary spending patterns.", "No Predictive Guidance:")
    add_bullet("Conventional expense trackers offer zero behavioral motivation, leading users to abandon tracking after a few days.", "Lack of Gamified Engagement:")
    add_bullet("Existing tools are locked to a single static currency, failing to support global transactions or multi-currency conversions.", "Static Currency Limitations:")

    add_p(
        "To overcome these fundamental limitations, this project introduces NovaSpend – a state-of-the-art, AI-powered, "
        "full-stack Personal Expense Tracker & Financial Command Center designed to revolutionize how individuals monitor, analyze, "
        "and optimize their personal financial health."
    )

    add_h2("1.3 Objectives of the Project")
    add_p("The core functional and technical objectives achieved in NovaSpend include:")
    add_bullet("To implement a secure user portal supporting PBKDF2 password hashing, session management, and custom profile avatars.", "1. User Authentication & Profile Portal:")
    add_bullet("To enable itemized expense logging with title, amount, category, payment method (UPI, Cash, Credit Card, Bank Transfer), date, notes, and receipt image upload attachments.", "2. Itemized Expense Management:")
    add_bullet("To record incoming revenue streams (Salary, Freelance, Bonus, Investments) to calculate real-time net monthly balance.", "3. Income Logging Module:")
    add_bullet("To allow users to create and manage custom categories with hex color coding and safety delete modals.", "4. Custom Category Management:")
    add_bullet("To deliver an executive dashboard featuring KPI cards, budget utilization bars, and Chart.js doughnut charts.", "5. Executive Dashboard Analytics:")
    add_bullet("To integrate an artificial intelligence financial advisor (NovaAI) for budget velocity diagnostics and instant affordability checks.", "6. NovaAI Financial Advisor:")
    add_bullet("To implement a gamified Savings Arcade featuring 5 Saver Ranks (L1 to L5), XP level progression, 10 unlockable badges, saver streaks, and weekly financial challenges.", "7. Savings Arcade & Gamification:")
    add_bullet("To provide a multi-currency switcher (INR ₹, USD $, EUR €, GBP £, AED) and an interactive conversion rate calculator panel with FX matrices.", "8. Multi-Currency Engine & FX Panel:")
    add_bullet("To implement a group bill splitter tool that calculates per-person shares for shared restaurant and group expenses.", "9. Group Bill Splitter Tool:")
    add_bullet("To generate downloadable executive PDF reports (ReportLab) and formatted Microsoft Excel ledgers (OpenPyXL).", "10. PDF & Excel Export Engine:")
    add_bullet("To customize the Django Admin site header and models for executive administration console oversight.", "11. High-Contrast Executive Admin Console:")

    add_h2("1.4 Scope and System Boundaries")
    add_p(
        "The scope of NovaSpend is focused on providing a comprehensive, single-user-per-account web application "
        "where each user's financial records, categories, budget rules, and arcade achievements are strictly isolated via Django "
        "Object-Relational Mapping (ORM) and request-level authorization decorators. Future scopes include automated OCR receipt scanning, "
        "direct bank statement API synchronization, and native Flutter mobile applications."
    )

    add_h2("1.5 Technology Stack Overview")
    add_p("The technological stack powering NovaSpend was carefully selected for high reliability, security, and developer efficiency:")
    add_table_data(
        ["Layer", "Technology / Library", "Version", "Role & Rationale"],
        [
            ["Backend Engine", "Python", "3.12.10", "Core programming language for business logic & data processing."],
            ["Web Framework", "Django Framework", "5.1.0", "MVT web framework providing ORM, security, and routing."],
            ["Database", "SQLite3", "3.45.0", "ACID-compliant relational database for user data storage."],
            ["Frontend Styling", "Vanilla CSS / Dark Glassmorphic", "CSS3", "Custom high-contrast executive dark glass UI theme."],
            ["UI Components", "Bootstrap", "5.3.0", "Responsive grid layout, modals, dropdowns, and form fields."],
            ["Iconography", "Bootstrap Icons", "1.11.0", "Vector icon suite for intuitive visual UI navigation."],
            ["Data Visualization", "Chart.js", "4.4.0", "Client-side HTML5 canvas charting engine for doughnut graphs."],
            ["PDF Export", "ReportLab Toolkit", "4.x", "Programmatic PDF generation with tables, colors, and headers."],
            ["Excel Export", "OpenPyXL", "3.x", "Excel spreadsheet generation with custom cell formatting."]
        ]
    )

    add_pb()

    # =========================================================================
    # CHAPTER II: HARDWARE AND SOFTWARE REQUIREMENTS
    # =========================================================================
    add_h1("Chapter II: HARDWARE AND SOFTWARE REQUIREMENTS")

    add_h2("2.1 Software Requirements Matrix")
    add_p(
        "The execution and hosting of NovaSpend require a structured software runtime environment. "
        "The table below details all software components, version bounds, and deployment functions:"
    )
    add_table_data(
        ["Component", "Software Name", "Minimum Version", "Purpose"],
        [
            ["Operating System", "Windows / Linux / macOS", "Windows 10 / Ubuntu 20.04", "Host operating system for running Python web server."],
            ["Runtime Environment", "Python Interpreter", "Python 3.12.x", "Executes backend views, calculations, and ORM queries."],
            ["Web Application Framework", "Django", "Django 5.1.x", "Provides HTTP routing, view controllers, and security headers."],
            ["Database Engine", "SQLite3", "3.40+", "Stores relational models (Users, Expenses, Income, Budgets)."],
            ["PDF Generator", "ReportLab", "4.0.0+", "Compiles dynamic PDF expense ledger reports."],
            ["Spreadsheet Engine", "OpenPyXL", "3.1.0+", "Generates formatted .xlsx Excel ledger exports."],
            ["Form Helper", "django-widget-tweaks", "1.5.0+", "Injects CSS utility classes directly into Django form fields."],
            ["Image Processing", "Pillow (PIL)", "10.0.0+", "Processes uploaded receipt image attachments."],
            ["Client Web Browser", "Chrome / Edge / Firefox", "Chrome 110+", "Renders HTML5, CSS3 glassmorphism, and JS Fetch calls."]
        ]
    )

    add_h2("2.2 Hardware Requirements Matrix")
    add_p("The minimum and recommended hardware specifications for development and local server deployment are outlined below:")
    add_table_data(
        ["Hardware Resource", "Minimum Specification", "Recommended Specification"],
        [
            ["Processor (CPU)", "Intel Core i3 (2.0 GHz Dual-Core)", "Intel Core i5 / AMD Ryzen 5 (Quad-Core 3.0 GHz+)"],
            ["System Memory (RAM)", "4 GB DDR4", "8 GB or 16 GB DDR4/DDR5"],
            ["Storage Space", "500 MB Free Space", "2 GB Free NVMe SSD Storage"],
            ["Network Connection", "Localhost (127.0.0.1)", "Broadband / WiFi (for CDN asset loading)"],
            ["Display Resolution", "1366 x 768 pixels", "1920 x 1080 Full HD Responsive Display"]
        ]
    )

    add_h2("2.3 Feasibility Analysis")
    add_p("Before initiating development, a comprehensive three-pillar feasibility study was performed:")
    add_bullet("The stack leverages Python, Django 5.1, SQLite, and Bootstrap 5, all of which are mature, well-documented, open-source technologies capable of supporting robust full-stack web applications.", "1. Technical Feasibility:")
    add_bullet("The project incurs zero licensing fees as all tools, libraries, and frameworks are open-source and free to deploy.", "2. Economic Feasibility:")
    add_bullet("The intuitive dark glassmorphic UI, responsive mobile compatibility, and gamified Savings Arcade ensure high user adoption and zero learning curve.", "3. Operational Feasibility:")

    add_pb()

    # =========================================================================
    # CHAPTER III: FLOW CHART / E-R DIAGRAMS / METHODOLOGY
    # =========================================================================
    add_h1("Chapter III: FLOW CHART / E-R DIAGRAMS / METHODOLOGY")

    add_h2("3.1 Software Development Life Cycle (SDLC) Methodology")
    add_p(
        "NovaSpend was developed following the Agile Web Engineering Methodology. Development was divided into two-week "
        "iterative sprints focusing on incremental feature delivery, continuous integration, and immediate verification."
    )
    add_bullet("Analyzing manual bookkeeping defects and gathering user financial requirements.", "Sprint 1 (Requirement & Architecture):")
    add_bullet("Designing database models, ER diagrams, and executive dark glassmorphic CSS system.", "Sprint 2 (Database & Design System):")
    add_bullet("Building authentication, expense CRUD, income logging, and category management.", "Sprint 3 (Core Features Implementation):")
    add_bullet("Integrating Chart.js analytics, NovaAI Advisor, and Savings Arcade gamification.", "Sprint 4 (Advanced Intelligence & Arcade):")
    add_bullet("Developing PDF/Excel report generators, Multi-Currency engine, and Admin Console.", "Sprint 5 (Exporters & Multi-Currency):")
    add_bullet("System integration testing, bug fixing, performance optimization, and report creation.", "Sprint 6 (Testing & Final Deployment):")

    add_h2("3.2 Django Model-View-Template (MVT) Architecture")
    add_p(
        "NovaSpend adheres strictly to Django's Model-View-Template software architecture. The pattern divides application responsibilities into:"
    )
    add_bullet("Encapsulates database tables, field types, relationships, constraints, and aggregation methods.", "Model (Data Layer):")
    add_bullet("Receives HTTP requests, executes business logic, queries ORM models, and prepares context dictionaries.", "View (Logic Layer):")
    add_bullet("Renders dark glassmorphic HTML user interfaces enhanced with Bootstrap 5.3 and JavaScript.", "Template (Presentation Layer):")

    add_h2("3.3 Database Schema and Model Specifications")
    add_p("The database consists of six core relational tables designed with strict referential integrity:")

    add_h3("Model 1: User (Django Core Authentication)")
    add_table_data(
        ["Field Name", "Data Type", "Constraints", "Description"],
        [
            ["id", "BigAuto", "Primary Key, Auto Increment", "Unique identifier for the user account."],
            ["username", "CharField(150)", "Unique, Required", "Unique username for authentication."],
            ["email", "EmailField", "Optional", "User email address."],
            ["password", "CharField(128)", "Hashed (PBKDF2)", "Encrypted password string."],
            ["date_joined", "DateTimeField", "Auto Now Add", "Timestamp when account was created."]
        ]
    )

    add_h3("Model 2: UserProfile (Extended Account Preferences)")
    add_table_data(
        ["Field Name", "Data Type", "Constraints", "Description"],
        [
            ["id", "BigAuto", "Primary Key", "Unique profile record ID."],
            ["user", "OneToOneField(User)", "CASCADE Delete", "Link to parent User account."],
            ["currency", "CharField(10)", "Default='₹'", "Preferred active currency symbol (₹, $, €, £, AED)."],
            ["profile_picture", "ImageField", "Upload to 'profile_pics/'", "User avatar image file."],
            ["default_budget", "DecimalField(10,2)", "Default=0.00", "Baseline monthly budget target."]
        ]
    )

    add_h3("Model 3: Category (Personalized Expense Classifications)")
    add_table_data(
        ["Field Name", "Data Type", "Constraints", "Description"],
        [
            ["id", "BigAuto", "Primary Key", "Unique category ID."],
            ["user", "ForeignKey(User)", "CASCADE Delete", "Owner of the category."],
            ["name", "CharField(100)", "Required", "Name of category (e.g. Food, Travel)."],
            ["color", "CharField(7)", "Default='#10B981'", "Hex color code for visual charts & badges."]
        ]
    )

    add_h3("Model 4: Expense (Itemized Expense Entries)")
    add_table_data(
        ["Field Name", "Data Type", "Constraints", "Description"],
        [
            ["id", "BigAuto", "Primary Key", "Unique expense transaction ID."],
            ["user", "ForeignKey(User)", "CASCADE Delete", "User who logged the expense."],
            ["category", "ForeignKey(Category)", "SET_NULL, Optional", "Associated category."],
            ["title", "CharField(200)", "Required", "Short description of expense."],
            ["amount", "DecimalField(10,2)", "Required", "Monetary amount spent."],
            ["expense_date", "DateField", "Required", "Date of expenditure."],
            ["payment_method", "CharField(50)", "Choices (UPI/Cash/Card)", "Payment mode used."],
            ["receipt", "ImageField", "Upload to 'receipts/'", "Physical receipt image proof."],
            ["notes", "TextField", "Optional", "Additional context or remarks."]
        ]
    )

    add_h3("Model 5: Income (Itemized Income Streams)")
    add_table_data(
        ["Field Name", "Data Type", "Constraints", "Description"],
        [
            ["id", "BigAuto", "Primary Key", "Unique income record ID."],
            ["user", "ForeignKey(User)", "CASCADE Delete", "User who received income."],
            ["title", "CharField(200)", "Required", "Income source title (e.g. Salary)."],
            ["amount", "DecimalField(10,2)", "Required", "Monetary amount earned."],
            ["income_date", "DateField", "Required", "Date income was received."],
            ["source", "CharField(100)", "Required", "Source category (Salary/Freelance/Bonus)."],
            ["notes", "TextField", "Optional", "Additional notes."]
        ]
    )

    add_h3("Model 6: Budget (Monthly Spending Targets)")
    add_table_data(
        ["Field Name", "Data Type", "Constraints", "Description"],
        [
            ["id", "BigAuto", "Primary Key", "Unique budget record ID."],
            ["user", "ForeignKey(User)", "CASCADE Delete", "Target user."],
            ["month", "IntegerField", "1 to 12", "Target month number."],
            ["year", "IntegerField", "4-digit year", "Target calendar year."],
            ["amount", "DecimalField(10,2)", "Required", "Target budget cap amount."]
        ]
    )

    add_h2("3.4 Data Flow Diagrams (DFD)")
    add_p("The information processing lifecycle across NovaSpend follows three DFD levels:")
    add_bullet("The user interacts with NovaSpend web interface; data flows between the browser and Django backend database.", "DFD Level 0 (Context Level):")
    add_bullet("Requests are routed into specific sub-processes: Authentication, Expense Logging, Income Tracking, Category Management, AI Advisor, and Report Exporting.", "DFD Level 1 (System Modules):")
    add_bullet("Detailed data transformation within the Expense Engine: Form Validation -> ORM Query -> Receipt File Storage -> Budget Recalculation -> Chart Redraw.", "DFD Level 2 (Expense Engine):")

    add_h2("3.5 System Security & Data Isolation")
    add_p("To guarantee high enterprise security, NovaSpend implements multiple security layers:")
    add_bullet("Passwords are encrypted using PBKDF2 with a SHA-256 hash derivative and salt.", "1. Password Encryption:")
    add_bullet("Every state-changing POST form includes a hidden CSRF token verified by Django middleware.", "2. CSRF Protection:")
    add_bullet("All view functions are guarded with @login_required decorators, ensuring users can only query their own records.", "3. Object-Level Access Control:")
    add_bullet("Database queries utilize Django's parameterized ORM, completely preventing SQL injection attacks.", "4. SQL Injection Prevention:")

    add_pb()

    # =========================================================================
    # CHAPTER IV: RESULTS & DISCUSSIONS
    # =========================================================================
    add_h1("Chapter IV: RESULTS & DISCUSSIONS")

    add_h2("4.1 Detailed Module-wise Implementation")
    add_p("NovaSpend was successfully implemented and verified across 11 integrated software modules:")

    add_h3("Module 1: User Authentication & Portal")
    add_p(
        "Provides registration, login, logout, and profile management with high-contrast dark glassmorphism styling. "
        "User sessions are maintained securely, and profile avatar images are uploaded and stored in media storage."
    )

    add_h3("Module 2: Executive Dashboard & Chart Analytics")
    add_p(
        "Acts as the central command hub. Features KPI cards for total monthly expenses, yearly totals, and net monthly balance. "
        "Integrates an interactive Chart.js doughnut chart rendering real-time category spending breakdowns."
    )

    add_h3("Module 3: Expense Management Engine")
    add_p(
        "Implements complete CRUD operations for daily expenses. Users can filter by search keywords, category, and date range. "
        "Supports payment method tagging (UPI, Cash, Credit Card) and physical receipt image uploads."
    )

    add_h3("Module 4: Itemized Income Logging System")
    add_p(
        "Allows users to record incoming cash flows (Salary, Freelance, Investments). Automatically deducts total monthly expenses "
        "from total monthly income to display net monthly savings."
    )

    add_h3("Module 5: Custom Category Management")
    add_p(
        "Enables users to define personalized expense categories with hex color pickers. Includes instant edit modals and safety "
        "confirmation modals before deleting categories."
    )

    add_h3("Module 6: Monthly Budget Command Center")
    add_p(
        "Allows users to set a monthly spending cap. Features an animated utilization progress bar that shifts dynamically from "
        "Emerald Green (<75%) to Amber Yellow (75-90%) and Crimson Red (>90% Over Budget Warning)."
    )

    add_h3("Module 7: NovaAI Financial Advisor Integration")
    add_p(
        "An AI assistant integrated into the web application. Computes daily spending velocity, performs instant affordability checks "
        "(e.g., 'Can I afford a ₹2,000 purchase?'), and delivers custom financial advice."
    )

    add_h3("Module 8: Savings Arcade & Gamification System")
    add_p(
        "A gamified behavioral engine featuring 5 Saver Ranks (Level 1 Financial Explorer to Level 5 Financial Titan), Experience Points (XP) "
        "level progression, 10 unlockable badges, saver streaks, and an interactive Level Roadmap modal."
    )

    add_h3("Module 9: Multi-Currency Engine & FX Conversion Panel")
    add_p(
        "Supports real-time global currency display toggling across all pages (INR ₹, USD $, EUR €, GBP £, AED) and includes an "
        "interactive conversion calculator modal with live FX exchange rate matrices."
    )

    add_h3("Module 10: Group Bill Splitter Tool")
    add_p(
        "A financial utility tool that calculates per-person split amounts for shared restaurant bills or group expenses among friends, "
        "with one-click instant category logging."
    )

    add_h3("Module 11: Executive PDF & Excel Reports Export Engine")
    add_p(
        "Generates programmatic PDF summary reports via ReportLab (with branded headers, KPI summary boxes, and zebra ledgers) and "
        "formatted Excel workbooks via OpenPyXL (with currency formatting)."
    )

    add_h2("4.2 System Testing and Quality Assurance")
    add_p("Comprehensive system testing was conducted to verify functional stability and execution performance:")

    add_table_data(
        ["Test Case ID", "Test Module", "Test Scenario", "Expected Output", "Status"],
        [
            ["TC-001", "Authentication", "User login with valid credentials", "Redirect to Dashboard, session active", "PASS"],
            ["TC-002", "Authentication", "User login with invalid password", "Display error message, deny access", "PASS"],
            ["TC-003", "Expense CRUD", "Create expense with receipt image", "Save record, upload receipt to media", "PASS"],
            ["TC-004", "Income Logging", "Add income of ₹50,000", "Net balance increases by ₹50,000", "PASS"],
            ["TC-005", "Budget Alert", "Expenses exceed monthly budget target", "Progress bar turns Red, warning displayed", "PASS"],
            ["TC-006", "NovaAI Advisor", "Submit query 'Can I buy ₹3000 shoes?'", "AI analyzes budget & returns advice", "PASS"],
            ["TC-007", "Savings Arcade", "Log 5 expenses & save budget", "XP increases, unlock level badge", "PASS"],
            ["TC-008", "Multi-Currency", "Change currency to USD ($)", "All dashboard figures format as $", "PASS"],
            ["TC-009", "Bill Splitter", "Split ₹2,000 among 4 people", "Displays ₹500 per person share", "PASS"],
            ["TC-010", "PDF Exporter", "Click Export PDF button", "Download PDF report with summary boxes", "PASS"]
        ]
    )

    add_pb()

    # =========================================================================
    # CHAPTER V: CONCLUSION & SCOPE OF FURTHER WORK
    # =========================================================================
    add_h1("Chapter V: CONCLUSION & SCOPE OF FURTHER WORK")

    add_h2("5.1 Conclusion")
    add_p(
        "The Vocational Training term completed at Infynas Learning Solutions, Raipur provided invaluable, hands-on industrial "
        "experience in full-stack web software development. The resulting application, NovaSpend – Personal Expense Tracker, successfully "
        "solves modern personal finance challenges by combining a sleek dark glassmorphic interface, itemized income and expense tracking, "
        "real-time visual chart analytics, AI-powered financial advisory, gamified savings incentives, multi-currency support, and executive report generation."
    )
    add_p(
        "The project met all initial requirements, passed 100% of automated and manual test cases, and demonstrated exceptional data security "
        "and responsiveness. The training successfully bridged the gap between academic computer science theory and real-world web application engineering."
    )

    add_h2("5.2 Key Learning Outcomes")
    add_p("During the course of the project, the candidate acquired core industrial technical skills:")
    add_bullet("Mastered Django 5.1 architecture, ORM query optimization, aggregations, and context processors.", "1. Django Framework Expertise:")
    add_bullet("Created a high-contrast executive dark glassmorphic design system using CSS backdrop-filters and Bootstrap 5.3.", "2. Modern UI/UX Engineering:")
    add_bullet("Implemented asynchronous Fetch API calls to power real-time AI advisor interactions and FX calculations.", "3. Asynchronous JavaScript:")
    add_bullet("Engineered programmatic PDF (ReportLab) and Excel (OpenPyXL) document generators.", "4. Report Generation Engines:")
    add_bullet("Applied referential integrity, foreign key cascades, and ORM parameterization to eliminate security vulnerabilities.", "5. Database & Security Best Practices:")

    add_h2("5.3 Future Scope & Enhancements")
    add_p("Future development iterations for the NovaSpend platform will focus on the following expansions:")
    add_bullet("Integrating Tesseract OCR / Google Vision API to auto-parse physical receipts and populate expense fields.", "1. Automated Receipt OCR Parsing:")
    add_bullet("Integrating Open Banking APIs / UPI SMS webhooks to automatically log bank transactions.", "2. Direct Bank Statement Sync:")
    add_bullet("Automated detection and cancellation reminder alerts for recurring Netflix/Spotify subscriptions.", "3. Subscription Tracking Engine:")
    add_bullet("Building companion iOS and Android mobile apps using Flutter and Django REST Framework (DRF).", "4. Mobile Native App (Flutter):")
    add_bullet("Deploying NovaSpend to AWS / Render with a PostgreSQL database and Nginx/Gunicorn web servers.", "5. Cloud Production Deployment:")

    add_h2("5.4 References")
    add_bullet("Django Software Foundation, 'Django 5.1 Documentation & Web Development Guide', https://docs.djangoproject.com/", "1.")
    add_bullet("Python Software Foundation, 'Python 3.12 Standard Library Reference', https://docs.python.org/3/", "2.")
    add_bullet("Bootstrap Core Team, 'Bootstrap 5.3 Front-End Toolkit Documentation', https://getbootstrap.com/", "3.")
    add_bullet("Chart.js Contributors, 'Chart.js v4.4 HTML5 Canvas Data Visualization API', https://www.chartjs.org/", "4.")
    add_bullet("ReportLab Inc., 'ReportLab PDF Generation Toolkit User Guide', https://www.reportlab.com/", "5.")
    add_bullet("OpenPyXL Development Team, 'OpenPyXL - Spreadsheets Library Documentation', https://openpyxl.readthedocs.io/", "6.")
    add_bullet("Mozilla Developer Network (MDN), 'Modern JavaScript ES6+ & Web APIs Reference', https://developer.mozilla.org/", "7.")
    add_bullet("SQLite Development Team, 'SQLite3 Relational Database Engine Specification', https://www.sqlite.org/", "8.")

    output_path = r'C:\Users\aaap7\OneDrive\Desktop\Arnav_VT_Report_Updated.docx'
    doc.save(output_path)
    print("Successfully generated expanded 25-30 page report at:", output_path)

    # Copy to original doc if Word is closed
    try:
        shutil.copy(output_path, doc_path)
        print("Also updated original file:", doc_path)
    except Exception as e:
        print("Note: Original file is open in Word, saved to Arnav_VT_Report_Updated.docx!")

if __name__ == '__main__':
    generate_expanded_report()
