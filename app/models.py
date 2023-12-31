from datetime import datetime
from app import database


class User(database.Model):
    __tablename__ = "user"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    salary = database.Column(database.Integer, nullable=False)
    gender = database.Column(database.String(20), nullable=False)
    date_of_birth = database.Column(database.Date, nullable=False)
    claims = database.relationship("Claim", back_populates="user")
    time_created = database.Column(database.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return "<User: {}>".format(self)

    def calculate_age(self):
        today = datetime.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age


class Claim(database.Model):
    __tablename__ = "claim"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=False
    )
    diagnosis = database.Column(database.String(1000), nullable=False)
    hmo = database.Column(database.String(10), nullable=False)
    services = database.relationship("Service", back_populates="claim")
    total_cost = database.Column(database.Integer, nullable=False)
    service_charge = database.Column(database.Integer, nullable=False)
    final_cost = database.Column(database.Integer, nullable=False)
    time_created = database.Column(database.DateTime, default=datetime.utcnow)
    user = database.relationship("User", back_populates="claims")

    def __repr__(self):
        return "<Claim: {}>".format(self.diagnosis)


class Service(database.Model):
    __tablename__ = "service"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    claim_id = database.Column(
        database.Integer, database.ForeignKey("claim.id"), nullable=False
    )
    service_date = database.Column(database.Date, nullable=False)
    service_name = database.Column(database.String(100), nullable=False)
    service_type = database.Column(database.String(50), nullable=False)
    provider_name = database.Column(database.String(100), nullable=False)
    source_hospital = database.Column(database.String(100), nullable=False)
    cost_of_service = database.Column(database.Integer, nullable=False)

    claim = database.relationship("Claim", back_populates="services")

    def __repr__(self):
        return "<Service: {}>".format(self.service_name)


class Diagnosis(database.Model):
    __tablename__ = "diagnosis"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    # claims = database.relationship('Claim', back_populates='diagnosis')

    def __repr__(self):
        return "<Diagnosis: {}>".format(self.name)


class HMO(database.Model):
    __tablename__ = "hmo"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    # claims = database.relationship('Claim', back_populates='hmo')

    def __repr__(self):
        return "<HMO: {}>".format(self.name)


# from datetime import datetime

# from app import database


# class User(database.Model):
#     __tablename__ = 'user'

#     id = database.Column(database.Integer, autoincrement=True, primary_key=True)
#     name = database.Column(database.String(100), nullable=False, unique=True)
#     salary = database.Column(database.Integer, nullable=False)
#     gender = database.Column(database.String(10), nullable=True)
#     date_of_birth = database.Column(database.Date, nullable=True)
#     time_created = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
#     claim = database.relationship('Claim')

#     def __repr__(self):
#         return '<User: {}>'.format(self.name)


# class Claim(database.Model):
#     __tablename__ = 'claim'

#     id = database.Column(database.Integer, autoincrement=True, primary_key=True)
#     user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
#     diagnosis = database.Column(database.String(1000))
#     hmo = database.Column(database.String(4))
#     age = database.Column(database.Integer, nullable=True)
#     service_charge = database.Column(database.Integer)
#     total_cost = database.Column(database.Integer)
#     final_cost = database.Column(database.Integer)
#     user = database.relationship('User', backref='')
#     service = database.relationship('Service', backref='')

#     def __repr__(self):
#         return '<CLaim: {}>'.format(self.service)


# class Service(database.Model):
#     __tablename__ = 'service'

#     id = database.Column(database.Integer, autoincrement=True, primary_key=True)
#     claim_id = database.Column(database.Integer, database.ForeignKey('claim.id'))
#     service_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
#     service_name = database.Column(database.String(100), nullable=False, unique=True)
#     type = database.Column(database.String(50), nullable=False, unique=True)
#     provider_name = database.Column(database.String(100), nullable=False, unique=True)
#     source = database.Column(database.String(100), nullable=False, unique=True)
#     cost_of_service = database.Column(database.Integer)

#     def __repr__(self):
#         return '<Service: {}>'.format(self.type)
