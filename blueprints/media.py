import os
from flask import Blueprint, render_template, request, url_for, current_app, jsonify

media_bp = Blueprint('media', __name__, template_folder='templates')

ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

def list_wallpapers(subfolder):
    static_root = current_app.static_folder
    folder_path = os.path.join(static_root, 'images', 'wallpapers', subfolder)
    if not os.path.isdir(folder_path):
        return []
    files = []
    for fname in sorted(os.listdir(folder_path), reverse=True):
        _, ext = os.path.splitext(fname.lower())
        if ext in ALLOWED_EXT:
            file_url = url_for('static', filename=f'images/wallpapers/{subfolder}/{fname}')
            files.append({'name': fname, 'url': file_url})
    return files

@media_bp.route('/laptop')
@media_bp.route('/laptop/')
def laptop_wallpapers():
    images = list_wallpapers('laptop')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('partials/media_list.html', title='Wallpapers — Laptop', images=images)
        return jsonify({'html': html})
    return render_template('media_laptop.html', title='Wallpapers — Laptop', images=images)

@media_bp.route('/mobile')
@media_bp.route('/mobile/')
def mobile_wallpapers():
    images = list_wallpapers('mobile')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('partials/media_list.html', title='Wallpapers — Mobile', images=images)
        return jsonify({'html': html})
    return render_template('media_mobile.html', title='Wallpapers — Mobile', images=images)
