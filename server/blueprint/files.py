from flask import current_app, g, request, send_from_directory, Blueprint
import logging
from .auth import login_required
from ..utils import parse_movies_excel
from ..db import get_db

logger = logging.getLogger(__name__)
bp = Blueprint('files', __name__, url_prefix='/files')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    logger.info('file upload')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            logger.warning('No file part')
            return {'statusCode':-1, 'message': 'No file part'}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            logger.warning('No selected file')
            return {'statusCode':-1, 'message': 'No selected file'}
        if not allowed_file(file.filename):
            logger.warning('Unsupported file format. ' + file.filename)
            return {'statusCode': -1, 'message': 'Unsupported file format'}
        
        data = parse_movies_excel(file)
        if data is None:
            logger.error('excel parse error')
            return {'statusCode': -1, 'message': 'file parse error'}
        db = get_db()
        db.insert_movie_df_by_userid(data, g.user['id'])
    return {'statusCode':0, 'message': 'upload success'}

@bp.route('/download/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['DOWNLOAD_FOLDER'], filename)