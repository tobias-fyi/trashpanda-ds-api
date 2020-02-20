"""
TDPS Detect API :: Models Blueprint
"""

from sqlalchemy.sql import func

from detect import db


# === Data model === #
class Material(db.Model):

    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), nullable=False)
    cluster = db.Column(db.String(64), nullable=False)

    def __init__(self, material_id, description, cluster):
        self.material_id = material_id
        self.description = description
        self.cluster = cluster
