"""
profiles.py — All portfolio data lives here.

To update a person's information, edit the dictionaries below.
No UI code needs to be changed.
"""

PROFILES = [
# Profile 01 — Krish Mahesh Kudchadkar
    # ──────────────────────────────────────────────────────────────────────────
    {
        "id": "krish",
        "number": "01",
        "name": "Krish Mahesh Kudchadkar",
        "role": "Computer Science & Engineering Student",
        "tagline": "Building practical solutions, one project at a time.",
        "accent_color": "#A8D977",    # fresh green
        "avatar_shape": "triangle",
        "avatar_image": "assets/krish.png",
        "about": (
            "A proactive Computer Science & Engineering student at SRMIST with a "
            "passion for technology, problem-solving, and building practical solutions. "
            "Strong in communication, teamwork, and taking initiative, with hands-on "
            "experience in developing full-stack projects and managing responsibilities "
            "in collaborative environments. Eager to take on challenging opportunities "
            "and continuously grow both technically and professionally."
        ),
        "interests": [
            "Web Development",
            "Full Stack Development",
            "Management & Leadership",
            "Operations & Project Management",
        ],
        "goals": "To develop innovative, practical software applications and grow as a well-rounded software engineer and leader.",
        "skills": {
            "Programming":    ["C", "Java", "JavaScript", "Python"],
            "Web Frameworks": ["HTML5", "CSS3", "React 19", "Vite", "Tailwind CSS"],
            "Tools & Tech":   ["Git", "GitHub", "VS Code", "Recharts", "Lucide React", "localStorage"],
            "Core Concepts":  ["Data Structures & Algorithms", "Object Oriented Design & Programming"],
            "Languages":      ["English", "Hindi", "Konkani (Native)", "Marathi", "German"],
            "Soft Skills":    ["Leadership", "Teamwork", "Project Management", "Problem Solving"],
        },
        "projects": [
            {
                "title": "CareerConnect — Placement Management Portal",
                "description": (
                    "A modern Training & Placement Management Portal designed to streamline college "
                    "placement operations. Provides centralized management of recruiting companies, "
                    "student profiles, and placement drives, with automated rule-based eligibility evaluation "
                    "(CGPA, backlogs, department) and interactive analytical dashboards."
                ),
                "tech": ["React 19", "JavaScript", "Vite", "Tailwind CSS", "Recharts", "localStorage"],
                "repo": "https://github.com/kudchadkarkrish",
                "live": "",
            },
            {
                "title": "BistroDesk — Restaurant Management System",
                "description": (
                    "A modular restaurant management and billing application built using core Object-Oriented "
                    "Programming (OOP) principles. Features classes for menu management, table reservations, "
                    "order processing, and dynamic bill generation with tax calculation and itemized receipts."
                ),
                "tech": ["Python", "OOP Concepts", "Data Structures", "File Handling"],
                "repo": "https://github.com/kudchadkarkrish",
                "live": "",
            },
            {
                "title": "CARTOON OS — Portfolio Application",
                "description": (
                    "A cartoon-inspired fictional OS desktop portfolio built entirely with Python "
                    "and Tkinter. Features interactive profile cards, custom animations, a persistent "
                    "taskbar, and responsive screen transitions."
                ),
                "tech": ["Python", "Tkinter"],
                "repo": "https://github.com/kudchadkarkrish/cartoon-os",
                "live": "",
            },
        ],
        "education": [
            {
                "institution": "SRMIST - Kattankulathur, Chennai",
                "degree": "B.Tech in Computer Science and Engineering",
                "duration": "2025 – 2029",
                "details": "CGPA: 8.77 / 10 | Relevant Coursework: Data Structures and Algorithms, Object Oriented Design and Programming.",
            },
            {
                "institution": "The Kings School, Margao, Goa",
                "degree": "Class XII (CBSE - PCMIP) & Class X (CBSE)",
                "duration": "2023 – 2025",
                "details": "Class XII: 71% | Class X: 90.8%",
            },
        ],
        "experience": [
            {
                "org": "Placfv's (SRM Placement Student Team)",
                "role": "Corporate Member",
                "duration": "Oct 2026 – Present",
                "description": "Contributing to corporate outreach, placement drive coordination, and student placement operations.",
                "achievements": [],
            },
            {
                "org": "Newton School Coding Club SRMIST",
                "role": "Member",
                "duration": "Sep 2026 – Present",
                "description": "Engaging in algorithmic problem solving, competitive coding contests, and peer technical workshops.",
                "achievements": [],
            },
        ],
        "email": "kk7814@srmist.edu.in",
        "socials": {
            "LinkedIn": "https://www.linkedin.com/in/krish-kudchadkar",
            "GitHub":   "https://github.com/kudchadkarkrish",
        },
    },

# Profile 02 — Devansh Vallabh Singh
    # ──────────────────────────────────────────────────────────────────────────
    {
        "id": "devansh",
        "number": "02",
        "name": "Devansh Vallabh Singh",
        "role": "Computer Science & Engineering Student",
        "tagline": "Building ideas into reality, one line of code at a time.",
        "accent_color": "#FF6347",    # tomato red
        "avatar_shape": "circle",
        "avatar_image": "assets/devansh.png",
        "about": (
            "I am a B.Tech Computer Science and Engineering student at SRM Institute of Science "
            "and Technology, passionate about technology, software development, and problem-solving. "
            "I enjoy exploring different areas of computer science, building practical applications, "
            "and continuously learning new technologies.\n\n"
            "Beyond coding, I enjoy exploring AI/ML, UI/UX design, photography, video editing, "
            "and 3D modelling. I love collaborating on projects, participating in hackathons, "
            "and turning creative ideas into functional solutions."
        ),
        "interests": [
            "Full-Stack Web Development",
            "Artificial Intelligence & Machine Learning",
            "Data Structures & Algorithms",
            "Software Engineering",
            "UI/UX Design & 3D Modelling",
            "Open Source Development",
        ],
        "goals": "To become a skilled software engineer, build impactful technology-driven products, and contribute to innovative projects.",
        "skills": {
            "Languages":          ["C", "C++", "Python", "Java", "JavaScript", "TypeScript", "HTML", "CSS"],
            "Frameworks & Tools": ["React.js", "Next.js 14", "Node.js", "Tailwind CSS", "Git", "GitHub", "MySQL", "VS Code"],
            "Design & 3D":        ["Blender", "Photoshop", "After Effects", "UI/UX Design"],
            "Core Concepts":      ["Data Structures & Algorithms", "OOP", "DBMS", "Operating Systems", "Computer Networks"],
            "Soft Skills":        ["Problem Solving", "Team Collaboration", "Adaptability", "Creative Thinking", "Communication"],
        },
        "projects": [
            {
                "title": "MediSense — AI Healthcare Platform",
                "description": (
                    "An AI-powered healthcare platform featuring prescription analysis via OCR, "
                    "disease analysis, first-aid educational resources, and an emergency blood donor finder."
                ),
                "tech": ["React.js", "JavaScript", "AI/ML", "OCR", "LLM Integration"],
                "repo": "https://github.com/devanshvsingh",
                "live": "",
            },
            {
                "title": "RefNet — Referral Management Platform",
                "description": (
                    "A referral management platform connecting students and alumni. "
                    "Features student and alumni profiles, referral requests, application reviews, and referral tracking."
                ),
                "tech": ["Next.js 14", "TypeScript", "Tailwind CSS", "shadcn/ui", "Zustand", "Zod"],
                "repo": "https://github.com/devanshvsingh",
                "live": "",
            },
            {
                "title": "Vehicle Service Center Management System",
                "description": (
                    "An object-oriented application designed to manage vehicle servicing operations, "
                    "customer information, maintenance scheduling, and service activities."
                ),
                "tech": ["C++", "OOP", "STL"],
                "repo": "https://github.com/devanshvsingh",
                "live": "",
            },
        ],
        "education": [
            {
                "institution": "SRM Institute of Science and Technology (SRMIST), Kattankulathur",
                "degree": "B.Tech in Computer Science and Engineering (Core)",
                "duration": "2025 – 2029",
                "details": "Relevant Coursework: Data Structures and Algorithms, OOP, DBMS, Operating Systems, Computer Organization and Architecture.",
            },
        ],
        "experience": [
            {
                "org": "SRM Ultron Hackathon",
                "role": "Hackathon Participant / Project Developer",
                "duration": "2024",
                "description": "Developed MediSense, an AI-powered healthcare technology solution addressing medical accessibility.",
                "achievements": [
                    "Developed MediSense, a healthcare technology solution",
                    "Explored AI-powered healthcare applications and OCR",
                    "Collaborated on solving real-world problems through technology",
                ],
            },
            {
                "org": "RefNet Project Team",
                "role": "Frontend Developer / Contributor",
                "duration": "2024 – Present",
                "description": "Contributed to student and alumni profile interfaces, referral workflows, and API integration.",
                "achievements": [
                    "Developed student and alumni profile interfaces and referral workflows",
                    "Contributed to frontend development and API integration",
                    "Collaborated using Git and GitHub in a team environment",
                ],
            },
        ],
        "email": "ds8193@srmist.edu.in",
        "socials": {
            "GitHub":   "https://github.com/devanshvsingh",
            "LinkedIn": "https://linkedin.com",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────,

    # ──────────────────────────────────────────────────────────────────────────
    # Profile 03 — Tanmay Rai
    # ──────────────────────────────────────────────────────────────────────────
{
        "id": "tanmay",
        "number": "03",
        "name": "Tanmay Rai",
        "role": "Computer Science & Engineering Student",
        "tagline": "Building things one bug at a time.",
        "accent_color": "#4776FF",    # cobalt blue
        "avatar_shape": "circle",
        "avatar_image": "assets/tanmay.png",
        "about": (
            "Hi! I'm Tanmay Rai, a Computer Science & Engineering student at SRMIST "
            "with a love for problem-solving, clean code, and creative technology. "
            "Alongside software engineering and full-stack web development, I am a published "
            "poet with work featured in two anthologies and Hindustan Times, and an active "
            "hackathon builder passionate about UI/UX and community leadership."
        ),
        "interests": [
            "Full Stack Web Development",
            "UI/UX Design & Web Applications",
            "Creative Writing & Poetry",
            "Public Speaking & Emceeing",
            "Hackathons & Innovation",
        ],
        "goals": "To develop impactful, scalable software applications and blend technical engineering with creative communication.",
        "skills": {
            "Languages":         ["JavaScript", "Python", "C++", "C", "Java"],
            "Web Frameworks":    ["React.js", "HTML5", "CSS3", "Tailwind CSS", "Supabase", "Firebase", "Mapbox"],
            "Tools & Libraries": ["Git", "GitHub", "NumPy", "Pandas", "VS Code", "Canva", "Google Stitch"],
            "Core Concepts":     ["Data Structures", "Algorithms", "OOP", "Technical Writing", "Backend Integration"],
            "Languages Known":   ["English", "Hindi", "Punjabi", "French (Elementary)"],
            "Soft Skills":       ["Public Speaking", "Creative Writing", "Team Collaboration", "Event Coordination"],
        },
        "projects": [
            {
                "title": "TRIAGEX — Healthcare Web Platform",
                "description": (
                    "A modular healthcare web platform developed for the IIT BHU hackathon. "
                    "Integrates symptom analysis, hospital discovery, medical term explanation, "
                    "and an emergency SOS module with intuitive UI/UX and scalable architecture."
                ),
                "tech": ["React.js", "Tailwind CSS", "JavaScript", "Supabase", "Mapbox"],
                "repo": "https://github.com/Tanmay2007",
                "live": "",
            },
            {
                "title": "Echo Campus — Web Safety Application",
                "description": (
                    "A campus safety web application developed during HackSummit (Finalist). "
                    "Features emergency SOS functionality, live interactive maps, and real-time "
                    "safety assistance in collaborative time-constrained environments."
                ),
                "tech": ["JavaScript", "Maps Integration", "APIs", "Web Technologies"],
                "repo": "https://github.com/Tanmay2007",
                "live": "",
            },
            {
                "title": "BookBuddy — Book Matchmaking Application",
                "description": (
                    "A book recommendation application inspired by Spotify-style matchmaking, "
                    "designed to suggest books based on user preferences with an emphasis on "
                    "personalization and UI design."
                ),
                "tech": ["JavaScript", "APIs", "HTML5", "CSS3"],
                "repo": "https://github.com/Tanmay2007",
                "live": "",
            },
        ],
        "education": [
            {
                "institution": "SRMIST - Kattankulathur, Chennai",
                "degree": "B.Tech in Computer Science and Engineering",
                "duration": "2025 – 2029",
                "details": "Core Computer Science & Engineering. Talent Discovery Test: Band C1.",
            },
            {
                "institution": "Delhi Public School & Ashiana Public School, Chandigarh",
                "degree": "Class XII (CBSE - PCM: 86.8%) & Class X (CBSE: 93.4%)",
                "duration": "2023 – 2025",
                "details": "Class XII: 86.8% | Class X: 93.4%",
            },
        ],
        "experience": [
            {
                "org": "Alexa Developers SRM & Team Envision",
                "role": "Technical Community Member",
                "duration": "2025 – Present",
                "description": (
                    "Active member engaging in technical discussions, project-based learning, "
                    "and emerging technology workshops."
                ),
                "achievements": [
                    "HackSummit Hackathon Finalist (Echo Campus)",
                    "IIT BHU Hackathon Participant (TRIAGEX)",
                    "ADS Hackathon Organising Committee Member",
                ],
            },
            {
                "org": "The Writers Pocket & Hindustan Times",
                "role": "Published Poetry Author",
                "duration": "2023 – Present",
                "description": (
                    "Published original poetry in two anthologies by The Writers Pocket "
                    "and featured multiple times in Hindustan Times."
                ),
                "achievements": [
                    "Published poetry author across two anthologies",
                    "Demonstrated high-impact creative communication and storytelling",
                ],
            },
        ],
        "email": "tr3970@srmist.edu.in",
        "socials": {
            "GitHub":   "https://github.com/Tanmay2007",
            "LinkedIn": "https://linkedin.com",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────,
]
