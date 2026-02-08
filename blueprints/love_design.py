from flask import Blueprint, render_template, request, jsonify

love_design_bp = Blueprint('love_design', __name__, template_folder='templates')

@love_design_bp.route('/')
def love_design():
    embeds = {
        'instagram': 'https://www.instagram.com/lovedesignseriesth/',
        'x': 'https://x.com/lovedesignth'
    }

    header = "<div class='celebrity-header'><h1>Love Design</h1></div>"

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = header + render_template('partials/celebrity_content.html', embeds=embeds)
        return jsonify({'html': html})
    return render_template('celebrity.html', embeds=embeds, header=header)
