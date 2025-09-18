from typing import List, Dict

def generate_care_plan(top_plants: List[dict]) -> List[dict]:
    day_names = ['সোম', 'মঙ্গল', 'বুধ', 'বৃহস্পতি', 'শুক্র', 'শনি', 'রবি']
    tasks = []

    needs_more_water = any(int(p.get('humidity_min', 0)) >= 55 for p in top_plants)
    prefers_sun = any(int(p.get('sunlight_min', 0)) >= 5 for p in top_plants)

    tasks.append({ 'day': day_names[0], 'time': 'সকাল ৮টা', 'task': 'মাটি আর্দ্রতা চেক ও হালকা পানি দিন' })
    tasks.append({ 'day': day_names[2], 'time': 'সকাল ৮টা', 'task': 'গভীর সেচ (পাত্রের তলা পর্যন্ত)' if needs_more_water else 'হালকা সেচ' })
    tasks.append({ 'day': day_names[4], 'time': 'সকাল ৯টা', 'task': 'পাতা পর্যবেক্ষণ, পোকা হলে নিম তেল স্প্রে' })
    tasks.append({ 'day': day_names[5], 'time': 'বিকাল ৪টা', 'task': 'রোদ পজিশনিং ঠিক করুন' if prefers_sun else 'আংশিক ছায়ায় সরান' })
    tasks.append({ 'day': day_names[6], 'time': 'সকাল ৯টা', 'task': 'কম্পোস্ট চা/বায়ো-ফার্টিলাইজার (হালকা ডোজ)' })

    return tasks
