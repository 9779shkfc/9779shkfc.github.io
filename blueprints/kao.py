from flask import Blueprint, render_template, request, jsonify

kao_bp = Blueprint('kao', __name__, template_folder='templates')

@kao_bp.route('/')
def kao():
    embeds = {
        'youtube': 'https://www.youtube.com/KaoSupatsara',
        'x': 'https://x.com/kaosupassara9',
        'instagram': 'https://www.instagram.com/supassra_sp',
        'instagram_pets': 'https://www.instagram.com/yawning_gang/',
        'tiktok': 'https://www.tiktok.com/@supassra_sp'
    }

    header = "<div class='celebrity-header'><h1>Kao</h1></div>"

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = header + render_template('partials/celebrity_content.html', embeds=embeds)
        return jsonify({'html': html})
    return render_template('celebrity.html', embeds=embeds, header=header)
