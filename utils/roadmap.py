"""Topics to learn. TOPICS[skill][level you are moving INTO] = {topic: [subtopics]}."""

TOPICS = {
    "python": {
        "Intermediate": {
            "Functions & modules": ["Args and kwargs", "Lambda functions", "Imports and packages"],
            "Data structures in depth": ["List/dict/set comprehensions", "Collections module", "Sorting and searching"],
            "OOP": ["Classes and objects", "Inheritance", "Dunder methods"],
            "Files & errors": ["File handling", "Exceptions", "JSON and CSV"],
            "Libraries": ["NumPy basics", "Pandas basics", "Virtual environments and pip"],
        },
        "Advanced": {
            "Advanced language features": ["Decorators", "Generators and iterators", "Context managers", "Type hints"],
            "Concurrency": ["Threading vs multiprocessing", "asyncio", "The GIL"],
            "Testing & quality": ["pytest", "Mocking", "Linting and formatting"],
            "Performance": ["Profiling", "Memory management", "Vectorization with NumPy"],
            "Production Python": ["Packaging", "FastAPI/REST APIs", "Logging and config", "Design patterns"],
        },
    },
    "sql": {
        "Intermediate": {
            "Joins": ["INNER/LEFT/RIGHT/FULL", "Self joins", "Cross joins"],
            "Aggregation": ["GROUP BY and HAVING", "COUNT, SUM, AVG", "CASE WHEN"],
            "Subqueries": ["Scalar and correlated subqueries", "EXISTS / IN", "CTEs (WITH)"],
            "Data changes": ["INSERT, UPDATE, DELETE", "Constraints", "Normalization"],
        },
        "Advanced": {
            "Window functions": ["ROW_NUMBER, RANK, DENSE_RANK", "LAG and LEAD", "Running totals and moving averages"],
            "Advanced querying": ["Recursive CTEs", "Pivot/unpivot", "Date and string functions"],
            "Performance": ["Indexes", "Reading execution plans", "Query optimization"],
            "Database design": ["Transactions and ACID", "Views and materialized views", "Stored procedures and triggers"],
            "Analytics SQL": ["Cohort and funnel analysis", "Data warehousing basics (star schema)"],
        },
    },
    "java": {
        "Intermediate": {
            "OOP in Java": ["Inheritance and polymorphism", "Interfaces and abstract classes", "Encapsulation"],
            "Collections": ["List, Set, Map", "Iterators", "Comparable and Comparator"],
            "Error handling & IO": ["Checked vs unchecked exceptions", "File IO", "Generics"],
            "Modern Java": ["Lambdas", "Streams API", "Optional"],
        },
        "Advanced": {
            "Concurrency": ["Threads and Executors", "Synchronization", "CompletableFuture"],
            "JVM internals": ["Memory model and garbage collection", "Class loading", "Performance tuning"],
            "Frameworks": ["Spring Boot", "REST APIs", "JPA/Hibernate"],
            "Engineering practice": ["JUnit and Mockito", "Design patterns", "Maven/Gradle", "Microservices basics"],
        },
    },
    "excel": {
        "Intermediate": {
            "Formulas": ["VLOOKUP/XLOOKUP", "IF, SUMIF, COUNTIF", "INDEX-MATCH"],
            "Data tools": ["Sorting and filtering", "Conditional formatting", "Data validation"],
            "Analysis": ["Pivot tables", "Basic charts", "Named ranges"],
        },
        "Advanced": {
            "Advanced formulas": ["Dynamic arrays", "LET and LAMBDA", "Array formulas"],
            "Data prep": ["Power Query", "Data cleaning at scale", "Merging sources"],
            "Modelling": ["Power Pivot and DAX basics", "Scenario analysis and Solver", "Dashboards with slicers"],
            "Automation": ["Macros", "VBA basics"],
        },
    },
    "power bi": {
        "Intermediate": {
            "Data preparation": ["Power Query transformations", "Merging and appending", "Data types and cleaning"],
            "Data modelling": ["Star schema", "Relationships", "Calculated columns"],
            "Reports": ["Visual types", "Slicers and filters", "Drill-through and bookmarks"],
        },
        "Advanced": {
            "DAX": ["Measures vs columns", "CALCULATE and filter context", "Time intelligence", "Iterators (SUMX)"],
            "Advanced modelling": ["Row-level security", "Composite models", "Incremental refresh"],
            "Performance": ["Optimizing data models", "Performance Analyzer", "Aggregations"],
            "Deployment": ["Power BI Service and workspaces", "Gateways and scheduled refresh", "Governance and sharing"],
        },
    },
    "data visualization": {
        "Intermediate": {
            "Choosing charts": ["Comparison, trend, distribution, relationship", "When not to use pie charts"],
            "Design principles": ["Colour and contrast", "Labels and annotations", "Reducing clutter"],
            "Tools": ["Matplotlib/Seaborn or Tableau basics", "Dashboards layout"],
        },
        "Advanced": {
            "Storytelling": ["Narrative structure", "Highlighting insights", "Presenting to stakeholders"],
            "Interactive visuals": ["Plotly/Altair", "Filters and tooltips", "Drill-downs"],
            "Advanced charts": ["Heatmaps and small multiples", "Geospatial maps", "Statistical plots"],
            "Dashboard craft": ["KPI design", "Accessibility", "Performance on large data"],
        },
    },
    "machine learning": {
        "Intermediate": {
            "Core algorithms": ["Linear/logistic regression", "Decision trees and random forests", "k-NN and SVM"],
            "Model evaluation": ["Train/test split and cross-validation", "Precision, recall, F1, ROC-AUC", "Overfitting"],
            "Data preparation": ["Feature engineering", "Scaling and encoding", "Handling missing data"],
        },
        "Advanced": {
            "Advanced models": ["Gradient boosting (XGBoost, LightGBM)", "Ensembles", "Unsupervised learning"],
            "Optimization": ["Hyperparameter tuning", "Regularization", "Imbalanced data"],
            "Deployment": ["ML pipelines", "Model serving with APIs", "Monitoring and drift"],
            "Deep learning intro": ["Neural network basics", "CNNs and RNNs overview", "Transfer learning"],
        },
    },
    "javascript": {
        "Intermediate": {
            "Core language": ["Closures and scope", "this and prototypes", "ES6+ features"],
            "Async JS": ["Promises", "async/await", "Fetch API"],
            "Browser": ["DOM manipulation", "Events", "Local storage"],
        },
        "Advanced": {
            "Deep language": ["Event loop", "Modules", "Iterators and generators"],
            "Tooling": ["TypeScript", "Bundlers", "Testing (Jest)"],
            "Performance": ["Debouncing and throttling", "Memory leaks", "Web workers"],
            "Architecture": ["State management", "Design patterns", "Security (XSS, CORS)"],
        },
    },
}

