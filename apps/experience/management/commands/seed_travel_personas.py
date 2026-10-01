from django.conf import settings
from django.core.management.base import BaseCommand

from apps.experience.models import (
    AgeGroup,
    AnswerOption,
    AnswerPersonaWeight,
    AssessmentSession,
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
            "text_bn": "ধরুন, এখনই ছুটিতে যাচ্ছেন। কেমন ট্রিপ চাইবেন?",
            "text_en": "Imagine you're leaving for a holiday right now. What kind of trip would you want?",
            "options": [
                {"order": 1, "text_bn": "স্থানীয় খাবার, মানুষ আর সংস্কৃতি এক্সপ্লোর করতে চাই", "text_en": "I want to explore local food, people and culture", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 2, "text_bn": "সমুদ্রের ধারে একদম রিল্যাক্স করতে চাই", "text_en": "I want total relaxation by the sea", "weights": {"beach_lover": 4, "nature_explorer": 1}},
                {"order": 3, "text_bn": "জমজমাট একটা শহর ঘুরে বেড়াতে চাই", "text_en": "I want to wander around a lively city", "weights": {"urban_explorer": 4, "culture_connector": 1}},
                {"order": 4, "text_bn": "প্রকৃতির মাঝে সময় কাটাতে চাই", "text_en": "I want to spend time in nature", "weights": {"nature_explorer": 4, "adventure_seeker": 1}},
                {"order": 5, "text_bn": "পুরোনো জায়গা, ইতিহাস আর ঐতিহ্য ঘুরে দেখতে চাই", "text_en": "I want to visit old places, history and heritage", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 6, "text_bn": "ট্রেকিং, ক্যাম্পিং আর রোমাঞ্চকর কিছু করতে চাই", "text_en": "I want to do some trekking, camping and thrilling things", "weights": {"adventure_seeker": 4, "nature_explorer": 1}},
            ],
        },
        {
            "order": 2,
            "text_bn": "কোন ধরনের জায়গা দেখলেই আপনার ব্যাগ গুছাতে ইচ্ছা করে?",
            "text_en": "What kind of place makes you want to pack your bags?",
            "options": [
                {"order": 1, "text_bn": "পুরোনো শহর বা ঐতিহাসিক জায়গা", "text_en": "Old cities or historic places", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 2, "text_bn": "আধুনিক ও প্রাণবন্ত শহর", "text_en": "Modern and lively cities", "weights": {"urban_explorer": 4, "culture_connector": 1}},
                {"order": 3, "text_bn": "পাহাড়, বন, লেক আর প্রাকৃতিক সৌন্দর্যের জায়গা", "text_en": "Hills, forests, lakes and naturally beautiful places", "weights": {"nature_explorer": 4, "adventure_seeker": 1}},
                {"order": 4, "text_bn": "সমুদ্র আর দ্বীপ", "text_en": "Sea and islands", "weights": {"beach_lover": 4, "nature_explorer": 1}},
                {"order": 5, "text_bn": "ট্রেকিং ট্রেইল বা অ্যাডভেঞ্চার স্পট", "text_en": "Trekking trails or adventure spots", "weights": {"adventure_seeker": 4, "nature_explorer": 1}},
                {"order": 6, "text_bn": "গ্রাম, স্থানীয় বাজার আর স্থানীয় জীবন", "text_en": "Villages, local markets and local life", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
            ],
        },
        {
            "order": 3,
            "text_bn": "ট্রিপে গিয়ে কোন কাজটা আপনি সবচেয়ে বেশি করতে চান?",
            "text_en": "What do you most want to do on a trip?",
            "options": [
                {"order": 1, "text_bn": "লোকাল খাবার খাব আর মানুষের সঙ্গে মিশব", "text_en": "I'll eat local food and mingle with people", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 2, "text_bn": "ট্রেকিং, ক্যাম্পিং, কায়াকিং বা অ্যাডভেঞ্চার কিছু করব", "text_en": "I'll do some trekking, camping, kayaking or adventure", "weights": {"adventure_seeker": 4, "nature_explorer": 1}},
                {"order": 3, "text_bn": "শপিং, ক্যাফে আর শহর ঘুরে দেখব", "text_en": "I'll shop, visit cafés and explore the city", "weights": {"urban_explorer": 4, "culture_connector": 1}},
                {"order": 4, "text_bn": "পাহাড়, বন, লেক বা বন্যপ্রাণী দেখার জায়গায় সময় কাটাব", "text_en": "I'll spend time in the hills, forests, lakes or wildlife spots", "weights": {"nature_explorer": 4, "adventure_seeker": 1}},
                {"order": 5, "text_bn": "পুরোনো স্থাপনা আর ঐতিহাসিক জায়গা ঘুরে দেখব", "text_en": "I'll visit old structures and historic places", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 6, "text_bn": "সমুদ্র বা নদীর ধারে আরাম করে সময় কাটাব", "text_en": "I'll relax by the sea or a river", "weights": {"beach_lover": 4, "nature_explorer": 1}},
            ],
        },
        {
            "order": 4,
            "text_bn": "ভ্রমণের সময় কোন অনুভূতিটা আপনি সবচেয়ে বেশি খুঁজে বেড়ান?",
            "text_en": "What feeling do you search for most while travelling?",
            "options": [
                {"order": 1, "text_bn": "রোমাঞ্চ, চ্যালেঞ্জ আর অ্যাডভেঞ্চার", "text_en": "Thrill, challenge and adventure", "weights": {"adventure_seeker": 4, "nature_explorer": 1}},
                {"order": 2, "text_bn": "নতুন মানুষ, সংস্কৃতি আর জীবনযাত্রার সঙ্গে পরিচিত হওয়া", "text_en": "Getting to know new people, cultures and ways of life", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 3, "text_bn": "শান্তি, বিশ্রাম আর নিজের জন্য একটু সময়", "text_en": "Peace, rest and a little time for myself", "weights": {"beach_lover": 4, "nature_explorer": 1}},
                {"order": 4, "text_bn": "প্রাণচাঞ্চল্য, বিনোদন আর নতুন কিছু করার সুযোগ", "text_en": "Liveliness, entertainment and chances to try new things", "weights": {"urban_explorer": 4, "culture_connector": 1}},
                {"order": 5, "text_bn": "প্রকৃতির কাছাকাছি থাকা আর সুন্দর পরিবেশ উপভোগ করা", "text_en": "Being close to nature and enjoying beautiful surroundings", "weights": {"nature_explorer": 4, "adventure_seeker": 1}},
                {"order": 6, "text_bn": "নতুন কিছু জানা, ইতিহাসের গল্প আবিষ্কার করা", "text_en": "Learning something new, discovering stories of history", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
            ],
        },
        {
            "order": 5,
            "text_bn": "কার সঙ্গে ঘুরতে গেলে আপনার সবচেয়ে ভালো লাগে?",
            "text_en": "Who do you most enjoy travelling with?",
            "options": [
                {"order": 1, "text_bn": "বন্ধুদের সঙ্গে", "text_en": "With friends", "trait": CompanionTrait.FRIENDS},
                {"order": 2, "text_bn": "একা", "text_en": "Alone", "trait": CompanionTrait.SOLO},
                {"order": 3, "text_bn": "পরিবারের সঙ্গে", "text_en": "With family", "trait": CompanionTrait.FAMILY},
                {"order": 4, "text_bn": "আসলে জায়গাটা ভালো হলেই হলো", "text_en": "Actually, it just needs to be a great destination", "trait": CompanionTrait.DESTINATION_FIRST},
                {"order": 5, "text_bn": "পার্টনারের সঙ্গে", "text_en": "With my partner", "trait": CompanionTrait.COUPLE},
            ],
        },
        {
            "order": 6,
            "text_bn": "কোন বিষয়টা একটি ট্রিপকে আপনার কাছে সবচেয়ে স্মরণীয় করে তোলে?",
            "text_en": "What makes a trip most memorable for you?",
            "options": [
                {"order": 1, "text_bn": "শহরের প্রাণবন্ত পরিবেশ", "text_en": "The lively atmosphere of a city", "weights": {"urban_explorer": 4, "culture_connector": 1}},
                {"order": 2, "text_bn": "অজানা কোনো ঐতিহাসিক গল্প", "text_en": "An unfamiliar story of history", "weights": {"heritage_hunter": 4, "culture_connector": 1}},
                {"order": 3, "text_bn": "অসাধারণ কোনো প্রাকৃতিক দৃশ্য", "text_en": "A breathtaking natural view", "weights": {"nature_explorer": 4, "adventure_seeker": 1}},
                {"order": 4, "text_bn": "সমুদ্রের ধারে শান্ত একটা মুহূর্ত", "text_en": "A peaceful moment by the sea", "weights": {"beach_lover": 4, "nature_explorer": 1}},
                {"order": 5, "text_bn": "স্থানীয় মানুষ ও সংস্কৃতির অভিজ্ঞতা", "text_en": "Experiencing local people and culture", "weights": {"culture_connector": 4, "heritage_hunter": 1}},
                {"order": 6, "text_bn": "রোমাঞ্চকর কিছু করার অভিজ্ঞতা", "text_en": "The experience of doing something thrilling", "weights": {"adventure_seeker": 4, "nature_explorer": 1}},
            ],
        },
    ],
}


