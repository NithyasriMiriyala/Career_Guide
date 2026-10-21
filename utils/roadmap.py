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


def yt_search(query: str) -> str:
    """A YouTube search link: it never goes dead."""
    return "https://www.youtube.com/results?search_query=" + quote_plus(query)


def channels_for(skill: str, level: str) -> list:
    return CHANNELS.get(skill.strip().lower(), {}).get(level) or DEFAULT_CHANNELS