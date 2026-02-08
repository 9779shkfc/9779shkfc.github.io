from flask import Blueprint, render_template, request, jsonify

jane_bp = Blueprint('jane', __name__, template_folder='templates')

@jane_bp.route('/')
def jane():
    embeds = {
        'youtube': 'https://www.youtube.com/@yehjaneyeh',
        'x': 'https://x.com/janeeeyeh',
        'instagram': 'https://www.instagram.com/janeeyeh',
        'tiktok': 'https://www.tiktok.com/@janeeyeh'
    }

    header = "<div class='celebrity-header'><h1>Jane</h1></div>"

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = header + render_template('partials/celebrity_content.html', embeds=embeds)
        return jsonify({'html': html})
    return render_template('celebrity.html', embeds=embeds, header=header)
