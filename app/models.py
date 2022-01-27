from datetime import datetime

from flask import url_for

from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)

        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }

        return data


class ModelConfig(PaginatedAPIMixin, db.Model):
    model_id = db.Column(db.Integer, primary_key=True)
    buid = db.Column(db.VARCHAR(120))
    payment_type = db.Column(db.String(64))
    inv_status = db.Column(db.String(120))
    segment = db.Column(db.String(120))
    segment_max_value = db.Column(db.Integer)
    segment_min_value = db.Column(db.Integer)
    period_data = db.Column(db.Integer)
    period = db.Column(db.Integer)
    ncalls = db.Column(db.Integer)
    region = db.Column(db.String(120))
    release_date = db.Column(db.Date)
    status = db.Column(db.String(120))
    executed_on = db.Column(db.DateTime)

    def bind(self, data):
        for field in ['buid', 'payment_type', 'inv_status', 'segment', 'segment_max_value', 'segment_min_value',
                      'period_data', 'period', 'ncalls', 'region', 'release_date', 'status', 'executed_on']:
            if field in data:
                setattr(self, field, data[field])

        for field in ['release_date']:
            if field in data:
                value = self.validate_date(data[field], '%Y-%m-%d')
                setattr(self, field, value)

    def validate_date(self, date_text, date_format='%Y-%m-%d'):
        try:
            parsed = datetime.strptime(date_text, date_format)
        except ValueError:
            raise ValueError("Incorrect date format")

        return parsed

    def to_dict(self):
        data = {
            'model_id': self.model_id,
            'buid': self.buid,
            'payment_type': self.payment_type,
            'inv_status': self.inv_status,
            'segment': self.segment,
            'segment_max_value': self.segment_max_value,
            'segment_min_value': self.segment_min_value,
            'period_data': self.period_data,
            'period': self.period,
            'ncalls': self.ncalls,
            'region': self.region,
            # 'release_date': self.release_date.isoformat() + 'Z',
            'release_date': self.release_date,
            'status': self.status,
            # 'executed_on': self.executed_on.isoformat() + 'Z',
            'executed_on': self.executed_on,
        }

        return data
