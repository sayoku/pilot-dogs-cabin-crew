"""Hardcoded sample data. Replace with database queries later."""

TOPICS = [
    {"topic_id": 1, "topic_name": "Boarding", "description": "Flying with a guide dog"},
    {
        "topic_id": 2,
        "topic_name": "Etiquette",
        "description": "Interacting with working dogs",
    },
    {
        "topic_id": 3,
        "topic_name": "Dog Care",
        "description": "Feeding, grooming, and health",
    },
]

FAQS = [
    {
        "faq_id": 1,
        "topic_id": 1,
        "question_text": "Can I pet the dog during boarding?",
        "answer_text": "No. Working dogs should not be distracted while in harness.",
        "date_created": "2026-10-01",
    },
    {
        "faq_id": 2,
        "topic_id": 2,
        "question_text": "How do I offer help to a handler?",
        "answer_text": "Ask the handler first and wait for their answer.",
        "date_created": "2026-10-02",
    },
    {
        "faq_id": 3,
        "topic_id": 3,
        "question_text": "How often should the dog be fed?",
        "answer_text": "Follow the feeding schedule from the trainer.",
        "date_created": "2026-10-03",
    },
]

TRAINING_MATERIALS = [
    {
        "material_id": 1,
        "topic_id": 1,
        "title": "Boarding basics",
        "description": "Walkthrough of boarding with a guide dog",
        "material_type": "video",
        "content_url": "https://example.com/videos/boarding-basics",
    },
    {
        "material_id": 2,
        "topic_id": 3,
        "title": "Dog sitting test study guide",
        "description": "Study material for the semester dog sitting test",
        "material_type": "document",
        "content_url": "https://example.com/docs/dog-sitting-guide",
    },
]

QUESTIONS = [
    {
        "question_id": 1,
        "user_id": 2,
        "question_text": "What if the dog refuses to eat?",
        "contact_info": "555-0100",
        "status": "pending",
        "date_created": "2026-11-05",
    },
]