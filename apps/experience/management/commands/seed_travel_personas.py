from django.conf import settings
from django.core.management.base import BaseCommand

from apps.experience.models import (
    AgeGroup,
    AnswerOption,
    AnswerPersonaWeight,
    CompanionTrait,
    Persona,
    PersonaAvatar,
    Question,
    QuestionnaireVersion,
)

PERSONA_SLUGS = [
    "heritage_hunter",
    "beach_lover",
    "adventure_seeker",
    "nature_explorer",
    "urban_explorer",
    "culture_connector",
]

PERSONAS = {
    "heritage_hunter": {
        "name": "Heritage Hunter",
        "sort_order": 1,
        "tie_break_order": 1,
        "tagline_bn": "ইতিহাসের সন্ধানে",
        "tagline_en": "In search of history",
        "short_description_bn": "পুরোনো প্রাসাদ, ঐতিহাসিক স্থাপনা আর গল্পে ভরা জায়গায় ঘুরতে ভালোবাসেন আপনি।",
        "short_description_en": "You love palaces, monuments and places full of stories from the past.",
        "description_bn": "প্রাচীন স্থাপত্য, জাদুঘর, পুরোনো শহর আর অতীতের গল্পে ডুবে থাকা আপনার সবচেয়ে প্রিয়। প্রতিটি পাথরে আপনি খুঁজে পান ইতিহাসের ছোঁয়া।",
        "description_en": "Ancient architecture, museums, old cities and stories of the past fascinate you most. You find history in every stone.",
        "keywords_bn": "ইতিহাস • ঐতিহ্য • স্থাপত্য • আবিষ্কার",
        "keywords_en": "History • Heritage • Architecture • Discovery",
    },
    "beach_lover": {
        "name": "Beach Lover",
        "sort_order": 2,
        "tie_break_order": 5,
        "tagline_bn": "সাগরের ছোঁয়ায়",
        "tagline_en": "By the sea",
        "short_description_bn": "সমুদ্র, সূর্যাস্ত আর একদম রিল্যাক্স ছুটির দিনই আপনার স্বপ্ন।",
        "short_description_en": "Beaches, sunsets and perfectly relaxed holidays are your dream.",
        "description_bn": "নীল সমুদ্র, বালির সৈকত আর শান্ত পরিবেশ—আপনার ছুটি মানেই আরাম। ঢেউয়ের শব্দে আপনি খুঁজে পান মনের শান্তি।",
        "description_en": "Blue seas, sandy shores and calm surroundings — your vacation means relaxation. The sound of waves brings you peace.",
        "keywords_bn": "সমুদ্র • সূর্যাস্ত • রিল্যাক্স • রিসোর্ট",
        "keywords_en": "Sea • Sunset • Relax • Resort",
    },
    "adventure_seeker": {
        "name": "Adventure Seeker",
        "sort_order": 3,
        "tie_break_order": 4,
        "tagline_bn": "রোমাঞ্চই জীবন",
        "tagline_en": "Thrill is life",
        "short_description_bn": "ট্রেকিং, ক্যাম্পিং আর রোমাঞ্চকর অভিজ্ঞতা আপনার শক্তি।",
        "short_description_en": "Trekking, camping and thrilling experiences give you energy.",
        "description_bn": "নতুন চ্যালেঞ্জ আর অ্যাড্রেনালিন আপনাকে বাঁচিয়ে রাখে। পাহাড়ে ট্রেকিং, নদীতে কায়াকিং—সাহসিকতায় ভরা প্রতিটি মুহূর্ত আপনার পছন্দ।",
        "description_en": "New challenges and adrenaline keep you alive. Trekking, kayaking — you love every moment filled with courage.",
        "keywords_bn": "ট্রেকিং • ক্যাম্পিং • কায়াকিং • রোমাঞ্চ",
        "keywords_en": "Trekking • Camping • Kayaking • Thrill",
    },
    "nature_explorer": {
        "name": "Nature Explorer",
        "sort_order": 4,
        "tie_break_order": 2,
        "tagline_bn": "প্রকৃতির মাঝে",
        "tagline_en": "Into the wild",
        "short_description_bn": "পাহাড়, বন আর শান্ত প্রকৃতির মাঝে আপনি খুঁজে পান প্রশান্তি।",
        "short_description_en": "Mountains, forests and quiet nature bring you peace.",
        "description_bn": "সবুজ পাহাড়, গভীর বন আর নৈসর্গিক দৃশ্য আপনার প্রাণের আরাম। প্রকৃতির সৌন্দর্যে মগ্ন থাকতেই আপনি সবচেয়ে বেশি ভালোবাসেন।",
        "description_en": "Green hills, deep forests and scenic views soothe your soul. Immersing yourself in natural beauty is what you love most.",
        "keywords_bn": "পাহাড় • বন • বন্যপ্রাণী • প্রশান্তি",
        "keywords_en": "Mountains • Forest • Wildlife • Serenity",
    },
    "urban_explorer": {
        "name": "Urban Explorer",
        "sort_order": 5,
        "tie_break_order": 6,
        "tagline_bn": "শহরের গতিতে",
        "tagline_en": "At city pace",
        "short_description_bn": "জমজমাট শহর, ক্যাফে আর আধুনিক জীবনই আপনার পছন্দ।",
        "short_description_en": "Lively cities, cafés and modern life are your thing.",
        "description_bn": "উঁচু ভবন, নিয়ন আলো, শপিং আর নাইটলাইফ—শহরের এনার্জি আপনাকে টানে। নতুন ক্যাফে আর ফ্যাশনেবল জায়গায় ঘোরা আপনার আনন্দ।",
        "description_en": "Skylines, neon lights, shopping and nightlife — city energy attracts you. Exploring new cafés and stylish spots is your joy.",
        "keywords_bn": "শহর • ক্যাফে • শপিং • নাইটলাইফ",
        "keywords_en": "City • Café • Shopping • Nightlife",
    },
    "culture_connector": {
        "name": "Culture Connector",
        "sort_order": 6,
        "tie_break_order": 3,
        "tagline_bn": "সংস্কৃতির সান্নিধ্যে",
        "tagline_en": "Close to culture",
        "short_description_bn": "লোকাল খাবার, মানুষ আর সংস্কৃতির সঙ্গে মিশতে ভালোবাসেন।",
        "short_description_en": "You love connecting with local food, people and culture.",
        "description_bn": "লোকাল বাজার, উৎসব আর গ্রামীণ জীবনের রঙ আপনার প্রিয়। নতুন মানুষের সঙ্গে মিশে, তাদের গল্প আর খাবার ভাগ করে নেওয়াই আপনার ভ্রমণের আসল আনন্দ।",
        "description_en": "Local markets, festivals and the colours of village life are your favourites. Meeting new people and sharing their stories and food is your real joy of travel.",
        "keywords_bn": "লোকাল খাবার • উৎসব • বাজার • গ্রাম",
        "keywords_en": "Local food • Festival • Market • Village",
    },
}

