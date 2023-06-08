from ..db import db

followers = db.Table(
    'followers',
    # 나를 팔로우하는 사람들의 id
    db.Column('follower_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True),
    # 내가 팔로우하는 사람들의 id
    db.Column('followed_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
)
updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

followed = db.relationship(                             # 본인이 팔로우한 유저들
    'User',                                             # User 모델 스스로를 참조
    secondary=followers,                                # 연관 테이블 이름을 저장
    primaryjoin=(followers.c.follower_id == id),        # follwers 테이블에서 특정 유저를 팔로우하는 유저들을 찾음
    secondaryjoin=(followers.c.followed_id == id),      # follwers 테이블에서 특정 유저가 팔로우한 모든 유저들을 찾음
    backref=db.backref('follower_set', lazy='dynamic'), # 역참조 관계 설정
    lazy='dynamic'                                      
)


class UserModel(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()