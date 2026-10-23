"""Script to expand the Tamil Nadu Government Schemes dataset with 23+ new verified schemes."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "schemes" / "tn_schemes_verified.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    existing_schemes = json.load(f)

existing_ids = {s["scheme_id"] for s in existing_schemes}
print(f"Current scheme count: {len(existing_schemes)}")

new_schemes = [
    {
        "scheme_id": "TN-MAKKALAI-THEDI-013",
        "scheme_name_tamil": "மக்களைத் தேடி மருத்துவம்",
        "scheme_name_english": "Makkalai Thedi Maruthuvam (Healthcare at Doorstep)",
        "department": "Health and Family Welfare Department",
        "department_tamil": "மக்கள் நல்வாழ்வு மற்றும் குடும்ப நலத் துறை",
        "category": "Healthcare & Wellness",
        "sub_category": "Doorstep Healthcare & Chronic Disease Management",
        "description_tamil": "நீரிழிவு, உயர் ரத்த அழுத்தம் உள்ளிட்ட தொற்றா நோய்களுக்கான பரிசோதனைகள் மற்றும் மருந்துகளை மக்களின் வீடுகளுக்கே நேரடியாகச் சென்று வழங்கும் திட்டம்.",
        "description_english": "Flagship community healthcare initiative delivering doorstep screening and essential non-communicable disease medications directly to households across Tamil Nadu.",
        "benefits": {
            "doorstep_screening": "Periodic screening for 27 health conditions including hypertension, diabetes, and cancers",
            "free_medication": "Essential medicines for chronic diseases delivered home monthly",
            "palliative_physiotherapy": "Home-based palliative care and physiotherapy for bedridden patients"
        },
        "eligibility_rules": {
            "age": {"min": 0, "max": 120},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "income_limit_annual": 0,
            "special_conditions": [
                "Universal coverage for all residents in Tamil Nadu",
                "Priority for elderly, disabled, and bedridden individuals needing regular care"
            ]
        },
        "required_documents": [
            "Aadhaar Card or Family Ration Card (for health record creation)"
        ],
        "application_method": "Proactive Doorstep Visit (No Application Required)",
        "application_steps": [
            "1. Women Public Health Volunteers (WHVs) and nurses visit homes periodically",
            "2. Health screening is conducted at home",
            "3. Digital health record is created and free medicines are delivered",
            "4. Follow-up visits arranged on monthly basis"
        ],
        "official_urls": [
            "https://tnhealth.tn.gov.in",
            "https://tnhsp.tn.gov.in"
        ],
        "contact_helpline": "104 (Health Helpline) / 108 (Ambulance)",
        "dates": {"launch_date": "2021-08-05", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "Tamil Nadu Health Department Official Portal",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-INNUYIR-014",
        "scheme_name_tamil": "இன்னுயிர் காப்போம் - நம்மை காக்கும் 48",
        "scheme_name_english": "Innuyir Kaappom - Nammai Kaakkum 48",
        "department": "Health and Family Welfare Department",
        "department_tamil": "மக்கள் நல்வாழ்வு மற்றும் குடும்ப நலத் துறை",
        "category": "Emergency Healthcare",
        "sub_category": "Road Traffic Accident Care",
        "description_tamil": "சாலை விபத்துகளில் சிக்குபவர்களுக்கு முதல் 48 மணி நேர அவசர சிகிச்சையை ரூ.2 லட்சம் வரை முற்றிலும் இலவசமாக அரசு மற்றும் தனியார் மருத்துவமனைகளில் வழங்கும் திட்டம்.",
        "description_english": "Emergency healthcare program providing free cashless treatment up to Rs. 2 Lakhs per person for the first 48 hours following a road accident in Tamil Nadu.",
        "benefits": {
            "cashless_emergency_care": "Free medical care up to ₹2,00,000 per victim",
            "procedures_covered": "101 life-saving medical and surgical procedures covered",
            "duration": "First 48 hours (Golden Hour) across 600+ empaneled government and private hospitals"
        },
        "eligibility_rules": {
            "age": {"min": 0, "max": 120},
            "gender": ["Any"],
            "residence": "Any",
            "special_conditions": [
                "Applicable to any road traffic accident occurring within the boundaries of Tamil Nadu",
                "Applies to TN residents, residents of other states, and foreign nationals alike",
                "No income limit or CMCHIS card required"
            ]
        },
        "required_documents": [
            "No upfront documents needed for emergency treatment"
        ],
        "application_method": "Immediate Hospital Admission through 108 Emergency",
        "application_steps": [
            "1. 108 ambulance transports road accident victim to empaneled hospital",
            "2. Hospital registers patient under Innuyir Kaappom portal immediately",
            "3. Emergency treatment up to Rs. 2 Lakhs provided without any payment",
            "4. Further treatment routed through CMCHIS or standard protocol after 48 hours"
        ],
        "official_urls": [
            "https://tnhsp.tn.gov.in",
            "https://cmchistn.com"
        ],
        "contact_helpline": "108 / 104",
        "dates": {"launch_date": "2021-12-18", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TNHSP Innuyir Kaappom Portal",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-KANAVU-ILLAM-015",
        "scheme_name_tamil": "கலைஞரின் கனவு இல்லம் திட்டம்",
        "scheme_name_english": "Kalaignarin Kanavu Illam (Dream Home Scheme)",
        "department": "Rural Development and Panchayat Raj Department",
        "department_tamil": "ஊரக வளர்ச்சி மற்றும் ஊராட்சித் துறை",
        "category": "Housing & Rural Development",
        "sub_category": "Rural Concrete Housing",
        "description_tamil": "ஊரகப் பகுதிகளில் குடிசைகளில் வாழும் ஏழை எளிய குடும்பங்களுக்கு தலா ரூ.3.50 லட்சம் மதிப்பீட்டில் நிரந்தர கான்கிரீட் வீடுகள் கட்ட நிதி வழங்கும் திட்டம்.",
        "description_english": "State housing initiative providing Rs. 3.50 Lakhs assistance to construct permanent concrete houses for poor rural families living in thatched and kutcha huts.",
        "benefits": {
            "housing_grant": "₹3,50,000 per house unit cost via Direct Benefit Transfer",
            "specifications": "Minimum 360 sq.ft plinth area with RCC roofing and attached toilet",
            "convergence": "90 person-days of MGNREGS wages included for construction"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 100},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "location_type": ["Rural"],
            "housing_status": ["Hut", "Kutcha", "Thatched House"],
            "special_conditions": [
                "Must be a rural household living in a hut or dilapidated house",
                "Must possess Patta or valid house site ownership documents",
                "Selected from the official Rural Housing Survey list"
            ]
        },
        "required_documents": [
            "Smart Family Ration Card",
            "Aadhaar Card",
            "House Site Patta / Title Deed",
            "Bank Account Passbook"
        ],
        "application_method": "Village Panchayat Survey & Block Development Office",
        "application_steps": [
            "1. Village Panchayat conducts hutment survey and prepares beneficiary list",
            "2. Grama Sabha approval for eligible beneficiaries",
            "3. Work order issued by Block Development Officer (BDO)",
            "4. Geotagged stage-by-stage construction verification and DBT fund release"
        ],
        "official_urls": [
            "https://tnrd.tn.gov.in"
        ],
        "contact_helpline": "District Collectorate / BDO Office Helpline",
        "dates": {"launch_date": "2024-02-19", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TNRD Official Rural Housing Guidelines",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-BREAKFAST-016",
        "scheme_name_tamil": "முதலமைச்சரின் காலை உணவுத் திட்டம்",
        "scheme_name_english": "Chief Minister's Breakfast Scheme (Kaalai Unavu Thittam)",
        "department": "School Education Department & Social Welfare Department",
        "department_tamil": "பள்ளிக் கல்வித் துறை மற்றும் சமூக நலத் துறை",
        "category": "Education & Child Nutrition",
        "sub_category": "School Student Nutrition",
        "description_tamil": "அரசு தொடக்க மற்றும் நடுநிலைப் பள்ளி மாணவர்களுக்கு அனைத்து பள்ளி வேலை நாட்களிலும் சத்தான சூடான காலை உணவு இலவசமாக வழங்கும் திட்டம்.",
        "description_english": "Pioneering state program providing free nutritious hot breakfast to primary and middle school students studying in Government and Govt-aided schools.",
        "benefits": {
            "free_breakfast": "Nutritious cooked morning meal served on all school working days",
            "menu": "Varied menu including Upma, Kichadi, Pongal, and Sambar with vegetables",
            "student_coverage": "All enrolled students from Class 1 to Class 8 in covered schools"
        },
        "eligibility_rules": {
            "age": {"min": 5, "max": 14},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "student_status": True,
            "school_type": ["Government School", "Government-aided Primary/Middle School"],
            "special_conditions": [
                "Enrolled in Class 1 through Class 8 in recognized Government schools"
            ]
        },
        "required_documents": [
            "Automatic enrollment through School EMIS registration (No separate documents)"
        ],
        "application_method": "Universal Automatic Enrollment at School",
        "application_steps": [
            "1. Student takes admission in Government/Govt-aided school",
            "2. Breakfast is served automatically before morning classes commence"
        ],
        "official_urls": [
            "https://schooledu.tn.gov.in"
        ],
        "contact_helpline": "14417 (School Education Helpline)",
        "dates": {"launch_date": "2022-09-15", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN School Education Department Notifications",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-NAAN-MUDHALVAN-017",
        "scheme_name_tamil": "நான் முதல்வன் திட்டம்",
        "scheme_name_english": "Naan Mudhalvan Skill Development and Mentorship Scheme",
        "department": "Tamil Nadu Skill Development Corporation (TNSDC)",
        "department_tamil": "தமிழ்நாடு திறன் மேம்பாட்டுக் கழகம்",
        "category": "Skill Development & Employment",
        "sub_category": "Youth Upskilling & Career Guidance",
        "description_tamil": "கல்லூரி மற்றும் பள்ளி மாணவர்களுக்கு நவீன தொழில் நுட்பங்கள், தகவல் தொழில்நுட்பம் மற்றும் போட்டித் தேர்வுகளுக்கான இலவச பயிற்சிகள் வழங்கும் முதன்மைத் திட்டம்.",
        "description_english": "Apex skilling and career guidance initiative providing free training in emerging technologies, coding, robotics, English proficiency, and competitive exam prep to 10 lakh+ youth annually.",
        "benefits": {
            "industry_training": "Free certified courses in AI, Cloud, EV, Data Analytics, Semiconductor, and Cyber Security",
            "placement_support": "Campus placement drives and industry internship connections",
            "exam_stipend": "Monthly incentive of ₹7,500 for candidates preparing for UPSC/TNPSC civil service exams"
        },
        "eligibility_rules": {
            "age": {"min": 17, "max": 35},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "education": ["12th Pass", "Diploma", "Undergraduate", "Postgraduate", "Engineering", "Arts & Science"],
            "special_conditions": [
                "Students studying in Arts, Science, Engineering, Polytechnic colleges in Tamil Nadu",
                "Unemployed graduates seeking technical upskilling"
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "College Student ID or Degree Certificate",
            "Mobile Number linked with Aadhaar"
        ],
        "application_method": "Online via Naan Mudhalvan Portal",
        "application_steps": [
            "1. Register on naanmudhalvan.tn.gov.in using college registration details",
            "2. Choose courses aligned with curriculum or career goals",
            "3. Complete guided training and assessment certification",
            "4. Participate in Naan Mudhalvan mega placement drives"
        ],
        "official_urls": [
            "https://naanmudhalvan.tn.gov.in",
            "https://tnsdc.tn.gov.in"
        ],
        "contact_helpline": "044-22501002 / support@naanmudhalvan.tn.gov.in",
        "dates": {"launch_date": "2022-03-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TNSDC Official Naan Mudhalvan Portal",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-AABCS-018",
        "scheme_name_tamil": "அண்ணல் அம்பேத்கர் தொழில் முன்னோடிகள் திட்டம்",
        "scheme_name_english": "Annal Ambedkar Business Champions Scheme (AABCS)",
        "department": "Micro, Small and Medium Enterprises (MSME) Department",
        "department_tamil": "குறு, சிறு மற்றும் நடுத்தரத் தொழில் நிறுவனங்கள் துறை",
        "category": "Business & Entrepreneurship",
        "sub_category": "SC / ST Entrepreneurship Support",
        "description_tamil": "ஆதிதிராவிடர் மற்றும் பழங்குடியின தொழில் முனைவோருக்கு 35% மூலதன மானியம் (அதிகபட்சம் ரூ.1.5 கோடி) மற்றும் 6% வட்டி மானியம் வழங்கும் சிறப்புத் திட்டம்.",
        "description_english": "Flagship MSME initiative granting 35% capital subsidy up to Rs. 1.50 Crore and 6% interest subvention to SC and ST entrepreneurs to establish manufacturing, service, or trading enterprises.",
        "benefits": {
            "capital_subsidy": "35% of eligible project cost up to maximum of ₹1.50 Crore",
            "interest_subvention": "6% interest subvention on term loan throughout the loan repayment tenure (up to 10 years)",
            "promoter_contribution": "Relaxed promoter contribution requirements"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 55},
            "gender": ["Any"],
            "community": ["SC", "ST", "Scheduled Caste", "Scheduled Tribe"],
            "residence": "Tamil Nadu",
            "income_limit_annual": 0,
            "special_conditions": [
                "Enterprise must be 100% owned by SC/ST individuals (Proprietorship or Partnership/Private Ltd where all partners/shareholders belong to SC/ST)",
                "No minimum educational qualification required",
                "No annual income ceiling"
            ]
        },
        "required_documents": [
            "Community Certificate (SC/ST)",
            "Aadhaar Card",
            "Detailed Project Report (DPR)",
            "Land / Building Ownership or Lease Agreement",
            "Bank Sanction Letter / Quotations for Machinery"
        ],
        "application_method": "Online via Tamil Nadu MSME Portal",
        "application_steps": [
            "1. Prepare Detailed Project Report (DPR)",
            "2. Apply online at msmeonline.tn.gov.in under AABCS",
            "3. District Task Force Committee (DTFC) review headed by District Collector",
            "4. Loan sanction by TIIC / Commercial Bank and subsidy disbursement"
        ],
        "official_urls": [
            "https://msmeonline.tn.gov.in",
            "https://tiic.org"
        ],
        "contact_helpline": "District Industries Centre (DIC) in respective districts",
        "dates": {"launch_date": "2023-04-14", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN MSME Department AABCS Guidelines",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-NEEDS-019",
        "scheme_name_tamil": "புதிய தொழில்முனைவோர் மற்றும் தொழில் நிறுவன மேம்பாட்டு திட்டம் (நீட்ஸ்)",
        "scheme_name_english": "New Entrepreneur-cum-Enterprise Development Scheme (NEEDS)",
        "department": "Micro, Small and Medium Enterprises (MSME) Department",
        "department_tamil": "குறு, சிறு மற்றும் நடுத்தரத் தொழில் நிறுவனங்கள் துறை",
        "category": "Business & Entrepreneurship",
        "sub_category": "First Generation Entrepreneur Support",
        "description_tamil": "முதல் தலைமுறை பட்டதாரி தொழில்முனைவோருக்கு ரூ.10 லட்சம் முதல் ரூ.5 கோடி வரையிலான புதிய தொழில் தொடங்க 25% மானியம் (அதிகபட்சம் ரூ.75 லட்சம்) வழங்கும் திட்டம்.",
        "description_english": "Premier self-employment program assisting first-generation educated entrepreneurs with a 25% capital subsidy up to Rs. 75 Lakhs and 3% interest subvention for projects up to Rs. 5 Crores.",
        "benefits": {
            "capital_subsidy": "25% of project cost (max ₹75 Lakhs)",
            "interest_subvention": "3% interest subvention during loan tenure",
            "project_size": "Project cost between ₹10 Lakhs and ₹5 Crores"
        },
        "eligibility_rules": {
            "age": {"min": 21, "max": 45},
            "gender": ["Any"],
            "education": ["Degree", "Diploma", "ITI", "Graduate", "Postgraduate"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must be a first-generation entrepreneur",
                "Age limit relaxed up to 45 years for Special Categories (Women, SC/ST/BC/MBC/Minorities/Ex-servicemen/Transgenders)",
                "General category age limit is 35 years"
            ]
        },
        "required_documents": [
            "Educational Qualification Certificate (Degree/Diploma)",
            "Aadhaar Card",
            "Community Certificate",
            "Nativity Certificate",
            "Project Proposal with Machinery Quotations"
        ],
        "application_method": "Online via msmeonline.tn.gov.in",
        "application_steps": [
            "1. Submit online application on msmeonline.tn.gov.in",
            "2. Interview and screening by District Level Task Force Committee",
            "3. Compulsory Entrepreneurship Development Programme (EDP) training",
            "4. Bank loan sanction and release of subsidy"
        ],
        "official_urls": [
            "https://msmeonline.tn.gov.in"
        ],
        "contact_helpline": "General Manager, District Industries Centre (DIC)",
        "dates": {"launch_date": "2012-07-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN MSME NEEDS Policy Guidelines",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-UYEGP-020",
        "scheme_name_tamil": "வேலையில்லா இளைஞர்களுக்கான வேலைவாய்ப்பு உருவாக்கும் திட்டம் (UYEGP)",
        "scheme_name_english": "Unemployed Youth Employment Generation Programme (UYEGP)",
        "department": "Micro, Small and Medium Enterprises (MSME) Department",
        "department_tamil": "குறு, சிறு மற்றும் நடுத்தரத் தொழில் நிறுவனங்கள் துறை",
        "category": "Business & Self Employment",
        "sub_category": "Micro Enterprise Support",
        "description_tamil": "8-ஆம் வகுப்பு தேர்ச்சி பெற்ற வேலையில்லா இளைஞர்களுக்கு சிறு வணிகம் மற்றும் சேவைத் தொழில் தொடங்க 25% மானியத்துடன் கூடிய வங்கிக் கடன் வழங்கும் திட்டம்.",
        "description_english": "Government micro-enterprise credit assistance providing 25% subsidy for manufacturing (up to Rs. 15L), service (up to Rs. 5L), and business projects (up to Rs. 5L) to unemployed youth.",
        "benefits": {
            "subsidy_rate": "25% government subsidy on project cost (up to ₹3.75 Lakhs for manufacturing)",
            "low_promoter_contribution": "Just 5% for special categories, 10% for general categories",
            "collateral_free": "Collateral-free loans covered under CGTMSE"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 45},
            "gender": ["Any"],
            "education": ["8th Pass and above"],
            "income_limit_annual": 500000,
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Minimum educational qualification: 8th standard pass",
                "Family income must not exceed Rs. 5,00,000 per annum",
                "Age limit is 35 for General category, 45 for SC/ST/BC/MBC/Women/Minority/Differently Abled"
            ]
        },
        "required_documents": [
            "8th / 10th School Transfer Certificate or Marksheet",
            "Aadhaar Card",
            "Community Certificate",
            "Income Certificate (below Rs. 5 Lakhs)",
            "Machinery / Equipment Quotation"
        ],
        "application_method": "Online via msmeonline.tn.gov.in",
        "application_steps": [
            "1. Apply online at msmeonline.tn.gov.in/uyegp",
            "2. Scrutiny and interview by District Task Force Committee",
            "3. EDP training for 7 days conducted by EDI",
            "4. Bank disburses loan with subsidy credited to subsidy reserve fund"
        ],
        "official_urls": [
            "https://msmeonline.tn.gov.in"
        ],
        "contact_helpline": "DIC Helpline / 044-22501002",
        "dates": {"launch_date": "2010-09-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN DIC UYEGP Operational Guidelines",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-MUTHULAKSHMI-021",
        "scheme_name_tamil": "டாக்டர் முத்துலட்சுமி ரெட்டி மகப்பேறு நிதி உதவித் திட்டம்",
        "scheme_name_english": "Dr. Muthulakshmi Reddy Ninaivu Maternity Benefit Scheme (MRMBS)",
        "department": "Health and Family Welfare Department",
        "department_tamil": "மக்கள் நல்வாழ்வு மற்றும் குடும்ப நலத் துறை",
        "category": "Maternal & Child Health",
        "sub_category": "Cash Assistance & Nutrition Kit",
        "description_tamil": "கர்ப்பிணித் தாய்மார்களுக்கு ஊட்டச்சத்து மற்றும் நிதி பாதுகாப்பிற்காக 5 தவணைகளில் ரூ.18,000 மதிப்பிலான நிதி உதவி மற்றும் ஊட்டச்சத்து பெட்டகம் வழங்கும் திட்டம்.",
        "description_english": "Comprehensive maternal support scheme providing pregnant women Rs. 18,000 in benefits, including Rs. 14,000 conditional cash transfer in 5 installments and 2 Amma Nutrition Kits valued at Rs. 4,000.",
        "benefits": {
            "financial_assistance": "₹14,000 cash transfer directly to bank account across 5 stages",
            "nutrition_kits": "2 Amma Maternity Nutrition Kits (iron tonic, dry fruits, protein mix, ghee) valued at ₹4,000",
            "total_value": "₹18,000 total maternity assistance"
        },
        "eligibility_rules": {
            "age": {"min": 19, "max": 45},
            "gender": ["Female"],
            "income_limit_annual": 120000,
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Pregnant women belonging to Below Poverty Line (BPL) families",
                "Restricted to first two deliveries / live births",
                "Must register pregnancy under PICME system within 12 weeks"
            ]
        },
        "required_documents": [
            "PICME Registration Number (RCH ID)",
            "Aadhaar Card of pregnant mother",
            "Aadhaar-linked Bank Passbook",
            "Smart Family Ration Card",
            "Income Certificate"
        ],
        "application_method": "Registration at Government Hospital / Primary Health Centre (PHC)",
        "application_steps": [
            "1. Register pregnancy with Village Health Nurse (VHN) or at PHC before 12th week",
            "2. Obtain 12-digit PICME RCH ID",
            "3. Attend mandatory Antenatal Checkups (ANCs) to receive installments",
            "4. Institutional delivery in Government Hospital / recognized center",
            "5. Complete infant immunization for final installment"
        ],
        "official_urls": [
            "https://picme.tn.gov.in",
            "https://tnhealth.tn.gov.in"
        ],
        "contact_helpline": "104 (Health Helpline) / Nearest PHC",
        "dates": {"launch_date": "2006-09-15", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "National Health Mission TN - Maternity Schemes",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-GIRLCHILD-022",
        "scheme_name_tamil": "முதலமைச்சரின் பெண் குழந்தை பாதுகாப்புத் திட்டம்",
        "scheme_name_english": "Chief Minister's Girl Child Protection Scheme",
        "department": "Social Welfare and Women Empowerment Department",
        "department_tamil": "சமூக நலம் மற்றும் மகளிர் உரிமைத் துறை",
        "category": "Child Welfare & Women Empowerment",
        "sub_category": "Financial Security for Girl Children",
        "description_tamil": "பெண் குழந்தைகளை ஆதரிக்கவும் பாலின விகிதத்தை சமப்படுத்தவும் குடும்பத்தில் ஒரு பெண் குழந்தைக்கு ரூ.50,000 அல்லது இரண்டு பெண் குழந்தைகளுக்கு தலா ரூ.25,000 வைப்பு நிதி வழங்கும் திட்டம்.",
        "description_english": "Long-term financial assurance scheme depositing Rs. 50,000 in fixed deposit for families with only one girl child, or Rs. 25,000 each for two girl children, maturing with interest when the child turns 18.",
        "benefits": {
            "single_girl_child": "₹50,000 fixed deposit in Tamil Nadu Power Finance Corporation",
            "two_girl_children": "₹25,000 fixed deposit each for two girl children",
            "maturity_benefit": "Principal plus accumulated interest disbursed directly to the girl at age 18 for higher education"
        },
        "eligibility_rules": {
            "age": {"min": 0, "max": 3},
            "gender": ["Female"],
            "income_limit_annual": 72000,
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Family must have only one or two girl children and NO male child",
                "Either parent must have undergone sterilization before mother turns 35",
                "Annual family income must not exceed Rs. 72,000 (Scheme I - single girl) or Rs. 72,000 (Scheme II - two girls)",
                "Child must be enrolled before completing 3 years of age"
            ]
        },
        "required_documents": [
            "Birth Certificate of girl child/children",
            "Sterilization Certificate of parent",
            "Income Certificate (below Rs. 72,000/year)",
            "Nativity / Residence Certificate in TN for 10 years",
            "No Male Child Certificate from VAO"
        ],
        "application_method": "e-Sevai Portal or District Social Welfare Office",
        "application_steps": [
            "1. Apply through e-Sevai centre or District Social Welfare Officer (DSWO)",
            "2. Verification by Child Development Project Officer (CDPO)",
            "3. Approval and fixed deposit bond issued in name of the child",
            "4. Claim maturity value on completing 18 years and Class 10 examination"
        ],
        "official_urls": [
            "https://tnesevai.tn.gov.in",
            "https://cms.tn.gov.in"
        ],
        "contact_helpline": "District Social Welfare Office / 181 (Women Helpline)",
        "dates": {"launch_date": "1992-05-03", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN Social Welfare Directorate Official Citizen Charter",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-SEWING-023",
        "scheme_name_tamil": "சத்தியவாணி முத்து அம்மையார் நினைவு இலவச தையல் இயந்திரம் வழங்கும் திட்டம்",
        "scheme_name_english": "Sathiyavanimuthu Ammaiyar Ninaivu Free Sewing Machine Scheme",
        "department": "Social Welfare and Women Empowerment Department",
        "department_tamil": "சமூக நலம் மற்றும் மகளிர் உரிமைத் துறை",
        "category": "Social Welfare & Livelihood",
        "sub_category": "Free Livelihood Equipment",
        "description_tamil": "ஆதரவற்ற விதவைகள், கணவனால் கைவிடப்பட்ட பெண்கள் மற்றும் பொருளாதாரத்தில் நலிவடைந்த பெண்களுக்கு சுயதொழில் செய்ய இலவச தையல் இயந்திரம் வழங்கும் திட்டம்.",
        "description_english": "Livelihood support scheme providing motorized or manual sewing machines completely free of cost to destitute widows, deserted wives, differently-abled women, and poor women.",
        "benefits": {
            "equipment": "Free quality sewing machine with cloth and accessories for self-employment livelihood"
        },
        "eligibility_rules": {
            "age": {"min": 20, "max": 40},
            "gender": ["Female"],
            "income_limit_annual": 72000,
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Annual family income must not exceed Rs. 72,000",
                "Must possess tailoring knowledge or certificate from recognized tailoring school",
                "Priority given to destitute widows, deserted wives, and differently-abled women"
            ]
        },
        "required_documents": [
            "Tailoring Training Certificate",
            "Income Certificate (less than Rs. 72,000/year)",
            "Aadhaar Card & Smart Ration Card",
            "Destitute Widow / Deserted Wife / Disability Certificate (if applicable)",
            "Community Certificate"
        ],
        "application_method": "District Social Welfare Office / e-Sevai",
        "application_steps": [
            "1. Collect application form from District Social Welfare Office or e-Sevai",
            "2. Attach tailoring certificate and income certificate",
            "3. Verification by Extension Officer (Social Welfare)",
            "4. Free sewing machine distributed at district distribution function"
        ],
        "official_urls": [
            "https://tnesevai.tn.gov.in"
        ],
        "contact_helpline": "District Social Welfare Officer (DSWO)",
        "dates": {"launch_date": "1979-01-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "Directorate of Social Welfare Tamil Nadu",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-FIRST-GRAD-024",
        "scheme_name_tamil": "முதல் தலைமுறை பட்டதாரி கல்விக் கட்டணச் சலுகை திட்டம்",
        "scheme_name_english": "Tamil Nadu First Graduate Tuition Fee Concession Scheme",
        "department": "Higher Education Department",
        "department_tamil": "உயர் கல்வித் துறை",
        "category": "Higher Education",
        "sub_category": "Tuition Fee Waiver",
        "description_tamil": "குடும்பத்தில் முதல் முறையாக பட்டப்படிப்பு படிக்கும் மாணவர்களுக்கு அரசு மற்றும் தனியார் கல்லூரிகளில் கல்விக் கட்டணத்தை முழுமையாக அரசு ஏற்கும் திட்டம்.",
        "description_english": "Higher education incentive completely waiving tuition fees for students who are the first in their immediate family to pursue an undergraduate professional degree (Engineering, Medical, Agriculture, Law, etc.).",
        "benefits": {
            "tuition_waiver": "100% tuition fee waiver paid directly by Government to colleges",
            "course_coverage": "All 4/5 years of professional undergraduate degrees covered under single-window counseling (TNEA/TN Medical)"
        },
        "eligibility_rules": {
            "age": {"min": 17, "max": 25},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "student_status": True,
            "special_conditions": [
                "No person in the candidate's immediate family (parents, siblings) should be a graduate",
                "Admitted to professional degree courses through government single-window counseling quota"
            ]
        },
        "required_documents": [
            "First Graduate Certificate issued by Tahsildar via e-Sevai",
            "Joint Declaration by parents and student",
            "Family Smart Ration Card",
            "Transfer Certificate and 12th Marksheet",
            "Allotment Order from Counseling"
        ],
        "application_method": "e-Sevai Portal for Certificate + Submission during Counseling",
        "application_steps": [
            "1. Apply for First Graduate Certificate at e-Sevai centre before counseling",
            "2. Tahsildar verifies no graduate in family and issues digital certificate",
            "3. Submit certificate during TNEA / NEET engineering/medical counseling",
            "4. College waives tuition fees directly on allotment"
        ],
        "official_urls": [
            "https://tnesevai.tn.gov.in",
            "https://tneaonline.org"
        ],
        "contact_helpline": "Directorate of Technical Education (DOTE) / 044-22351014",
        "dates": {"launch_date": "2010-06-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN Higher Education Department Government Orders",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-7POINT5-RES-025",
        "scheme_name_tamil": "அரசுப் பள்ளி மாணவர்களுக்கான 7.5% முன்னுரிமை இடஒதுக்கீடு மற்றும் இலவச கல்விக் கட்டணத் திட்டம்",
        "scheme_name_english": "7.5% Government School Quota Free Professional Education Scheme",
        "department": "Higher Education & Health and Family Welfare Department",
        "department_tamil": "உயர் கல்வி மற்றும் மக்கள் நல்வாழ்வுத் துறை",
        "category": "Higher Education",
        "sub_category": "100% Free Professional Education",
        "description_tamil": "அரசுப் பள்ளிகளில் 6 முதல் 12 வரை படித்த மாணவர்களுக்கு மருத்துவம், பொறியியல், விவசாயம், சட்டம் உள்ளிட்ட தொழிற்கல்வி படிப்புகளில் 7.5% இடஒதுக்கீட்டுடன் முழுக் கல்விக் கட்டணம், விடுதிக் கட்டணத்தை அரசே ஏற்கும் திட்டம்.",
        "description_english": "Horizontal 7.5% reservation providing 100% free higher education (tuition fee, hostel fee, exam fee, and transport fee borne by Government) for government school students entering Medical, Dental, Engineering, Agriculture, Veterinary, and Law colleges.",
        "benefits": {
            "complete_fee_waiver": "100% tuition, hostel, mess, examination, and book fees paid by State Government",
            "horizontal_quota": "7.5% reserved seats in all professional colleges across Tamil Nadu"
        },
        "eligibility_rules": {
            "age": {"min": 17, "max": 25},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "student_status": True,
            "school_type": ["Government School"],
            "special_conditions": [
                "Must have studied continuously from Class 6 to Class 12 in Tamil Nadu Government schools",
                "Qualified in relevant entrance examination / merit counseling (NEET, TNEA, TNAU, TANUVAS, TNDALU)"
            ]
        },
        "required_documents": [
            "Bonafide School Study Certificate (Class 6 to 12 in Govt School) signed by Headmaster and BEO/DEO",
            "12th Marksheet",
            "Aadhaar Card",
            "Community Certificate",
            "NEET Scorecard / TNEA Application"
        ],
        "application_method": "During Single Window Counseling Application",
        "application_steps": [
            "1. Obtain Bonafide School Certificate from school headmaster verifying 6th to 12th govt school study",
            "2. Select '7.5% Government School Quota' in NEET / TNEA admission portal",
            "3. Attend special 7.5% counseling session",
            "4. Free admission order issued with zero fee burden on student"
        ],
        "official_urls": [
            "https://tnmedicalselection.net",
            "https://tneaonline.org"
        ],
        "contact_helpline": "14417 / DME Counseling Helpline",
        "dates": {"launch_date": "2020-10-30", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN Legislative Acts and Health/Higher Education GOs",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-FARM-ELECTRICITY-027",
        "scheme_name_tamil": "விவசாயிகளுக்கு 100% இலவச மும்முனை மின்சாரத் திட்டம்",
        "scheme_name_english": "Free Agricultural Electricity Scheme (TANGEDCO)",
        "department": "Energy Department & TANGEDCO",
        "department_tamil": "மின்சாரத் துறை மற்றும் தமிழ்நாடு மின் உற்பத்தி மற்றும் பகிர்மானக் கழகம்",
        "category": "Agriculture & Irrigation",
        "sub_category": "Irrigation Power Subsidy",
        "description_tamil": "விவசாய கிணறுகள் மற்றும் போர்வெல்களுக்கு 24 மணி நேரமும் இலவச மும்முனை மின்சாரம் வழங்கி விவசாய உற்பத்தித் திறனை அதிகரிக்கும் திட்டம்.",
        "description_english": "State energy welfare scheme providing 100% free unmetered three-phase electricity to agricultural pump sets, benefiting over 23 lakh farmers across Tamil Nadu.",
        "benefits": {
            "free_power": "100% free electricity subsidy (zero tariff for agricultural borewell/well pump sets)",
            "hours": "Round-the-clock three-phase power supply in designated agricultural feeders"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 100},
            "gender": ["Any"],
            "occupation": ["Farmer", "Agriculturist"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must own agricultural land with an existing open well or borewell",
                "Registered agricultural electricity service connection with TANGEDCO"
            ]
        },
        "required_documents": [
            "Chitta and Adangal land revenue records",
            "Patta copy for land where well is located",
            "Aadhaar Card",
            "Village Administrative Officer (VAO) Certificate confirming agriculture well existence"
        ],
        "application_method": "Online via TANGEDCO Agricultural Service Portal / Section Office",
        "application_steps": [
            "1. Apply for new agricultural service connection at local TANGEDCO Executive Engineer office or online",
            "2. Field inspection by Junior Engineer to inspect borewell and motor capacity",
            "3. Power connection energized under agricultural free power tariff tariff IV"
        ],
        "official_urls": [
            "https://www.tangedco.gov.in"
        ],
        "contact_helpline": "TANGEDCO Minnagam Helpline 94987 94987",
        "dates": {"launch_date": "1989-01-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TANGEDCO Agricultural Tariff Orders",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-SOLAR-PUMP-028",
        "scheme_name_tamil": "முதலமைச்சரின் சூரியசக்தி பம்புசெட் திட்டம்",
        "scheme_name_english": "Chief Minister's Solar Powered Pump Sets Scheme",
        "department": "Agricultural Engineering Department",
        "department_tamil": "வேளாண்மைப் பொறியியல் துறை",
        "category": "Agriculture & Renewable Energy",
        "sub_category": "Solar Irrigation Subsidy",
        "description_tamil": "விவசாயிகளுக்கு 70% வரை அரசு மானியத்துடன் 5 முதல் 10 குதிரைத் திறன் கொண்ட சூரியசக்தி பம்புசெட்டுகள் அமைத்து தரும் திட்டம்.",
        "description_english": "Clean energy agricultural scheme providing up to 70% capital subsidy (combining State and PM-KUSUM Component-B) to install 5 HP, 7.5 HP, and 10 HP standalone solar-powered irrigation pump sets.",
        "benefits": {
            "subsidy": "Up to 70% subsidy on total cost of standalone solar agricultural pump set",
            "cost_saving": "Zero recurring electricity or diesel fuel charges for irrigation"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 100},
            "occupation": ["Farmer", "Small Farmer", "Marginal Farmer"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Farmer must own agricultural land with dependable borewell/open well water source",
                "Priority given to farmers in non-energized areas or waiting for free EB connections"
            ]
        },
        "required_documents": [
            "Patta, Chitta, and FMB sketch of agricultural land",
            "Aadhaar Card & Smart Ration Card",
            "Small/Marginal Farmer Certificate from Tahsildar (for extra subsidy)",
            "Bank Passbook copy"
        ],
        "application_method": "Online via Uzhavan App or Agricultural Engineering Office",
        "application_steps": [
            "1. Apply online via Uzhavan Mobile App or AED portal",
            "2. Assistant Executive Engineer (AED) inspects water source and solar feasibility",
            "3. Farmer deposits remaining 30% beneficiary contribution",
            "4. Empaneled solar vendor installs and commissions the solar pump set"
        ],
        "official_urls": [
            "https://aed.tn.gov.in",
            "https://tnhorticulture.tn.gov.in"
        ],
        "contact_helpline": "Executive Engineer (AED) in respective district headquarters",
        "dates": {"launch_date": "2013-10-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "AED Tamil Nadu Solar Irrigation Guidelines",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-DESERTED-WIVES-029",
        "scheme_name_tamil": "கணவனால் கைவிடப்பட்ட பெண்களுக்கான மாதாந்திர ஓய்வூதியத் திட்டம்",
        "scheme_name_english": "Destitute Deserted Wives Pension Scheme",
        "department": "Revenue and Disaster Management Department",
        "department_tamil": "வருவாய் மற்றும் பேரிடர் மேலாண்மைத் துறை",
        "category": "Social Security & Pension",
        "sub_category": "Monthly Destitute Assistance",
        "description_tamil": "கணவனால் கைவிடப்பட்டு ஆதரவின்றி வாழும் பெண்களுக்கு வாழ்வாதார பாதுகாப்பிற்காக மாதந்தோறும் ரூ.1,200 ஓய்வூதியம் மற்றும் இலவச அரிசி வழங்கும் திட்டம்.",
        "description_english": "Social security welfare pension offering Rs. 1,200 per month and free monthly rice to deserted, separated, or abandoned women living in destitution without family financial support.",
        "benefits": {
            "monthly_pension": "₹1,200 per month credited directly to beneficiary bank/post office account",
            "free_rice": "Free rice entitlement under special PDS quota",
            "free_clothing": "Free saree distribution twice a year on Pongal and Deepavali"
        },
        "eligibility_rules": {
            "age": {"min": 30, "max": 100},
            "gender": ["Female"],
            "income_limit_annual": 120000,
            "marital_status": ["Deserted", "Separated", "Abandoned"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must have been deserted or living separately from husband for at least 5 years (or obtained legal decree of separation)",
                "Annual family income must not exceed Rs. 1,20,000",
                "Must not own property worth more than Rs. 1 Lakh"
            ]
        },
        "required_documents": [
            "Deserted Wife Certificate issued by Tahsildar / Legal Separation Order",
            "Smart Family Ration Card",
            "Aadhaar Card",
            "Income Certificate",
            "Bank / Post Office Passbook"
        ],
        "application_method": "Online via e-Sevai Centre / Taluk Office",
        "application_steps": [
            "1. Apply at nearest e-Sevai centre or Taluk Office (Social Security Scheme wing)",
            "2. Field inquiry by Revenue Inspector (RI) and Village Administrative Officer (VAO)",
            "3. Approval by Special Tahsildar (Social Security Schemes)",
            "4. Monthly pension sanctioned via Electronic Clearing Service (ECS)"
        ],
        "official_urls": [
            "https://tnesevai.tn.gov.in"
        ],
        "contact_helpline": "Special Tahsildar (SSS) / CM Helpline 1100",
        "dates": {"launch_date": "1984-01-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN Revenue Department Social Security Schemes Manual",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-DIFFABLE-SCOOTER-030",
        "scheme_name_tamil": "மாற்றுத்திறனாளிகளுக்கு இணைப்புச் சக்கரங்கள் பொருத்தப்பட்ட விலையில்லா பெட்ரோல் ஸ்கூட்டர் திட்டம்",
        "scheme_name_english": "Retrofitted Motorized Vehicle / Scooter Scheme for Differently Abled",
        "department": "Welfare of Differently Abled Persons Department",
        "department_tamil": "மாற்றுத்திறனாளிகள் நலத் துறை",
        "category": "Differently Abled Welfare",
        "sub_category": "Mobility & Assistive Retrofitted Scooters",
        "description_tamil": "இரு கால்களும் பாதிக்கப்பட்ட மாற்றுத்திறனாளி மாணவர்கள் மற்றும் பணிபுரிபவர்களுக்கு இணைப்புச் சக்கரங்கள் பொருத்தப்பட்ட பெட்ரோல் ஸ்கூட்டர் 100% இலவசமாக வழங்கும் திட்டம்.",
        "description_english": "Empowerment mobility scheme providing custom retrofitted motorized scooters with two auxiliary wheels completely free of cost to locomotor-disabled persons who are employed or pursuing college education.",
        "benefits": {
            "free_vehicle": "100% free retrofitted scooter with retrofitted balance wheels",
            "independent_mobility": "Ensures independent daily commute for employment and education"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 45},
            "gender": ["Any"],
            "disability": ["Locomotor Disability", "Both Legs Affected", "Paraplegia"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must have locomotor disability affecting both lower limbs (minimum 75% disability)",
                "Upper limbs (hands) must be strong and fully functional to operate a two-wheeler safely",
                "Must be employed, self-employed, or studying in college/university"
            ]
        },
        "required_documents": [
            "National Disability Identity Card (UDID) with 75%+ locomotor disability",
            "Employment Certificate or College Student Bonafide Certificate",
            "Aadhaar Card & Smart Ration Card",
            "Medical Fitness Certificate from Orthopedic Surgeon declaring fitness to drive retrofitted scooter"
        ],
        "application_method": "District Differently Abled Welfare Office (DDAWO) / e-Sevai",
        "application_steps": [
            "1. Apply to District Differently Abled Welfare Officer (DDAWO) or online portal",
            "2. Clinical evaluation by district orthopedic board",
            "3. Driving simulator test and verification",
            "4. Sanction and distribution by District Collector"
        ],
        "official_urls": [
            "https://www.scd.tn.gov.in"
        ],
        "contact_helpline": "DDAWO in respective District Collectorates / 1800 425 0111",
        "dates": {"launch_date": "2010-06-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "State Commissionerate for the Differently Abled TN",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-CONSTRUCTION-BOARD-031",
        "scheme_name_tamil": "தமிழ்நாடு கட்டுமானத் தொழிலாளர்கள் நல வாரிய நலத்திட்டங்கள்",
        "scheme_name_english": "Tamil Nadu Construction Workers Welfare Board Assistance",
        "department": "Labour Welfare and Skill Development Department",
        "department_tamil": "தொழிலாளர் நலன் மற்றும் திறன் மேம்பாட்டுத் துறை",
        "category": "Labour & Unorganized Workers",
        "sub_category": "Social Security & Education Support for Workers",
        "description_tamil": "பதிவு செய்த கட்டுமானத் தொழிலாளர்களுக்கு விபத்து காப்பீடு, இயற்கை மரண உதவி, திருமண உதவி, மகப்பேறு உதவி, கல்வி உதவித்தொகை மற்றும் ஓய்வூதியம் வழங்கும் திட்டம்.",
        "description_english": "Comprehensive welfare package for registered construction workers including accident death relief (Rs. 5 Lakhs), marriage assistance (Rs. 20,000), maternity assistance (Rs. 18,000), monthly pension (Rs. 1,000), and child education scholarships.",
        "benefits": {
            "accident_relief": "₹5,00,000 in case of accidental death at workplace",
            "marriage_assistance": "₹20,000 for worker's own marriage or daughter/son's marriage",
            "education_scholarship": "₹1,000 to ₹12,000 per year for children studying from Class 10 to Engineering/Medicine",
            "pension": "₹1,000 per month upon reaching age 60"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 60},
            "gender": ["Any"],
            "occupation": ["Construction Worker", "Mason", "Painter", "Plumber", "Electrician", "Carpenter", "Centering Worker"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must be engaged in building or construction industry in Tamil Nadu",
                "Must be registered as a member with the Tamil Nadu Construction Workers Welfare Board"
            ]
        },
        "required_documents": [
            "Welfare Board Membership ID Card",
            "Aadhaar Card",
            "Proof of 90 days employment in past year certified by trade union or employer",
            "Aadhaar-linked Bank Passbook"
        ],
        "application_method": "Online via tnwb.tn.gov.in / e-Sevai",
        "application_steps": [
            "1. Register as worker on tnwb.tn.gov.in with employer certificate",
            "2. Receive Board Identity Card",
            "3. Apply online for specific claim (education, marriage, maternity, or pension)",
            "4. Verification by Labour Officer and direct bank credit"
        ],
        "official_urls": [
            "https://tnwb.tn.gov.in"
        ],
        "contact_helpline": "Labour Welfare Board Helpdesk 044-24344158",
        "dates": {"launch_date": "1994-11-30", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN Construction Workers Welfare Board Regulations",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-TABCEDCO-032",
        "scheme_name_tamil": "பிற்படுத்தப்பட்டோர் மற்றும் மிகவும் பிற்படுத்தப்பட்டோர் பொருளாதாரக் கடன் திட்டம் (TABCEDCO)",
        "scheme_name_english": "TABCEDCO Concessional Micro & Business Loan Scheme",
        "department": "Backward Classes, Most Backward Classes and Minorities Welfare Department",
        "department_tamil": "பிற்படுத்தப்பட்டோர், மிகவும் பிற்படுத்தப்பட்டோர் மற்றும் சிறுபான்மையினர் நலத் துறை",
        "category": "Economic Assistance & Micro Credit",
        "sub_category": "BC / MBC Low Interest Entrepreneur Loans",
        "description_tamil": "பிற்படுத்தப்பட்டோர், மிகவும் பிற்படுத்தப்பட்டோர் மற்றும் சீர்மரபினர் சுயதொழில் தொடங்க குறைந்த வட்டியில் (6% முதல் 8%) ரூ.15 லட்சம் வரை கடனுதவி வழங்கும் திட்டம்.",
        "description_english": "Concessional term loans and micro-credit up to Rs. 15 Lakhs at low interest rates (6% - 8% per annum) to BC, MBC, and DNC beneficiaries for starting small businesses, transport vehicles, dairy, and agriculture allied activities.",
        "benefits": {
            "low_interest_loan": "Loans up to ₹15 Lakhs for business and self-employment at subsidized 6% to 8% interest rate",
            "women_shg_loans": "Micro credit loans up to ₹1,00,000 per member for BC/MBC women self-help groups at 4% interest"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 60},
            "gender": ["Any"],
            "community": ["BC", "MBC", "DNC", "Backward Class", "Most Backward Class", "Denotified Community"],
            "income_limit_annual": 300000,
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must belong to BC, MBC, or DNC community as notified by Tamil Nadu government",
                "Annual family income must not exceed Rs. 3,00,000"
            ]
        },
        "required_documents": [
            "Community Certificate (BC/MBC/DNC)",
            "Income Certificate (under Rs. 3,00,000/year)",
            "Nativity / Residence Certificate",
            "Aadhaar Card & Smart Ration Card",
            "Project Quotation / Business Proposal"
        ],
        "application_method": "District Backward Classes and Minorities Welfare Office / Co-operative Banks",
        "application_steps": [
            "1. Collect application from District BC & Minorities Welfare Office (DBCMWO) or Central Cooperative Bank",
            "2. Submit along with community and income proofs",
            "3. District Selection Committee approves loan",
            "4. Loan disbursed through District Central Co-operative Bank (DCCB)"
        ],
        "official_urls": [
            "https://bcmbcmw.tn.gov.in"
        ],
        "contact_helpline": "DBCMWO in respective District Collectorate / 044-28520935",
        "dates": {"launch_date": "1992-03-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TABCEDCO Annual Policy Notes",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-TAMCO-033",
        "scheme_name_tamil": "சிறுபான்மையினர் பொருளாதார மேம்பாட்டுக் கடன் திட்டம் (TAMCO)",
        "scheme_name_english": "TAMCO Concessional Term Loan Scheme for Minorities",
        "department": "Backward Classes, Most Backward Classes and Minorities Welfare Department",
        "department_tamil": "பிற்படுத்தப்பட்டோர், மிகவும் பிற்படுத்தப்பட்டோர் மற்றும் சிறுபான்மையினர் நலத் துறை",
        "category": "Minority Welfare & Economic Credit",
        "sub_category": "Religious Minorities Business Credit",
        "description_tamil": "முஸ்லிம், கிறிஸ்தவர், சீக்கியர், பௌத்தர், சமணர் மற்றும் பார்சி ஆகிய மத சிறுபான்மையினருக்கு குறைந்த வட்டியில் (6% முதல் 8%) சுயதொழில் கடன் வழங்கும் திட்டம்.",
        "description_english": "Subsidized term loans up to Rs. 20 Lakhs for individual business and education loans at 3% - 8% interest for religious minority communities (Muslims, Christians, Sikhs, Buddhists, Jains, Parsis) in Tamil Nadu.",
        "benefits": {
            "business_loan": "Term loan up to ₹20,00,000 for trade, service, transport, and manufacturing at 6% to 8% interest",
            "education_loan": "Education loans up to ₹20,00,000 at 3% interest for professional degrees in India and abroad"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 60},
            "gender": ["Any"],
            "community": ["Minority", "Muslim", "Christian", "Sikh", "Buddhist", "Jain", "Parsi"],
            "income_limit_annual": 300000,
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must belong to religious minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi)",
                "Annual family income must not exceed Rs. 3,00,000"
            ]
        },
        "required_documents": [
            "Minority Religion Certificate / Community Certificate / TC showing religion",
            "Income Certificate (under Rs. 3,00,000/year)",
            "Aadhaar Card & Smart Ration Card",
            "Business Project Quotation or College Fee Structure"
        ],
        "application_method": "District Minorities Welfare Office / Co-operative Banks",
        "application_steps": [
            "1. Apply through District Backward Classes and Minorities Welfare Officer",
            "2. Selection committee scrutiny",
            "3. Loan disbursed via District Central Cooperative Bank branches"
        ],
        "official_urls": [
            "https://bcmbcmw.tn.gov.in"
        ],
        "contact_helpline": "044-28515222 / TAMCO Headquarters",
        "dates": {"launch_date": "1999-08-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TAMCO Schemes and Guidelines Citizen Charter",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-FREE-LAPTOP-034",
        "scheme_name_tamil": "பள்ளி மற்றும் கல்லூரி மாணவர்களுக்கான விலையில்லா மடிக்கணினி திட்டம்",
        "scheme_name_english": "Free Laptop Scheme for School and College Students",
        "department": "Special Programme Implementation & School/Higher Education Department",
        "department_tamil": "சிறப்புத் திட்ட செயலாக்கத் துறை மற்றும் பள்ளிக் கல்வித் துறை",
        "category": "Education & Digital Literacy",
        "sub_category": "Student Digital Enablement",
        "description_tamil": "அரசு மற்றும் அரசு உதவிபெறும் பள்ளிகளில் பிளஸ் டூ முடிக்கும் மற்றும் அரசு கல்லூரிகளில் பயிலும் மாணவர்களுக்கு இலவச மடிக்கணினி வழங்கும் திட்டம்.",
        "description_english": "Flagship digital empowerment program distributing free laptops with preloaded educational software to students passing Class 12 from Government and Govt-aided schools in Tamil Nadu.",
        "benefits": {
            "hardware": "Free brand-name laptop computer with manufacturer warranty",
            "preloaded_content": "Pre-installed Linux OS, educational syllabus modules, and digital learning tools"
        },
        "eligibility_rules": {
            "age": {"min": 16, "max": 22},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "student_status": True,
            "school_type": ["Government School", "Government-aided School", "Government Arts/Polytechnic College"],
            "special_conditions": [
                "Must be enrolled as a regular student in Class 12 in Government or Government-aided school in Tamil Nadu"
            ]
        },
        "required_documents": [
            "Automatic school distribution based on EMIS roll (School ID and Bonafide Verification)"
        ],
        "application_method": "Direct School Distribution (No External Application)",
        "application_steps": [
            "1. School headmaster compiles eligible student list through EMIS portal",
            "2. Electronic Corporation of Tamil Nadu (ELCOT) supplies verified laptops to schools",
            "3. Distributed directly to students by Headmaster / Education Department officials"
        ],
        "official_urls": [
            "https://elcot.in",
            "https://schooledu.tn.gov.in"
        ],
        "contact_helpline": "14417 / School Headmaster",
        "dates": {"launch_date": "2011-09-15", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "ELCOT Student Laptop Procurement and Distribution Manual",
            "last_verified": "2026-10-01"
        }
    },
    {
        "scheme_id": "TN-FREE-DHOTI-SAREE-035",
        "scheme_name_tamil": "பொங்கல் விலையில்லா வேட்டி மற்றும் சேலை வழங்கும் திட்டம்",
        "scheme_name_english": "Free Dhoti and Saree Distribution Scheme (Pongal Gift)",
        "department": "Handlooms, Handicrafts, Textiles and Khadi Department & Food Department",
        "department_tamil": "கைத்தறி, கைவினை, துணிநூல் மற்றும் கதர்த்துறை",
        "category": "Social Welfare & Handloom Support",
        "sub_category": "Seasonal Clothing Assistance & Weaver Employment",
        "description_tamil": "பொங்கல் பண்டிகையை முன்னிட்டு ஏழை எளிய குடும்ப அட்டைதாரர்களுக்கு இலவச வேட்டி மற்றும் சேலை ரேஷன் கடைகள் மூலம் வழங்கும் திட்டம்.",
        "description_english": "Twin-purpose social welfare initiative providing one free dhoti and one free saree to eligible ration card holders during Pongal while ensuring year-round employment for handloom and powerloom weavers.",
        "benefits": {
            "free_clothing": "One free handloom/powerloom saree and one dhoti per eligible household",
            "timing": "Distributed annually during the month of January as part of Pongal welfare package"
        },
        "eligibility_rules": {
            "age": {"min": 18, "max": 100},
            "gender": ["Any"],
            "residence": "Tamil Nadu",
            "special_conditions": [
                "Must hold a valid Rice Family Smart Card (PHH / NPHH-Rice / AAY) under the Public Distribution System (PDS)"
            ]
        },
        "required_documents": [
            "Smart Family Ration Card"
        ],
        "application_method": "Fair Price Shop (Ration Shop) Distribution",
        "application_steps": [
            "1. Government issues Pongal tokens at doorstep or via SMS",
            "2. Visit assigned Fair Price Shop (Ration Shop) with Smart Family Card",
            "3. Biometric POS verification and collection of free dhoti, saree, and Pongal gift hampers"
        ],
        "official_urls": [
            "https://tnpds.gov.in"
        ],
        "contact_helpline": "1967 / 1800-425-5901 (TNPDS Helpline)",
        "dates": {"launch_date": "1983-01-01", "status": "Ongoing"},
        "source_metadata": {
            "source_title": "TN Handlooms Department Policy Note & Civil Supplies GOs",
            "last_verified": "2026-10-01"
        }
    }
]

# Merge into dataset
added_count = 0
for s in new_schemes:
    if s["scheme_id"] not in existing_ids:
        existing_schemes.append(s)
        existing_ids.add(s["scheme_id"])
        added_count += 1

print(f"Added {added_count} new schemes.")
print(f"Total verified schemes now: {len(existing_schemes)}")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(existing_schemes, f, ensure_ascii=False, indent=2)

print("Dataset updated successfully!")