AGE_GROUPS = [
    {"name": "Teen", "min_age": 10, "max_age": 17, "order": 1},
    {"name": "Young Adult", "min_age": 18, "max_age": 29, "order": 2},
    {"name": "Adult", "min_age": 30, "max_age": 49, "order": 3},
    {"name": "Mature Adult", "min_age": 50, "max_age": 64, "order": 4},
    {"name": "Senior", "min_age": 65, "max_age": 100, "order": 5},
]

QUESTIONNAIRE = {
    "name": "World Tourism Day 2026",
    "version": "v1",
    "questions": [
        {
            "order": 1,
            "text_bn": "ধরুন, এখনই ছুটিতে যাচ্ছেন—কেমন ট্রিপ চাইবেন?",
            "text_en": "Imagine you're going on holiday right now — what kind of trip do you want?",
            "options": [
                {"order": 1, "text_bn": "সমুদ্রের ধারে একদম রিল্যাক্স", "text_en": "Total relaxation by the sea", "weights": {"beach_lover": 4}},
                {"order": 2, "text_bn": "পুরোনো জায়গা, ইতিহাস আর ঐতিহ্য ঘুরে দেখা", "text_en": "Old places, history and heritage", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 3, "text_bn": "পাহাড়, ট্রেকিং আর একটু অ্যাডভেঞ্চার", "text_en": "Mountains, trekking and a bit of adventure", "weights": {"adventure_seeker": 3, "nature_explorer": 3}},
                {"order": 4, "text_bn": "স্থানীয় খাবার, মানুষ আর সংস্কৃতি এক্সপ্লোর করা", "text_en": "Exploring local food, people and culture", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 5, "text_bn": "জমজমাট একটা শহর ঘুরে বেড়ানো", "text_en": "Wandering around a lively city", "weights": {"urban_explorer": 4}},
            ],
        },
        {
            "order": 2,
            "text_bn": "কোন ধরনের জায়গা দেখলেই আপনার ব্যাগ গুছাতে ইচ্ছা করে?",
            "text_en": "What kind of place makes you want to pack your bags?",
            "options": [
                {"order": 1, "text_bn": "সমুদ্র আর দ্বীপ", "text_en": "Sea and islands", "weights": {"beach_lover": 4}},
                {"order": 2, "text_bn": "পাহাড় আর বন", "text_en": "Mountains and forests", "weights": {"nature_explorer": 4, "adventure_seeker": 2}},
                {"order": 3, "text_bn": "পুরোনো শহর বা ঐতিহাসিক জায়গা", "text_en": "Old cities or historic places", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 4, "text_bn": "গ্রাম আর স্থানীয় জীবন", "text_en": "Villages and local life", "weights": {"culture_connector": 4, "nature_explorer": 1}},
                {"order": 5, "text_bn": "আধুনিক শহর", "text_en": "A modern city", "weights": {"urban_explorer": 4}},
            ],
        },
        {
            "order": 3,
            "text_bn": "ট্রিপে গিয়ে কোন কাজটা আপনি সবচেয়ে বেশি করতে চান?",
            "text_en": "What do you most want to do on a trip?",
            "options": [
                {"order": 1, "text_bn": "আরাম করব, ছবি তুলব, ভিউ উপভোগ করব", "text_en": "Relax, take photos and enjoy the view", "weights": {"beach_lover": 3, "nature_explorer": 3}},
                {"order": 2, "text_bn": "পুরোনো স্থাপনা আর ঐতিহাসিক জায়গা ঘুরব", "text_en": "Visit old structures and historic places", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 3, "text_bn": "ট্রেকিং, ক্যাম্পিং বা অ্যাডভেঞ্চার কিছু করব", "text_en": "Trek, camp or do something adventurous", "weights": {"adventure_seeker": 4, "nature_explorer": 2}},
                {"order": 4, "text_bn": "লোকাল খাবার খাব আর মানুষের সঙ্গে মিশব", "text_en": "Eat local food and mingle with people", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 5, "text_bn": "শপিং, ক্যাফে আর শহর ঘুরে দেখব", "text_en": "Shop, café-hop and explore the city", "weights": {"urban_explorer": 4, "culture_connector": 1}},
            ],
        },
        {
            "order": 4,
            "text_bn": "কোন ধরনের ট্রিপ আপনার কাছে সবচেয়ে মজার?",
            "text_en": "What kind of trip is the most fun for you?",
            "options": [
                {"order": 1, "text_bn": "একদম শান্ত আর আরামদায়ক", "text_en": "Totally calm and relaxing", "weights": {"beach_lover": 3, "nature_explorer": 2}},
                {"order": 2, "text_bn": "ইতিহাস আর গল্পে ভরা", "text_en": "Full of history and stories", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 3, "text_bn": "একটু ঝুঁকি, একটু রোমাঞ্চ", "text_en": "A little risk, a little thrill", "weights": {"adventure_seeker": 4, "nature_explorer": 1}},
                {"order": 4, "text_bn": "লোকাল কালচার আর নতুন অভিজ্ঞতায় ভরা", "text_en": "Full of local culture and new experiences", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 5, "text_bn": "ফান, এন্টারটেইনমেন্ট আর সিটি লাইফ", "text_en": "Fun, entertainment and city life", "weights": {"urban_explorer": 4}},
            ],
        },
        {
            "order": 5,
            "text_bn": "কার সঙ্গে ঘুরতে গেলে আপনার সবচেয়ে ভালো লাগে?",
            "text_en": "Who do you enjoy travelling with the most?",
            "options": [
                {"order": 1, "text_bn": "একাই", "text_en": "Alone", "trait": CompanionTrait.SOLO},
                {"order": 2, "text_bn": "পার্টনারের সঙ্গে", "text_en": "With my partner", "trait": CompanionTrait.COUPLE},
                {"order": 3, "text_bn": "পরিবারের সঙ্গে", "text_en": "With family", "trait": CompanionTrait.FAMILY},
                {"order": 4, "text_bn": "বন্ধুদের সঙ্গে", "text_en": "With friends", "trait": CompanionTrait.FRIENDS},
                {"order": 5, "text_bn": "আসলে জায়গাটা ভালো হলেই হলো!", "text_en": "The destination matters most!", "trait": CompanionTrait.DESTINATION_FIRST},
            ],
        },
        {
            "order": 6,
            "text_bn": "ট্রিপে একটা পুরো দিন নিজের মতো কাটাতে পারলে কী করবেন?",
            "text_en": "If you had a full day to yourself on a trip, what would you do?",
            "options": [
                {"order": 1, "text_bn": "সমুদ্র বা নদীর ধারে বসে সূর্যাস্ত দেখব", "text_en": "Sit by the sea or river and watch the sunset", "weights": {"beach_lover": 4, "nature_explorer": 2}},
                {"order": 2, "text_bn": "কোনো পুরোনো প্রাসাদ, মন্দির বা ঐতিহাসিক জায়গা ঘুরব", "text_en": "Visit an old palace, temple or historic place", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 3, "text_bn": "ট্রেকিং, কায়াকিং বা সাইক্লিং করব", "text_en": "Go trekking, kayaking or cycling", "weights": {"adventure_seeker": 4, "nature_explorer": 2}},
                {"order": 4, "text_bn": "লোকাল বাজার, উৎসব বা গ্রাম ঘুরে দেখব", "text_en": "Explore a local market, festival or village", "weights": {"culture_connector": 4, "heritage_hunter": 1, "nature_explorer": 1}},
                {"order": 5, "text_bn": "শহর, রেস্টুরেন্ট আর মজার জায়গাগুলো এক্সপ্লোর করব", "text_en": "Explore the city, restaurants and fun spots", "weights": {"urban_explorer": 4, "culture_connector": 1}},
            ],
        },
    ],
}


