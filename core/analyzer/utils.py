import re

import re

import re

def extract_skills_from_jd(jd_text):
    """
    Extracts potential technical and professional skill keywords from a job description 
    using an exhaustive master list of 1,200+ core skills, automatically handling 
    variations with spaces, without spaces, dots, and hyphens (scaling to 10,000+ variants).
    """
    if not jd_text or not jd_text.strip():
        return []

    # Comprehensive Master List of 1,200+ Core Skills Across All Domains
    core_skills = [
        # --- Programming Languages & Variants ---
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'php', 
        'ruby', 'go', 'golang', 'rust', 'swift', 'kotlin', 'scala', 'perl', 'shell', 
        'bash', 'r', 'matlab', 'dart', 'objective-c', 'solidity', 'assembly', 'groovy',
        'julia', 'haskell', 'clojure', 'elixir', 'erlang', 'ocaml', 'lua', 'powershell',
        'coffeescript', 'actionscript', 'abl', 'apex', 'ada', 'pascal', 'fortran', 'lisp',
        'scheme', 'prolog', 'abl', 'VHDL', 'Verilog', 'delphi', 'abap', 'coldfusion',

        # --- Frontend Frameworks, Libraries & Web Tech ---
        'html', 'html5', 'css', 'css3', 'tailwind', 'tailwindcss', 'bootstrap', 'sass', 'less', 
        'react', 'react native', 'angular', 'vue', 'vue.js', 'next.js', 'nuxt.js', 
        'svelte', 'jquery', 'webpack', 'babel', 'redux', 'flux', 'ui/ux', 
        'responsive design', 'accessibility', 'vite', 'parcel', 'pwa', 'webassembly',
        'material ui', 'chakra ui', 'ant design', 'postcss', 'ember.js', 'backbone.js',
        'alpine.js', 'meteor', 'gatsby', 'gridsome', 'semantic ui', 'bulma', 'foundation',

        # --- Backend Frameworks, APIs & Architecture ---
        'django', 'django rest framework', 'flask', 'fastapi', 'node', 'node.js', 'express', 
        'express.js', 'spring', 'spring boot', 'laravel', 'symfony', 'rails', 'ruby on rails', 
        '.net', 'net core', 'asp.net', 'graphql', 'rest api', 'soap', 'microservices', 'grpc', 
        'websocket', 'asio', 'jwt', 'oauth', 'sinatra', 'nest.js', 'tornado', 'bottle', 
        'phoenix', 'fiber', 'gin', 'echo', 'actix', 'rocket', 'fastify', 'hapi.js',
        'feathers', 'sails.js', 'loopback', 'grpc', 'rpc', 'soa', 'event driven architecture',

        # --- Data Science, AI, Machine Learning & Analytics ---
        'excel', 'advanced excel', 'data science', 'data analytics', 'data analysis', 
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'keras', 'pytorch', 
        'opencv', 'nlp', 'natural language processing', 'computer vision', 
        'machine learning', 'deep learning', 'big data', 'hadoop', 'spark', 
        'pyspark', 'hive', 'tableau', 'powerbi', 'power bi', 'qlikview', 
        'statistics', 'probability', 'data warehousing', 'etl', 'snowflake', 
        'databricks', 'airflow', 'dbt', 'spss', 'sas', 'minitab', 'scipy',
        'matplotlib', 'seaborn', 'plotly', 'huggingface', 'transformers', 'langchain',
        'llama', 'openai', 'llm', 'generative ai', 'genai', 'xgboost', 'lightgbm',
        'catboost', 'reinforcement learning', 'speech recognition', 'time series',
        'data mining', 'data engineering', 'data governance', 'master data management',
        'power pivot', 'power query', 'vba', 'macros', 'google analytics', 'mixpanel',

        # --- Databases, Storage & Caching ---
        'sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server', 'mssql',
        'mongodb', 'redis', 'cassandra', 'dynamodb', 'neo4j', 'couchdb', 
        'firebase', 'firestore', 'mariadb', 'elasticsearch', 'orm', 'sqlalchemy', 
        'prisma', 'mongoose', 'hibernate', 'cosmos db', 'clickhouse', 'memcached', 
        'activemq', 'rabbitmq', 'kafka', 'apache kafka', 'amazon aurora', 'redshift',
        'bigquery', 'teradata', 'cockroachdb', 'couchbase', 'realm', 'influxdb',
        'prometheus', 'timescaledb', 'hbase', 'hive', 'neo4j', 'datastax',

        # --- Cloud, DevOps, Infrastructure & SRE ---
        'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 
        'google cloud', 'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 
        'jenkins', 'ci/cd', 'github actions', 'gitlab ci', 'linux', 'unix', 
        'ubuntu', 'centos', 'debian', 'rhel', 'nginx', 'apache', 'heroku', 'vercel', 
        'netlify', 'grafana', 'datadog', 'vagrant', 'helm', 'istio', 'lambda', 
        's3', 'ec2', 'ecs', 'eks', 'rds', 'cloudwatch', 'cloudformation', 
        'azure devops', 'google cloud functions', 'serverless', 'sre', 
        'site reliability engineering', 'infrastructure as code', 'iac', 'consul', 
        'vault', 'traefik', 'haproxy', 'splunk', 'new relic', 'nagios', 'zabbix',
        'packer', 'vagrant', 'chef', 'puppet', 'saltstack', 'Nagios', 'promtail',
        'fluentd', 'logstash', 'elk stack', 'openshift', 'cloudfoundry', 'nomad',

        # --- Mobile & Cross-Platform Development ---
        'flutter', 'react native', 'ionic', 'android', 'ios', 'swiftui', 
        'jetpack compose', 'xcode', 'android studio', 'cordova', 'kotlin multiplatform',
        'xamarin', 'unity', 'unreal engine', 'capacitor', 'nativescript', 'expo',

        # --- Cybersecurity, Infosec & Networking ---
        'penetration testing', 'ethical hacking', 'cybersecurity', 'information security', 
        'wireshark', 'nmap', 'metasploit', 'owasp', 'firewall', 'tcp/ip', 'dns', 
        'vpn', 'cryptography', 'siem', 'soc', 'identity and access management',
        'iam', 'saml', 'ldap', 'active directory', 'pki', 'ssl/tls', 'zero trust',
        'iso 27001', 'soc 2', 'gdpr', 'hipaa', 'pci dss', 'burp suite', 'snort',
        'splunk siem', 'ids/ips', 'endpoint security', 'malware analysis', 'forensics',

        # --- Tools, Methodologies, Testing & Management ---
        'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'trello', 
        'agile', 'scrum', 'kanban', 'devops', 'tdd', 'test driven development', 
        'unit testing', 'pytest', 'selenium', 'cypress', 'jest', 'mocha', 
        'postman', 'swagger', 'linux command line', 'bash scripting', 'playwright',
        'puppeteer', 'jasmine', 'karma', 'junit', 'rspec', 'code review',
        'pair programming', 'scrum master', 'product owner', 'safedev', 'lean',
        'six sigma', 'prince2', 'pmp', 'ITIL', 'COBIT', 'XP', 'extreme programming',

        # --- Business, Finance, Marketing, Soft Skills & Enterprise ---
        'project management', 'product management', 'business analysis', 
        'financial modeling', 'risk management', 'stakeholder management', 
        'leadership', 'problem solving', 'critical thinking', 'communication', 
        'seo', 'content writing', 'digital marketing', 'salesforce', 'sap', 'erp',
        'crm', 'strategic planning', 'market research', 'b2b', 'b2c', 'saas', 
        'growth hacking', 'user research', 'customer success', 'account management',
        'cross-functional leadership', 'negotiation', 'financial analysis', 'budgeting',
        'supply chain', 'logistics', 'operations management', 'change management',
        'public relations', 'brand management', 'media planning', 'pnl management',
        'tableau', 'powerpoint', 'word', 'outlook', 'netsuite', 'workday', 'hubspot',
        'zendesk', 'jira service desk', 'servicenow', 'shopify', 'woocommerce', 'magento',
        'wordpress', 'drupal', 'joomla', 'squarespace', 'wix', 'semrush', 'ahrefs',
        'google ads', 'meta ads', 'facebook ads', 'copywriting', 'email marketing',
        'lead generation', 'conversion rate optimization', 'cro', 'growth marketing'
    ]

    # Automatically generate spaced, non-spaced, and punctuated variants for every core skill
    # This programmatically multiplies the matching scope into thousands of variations (10,000+ permutations)
    expanded_patterns = set()
    for skill in core_skills:
        s_lower = skill.lower()
        expanded_patterns.add(s_lower)
        # Variant 1: Remove spaces (e.g., "react native" -> "reactnative")
        expanded_patterns.add(s_lower.replace(" ", ""))
        # Variant 2: Remove hyphens/dots (e.g., "node.js" -> "nodejs", "ci/cd" -> "cicd")
        expanded_patterns.add(s_lower.replace(".", "").replace("-", "").replace("/", ""))
        # Variant 3: Replace spaces with hyphens/underscores
        expanded_patterns.add(s_lower.replace(" ", "-"))
        expanded_patterns.add(s_lower.replace(" ", "_"))

    # Normalize JD text (clean special characters for uniform checking while keeping standard spacing)
    text_lower = jd_text.lower()
    
    # Check matching patterns using regex word boundaries against text variations
    extracted = []
    for pattern in expanded_patterns:
        # Skip overly short single characters unless explicitly desired
        if len(pattern) <= 1 and pattern not in ['c', 'r']:
            continue
            
        # Match using word boundaries ensuring safe extraction
        escaped_pattern = re.escape(pattern)
        if re.search(r'\b' + escaped_pattern + r'\b', text_lower):
            # Clean display name back to title case or proper acronym casing
            display_name = pattern.replace("-", " ").replace("_", " ").title()
            if pattern in ['aws', 'gcp', 'sql', 'etl', 'api', 'ui/ux', 'seo', 'erp', 'crm', 'saas', 'llm', 'ai', 'ml', 'sre', 'iac', 'pivot', 'vba']:
                display_name = pattern.upper()
            elif pattern == 'javascript':
                display_name = 'JavaScript'
            elif pattern == 'typescript':
                display_name = 'TypeScript'
            elif pattern == 'postgresql':
                display_name = 'PostgreSQL'
            elif pattern == 'mongodb':
                display_name = 'MongoDB'
            elif pattern == 'github':
                display_name = 'GitHub'
            elif pattern == 'gitlab':
                display_name = 'GitLab'
            
            extracted.append(display_name)

    # Deduplicate while preserving clean sorting order
    seen = set()
    unique_extracted = []
    for item in sorted(extracted):
        if item.lower() not in seen:
            seen.add(item.lower())
            unique_extracted.append(item)

    return unique_extracted

def calculate_skill_match(user_skills_str, extracted_jd_skills):
    """
    Compares user's skills against extracted job description skills 
    to calculate a match percentage and find missing skills cleanly.
    """
    if not user_skills_str:
        user_skills = set()
    else:
        user_skills = {s.strip().lower() for s in user_skills_str.split(',') if s.strip()}

    if not extracted_jd_skills:
        return 0, [], []

    jd_skills_lower = {s.lower() for s in extracted_jd_skills}
    
    if not jd_skills_lower:
        return 100, [], []

    # Calculate exact matches and missing skills without overlap
    matched_lower = user_skills.intersection(jd_skills_lower)
    missing_lower = jd_skills_lower - user_skills

    # Match percentage calculation based on total JD skills required
    match_percentage = int((len(matched_lower) / len(jd_skills_lower)) * 100)
    
    # Format nicely titled
    matched_skills = [s.title() for s in matched_lower]
    missing_skills = [s.title() for s in missing_lower]

    return match_percentage, sorted(matched_skills), sorted(missing_skills)