GENERIC = {
    "Intermediate": {
        "Strengthen the basics": ["Revisit core concepts", "Build 2 small projects", "Read the official documentation"],
        "Apply it": ["Solve practice problems", "Follow an intermediate course", "Use it in a real task"],
    },
    "Advanced": {
        "Go deeper": ["Internals and best practices", "Performance and scale", "Testing and quality"],
        "Prove it": ["Build a portfolio project", "Contribute to open source or mentor others", "Prepare for interviews on this skill"],
    },
}


def topics_for(skill: str, level: str) -> dict:
    return TOPICS.get(skill.strip().lower(), {}).get(level) or GENERIC[level]
# ---------- YouTube learning resources ----------
from urllib.parse import quote_plus

CHANNELS = {
    "python": {"Intermediate": ["Corey Schafer", "Tech With Tim", "freeCodeCamp.org"],
            "Advanced": ["ArjanCodes", "mCoding", "Corey Schafer"]},
    "sql": {"Intermediate": ["Alex The Analyst", "freeCodeCamp.org", "Kudvenkat"],
            "Advanced": ["Alex The Analyst", "Luke Barousse", "freeCodeCamp.org"]},
    "java": {"Intermediate": ["Telusko", "Programming with Mosh", "Amigoscode"],
            "Advanced": ["Java Brains", "Amigoscode", "Telusko"]},
    "javascript": {"Intermediate": ["Traversy Media", "Web Dev Simplified", "freeCodeCamp.org"],
                "Advanced": ["Namaste JavaScript", "Fireship", "Web Dev Simplified"]},
    "html": {"Intermediate": ["Kevin Powell", "Traversy Media", "freeCodeCamp.org"],
            "Advanced": ["Kevin Powell", "Web Dev Simplified", "Traversy Media"]},
    "css": {"Intermediate": ["Kevin Powell", "Traversy Media", "freeCodeCamp.org"],
            "Advanced": ["Kevin Powell", "Web Dev Simplified", "Fireship"]},
    "react": {"Intermediate": ["The Net Ninja", "Traversy Media", "freeCodeCamp.org"],
            "Advanced": ["Jack Herrington", "Codevolution", "Fireship"]},
    "node.js": {"Intermediate": ["Traversy Media", "The Net Ninja", "freeCodeCamp.org"],
                "Advanced": ["Academind", "Fireship", "Traversy Media"]},
    "machine learning": {"Intermediate": ["StatQuest with Josh Starmer", "Krish Naik", "Codebasics"],
                        "Advanced": ["Krish Naik", "StatQuest with Josh Starmer", "Sentdex"]},
    "deep learning": {"Intermediate": ["DeepLearning.AI", "3Blue1Brown", "Krish Naik"],
                    "Advanced": ["Andrej Karpathy", "DeepLearning.AI", "Yannic Kilcher"]},
    "llms": {"Intermediate": ["DeepLearning.AI", "Krish Naik", "freeCodeCamp.org"],
            "Advanced": ["Andrej Karpathy", "DeepLearning.AI", "Umar Jamil"]},
    "apis": {"Intermediate": ["freeCodeCamp.org", "Traversy Media", "Amigoscode"],
            "Advanced": ["ByteByteGo", "Hussein Nasser", "Amigoscode"]},
    "docker": {"Intermediate": ["TechWorld with Nana", "freeCodeCamp.org", "Bret Fisher"],
            "Advanced": ["Bret Fisher", "KodeKloud", "TechWorld with Nana"]},
    "git": {"Intermediate": ["freeCodeCamp.org", "Fireship", "Kunal Kushwaha"],
            "Advanced": ["Fireship", "Kunal Kushwaha", "freeCodeCamp.org"]},
    "cloud": {"Intermediate": ["freeCodeCamp.org", "KodeKloud", "TechWorld with Nana"],
            "Advanced": ["TechWorld with Nana", "KodeKloud", "freeCodeCamp.org"]},
    "excel": {"Intermediate": ["Kevin Stratvert", "Leila Gharani", "ExcelIsFun"],
            "Advanced": ["Leila Gharani", "MyOnlineTrainingHub", "ExcelIsFun"]},
    "power bi": {"Intermediate": ["Guy in a Cube", "Kevin Stratvert", "Alex The Analyst"],
                "Advanced": ["Guy in a Cube", "SQLBI", "RADACAD"]},
    "statistics": {"Intermediate": ["StatQuest with Josh Starmer", "Khan Academy", "Brandon Foltz"],
                "Advanced": ["StatQuest with Josh Starmer", "zedstatistics", "Khan Academy"]},
    "data visualization": {"Intermediate": ["Alex The Analyst", "Storytelling with Data", "Guy in a Cube"],
                        "Advanced": ["Storytelling with Data", "Guy in a Cube", "Alex The Analyst"]},
    "communication": {"Intermediate": ["Vinh Giang", "TED", "Charisma on Command"],
                    "Advanced": ["Charisma on Command", "Vinh Giang", "TED"]},
}
DEFAULT_CHANNELS = ["freeCodeCamp.org", "Programming with Mosh"]
# ---------- Certifications and project ideas ----------
CERTS = {
    "python": {"Intermediate": ["Python Institute PCAP: Certified Associate in Python Programming",
                                "Google IT Automation with Python (Coursera)"],
            "Advanced": ["Python Institute PCPP1: Certified Professional in Python Programming"]},
    "sql": {"Intermediate": ["HackerRank SQL (Intermediate) skill certificate",
                            "Microsoft Azure Data Fundamentals (DP-900)"],
            "Advanced": ["HackerRank SQL (Advanced) skill certificate",
                        "Oracle Database SQL Certified Associate"]},
    "java": {"Intermediate": ["Oracle Certified Foundations Associate, Java"],
            "Advanced": ["Oracle Certified Professional: Java SE Developer"]},
    "javascript": {"Intermediate": ["freeCodeCamp JavaScript Algorithms and Data Structures"],
                "Advanced": ["freeCodeCamp Front End Development Libraries",
                                "OpenJS Node.js Application Developer (JSNAD)"]},
    "html": {"Intermediate": ["freeCodeCamp Responsive Web Design"],
            "Advanced": ["Meta Front-End Developer Professional Certificate (Coursera)"]},
    "css": {"Intermediate": ["freeCodeCamp Responsive Web Design"],
            "Advanced": ["Meta Front-End Developer Professional Certificate (Coursera)"]},
    "react": {"Intermediate": ["Meta Front-End Developer Professional Certificate (Coursera)"],
            "Advanced": ["freeCodeCamp Front End Development Libraries"]},
    "node.js": {"Intermediate": ["Meta Back-End Developer Professional Certificate (Coursera)"],
                "Advanced": ["OpenJS Node.js Application Developer (JSNAD)",
                            "OpenJS Node.js Services Developer (JSNSD)"]},
    "machine learning": {"Intermediate": ["Machine Learning Specialization (DeepLearning.AI and Stanford, Coursera)"],
                        "Advanced": ["AWS Certified Machine Learning Engineer - Associate",
                                    "Google Cloud Professional Machine Learning Engineer"]},
    "deep learning": {"Intermediate": ["Deep Learning Specialization (DeepLearning.AI, Coursera)"],
                    "Advanced": ["NVIDIA Deep Learning Institute certificate courses"]},
    "llms": {"Intermediate": ["Generative AI with Large Language Models (DeepLearning.AI and AWS, Coursera)"],
            "Advanced": ["Hugging Face LLM Course (free, with exercises)",
                        "NVIDIA Deep Learning Institute: generative AI courses"]},
    "apis": {"Intermediate": ["Postman API Fundamentals Student Expert"],
            "Advanced": ["Meta Back-End Developer Professional Certificate (Coursera)"]},
    "docker": {"Intermediate": ["KodeKloud Docker course completion certificate"],
            "Advanced": ["Certified Kubernetes Application Developer (CKAD)",
                            "Docker Certified Associate (DCA), if still offered"]},
    "git": {"Intermediate": ["GitHub Foundations (GH-900)"],
            "Advanced": ["GitHub Actions (GH-200)"]},
    "cloud": {"Intermediate": ["AWS Certified Cloud Practitioner", "Microsoft Azure Fundamentals (AZ-900)",
                            "Google Cloud Digital Leader"],
            "Advanced": ["AWS Certified Solutions Architect - Associate",
                        "Microsoft Azure Administrator (AZ-104)"]},
    "excel": {"Intermediate": ["Microsoft Office Specialist: Excel Associate"],
            "Advanced": ["Microsoft Office Specialist: Excel Expert"]},
    "power bi": {"Intermediate": ["Microsoft Power BI Data Analyst Associate (PL-300)"],
                "Advanced": ["Microsoft Fabric Analytics Engineer Associate (DP-600)"]},
    "statistics": {"Intermediate": ["Statistics with Python Specialization (University of Michigan, Coursera)"],
                "Advanced": ["Google Advanced Data Analytics Certificate (Coursera)"]},
    "data visualization": {"Intermediate": ["Tableau Desktop Specialist",
                                            "Google Data Analytics Certificate (Coursera)"],
                        "Advanced": ["Tableau Certified Data Analyst"]},
    "communication": {"Intermediate": ["Toastmasters Pathways (club-based)"],
                    "Advanced": ["Toastmasters Pathways advanced levels"]},
}