class Command(BaseCommand):
    help = "Seed the World Tourism Day 2026 questionnaire, personas, weights and age groups. Idempotent."

    def handle(self, *args, **options):
        personas = {slug: self._seed_persona(slug) for slug in PERSONA_SLUGS}
        version = self._seed_version()
        for q_data in QUESTIONNAIRE["questions"]:
            question = self._seed_question(version, q_data)
            for o_data in q_data["options"]:
                option = self._seed_option(question, o_data)
                for slug, weight in o_data.get("weights", {}).items():
                    AnswerPersonaWeight.objects.update_or_create(
                        answer_option=option,
                        persona=personas[slug],
                        defaults={"weight": weight},
                    )
        self._seed_age_groups()
        self._seed_avatars(personas)
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(personas)} personas, version '{version}', "
                f"{len(QUESTIONNAIRE['questions'])} questions, age groups and avatars."
            )
        )

    def _seed_persona(self, slug):
        data = PERSONAS[slug]
        persona, _ = Persona.objects.get_or_create(slug=slug, defaults=data)
        updates = {}
        if not persona.name:
            updates["name"] = data["name"]
        if not persona.tie_break_order:
            updates["tie_break_order"] = data["tie_break_order"]
        if updates:
            for field, value in updates.items():
                setattr(persona, field, value)
            persona.save(update_fields=list(updates))
        return persona

    def _seed_version(self):
        version, _ = QuestionnaireVersion.objects.get_or_create(
            name=QUESTIONNAIRE["name"],
            version=QUESTIONNAIRE["version"],
        )
        if not QuestionnaireVersion.objects.filter(is_active=True).exists():
            version.is_active = True
            version.save(update_fields=["is_active"])
        return version

    def _seed_question(self, version, q_data):
        return Question.objects.get_or_create(
            questionnaire_version=version,
            order=q_data["order"],
            defaults={
                "text_bn": q_data["text_bn"],
                "text_en": q_data["text_en"],
            },
        )[0]

    def _seed_option(self, question, o_data):
        return AnswerOption.objects.get_or_create(
            question=question,
            order=o_data["order"],
            defaults={
                "text_bn": o_data["text_bn"],
                "text_en": o_data["text_en"],
                "companion_trait": o_data.get("trait") or "",
            },
        )[0]

    def _seed_age_groups(self):
        for data in AGE_GROUPS:
            AgeGroup.objects.get_or_create(name=data["name"], defaults=data)

    def _seed_avatars(self, personas):
        for slug, persona in personas.items():
            PersonaAvatar.objects.get_or_create(
                persona=persona,
                gender="",
                age_group=None,
                defaults={"image": f"avatars/{slug}/neutral.svg", "is_default": True},
            )
            for gender in ("male", "female"):
                for age_group in AgeGroup.objects.all():
                    key = age_group.name.lower().replace(" ", "_")
                    image = f"avatars/{slug}/{gender}-{key}.webp"
                    if not (settings.BASE_DIR / "static" / image).exists():
                        continue
                    PersonaAvatar.objects.get_or_create(
                        persona=persona,
                        gender=gender,
                        age_group=age_group,
                        defaults={"image": image, "is_default": False},
                    )
