from flask import current_app, g, request, send_from_directory, Blueprint
import logging
from .auth import login_required
from ..utils import parse_movies_excel, match_movie
from .. import db
import pathlib

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
        
        for _, row in data.iterrows():
            # 先去库中匹配电影，若匹配不到则创建一个，movie_id为匹配到的或新创建的movie
            temp_l = db.query_movie_match_name(row['name'])
            matcher = match_movie(temp_l, {'rating': row['rating'], 'runtime': row['runtime']})
            movie_id = -1
            if matcher == None:
                movie_id = db.insert_movie(row['name'], [db.RunningTime('default', int(row['runtime']))], row['rating'],
                                            starring=row['starring'], genre=row['genre'])
                logger.info('创建movie' + row['name'])
            else:
                movie_id = matcher.id
            try:
                db.insert_user_movie_map(g.user.id, movie_id, row['likability'], row['have_seen'], row['comment'])
            except Exception as e:
                logger.error('error insert user_movie_map when handle movie' + row['name'])
                logger.error(e)

    return {'statusCode':0, 'message': 'upload success'}

@bp.route('/download/<filename>')
def uploaded_file(filename):
    logger.info('download file')
    download_dir_absolute = pathlib.Path(current_app.config['DOWNLOAD_FOLDER']).absolute()
    # print('download folder is', download_dir_absolute)
    return send_from_directory(download_dir_absolute, filename)