PROJECTS = {
    "python": {"Intermediate": ["Expense tracker that saves to CSV or JSON", "Web scraper that collects job postings into a spreadsheet"],
            "Advanced": ["REST API with FastAPI, tests and logging", "A command-line tool published as a package"]},
    "sql": {"Intermediate": ["Design a library or school database and write 20 queries on it", "Analyse a public sales dataset with joins and GROUP BY"],
            "Advanced": ["Cohort and retention analysis with window functions", "Optimise slow queries with indexes and explain plans"]},
    "java": {"Intermediate": ["Bank account system using OOP and collections", "Library management app with file storage"],
            "Advanced": ["REST API with Spring Boot and a database", "Multi-threaded download manager"]},
    "javascript": {"Intermediate": ["To-do app with local storage", "Weather app using a public API with fetch"],
                "Advanced": ["Real-time chat app", "A small framework-free single page app with routing"]},
    "html": {"Intermediate": ["Personal portfolio page", "Landing page copied from a design"],
            "Advanced": ["Accessible multi-page site that scores 90+ on Lighthouse"]},
    "css": {"Intermediate": ["Responsive layout with Flexbox and Grid", "Recreate a popular site's homepage"],
            "Advanced": ["Design system with CSS variables and dark mode", "Animated components without a library"]},
    "react": {"Intermediate": ["Movie search app with an API", "Notes app with state and hooks"],
            "Advanced": ["Full dashboard with routing, state management and tests", "E-commerce front end with a cart"]},
    "node.js": {"Intermediate": ["Blog API with Express and a database", "URL shortener"],
                "Advanced": ["Authenticated API with JWT, validation and tests", "Real-time app with WebSockets"]},
    "machine learning": {"Intermediate": ["House price prediction with regression", "Spam classifier with scikit-learn"],
                        "Advanced": ["End-to-end model served as an API", "Imbalanced-data fraud detection with proper evaluation"]},
    "deep learning": {"Intermediate": ["Digit or image classifier with a small neural network", "Sentiment analysis with an RNN or transformer"],
                    "Advanced": ["Transfer learning on your own image dataset", "Reproduce a small research paper"]},
    "llms": {"Intermediate": ["Chatbot that answers questions from your notes (RAG)", "Summariser for articles or PDFs"],
            "Advanced": ["Agent that uses tools and APIs", "Evaluate and compare prompts or models on your own test set"]},
    "apis": {"Intermediate": ["CRUD REST API with a database", "Dashboard that consumes a public API"],
            "Advanced": ["API with authentication, rate limiting and docs", "Webhook receiver that processes events"]},
    "docker": {"Intermediate": ["Containerise a Python or Node app", "Docker Compose with an app and a database"],
            "Advanced": ["CI pipeline that builds and pushes an image", "Deploy a multi-container app to a cloud host"]},
    "git": {"Intermediate": ["Use branches and pull requests on a real project", "Resolve a merge conflict on purpose and document it"],
            "Advanced": ["GitHub Actions workflow that runs tests", "Contribute a fix to an open-source project"]},
    "cloud": {"Intermediate": ["Host a static site on a cloud service", "Deploy a small API with a managed database"],
            "Advanced": ["Infrastructure as code for a full app", "Serverless pipeline with storage and functions"]},
    "excel": {"Intermediate": ["Personal budget with formulas and charts", "Sales report with pivot tables"],
            "Advanced": ["Interactive dashboard with slicers", "Automate a report with Power Query or macros"]},
    "power bi": {"Intermediate": ["Sales dashboard from a CSV", "Model with relationships between 3 tables"],
            "Advanced": ["Dashboard with DAX time intelligence and row-level security", "Published report with scheduled refresh"]},
    "statistics": {"Intermediate": ["A/B test analysis on sample data", "Descriptive analysis of a public dataset"],
                "Advanced": ["Regression with assumptions checked", "Bayesian vs frequentist comparison on a real question"]},
    "data visualization": {"Intermediate": ["Dashboard on a topic you care about", "Redo a bad chart and explain the improvements"],
                        "Advanced": ["Interactive Plotly or Altair story with filters", "Map-based visualisation"]},
    "communication": {"Intermediate": ["Record a 3-minute talk and review it", "Write a clear project README"],
                    "Advanced": ["Give a talk or workshop to a group", "Write a case study of a project for non-technical readers"]},
}

DEFAULT_CERTS = {
    "Intermediate": ["A recognised course certificate from Coursera, edX or the tool's own learning site"],
    "Advanced": ["A professional-level certificate offered by the tool's vendor"],
}
DEFAULT_PROJECTS = {
    "Intermediate": ["Build a small end-to-end project and publish it on GitHub"],
    "Advanced": ["Build a larger project with tests and documentation, and deploy it"],
}


def google_search(query: str) -> str:
    return "https://www.google.com/search?q=" + quote_plus(query)


def certs_for(skill: str, level: str) -> list:
    return CERTS.get(skill.strip().lower(), {}).get(level) or DEFAULT_CERTS.get(level, [])


def projects_for(skill: str, level: str) -> list:
    return PROJECTS.get(skill.strip().lower(), {}).get(level) or DEFAULT_PROJECTS.get(level, [])

def yt_search(query: str) -> str:
    """A YouTube search link: it never goes dead."""
    return "https://www.youtube.com/results?search_query=" + quote_plus(query)


def channels_for(skill: str, level: str) -> list:
    return CHANNELS.get(skill.strip().lower(), {}).get(level) or DEFAULT_CHANNELS