class Command(BaseCommand):
    help = "Seed the World Tourism Day 2026 questionnaire, personas, weights and age groups. Idempotent."

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge-assessments",
            action="store_true",
            help="Delete all assessments of the seeded questionnaire version before updating content.",
        )

    def handle(self, *args, **options):
        personas = {slug: self._seed_persona(slug) for slug in PERSONA_SLUGS}
        version = self._seed_version()

        if options["purge_assessments"]:
            purged = AssessmentSession.objects.filter(
                questionnaire_version=version
            ).delete()
            self.stdout.write(
                self.style.WARNING(f"Purged assessments: {purged[0]} object(s) deleted.")
            )

        for q_data in QUESTIONNAIRE["questions"]:
            question = self._seed_question(version, q_data)
            option_ids = []
            for o_data in q_data["options"]:
                option = self._seed_option(question, o_data)
                option_ids.append(option.id)
                AnswerPersonaWeight.objects.filter(answer_option=option).delete()
                for slug, weight in o_data.get("weights", {}).items():
                    AnswerPersonaWeight.objects.create(
                        answer_option=option,
                        persona=personas[slug],
                        weight=weight,
                    )
            AnswerOption.objects.filter(
                question=question
            ).exclude(pk__in=option_ids).update(is_active=False)

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
        question, _ = Question.objects.update_or_create(
            questionnaire_version=version,
            order=q_data["order"],
            defaults={
                "text_bn": q_data["text_bn"],
                "text_en": q_data["text_en"],
            },
        )
        return question

    def _seed_option(self, question, o_data):
        option, _ = AnswerOption.objects.update_or_create(
            question=question,
            order=o_data["order"],
            defaults={
                "text_bn": o_data["text_bn"],
                "text_en": o_data["text_en"],
                "companion_trait": o_data.get("trait") or "",
                "is_active": True,
            },
        )
        return option

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