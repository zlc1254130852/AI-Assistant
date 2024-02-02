from functions.AI_chat import AI_chat_bp
from functions.real_time_translation import real_time_translation_bp
from functions.writing_grader import writing_grader_bp
from functions.oral_assessment import oral_assessment_bp
from functions.video_chat import video_chat_bp
from functions.text_summary import text_summary_bp
from functions.object_detection import object_detection_bp
from functions.speaking_grader import speaking_grader_bp
from login_reg import login_reg_bp
from functions.practice import practice_bp

def build_blueprint(app):
    app.register_blueprint(AI_chat_bp)
    app.register_blueprint(real_time_translation_bp)
    app.register_blueprint(writing_grader_bp)
    app.register_blueprint(oral_assessment_bp)
    app.register_blueprint(video_chat_bp)
    app.register_blueprint(text_summary_bp)
    app.register_blueprint(object_detection_bp)
    app.register_blueprint(speaking_grader_bp)
    app.register_blueprint(login_reg_bp)
    app.register_blueprint(practice_bp)

    print(app.url_map)